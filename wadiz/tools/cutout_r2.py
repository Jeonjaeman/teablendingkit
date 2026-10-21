"""2차 수정 실사(파우치·원료카드) 누끼 → 미장 배경 합성.

  python wadiz/tools/cutout_r2.py
입력: wadiz/2차수정/*.jpg  출력: wadiz/assets/photo/{pouch_v2,cards_pair,danpatt_sample,random3_packs,kit_real,prize_teas_real}.jpg
- 원료카드: 윤곽선 4점 → 원근 보정으로 반듯한 직사각형
- 파우치: grabCut 누끼(유산지 모양 그대로)
- 배경: assets/photo/plaster-eu-1.jpg(아이보리 미장) + 부드러운 그림자
"""
import os, cv2, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
SRC = os.path.join(W, '2차수정')


def imread(p):
    return cv2.imdecode(np.fromfile(p, np.uint8), cv2.IMREAD_COLOR)


def imwrite(p, im):
    cv2.imencode('.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 88])[1].tofile(p)


def order(pts):
    pts = pts.reshape(4, 2).astype(np.float32)
    s, d = pts.sum(1), np.diff(pts, axis=1).ravel()
    return np.array([pts[s.argmin()], pts[d.argmin()], pts[s.argmax()], pts[d.argmax()]], np.float32)


def grab(im, rect, k=4):
    """축소본에서 grabCut → 원본 크기 마스크(0~255)."""
    sm = cv2.resize(im, None, fx=1 / k, fy=1 / k, interpolation=cv2.INTER_AREA)
    m = np.zeros(sm.shape[:2], np.uint8)
    r = tuple(int(v / k) for v in rect)
    cv2.grabCut(sm, m, r, np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64), 6, cv2.GC_INIT_WITH_RECT)
    fg = np.where((m == 1) | (m == 3), 255, 0).astype(np.uint8)
    # 가장 큰 덩어리만, 구멍 메움
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg)
    fg = np.where(lab == 1 + st[1:, cv2.CC_STAT_AREA].argmax(), 255, 0).astype(np.uint8)
    cs, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    fg = cv2.drawContours(np.zeros_like(fg), cs, -1, 255, -1)
    return cv2.resize(fg, (im.shape[1], im.shape[0]), interpolation=cv2.INTER_LINEAR), cs[0] * k


def card(f, rect, ratio, corners=None):
    """카드 시트: grabCut 윤곽 → 4점 근사 → 원근 보정. 반사광으로 윤곽이 번지면 corners 로 직접 지정."""
    im = imread(os.path.join(SRC, f))
    if corners is not None:
        q = order(np.float32(corners))
    else:
        _, c = grab(im, rect)
        peri = cv2.arcLength(c.astype(np.float32), True)
        q = cv2.approxPolyDP(c.astype(np.float32), 0.02 * peri, True)
        if len(q) != 4:
            q = cv2.boxPoints(cv2.minAreaRect(c.astype(np.float32)))
        q = order(q)
    w = int(np.linalg.norm(q[1] - q[0])); h = int(w / ratio)
    M = cv2.getPerspectiveTransform(q, np.float32([[0, 0], [w, 0], [w, h], [0, h]]))
    out = cv2.warpPerspective(im, M, (w, h), flags=cv2.INTER_CUBIC)
    # 가장자리에 걸린 테이블 한 줄을 덜어냄
    m = int(w * .01)
    out = out[m:h - m, m:w - m]
    return out, np.full(out.shape[:2], 255, np.uint8)


def plaster(w, h):
    bg = imread(os.path.join(W, 'assets', 'photo', 'plaster-eu-1.jpg'))
    s = max(w / bg.shape[1], h / bg.shape[0])
    bg = cv2.resize(bg, None, fx=s, fy=s, interpolation=cv2.INTER_CUBIC)
    y0, x0 = (bg.shape[0] - h) // 2, (bg.shape[1] - w) // 2
    return bg[y0:y0 + h, x0:x0 + w].astype(np.float32)


def place(obj, mask, W_, H_, width_frac, dy=0.0):
    """미장 배경 가운데에 obj 배치 + 그림자."""
    return place_many([(obj, mask, width_frac, .5)], W_, H_, dy)


