"""플랫레이 3D 씬용 텍스처 — 실물 사진에서 펴서 잘라 낸 면 + 원료별 파우치 라벨.

실행:  python 3d/make_flatlay_tex.py
입력:  wadiz/2차수정/ (대표가 준 실물 사진)
출력:  3d/tex/flatlay/*.png
- pouch_<key>.png  : 캐모마일 실물 파우치(펴서 반듯하게)를 템플릿으로, 라벨 글자와 창 속 내용물을 원료별로 바꿈
                     (내용물 = 대표 실촬영 누끼 wadiz/assets/real/herb_<key>.png, 10/22)
- pouch_teabag.png : 빈 티백 파우치 실물
- postcard_use.png : 사용 안내 엽서 실물
- card_taste.png   : 키트 실물 컷의 분홍 원료 카드
- card_depth.png   : 원료 카드 디자인 원본(곡물)의 왼쪽 두 열
- card_<ver>_full.png : 일러카드 전체 시트(디자인 원본)
- pouch_blank_*.png: 원료 랜덤 3팩(라벨 비움)
- danpatt.png      : 단팥차 샘플 티백(누끼)
"""
import os, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'wadiz', '2차수정')
OUT = os.path.join(ROOT, '3d', 'tex', 'flatlay')
FONT = r'C:\Windows\Fonts\NotoSansKR-VF.ttf'
PW, PH = 880, 1160                       # 파우치 텍스처(88 x 116 mm)
LABEL = np.float32([(228, 95), (668, 105), (666, 238), (230, 228)])   # 템플릿 라벨 네 모서리
WINDOW = (60, 470, 820, 960)              # 템플릿 유산지 창(내용물 보이는 곳)

TASTE = [('lemon_balm', '레몬밤', 'Lemon Balm · Melissa officinalis'),
         ('peppermint', '페퍼민트', 'Peppermint · Mentha piperita'),
         ('chamomile', '캐모마일', 'Chamomile · Matricaria chamomilla'),
         ('hibiscus', '히비스커스', 'Hibiscus · Hibiscus sabdariffa'),
         ('yuza', '유자', 'Yuzu · Citrus junos'),
         ('rose', '장미', 'Rose · Rosa damascena')]
DEPTH = [('brown_rice', '현미', 'Brown Rice · Oryza sativa'),
         ('dandelion_root', '민들레뿌리', 'Dandelion Root · Taraxacum officinale'),
         ('sorghum', '찰수수', 'Glutinous Sorghum · Sorghum bicolor'),
         ('barley', '보리', 'Barley · Hordeum vulgare'),
         ('red_bean', '단팥', 'Red Bean · Vigna angularis'),
         ('solomons_seal', '둥굴레', "Solomon's Seal · Polygonatum odoratum")]
# 곡물은 알갱이 모양이 보여야 해서 원료 썸네일의 병 속 부분을 그대로 쓴다(왼쪽 위, 240 x 160, 1024 원본 좌표)
GRAIN_XY = {'red_bean': (450, 430), 'sorghum': (400, 460)}
# 키트 실물 컷(폭 900 축소 좌표 기준) — 분홍 원료 카드를 잘라 옴
KIT = 'KakaoTalk_20261021_142249431.jpg'


def rd(p, flag=cv2.IMREAD_UNCHANGED):
    return cv2.imdecode(np.fromfile(p, np.uint8), flag)


def wr(p, im):
    cv2.imencode('.png', im)[1].tofile(p)


def rectify(im, q, W, H):
    M = cv2.getPerspectiveTransform(np.float32(q), np.float32([[0, 0], [W, 0], [W, H], [0, H]]))
    return cv2.warpPerspective(im, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def label_img(w, h, ko, en, bg):
    """라벨 한 장: 위에 한글 굵게, 아래 영문 이탤릭(기울여 그림)."""
    sc = 3
    im = Image.new('RGB', (w * sc, h * sc), tuple(int(c) for c in bg[::-1]))
    d = ImageDraw.Draw(im)
    fk = font(36 * sc, 800)
    tw = d.textlength(ko, font=fk)
    d.text(((w * sc - tw) / 2, 22 * sc), ko, font=fk, fill=(34, 32, 34))
    # 영문: 따로 그린 뒤 기울여 붙임
    fe = font(21 * sc, 480)
    ew = int(d.textlength(en, font=fe)) + 40 * sc
    lay = Image.new('L', (ew, 36 * sc), 0)
    ImageDraw.Draw(lay).text((20 * sc, 0), en, font=fe, fill=255)
    lay = lay.transform(lay.size, Image.AFFINE, (1, 0.2, -3 * sc, 0, 1, 0), resample=Image.BICUBIC)
    col = Image.new('RGB', lay.size, (58, 56, 62))
    im.paste(col, (int((w * sc - ew) / 2), 76 * sc), lay)
    return cv2.cvtColor(np.array(im.resize((w, h), Image.LANCZOS)), cv2.COLOR_RGB2BGR)


def pouch_template():
    src = rd(os.path.join(OUT, '_pouch_src.png'))           # 캐모마일 파우치 누끼(RGBA)
    q = np.float32([(12, 0), (822, 28), (800, 1012), (18, 1000)]) * 2
    return rectify(src, q, PW, PH)


def put_label(t, ko, en):
    out = t.copy()
    lw, lh = 440, 140
    bg = np.median(t[120:210, 250:300, :3].reshape(-1, 3), axis=0)
    lab = label_img(lw, lh, ko, en, bg)
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [lw, 0], [lw, lh], [0, lh]]), LABEL)
    warped = cv2.warpPerspective(lab, M, (PW, PH), flags=cv2.INTER_CUBIC)
    m = cv2.warpPerspective(np.full((lh, lw), 255, np.uint8), M, (PW, PH))
    m = cv2.erode(m, np.ones((3, 3), np.uint8))
    out[..., :3][m > 0] = warped[m > 0]
    return out


