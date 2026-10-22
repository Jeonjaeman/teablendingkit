"""3차 수정(10/22): 대표가 보낸 실사 원료 누끼 12종 + 버전별 묶음 → 페이지·3D 용 이미지.

  python wadiz/tools/herbs_r3.py
입력: wadiz/3차수정/ (카톡 원본, 추적 제외)
출력:
  wadiz/assets/real/herb_<key>.png   원료 하나(투명 배경, 정사각 900)
  wadiz/assets/real/herbs_taste.jpg  VER.1 묶음 6종(크림 배경, 3:2)
  wadiz/assets/real/herbs_depth.jpg  VER.2 묶음 6종(크림 배경, 3:2)
색 보정(대표 요청): 히비스커스 더 붉게(대표가 준 보정본 사용) · 유자 더 주황빛 · 찰수수 살짝 와인빛
"""
import os, cv2, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
SRC = os.path.join(W, '3차수정')
OUT = os.path.join(W, 'assets', 'real')
CREAM = (234, 240, 245)                  # BGR — 대표 묶음 사진(…120724273.jpg) 배경 크림색

# 카톡 순서 = IMG_1444 … 1466 순서(대표가 이름을 붙여 보낸 순서)
FILES = {
    'lemon_balm': 'KakaoTalk_20261022_120205443.png',
    'peppermint': 'KakaoTalk_20261022_120220348.png',
    'hibiscus': 'KakaoTalk_20261022_120742076.png',      # 대표 색보정본(원래 120244495 는 검붉음)
    'yuza': 'KakaoTalk_20261022_120307234.png',
    'rose': 'KakaoTalk_20261022_120321489.png',
    'chamomile': 'KakaoTalk_20261022_120335425.png',
    'red_bean': 'KakaoTalk_20261022_120348369.png',
    'brown_rice': 'KakaoTalk_20261022_120403243.png',
    'solomons_seal': 'KakaoTalk_20261022_120427603.png',
    'dandelion_root': 'KakaoTalk_20261022_120446837.png',
    'barley': 'KakaoTalk_20261022_120500866.png',
    'sorghum': 'KakaoTalk_20261022_120523231.png',
}
# Lab 이동(L, a, b): 유자는 노랑·주황 쪽으로, 찰수수는 붉은(와인) 쪽으로
FIX = {'yuza': (3, 5, 14, 1.12), 'sorghum': (-2, 7, -3, 1.04)}
# 묶음 사진(가로형) 속 칸 배치: 3 x 2, 위→아래, 왼→오
GROUP = {
    'taste': ('KakaoTalk_20261022_120833727.png', ['chamomile', 'lemon_balm', 'hibiscus', 'rose', 'yuza', 'peppermint']),
    'depth': ('KakaoTalk_20261022_121013744.png', ['sorghum', 'brown_rice', 'dandelion_root', 'red_bean', 'barley', 'solomons_seal']),
}


def rd(p):
    return cv2.imdecode(np.fromfile(p, np.uint8), cv2.IMREAD_UNCHANGED)


def wr(p, im, q=88):
    ext = os.path.splitext(p)[1]
    cv2.imencode(ext, im, [cv2.IMWRITE_JPEG_QUALITY, q] if ext == '.jpg' else [])[1].tofile(p)


def fix(bgra, key, mask=None):
    """알파가 있는 픽셀(또는 mask 안)에만 Lab 이동 + 채도 배율."""
    if key not in FIX:
        return bgra
    dL, da, db, sat = FIX[key]
    bgr = bgra[..., :3]
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    lab[..., 1] = 128 + (lab[..., 1] - 128) * sat + da
    lab[..., 2] = 128 + (lab[..., 2] - 128) * sat + db
    lab[..., 0] += dL
    new = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    m = (bgra[..., 3] > 0) if mask is None else mask
    out = bgra.copy()
    out[..., :3][m] = new[m]
    return out


def crop_square(bgra, size=900, pad=0.06):
    ys, xs = np.where(bgra[..., 3] > 20)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    side = int(max(y1 - y0, x1 - x0) * (1 + 2 * pad))
    cy, cx = (y0 + y1) // 2, (x0 + x1) // 2
    canvas = np.zeros((side, side, 4), np.uint8)
    sy, sx = cy - side // 2, cx - side // 2
    H, Wd = bgra.shape[:2]
    a0, b0 = max(0, sy), max(0, sx)
    a1, b1 = min(H, sy + side), min(Wd, sx + side)
    canvas[a0 - sy:a1 - sy, b0 - sx:b1 - sx] = bgra[a0:a1, b0:b1]
    return cv2.resize(canvas, (size, size), interpolation=cv2.INTER_AREA)


def on_cream(bgra, W_, H_, shadow=True):
    """투명 묶음 사진을 크림 배경 W_ x H_ 가운데에(살짝 그림자)."""
    h, w = bgra.shape[:2]
    s = min(W_ * .94 / w, H_ * .94 / h)
    im = cv2.resize(bgra, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    h, w = im.shape[:2]
    x, y = (W_ - w) // 2, (H_ - h) // 2
    bg = np.full((H_, W_, 3), CREAM, np.float32)
    a = np.zeros((H_, W_), np.float32); a[y:y + h, x:x + w] = im[..., 3] / 255
    lay = np.zeros_like(bg); lay[y:y + h, x:x + w] = im[..., :3]
    if shadow:
        sh = cv2.GaussianBlur(np.roll(a, (int(H_ * .012), int(W_ * .006)), (0, 1)), (0, 0), W_ * .006) * .22
        bg *= (1 - sh)[..., None]
    out = bg * (1 - a[..., None]) + lay * a[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)


def main():
    os.makedirs(OUT, exist_ok=True)
    for key, f in FILES.items():
        im = rd(os.path.join(SRC, f))
        if im.shape[2] == 3:
            im = np.dstack([im, np.full(im.shape[:2], 255, np.uint8)])
        wr(os.path.join(OUT, f'herb_{key}.png'), crop_square(fix(im, key)))
    for ver, (f, keys) in GROUP.items():
        im = rd(os.path.join(SRC, f))
        H, Wd = im.shape[:2]
        # 칸마다 보정이 필요한 원료만(3 x 2 격자)
        for i, key in enumerate(keys):
            if key in FIX:
                r, c = divmod(i, 3)
                m = np.zeros((H, Wd), bool)
                m[r * H // 2:(r + 1) * H // 2, c * Wd // 3:(c + 1) * Wd // 3] = True
                im = fix(im, key, m & (im[..., 3] > 0))
        wr(os.path.join(OUT, f'herbs_{ver}.jpg'), on_cream(im, 1500, 1000))
    print('ok')


if __name__ == '__main__':
    main()