def place_many(items, W_, H_, dy=0.0):
    """items: (obj, mask, 폭 비율, 가로 중심 비율) 여러 개를 한 배경에."""
    bg = plaster(W_, H_)
    full = np.zeros((H_, W_), np.float32); layer = np.zeros_like(bg)
    for obj, mask, width_frac, cx in items:
        s = min(W_ * width_frac / obj.shape[1], H_ * .88 / obj.shape[0])  # 높이도 넘지 않게
        obj = cv2.resize(obj, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
        mask = cv2.resize(mask, (obj.shape[1], obj.shape[0]), interpolation=cv2.INTER_AREA)
        mask = cv2.GaussianBlur(mask, (0, 0), 0.8)
        h, w = obj.shape[:2]
        x, y = int(W_ * cx - w / 2), int((H_ - h) / 2 + dy * H_)
        full[y:y + h, x:x + w] = np.maximum(full[y:y + h, x:x + w], mask / 255)
        layer[y:y + h, x:x + w] = obj
    return _composite(bg, full, layer, W_, H_)


def _composite(bg, full, layer, W_, H_):
    # 그림자: 아래로 살짝, 넓게 번진 것 + 가까이 진한 것
    sh = cv2.GaussianBlur(np.roll(full, (int(H_ * .018), int(W_ * .008)), (0, 1)), (0, 0), W_ * .022) * .30 \
        + cv2.GaussianBlur(np.roll(full, (int(H_ * .004), 0), (0, 1)), (0, 0), W_ * .004) * .22
    bg *= (1 - np.clip(sh, 0, .6))[..., None]
    out = bg * (1 - full[..., None]) + layer * full[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)


def kit_real(f):
    """키트 실물 촬영(검은 테이블): 직사각형 물체는 다각형, 책갈피·인퓨저만 grabCut."""
    im = imread(os.path.join(SRC, f))
    H, W_ = im.shape[:2]; k = W_ / 900  # 좌표는 폭 900 축소본 기준
    P = lambda pts: (np.array(pts, np.float32) * k).astype(np.int32)
    mask = np.zeros((H, W_), np.uint8)
    for q in [[(102, 315), (520, 310), (521, 630), (93, 629)],            # 상자
              [(523, 398), (672, 398), (682, 405), (681, 616), (523, 616)],   # 사용 안내 엽서 + 원료 카드
              [(673, 391), (847, 386), (869, 619), (678, 626)],           # 블렌딩 노트(살짝 기울어짐)
              [(293, 652), (700, 652), (700, 656), (838, 657), (841, 832), (293, 829)],   # 파우치 윗줄
              [(353, 795), (768, 794), (769, 978), (630, 979), (630, 975), (490, 975), (490, 980), (353, 980)]]:  # 파우치 아랫줄
        cv2.fillPoly(mask, [P(q)], 255)
    # 인퓨저: 손잡이 + 거름망
    cv2.line(mask, tuple(P([(285, 694)])[0]), tuple(P([(284, 870)])[0]), 255, int(9 * k))
    cv2.circle(mask, tuple(P([(283, 905)])[0]), int(38 * k), 255, -1)
    # 책갈피 부채꼴: grabCut
    sm = cv2.resize(im, (900, int(H / k)), interpolation=cv2.INTER_AREA)
    g = np.full(sm.shape[:2], cv2.GC_BGD, np.uint8)
    g[670:970, 15:275] = cv2.GC_PR_BGD
    g[682:958, 22:262] = cv2.GC_PR_FGD
    g[740:900, 120:240] = cv2.GC_FGD
    cv2.grabCut(sm, g, None, np.zeros((1, 65)), np.zeros((1, 65)), 8, cv2.GC_INIT_WITH_MASK)
    fan = np.where((g == 1) | (g == 3), 255, 0).astype(np.uint8)
    fan = cv2.morphologyEx(fan, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    fan = cv2.resize(fan, (W_, H), interpolation=cv2.INTER_LINEAR)
    mask = cv2.max(mask, fan)
    ys, xs = np.where(mask > 0)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    return im[y0:y1, x0:x1], mask[y0:y1, x0:x1]


def sheet(f):
    """원료카드 디자인 원본: 체커보드(가짜 투명 배경) 바깥을 잘라냄."""
    im = imread(os.path.join(SRC, f))[..., :3]
    card = (cv2.cvtColor(im, cv2.COLOR_BGR2HSV)[..., 1] > 18).astype(np.uint8)
    xs = np.where(card.mean(0) > .5)[0]; ys = np.where(card.mean(1) > .5)[0]
    out = im[ys.min() + 4:ys.max() - 3, xs.min() + 4:xs.max() - 3]
    return out, np.full(out.shape[:2], 255, np.uint8)


def stage_kit(obj, mask, W_=1800, H_=1200, seed=7):
    """실물 누끼로 '전체 연출 컷': 따뜻한 미장 바닥 + 왼쪽 위 창빛 + 오른쪽 위 잎 그림자 + 긴 그림자.
    구성은 실물 그대로라 생성 이미지처럼 라벨·원료가 틀어지지 않는다."""
    rng = np.random.default_rng(seed)
    bg = plaster(W_, H_) * np.array([0.80, 0.90, 1.0], np.float32)[None, None, :]  # BGR: 따뜻한 베이지
    bg = np.clip(bg * 1.04 + 6, 0, 255)
    # 물체 배치(가운데, 폭 86%)
    s = min(W_ * .86 / obj.shape[1], H_ * .86 / obj.shape[0])
    o = cv2.resize(obj, None, fx=s, fy=s, interpolation=cv2.INTER_AREA).astype(np.float32)
    m = cv2.resize(mask, (o.shape[1], o.shape[0]), interpolation=cv2.INTER_AREA)
    m = cv2.GaussianBlur(m, (0, 0), 0.8).astype(np.float32) / 255
    h, w = o.shape[:2]; x, y = (W_ - w) // 2, (H_ - h) // 2 + int(H_ * .01)
    full = np.zeros((H_, W_), np.float32); full[y:y + h, x:x + w] = m
    layer = np.zeros_like(bg); layer[y:y + h, x:x + w] = o
    # 물체 색: 사무실 형광등 톤 → 오후 햇빛 톤
    layer = np.clip(layer * np.array([0.90, 0.98, 1.08], np.float32) + np.array([0, 4, 12], np.float32), 0, 255)
    # 그림자: 빛이 왼쪽 위에서 오므로 오른쪽 아래로 길게
    sh = cv2.GaussianBlur(np.roll(full, (int(H_ * .022), int(W_ * .016)), (0, 1)), (0, 0), W_ * .012) * .42         + cv2.GaussianBlur(np.roll(full, (int(H_ * .005), int(W_ * .003)), (0, 1)), (0, 0), W_ * .003) * .25
    bg *= (1 - np.clip(sh, 0, .6))[..., None]
    out = bg * (1 - full[..., None]) + layer * full[..., None]
    # 창빛: 왼쪽 위에서 비스듬히 들어오는 밝은 띠 두 줄
    light = np.zeros((H_, W_), np.float32)
    for off in (0, int(W_ * .16)):
        pts = np.array([[-W_ * .1 + off, 0], [W_ * .12 + off, 0], [W_ * .5 + off, H_], [W_ * .28 + off, H_]], np.int32)
        cv2.fillPoly(light, [pts], 1.0)
    light = cv2.GaussianBlur(light, (0, 0), W_ * .03)
    light *= np.clip(1.15 - np.linspace(0, 1, W_)[None, :] * 1.3, 0, 1)  # 왼쪽일수록 강하게
    out = out * (1 + .16 * light[..., None]) + np.array([4, 10, 18], np.float32) * light[..., None]
    # 잎 그림자: 오른쪽 위 모서리에서 내려오는 가지
    leaf = np.zeros((H_, W_), np.float32)
    def branch(x0, y0, ang, length, depth):
        x1 = x0 + np.cos(ang) * length; y1 = y0 + np.sin(ang) * length
        cv2.line(leaf, (int(x0), int(y0)), (int(x1), int(y1)), 1.0, max(2, int(6 - depth * 2)))
        for t in np.linspace(.15, 1, 7):
            px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            for side in (-1, 1):
                a = ang + side * rng.uniform(.6, 1.1)
                L = rng.uniform(26, 44) * (1 - depth * .2)
                cv2.ellipse(leaf, (int(px + np.cos(a) * L * .6), int(py + np.sin(a) * L * .6)),
                            (int(L * .62), int(L * .26)), np.degrees(a), 0, 360, 1.0, -1)
        if depth < 2:
            for _ in range(2):
                branch(x1, y1, ang + rng.uniform(-.6, .6), length * .62, depth + 1)
    branch(W_ * 1.02, -H_ * .04, np.radians(150), W_ * .17, 0)
    branch(W_ * 1.03, H_ * .10, np.radians(170), W_ * .12, 1)
    leaf = cv2.GaussianBlur(leaf, (0, 0), W_ * .006)
    out *= (1 - .26 * np.clip(leaf, 0, 1))[..., None]
    # 가장자리 살짝 어둡게
    yy, xx = np.mgrid[0:H_, 0:W_].astype(np.float32)
    vig = ((xx / W_ - .45) ** 2 + (yy / H_ - .45) ** 2)
    out *= (1 - .22 * np.clip(vig, 0, 1))[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)


def main():
    P = os.path.join(W, 'assets', 'photo')
    # 원료카드 시트 (A5 비율에 가까운 0.69)
    # Taste 시트는 윗면 반사광·오른쪽 나뭇결 때문에 윤곽이 번져 모서리를 직접 지정(원본 픽셀)
    t, tm = card('KakaoTalk_20261021_104335602.jpg', None, 0.69,
                 corners=[(446, 736), (2318, 714), (2334, 3496), (412, 3536)])
    d, dm = card('KakaoTalk_20261021_104328230.jpg', (550, 880, 2050, 2850), 0.69)
    # (v1.5 2차) 대표가 보낸 원료카드 디자인 원본으로 교체 — 위 실사 t·d 는 참고용으로 남김
    t, tm = sheet('KakaoTalk_20261021_132124239.png')
    d, dm = sheet('KakaoTalk_20261021_132155503.png')
    imwrite(os.path.join(P, 'cards_pair.jpg'), place_many([(t, tm, .43, .265), (d, dm, .43, .735)], 1400, 1400))
    # 파우치
    im = imread(os.path.join(SRC, 'KakaoTalk_20261021_103935472.jpg'))
    m, c = grab(im, (420, 1080, 1880, 2400))
    x, y, w, h = cv2.boundingRect(c)
    imwrite(os.path.join(P, 'pouch_v2.jpg'), place(im[y:y + h, x:x + w], m[y:y + h, x:x + w], 1080, 1350, .62))
    # 단팥차 샘플 티백(대표 제공 누끼 PNG, 알파 채널 그대로)
    rgba = cv2.imdecode(np.fromfile(os.path.join(SRC, 'KakaoTalk_20261021_113400192.png'), np.uint8), cv2.IMREAD_UNCHANGED)
    a = rgba[..., 3]
    ys, xs = np.where(a > 8)
    rgba = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    imwrite(os.path.join(P, 'danpatt_sample.jpg'), place(rgba[..., :3], rgba[..., 3], 1500, 1000, .40))
    # 원료 랜덤 3팩(대표 제공 누끼 PNG)
    rgba = cv2.imdecode(np.fromfile(os.path.join(SRC, 'KakaoTalk_20261021_140755518.png'), np.uint8), cv2.IMREAD_UNCHANGED)
    imwrite(os.path.join(P, 'random3_packs.jpg'), place(rgba[..., :3], rgba[..., 3], 1600, 800, .62))
    # 키트 구성: 실물 촬영본 누끼(생성 플랫레이는 라벤더·유자 중복 등 구성 오류가 있어 쓰지 않음)
    o, m = kit_real('KakaoTalk_20261021_142249431.jpg')
    imwrite(os.path.join(P, 'kit_real.jpg'), place(o, m, 1800, 1200, .90))
    imwrite(os.path.join(P, 'kit_staged.jpg'), stage_kit(o, m))
    # 경품: 티아포테카 차 4종(대표 제공 연출 컷, 그대로)
    imwrite(os.path.join(P, 'prize_teas_real.jpg'), imread(os.path.join(SRC, 'KakaoTalk_20261021_141128112.png')))
    print('ok')


if __name__ == '__main__':
    main()