def jar_color(key):
    """원료 썸네일(유리병) 내용물의 평균 색(Lab) — 흰 배경·유리 반사는 뺀다."""
    im = rd(os.path.join(ROOT, 'wadiz', 'assets', 'real', f'ing_{key}.png'), cv2.IMREAD_COLOR)
    c = im[380:640, 380:640]
    hsv = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    keep = (hsv[..., 1] > 60) & (hsv[..., 2] > 40)
    lab = cv2.cvtColor(c, cv2.COLOR_BGR2LAB).reshape(-1, 3)[keep.ravel()].astype(np.float32)
    return lab.mean(0)


DARKEN = {'hibiscus': -28, 'peppermint': -10}     # 말린 히비스커스·페퍼민트는 더 짙다


def put_contents(t, key, n):
    """유산지 창: 실물 캐모마일 파우치의 잎 결(밝기)은 그대로 두고 색만 원료 색으로 옮긴다.
    파우치마다 결을 뒤집거나 돌려 같은 무늬가 반복되지 않게 한다."""
    x0, y0, x1, y1 = WINDOW
    base = t[y0:y1, x0:x1, :3]
    var = [base, cv2.flip(base, 1), cv2.flip(base, 0), cv2.rotate(base, cv2.ROTATE_180), cv2.flip(base, -1)][n % 5]
    var = cv2.resize(var, (x1 - x0, y1 - y0))
    lab = cv2.cvtColor(var, cv2.COLOR_BGR2LAB).astype(np.float32)
    L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]
    tL, tA, tB = jar_color(key)
    # 유산지 너머라 색은 70%만, 밝기는 원료가 어두우면 조금 낮춤
    A2 = 128 + (tA - 128) * .70 + (A - A.mean()) * .5
    B2 = 128 + (tB - 128) * .70 + (B - B.mean()) * .5
    L2 = (L - L.mean()) * 1.1 + L.mean() + (tL - 150) * .25 + DARKEN.get(key, 0)
    new = cv2.cvtColor(np.clip(np.dstack([L2, A2, B2]), 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)
    h, w = new.shape[:2]
    m = np.zeros((h, w), np.float32); cv2.rectangle(m, (40, 30), (w - 40, h - 30), 1, -1)
    m = cv2.GaussianBlur(m, (0, 0), 20)[..., None]
    out = t.copy()
    out[y0:y1, x0:x1, :3] = np.clip(base.astype(np.float32) * (1 - m) + new * m, 0, 255).astype(np.uint8)
    return out


def put_grains(t, key):
    """곡물 파우치: 병 속 알갱이 사진을 창에 깔고 유산지 흰빛·주름을 얹는다."""
    im = rd(os.path.join(ROOT, 'wadiz', 'assets', 'real', f'ing_{key}.png'), cv2.IMREAD_COLOR)
    gx, gy = GRAIN_XY.get(key, (390, 430))
    x0, y0, x1, y1 = WINDOW
    w, h = x1 - x0, y1 - y0
    p = cv2.resize(im[gy:gy + 160, gx:gx + 240], (w, h), interpolation=cv2.INTER_CUBIC).astype(np.float32)
    p = cv2.GaussianBlur(p, (0, 0), 1.6)
    base = t[y0:y1, x0:x1, :3].astype(np.float32)
    lum = cv2.cvtColor(base.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    lum = (lum / lum.mean())[..., None]
    frost = (p * .72 + 226 * .28) * lum ** .55
    m = np.zeros((h, w), np.float32); cv2.rectangle(m, (40, 30), (w - 40, h - 30), 1, -1)
    m = cv2.GaussianBlur(m, (0, 0), 20)[..., None]
    out = t.copy()
    out[y0:y1, x0:x1, :3] = np.clip(base * (1 - m) + frost * m, 0, 255).astype(np.uint8)
    return out


def put_real(t, key):
    """(10/22) 대표 실촬영 원료 누끼(herb_<key>.png) 가운데를 유산지 창에 깐다 — 모든 원료 공통."""
    im = rd(os.path.join(ROOT, 'wadiz', 'assets', 'real', f'herb_{key}.png'))
    S = im.shape[0]
    x0, y0, x1, y1 = WINDOW
    w, h = x1 - x0, y1 - y0
    cw = int(S * .56); ch = int(cw * h / w)
    cx, cy = S // 2, S // 2
    p = im[cy - ch // 2:cy + ch // 2, cx - cw // 2:cx + cw // 2]
    a = p[..., 3:4].astype(np.float32) / 255
    p = p[..., :3].astype(np.float32) * a + 200 * (1 - a)          # 혹시 빈틈은 유산지색
    p = cv2.resize(p, (w, h), interpolation=cv2.INTER_AREA)
    p = cv2.GaussianBlur(p, (0, 0), 1.2)
    base = t[y0:y1, x0:x1, :3].astype(np.float32)
    lum = cv2.cvtColor(base.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    lum = (lum / lum.mean())[..., None]
    frost = (p * .74 + 226 * .26) * lum ** .5
    m = np.zeros((h, w), np.float32); cv2.rectangle(m, (40, 30), (w - 40, h - 30), 1, -1)
    m = cv2.GaussianBlur(m, (0, 0), 20)[..., None]
    out = t.copy()
    out[y0:y1, x0:x1, :3] = np.clip(base * (1 - m) + frost * m, 0, 255).astype(np.uint8)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    t = pouch_template()
    for n, (key, ko, en) in enumerate(TASTE):
        p = put_real(t, key)
        wr(os.path.join(OUT, f'pouch_{key}.png'), put_label(p, ko, en))
    for key, ko, en in DEPTH:
        wr(os.path.join(OUT, f'pouch_{key}.png'), put_label(put_real(t, key), ko, en))
    # 원료 랜덤 3팩: 라벨을 비워 두고 내용물만 서로 다르게
    for i, key in enumerate(['rose', 'peppermint', 'yuza']):
        wr(os.path.join(OUT, f'pouch_blank_{i + 1}.png'), put_label(put_real(t, key), '', ''))
    # Depth 원료 카드: 디자인 원본(곡물 시트)의 왼쪽 두 열 — Taste 카드(실물)와 같은 폭
    sh = rd(os.path.join(SRC, 'KakaoTalk_20261021_132155503.png'), cv2.IMREAD_COLOR)
    wr(os.path.join(OUT, 'card_depth.png'), cv2.resize(sh[100:1372, 101:701], (520, 1070), interpolation=cv2.INTER_AREA))
    # 일러카드(원료 카드 전체 시트 3 x 2): 디자인 원본의 체커보드 바깥을 잘라 냄
    for ver, f in (('taste', 'KakaoTalk_20261021_132124239.png'), ('depth', 'KakaoTalk_20261021_132155503.png')):
        im = rd(os.path.join(SRC, f), cv2.IMREAD_COLOR)
        card = (cv2.cvtColor(im, cv2.COLOR_BGR2HSV)[..., 1] > 18).astype(np.uint8)
        xs = np.where(card.mean(0) > .5)[0]; ys = np.where(card.mean(1) > .5)[0]
        wr(os.path.join(OUT, f'card_{ver}_full.png'), im[ys.min() + 4:ys.max() - 3, xs.min() + 4:xs.max() - 3])
    # 단팥차 샘플(대표 제공 누끼 PNG)
    dp = rd(os.path.join(SRC, 'KakaoTalk_20261021_113400192.png'))
    ys, xs = np.where(dp[..., 3] > 8)
    wr(os.path.join(OUT, 'danpatt.png'), dp[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    # 빈 티백 파우치(뒷면 실물: 라벨 없이 티백·택 카드가 비침), 1/4 축소 좌표 ×4
    im = rd(os.path.join(SRC, 'KakaoTalk_20261021_103944923.jpg'), cv2.IMREAD_COLOR)
    q = np.float32([(176, 315), (590, 322), (575, 857), (166, 845)]) * 4
    tb = rectify(im, q, PW, PH)
    wr(os.path.join(OUT, 'pouch_teabag.png'), np.dstack([tb, np.full(tb.shape[:2], 255, np.uint8)]))
    # 사용 안내 엽서(148 x 104 mm)
    im = rd(os.path.join(SRC, 'KakaoTalk_20261021_104416048.jpg'), cv2.IMREAD_COLOR)
    q = np.float32([(81, 322), (690, 325), (686, 752), (75, 748)]) * 4
    pc = rectify(im, q, 1480, 1040)
    # 실내등 아래라 회색 → 종이 흰색 기준으로 밝힘
    gain = 238 / np.median(pc.reshape(-1, 3), axis=0)
    wr(os.path.join(OUT, 'postcard_use.png'), np.clip(pc * gain, 0, 255).astype(np.uint8))
    # 분홍 원료 카드(키트 실물 컷)
    im = rd(os.path.join(SRC, KIT), cv2.IMREAD_COLOR)
    k = im.shape[1] / 900
    q = np.float32([(580, 404), (676, 406), (675, 615), (581, 614)]) * k
    card = cv2.convertScaleAbs(rectify(im, q, 520, 1070), alpha=1.08, beta=10)
    wr(os.path.join(OUT, 'card_taste.png'), card)
    print('ok')


if __name__ == '__main__':
    main()
