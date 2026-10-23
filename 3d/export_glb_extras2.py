"""홈페이지용 GLB 추가 내보내기 — 간지 · 단팥차 샘플 (10/23, 와디즈 E안과 같은 구성으로).

  blender -b --python 3d/export_glb_extras2.py
출력: 3d/web/extras2.glb  (ganji: 128×172mm 미장 인쇄 간지 / danpatt: 단팥차 샘플 티백 74mm)
"""
import bpy, os, sys

os.environ['BOARD_T'] = '2.6'
os.environ['WEB_EXPORT'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_scene as K
import flatlay_scene as F
from export_glb_common import export, shrink_textures  # noqa: E402  (아래에서 만든 공용 모듈)

MOBILE = os.environ.get('MOBILE') == '1'
OUT = os.path.join(K.ROOT, '3d', 'web', 'm') if MOBILE else os.path.join(K.ROOT, '3d', 'web')
os.makedirs(OUT, exist_ok=True)


def ganji(x, y, z):
    """간지: 노트 밑에 까는 미장 인쇄 판지(base_floor 텍스처 = 실물 간지 무늬). unbox_anim.ganji 와 같은 치수."""
    m = K.img_mat('ganji', K.tex('base_floor'), rough=0.85, bump=0.2)
    w, h = 128.0, 172.0
    K.quad('ganji', [(x - w / 2, y + h / 2, z), (x + w / 2, y + h / 2, z), (x + w / 2, y - h / 2, z), (x - w / 2, y - h / 2, z)],
           m, K.img_mat('paper_back', None, rgb=(0.93, 0.92, 0.89), rough=0.85), thick=1.2, out=(0, 0, 1))


K.reset(); K._mats.clear()
ganji(0, 0, 0)
F.danpatt(220, 0, 0.3, 0)
shrink_textures(384 if MOBILE else 768)
export(os.path.join(OUT, 'extras2.glb'))
