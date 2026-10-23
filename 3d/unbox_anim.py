"""키트 언박싱 — 실물 포장 순서대로 하나씩 꺼내 펼치는 애니메이션(블렌더 직접 연출).

실행:  blender -b --python 3d/unbox_anim.py -- [taste|depth] [--preview]
       PORTRAIT=1 blender -b --python 3d/unbox_anim.py -- taste   → 세로 9:16(1080x1920) 홈페이지 모바일 대체 영상용
실물 포장(대표 확인 10/21):
  왼칸 = 띠지 두른 아코디언 북(첫 장 빈 티백 파우치 + 원료 6팩 + 엽서)
  오른칸 = 위에서부터 허브 스티커(일러카드) → 종이 스쿱 → 노트(책) → 간지 → 간지 아래 단팥차 샘플·인퓨저   (10/23 확정)
순서: 뚜껑 열림 → 오른칸 허브 스티커 → 종이 스쿱 → 노트 → 왼칸 북에서 빈 티백 → 원료 6팩 → 엽서
      → 간지를 왼칸 위로 밀어 둠 → 단팥차 샘플·인퓨저 → 간지 다시 넣음 → 뚜껑 닫힘
마지막 프레임 = flatlay_scene 정지 컷 배열(대표 레퍼런스 10/21): 닫힌 상자 왼쪽 위, 스쿱 종이·카드·노트 오른쪽 위,
책갈피 부채꼴·인퓨저 왼쪽 아래, 파우치 4+3 오른쪽 아래.
앞 6초(144프레임)만 렌더하고 인코딩 때 거꾸로 이어 12초 끊김 없는 루프로 만든다.
출력: 3d/anim/unbox_<ver>/####.png  →  python 3d/make_unbox_mp4.py <ver>
      세로: 3d/anim/unbox_<ver>_v/####.png  →  python 3d/make_unbox_mp4.py <ver>_v  (wadiz/assets/loop/unbox_<ver>_v.mp4)
"""
import bpy, math, os, sys
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_scene as K
import flatlay_scene as F

MM = K.MM
FPS, N = 24, 144
RES = (960, 640)
WIDTH = 0.78                       # 화면 폭(m) — flatlay_scene 정지 컷과 같음
# 세로(PORTRAIT=1): 홈페이지 모바일 대체 영상. 폰에서 object-fit: cover 로 좌우가 10% 안팎 잘리므로 피사체를 화면 폭의
# 중앙 78% 안에, 세로로는 위쪽 60% 안에 둔다(아래 40% = 글 상자 자리). 가로 플랫레이(0.59 x 0.48)를 정사각형에 가깝게 다시 짠다:
# 상자·카드·노트 줄은 그대로, 파우치 7팩은 50mm 오른쪽으로, 책갈피 부채꼴은 상자 바로 아래(왼쪽 끝 = 상자 왼쪽 끝),
# 인퓨저는 파우치 아래에 눕히고 그 오른쪽에 단팥차 샘플 → 0.53 x 0.53.
PORTRAIT = os.environ.get('PORTRAIT') == '1'
P_RES = (1080, 1920)
P_WIDTH = 0.68                     # 화면 폭(m) → 높이 = 0.68 * 16 / 9 = 1.209
P_CAM = (0.038, -0.317)            # 카메라 중심(m): 피사체(x -0.226~0.303, y -0.318~0.215)가 위쪽 6~50% 에 오도록
POUCH_DX = 50 if PORTRAIT else 0                                      # 파우치 x 이동(mm)
MARKS = (-68, -160) if PORTRAIT else F.P(222, 948)                    # 책갈피 부채꼴 축(오른쪽 아래 모서리)
INFUSER = ((-85, -275), (50, -275)) if PORTRAIT else (F.P(285, 694), F.P(283, 905))   # (손잡이 끝, 공)
DANPATT = (165, -275) if PORTRAIT else (330, -205)
BOX = F.P(307, 470)                # 상자 중심(mm) — 정지 컷 자리
CY = -K.LEDGE / 2 - 1              # 칸 중심 y(상자 기준)
LEFT = (BOX[0] - K.BX / 4, BOX[1] + CY)
RIGHT = (BOX[0] + K.BX / 4, BOX[1] + CY)
FLIGHT = 16


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def group(name, fn):
    """fn 이 새로 만든 오브젝트들을 빈 오브젝트 하나 아래로 묶는다(피벗 = 바운딩 중심, 바닥 높이 0)."""
    before = set(bpy.data.objects)
    fn()
    bpy.context.view_layer.update()
    new = [o for o in bpy.data.objects if o not in before]
    tops = [o for o in new if o.parent is None]
    pts = [o.matrix_world @ Vector(c) for o in new if o.type == 'MESH' for c in o.bound_box]
    c = sum(pts, Vector()) / len(pts)
    e = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(e)
    e.location = (c.x, c.y, 0)
    bpy.context.view_layer.update()
    for o in tops:
        mw = o.matrix_world.copy()
        o.parent = e
        o.matrix_world = mw
    return e


