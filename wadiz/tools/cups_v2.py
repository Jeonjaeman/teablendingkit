"""cups_two.png 2차 수정: 오른쪽 잔 빨강 → 맑은 브라운, 잔 주변 꽃·원료 제거."""
import cv2, numpy as np, sys
src, out = sys.argv[1], sys.argv[2]
im = cv2.imdecode(np.fromfile(src, np.uint8), cv2.IMREAD_COLOR)
H, W = im.shape[:2]

def ell(m, cx, cy, rx, ry=None):
    cv2.ellipse(m, (cx, cy), (rx, ry or rx), 0, 0, 360, 255, -1)

# 1) 잔 속 꽃 반사 무늬 제거
refl = np.zeros((H, W), np.uint8)
for cx, cy, rx, ry in [(790, 560, 52, 55), (815, 600, 30, 20), (945, 585, 18, 30),
                       (380, 565, 35, 40), (468, 590, 16, 14)]:
    ell(refl, cx, cy, rx, ry)
# 반사 무늬 중 실제로 어두운/진한 픽셀만
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32)
blur = cv2.GaussianBlur(im, (0, 0), 14).astype(np.float32)
diff = np.abs(im.astype(np.float32) - blur).sum(2)
spots = ((diff > 28) & (refl > 0)).astype(np.uint8) * 255
spots = cv2.dilate(spots, np.ones((7, 7), np.uint8))
im = cv2.inpaint(im, spots, 7, cv2.INPAINT_TELEA)

# 2) 테이블 위 꽃·원료 제거
obj = np.zeros((H, W), np.uint8)
for e in [(185, 660, 85, 62), (205, 700, 40, 32), (83, 660, 18, 16), (345, 685, 48, 32),
          (515, 688, 24, 20), (672, 660, 80, 66), (760, 662, 40, 30), (722, 714, 14, 12),
          (835, 704, 46, 38), (1028, 666, 22, 16), (1130, 656, 52, 32), (1078, 695, 14, 12),
          (972, 718, 14, 12), (288, 704, 12, 12), (440, 700, 10, 8)]:
    ell(obj, *e)
# 잔 몸통(유리)은 건드리지 않음
cv2.ellipse(obj, (448, 560), (170, 105), 0, 0, 360, 0, -1)
cv2.ellipse(obj, (848, 556), (172, 104), 0, 0, 360, 0, -1)
im = cv2.inpaint(im, obj, 25, cv2.INPAINT_TELEA)
# 남은 작은 부스러기·그림자 점: 테이블 영역에서 주변보다 확 어두운 작은 점
g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
bg = cv2.medianBlur(im, 31); gb = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY).astype(np.float32)
spk = ((gb - g) > 14).astype(np.uint8) * 255
spk[:600] = 0
cv2.ellipse(spk, (448, 560), (172, 112), 0, 0, 360, 0, -1)
cv2.ellipse(spk, (848, 556), (174, 112), 0, 0, 360, 0, -1)
cv2.rectangle(spk, (150, 380), (350, 640), 0, -1); cv2.rectangle(spk, (940, 380), (1150, 640), 0, -1)
n, lab, st, _ = cv2.connectedComponentsWithStats(spk)
for i in range(1, n):
    if st[i, cv2.CC_STAT_AREA] > 400: spk[lab == i] = 0
spk = cv2.dilate(spk, np.ones((9, 9), np.uint8))
obj = cv2.max(obj, spk)
im = cv2.inpaint(im, spk, 9, cv2.INPAINT_TELEA)
# 넓게 채운 자리의 얼룩을 부드럽게
soft = cv2.GaussianBlur(obj, (0, 0), 10).astype(np.float32)[..., None] / 255
im = (im * (1 - soft) + cv2.GaussianBlur(im, (0, 0), 12) * soft).astype(np.uint8)

# 잔 밑동에 걸친 부스러기
cr = np.zeros((H, W), np.uint8); ell(cr, 760, 641, 20, 9)
im = cv2.inpaint(im, cr, 6, cv2.INPAINT_TELEA)

# 3) 오른쪽 잔·바닥 붉은 빛 → 맑은 브라운
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32)
h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
red = (((h < 12) | (h > 160)) & (s > 40)).astype(np.float32)
red[:, :660] = 0
# 잔 안 수면·가장자리의 옅은 분홍까지
zone = np.zeros((H, W), np.uint8); cv2.ellipse(zone, (848, 540), (175, 140), 0, 0, 360, 255, -1)
red = np.maximum(red, (((h < 12) | (h > 150)) & (s > 12) & (zone > 0)).astype(np.float32))
red = cv2.GaussianBlur(red, (0, 0), 2)
s2 = s / 255
# 브라운: 색상 14(≈28°), 채도·명도 조정 — 진할수록 더 어둡게
nh = np.full_like(h, 13.0)
ns = np.clip(s * 0.95 + 8, 0, 255)
nv = np.clip(v * (0.86 - 0.12 * s2) + 6, 0, 255)
new = cv2.cvtColor(np.dstack([nh, ns, nv]).astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
im = (im * (1 - red[..., None]) + new * red[..., None]).astype(np.uint8)
cv2.imencode(".png", im)[1].tofile(out)