def ganji(x, y, z):
    """간지: 노트 밑에 까는 미장 인쇄 판지(base_floor 텍스처 = 실물 간지 무늬)."""
    m = K.img_mat('ganji', K.tex('base_floor'), rough=0.85, bump=0.2)
    w, h = 128.0, 172.0
    K.quad('ganji', [(x - w / 2, y + h / 2, z), (x + w / 2, y + h / 2, z), (x + w / 2, y - h / 2, z), (x - w / 2, y - h / 2, z)],
           m, K.img_mat('paper_back', None, rgb=(0.93, 0.92, 0.89), rough=0.85), thick=1.2, out=(0, 0, 1))


def build(ver):
    """plan: (이름, 최종 자리에 만드는 함수, 상자 안 시작 자리 mm(x, y, z), 시작 회전(도), 시작 배율, 출발 프레임)
    최종 배치 = flatlay_scene 정지 컷(대표 제공 레퍼런스 배열). 시작 배율이 음수면 출발 전에는 숨긴다
    (파우치·엽서: 왼칸 병풍책 안에서 나오는 것처럼). 병풍책과 간지는 상자 안에 남는다."""
    kit = F.KITS[ver]
    Q = F.P
    root, hinge = K.build_box(0.0, with_contents=False)
    root.location = (BOX[0] * MM, BOX[1] * MM, 0)
    K.build_closed_book(root, (-K.BX / 4, CY, K.T), band=ver)          # 왼칸 병풍책(띠지) — 그대로 둠
    R = RIGHT
    bk = (LEFT[0], LEFT[1], K.BOOK[2] - 10)
    plan = []
    slots = list(zip((361.5, 497.5, 631.5, 769.5), [741.5] * 4, kit['row1'], (0.2, 0.25, 0.3, 0.35))) +         list(zip((421, 560, 699.5), [887] * 3, kit['row2'], (4.2, 4.3, 4.4)))
    L = LEFT
    top = K.BOOK[2] + K.T                                            # 병풍책 윗면 높이
    # ▶ 오른칸 노트 위(10/23 확정): 허브 스티커(일러카드) → 종이 스쿱 → 노트(책)
    plan.append(('card', lambda: F.flat_card(kit['card'] + '_c', F.flt(kit['card']), F.CARD[0], F.CARD[1], 116, 166, 0.45, rot=F.CARD[2]),
                 (R[0], R[1], 57), 0, 0.95, 26))
    plan.append(('scoop', lambda: F.flat_card('scoop_paper', F.flt('postcard_use'), F.SCOOP[0], F.SCOOP[1], 104, 146, 0.0, uv_rot=3, rot=F.SCOOP[2]),
                 (R[0], R[1], 56), 0, 0.95, 31))
    plan.append(('note', lambda: F.note(F.NOTE[0], F.NOTE[1], 115, 152, 11, F.NOTE[2]), (R[0], R[1], 44), 0, 1.0, 36))
    # ▶ 왼칸: 아코디언 북 — 첫 장의 빈 티백 파우치(대표 확인 10/22 16:53) → 원료 6팩 → 엽서
    pouch_slots = [sl for sl in slots if sl[2] == 'teabag'] + [sl for sl in slots if sl[2] != 'teabag']
    for n, (u, v, key, z) in enumerate(pouch_slots):
        x, y = Q(u, v)
        x += POUCH_DX
        fn = (lambda key=key, x=x, y=y, z=z: F.pouch('pouch_' + key, F.flt('pouch_' + key), x, y, z))
        plan.append(('p_' + key, fn, (bk[0], bk[1], bk[2] + n * 0.6), 25 if n % 2 else -25, -0.4, 44 + n * 4.5))
    plan.append(('marks', lambda: F.bookmarks(*MARKS), (bk[0], bk[1], bk[2] - 4), 60, -0.5, 76))
    # ▶ 오른칸 아래: 간지를 왼칸 위로 밀어 두면 그 아래 단팥차 샘플 · 인퓨저
    plan.append(('danpatt', lambda: F.danpatt(DANPATT[0], DANPATT[1], 0.3, 9), (R[0] + 15, R[1] - 25, 10), -10, 0.9, 97))
    plan.append(('infuser', lambda: F.infuser(*INFUSER), (R[0], R[1] - 10, 4), 0, 0.7, 104))
    items = [(group(n_, fn), s_, r, sc, t0) for (n_, fn, s_, r, sc, t0) in plan]
    g = group('ganji', lambda: ganji(0, 0, 0))
    return hinge, items, g


def key_obj(e, f, loc, rz, s):
    e.location = loc
    e.rotation_euler = (0, 0, rz)
    e.scale = (s, s, s)
    for p in ('location', 'rotation_euler', 'scale'):
        e.keyframe_insert(p, frame=f)


def animate(hinge, items, ganji_obj):
    for e, (sx, sy, sz), rot, sc, t0 in items:
        end, end_r = e.location.copy(), e.rotation_euler.z
        start = Vector((sx * MM, sy * MM, sz * MM))
        start_r = end_r + math.radians(rot)
        for f in range(1, N + 2):
            t = ease((f - 1 - t0) / FLIGHT)
            p = start.lerp(end, t)
            p.z += math.sin(math.pi * t) * 0.10                   # 들어 올렸다 내려놓기
            if sc < 0:              # 음수 배율 = 출발 전에는 숨김(병풍책 안에서 튀어나옴)
                s_ = 0.001 if f - 1 < t0 else -sc + (1 + sc) * t
            else:
                s_ = sc + (1 - sc) * t
            key_obj(e, f, p, start_r + (end_r - start_r) * t, s_)
    # 간지: 오른칸 노트 밑(z=42) → 왼칸 병풍책 위로 밀어 두었다가(82~) → 빈 티백·단팥차·인퓨저가 나오면(116~) 오른칸 바닥에 다시 넣음
    inbox = Vector((RIGHT[0] * MM, RIGHT[1] * MM, 42 * MM))   # 인퓨저(공 지름 약 33mm) 위로
    up = Vector((LEFT[0] * MM, LEFT[1] * MM, (K.BOOK[2] + 8) * MM))      # 왼칸 병풍책 위로 밀어 둠 → 오른칸이 드러남
    floor = Vector((RIGHT[0] * MM, RIGHT[1] * MM, (K.T + 0.6) * MM))
    for f in range(1, N + 2):
        a, b = ease((f - 1 - 82) / 12.0), ease((f - 1 - 116) / 12.0)
        pos = inbox.lerp(up, a).lerp(floor, b)
        pos.z += (math.sin(math.pi * a) + math.sin(math.pi * b)) * 0.04          # 옮길 때 살짝 들어 올림
        key_obj(ganji_obj, f, pos, math.radians(-4) * a * (1 - b), 1.0)
    # 뚜껑: 8~26 열림, 128~142 닫힘 → 마지막 프레임 = 정지 컷(닫힌 상자 + 펼친 구성품)
    for f in range(1, N + 2):
        ang = 100 * ease((f - 1 - 8) / 18.0) * (1 - ease((f - 1 - 128) / 14.0))
        hinge.rotation_euler = (math.radians(-ang), 0, 0)
        hinge.keyframe_insert('rotation_euler', frame=f)


def main():
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    ver = 'depth' if 'depth' in argv else 'taste'
    preview = '--preview' in argv
    K.reset(); K._mats.clear()
    sun = F.floor_and_light()
    if PORTRAIT:
        w, h = P_WIDTH, P_WIDTH * 16 / 9
        before = set(bpy.data.objects)
        F.occluders(sun, hw=w / 2, hh=h / 2)
        for o in bpy.data.objects:                 # 가림판(창틀 띠·잎 그림자)은 원점 기준이라 카메라 중심만큼 같이 옮긴다
            if o not in before:
                o.location.x += P_CAM[0]; o.location.y += P_CAM[1]
    else:
        F.occluders(sun, hw=WIDTH / 2, hh=WIDTH / 3)
    hinge, items, g = build(ver)
    animate(hinge, items, g)
    cam = bpy.data.cameras.new('cam'); cam.type = 'ORTHO'
    cam.ortho_scale = P_WIDTH * 16 / 9 if PORTRAIT else WIDTH      # 세로는 긴 변(높이)이 ortho_scale
    co = bpy.data.objects.new('cam', cam); bpy.context.scene.collection.objects.link(co)
    co.location = (P_CAM[0], P_CAM[1], 1.5) if PORTRAIT else (0, 0, 1.5)
    sc = bpy.context.scene
    sc.camera = co
    if PORTRAIT:
        K.render_setup(*((540, 960) if preview else P_RES), samples=16 if preview else 24)
    else:
        K.render_setup(*((600, 400) if preview else RES), samples=16 if preview else 24)
    sc.view_settings.view_transform = 'Standard'
    sc.view_settings.exposure = -0.45
    sc.render.fps = FPS
    sc.render.use_persistent_data = True
    sc.cycles.use_animated_seed = False
    out = os.path.join(K.ROOT, '3d', 'anim', f'unbox_{ver}' + ('_v' if PORTRAIT else '') + ('_preview' if preview else ''))
    os.makedirs(out, exist_ok=True)
    for old in os.listdir(out):
        if old.endswith('.png'):
            os.remove(os.path.join(out, old))
    frames = [1, 28, 34, 40, 56, 76, 88, 100, 110, 145] if preview else range(1, N + 2)
    for f in frames:
        sc.frame_set(f)
        sc.render.filepath = os.path.join(out, f'{f:04d}.png')
        bpy.ops.render.render(write_still=True)
    print('RENDERED unbox', ver, 'portrait' if PORTRAIT else 'landscape', len(list(frames)))


main()
