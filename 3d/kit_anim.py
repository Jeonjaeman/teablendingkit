"""취향의 권리 키트 — 영상 컷 6종 (kit_scene.py 모델 재사용).

실행:  blender -b --python 3d/kit_anim.py -- <clip> [<clip> ...] [--preview]
clip:  rotate | lid_open | acc_unfold | acc_flip | note_flip | all
       (lid_close = lid_open 역재생, 인코딩 단계에서 만든다)
--preview: 각 클립 대표 프레임 몇 장만 저해상도로 렌더(구도 확인용)
출력: 3d/anim/<clip>/0001.png …  → make_anim_mp4.py 로 mp4 인코딩
"""
import bpy, math, os, sys
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_scene as K

MM = K.MM
FPS = 24
RES = (1280, 720)
SAMPLES = 32
ANIM = os.path.join(K.ROOT, '3d', 'anim')


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def setup(stage_size=5.0):
    _acc_objs.clear(); _note_objs.clear()
    K.reset(); K._mats.clear()
    K.stage(stage_size)
    K.render_setup(*RES, samples=SAMPLES)
    sc = bpy.context.scene
    sc.render.fps = FPS
    sc.cycles.use_animated_seed = False
    sc.render.use_persistent_data = True
    return sc


def outdir(clip):
    d = os.path.join(ANIM, clip)
    os.makedirs(d, exist_ok=True)
    return d


def render_frame(clip, f):
    sc = bpy.context.scene
    sc.frame_set(f)
    sc.render.filepath = os.path.join(outdir(clip), f'{f:04d}.png')
    bpy.ops.render.render(write_still=True)


def aim(cam, loc, target):
    cam.location = loc
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()


# ---------- 1. 회전 (닫힌 상자 턴테이블, 무한 반복용) ----------
def clip_rotate(frames):
    N = 144
    setup()
    root, hinge = K.build_box(0, with_contents=False)
    K.camera((0.0, -0.60, 0.34), (0, 0, 0.04), 50)
    for f in frames(N):
        root.rotation_euler = (0, 0, math.radians(360.0 * (f - 1) / N))
        render_frame('rotate', f)


# ---------- 2. 뚜껑 열림 (역재생 = 닫힘) ----------
def clip_lid_open(frames):
    N, HOLD0, OPEN = 108, 14, 62
    setup()
    root, hinge = K.build_box(0, with_contents=True)
    dust = [bpy.data.objects[f'dust_pivot_{s:+d}'] for s in (1, -1)]
    ears = [bpy.data.objects[f'ear_pivot_{s:+d}'] for s in (1, -1)]
    cam = K.camera((0.44, -0.60, 0.40), (0.0, 0.03, 0.06), 50)
    for f in frames(N):
        t = ease((f - 1 - HOLD0) / OPEN)
        # 날개·귀는 뚜껑이 어느 정도 들린 뒤 벌어진다
        tw = ease((f - 1 - HOLD0 - OPEN * 0.25) / (OPEN * 0.75))
        hinge.rotation_euler = (math.radians(-112.0 * t), 0, 0)
        for s, p in zip((1, -1), dust):
            p.rotation_euler = (0, math.radians(-s * 30.0 * tw), 0)
        for s, p in zip((1, -1), ears):
            p.rotation_euler = (0, 0, math.radians(-s * 25.0 * tw))
        # 카메라는 아주 느리게 다가간다
        k = (f - 1) / (N - 1)
        aim(cam, (lerp(0.52, 0.47, k), lerp(-0.74, -0.70, k), lerp(0.46, 0.53, k)), (0.0, 0.05, lerp(0.07, 0.115, ease(k * 1.4))))
        render_frame('lid_open', f)


# ---------- 아코디언: 패널별 각도로 매 프레임 재구성 ----------
_acc_objs = []


def clear_acc():
    for ob in _acc_objs:
        me = ob.data
        bpy.data.objects.remove(ob, do_unlink=True)
        if me is not None and me.users == 0:
            bpy.data.meshes.remove(me)
    _acc_objs.clear()


def build_acc_chain(angles, cov_f, cov_b, origin):
    """angles[i]: 패널 i 접힘각(도, 90=완전히 접힘). cov_f/cov_b: 앞·뒤 표지 방향각(도, +X 기준)."""
    pw, ph = K.PANEL
    faces = ['acc_in_01', 'acc_in_02', 'acc_in_03_win', 'acc_in_04', 'acc_in_05_win', 'acc_in_06',
             'acc_in_07_win', 'acc_in_08', 'acc_in_09_win', 'acc_in_10', 'acc_in_11_win', 'acc_in_12']
    pouch_faces = {1, 3, 5, 7, 9, 11}
    back = K.img_mat('paper_back', None, rgb=(0.95, 0.94, 0.91), rough=0.8)
    pouch = K.img_mat('pouch', K.tex('pouch'), rough=0.45)
    root = K.empty('accordion', (0, 0, 0))
    _acc_objs.append(root)
    x = y = 0.0
    for i, adeg in enumerate(angles):
        a = math.radians(adeg)
        sgn = 1 if i % 2 == 0 else -1
        dx, dy = pw * math.cos(a), sgn * pw * math.sin(a)
        p0, p1 = (x, y), (x + dx, y + dy)
        m = K.img_mat(faces[i], K.tex(faces[i]), rough=0.75, bump=0.1)
        _acc_objs.append(K.quad(f'panel_{i+1:02d}', [(p0[0], p0[1], ph), (p1[0], p1[1], ph), (p1[0], p1[1], 0), (p0[0], p0[1], 0)], m, back, thick=0.9, parent=root, out=(0, -1, 0)))
        if i in pouch_faces:
            nx, ny = -(p1[1] - p0[1]) / pw, (p1[0] - p0[0]) / pw
            if ny > 0:
                nx, ny = -nx, -ny
            off, u0, u1 = 2.5, 0.07, 0.93
            q0 = (p0[0] + dx * u0 + nx * off, p0[1] + dy * u0 + ny * off)
            q1 = (p0[0] + dx * u1 + nx * off, p0[1] + dy * u1 + ny * off)
            top, bot = ph * 0.86, ph * 0.86 - pw * 0.86
            _acc_objs.append(K.quad(f'pouch_{i+1:02d}', [(q0[0], q0[1], top), (q1[0], q1[1], top), (q1[0], q1[1], bot), (q0[0], q0[1], bot)], pouch, back, thick=1.5, parent=root, out=(0, -1, 0)))
        x, y = p1
    w, h = K.BOOK[0], K.BOOK[1]
    front = K.img_mat('acc_front_cover', K.tex('acc_front_cover'), rough=0.6)
    backc = K.img_mat('acc_back_cover', K.tex('acc_back_cover'), rough=0.6)
    cf, cb = math.radians(cov_f), math.radians(cov_b)
    e = (w * math.cos(cf), w * math.sin(cf))
    _acc_objs.append(K.quad('cover_front_open', [(e[0], e[1], h), (0, 0, h), (0, 0, 0), (e[0], e[1], 0)], front, back, thick=2.2, parent=root, out=(0, -1, 0)))
    e = (x + w * math.cos(cb), y + w * math.sin(cb))
    _acc_objs.append(K.quad('cover_back_open', [(x, y, h), (e[0], e[1], h), (e[0], e[1], 0), (x, y, 0)], backc, back, thick=2.2, parent=root, out=(0, -1, 0)))
    root.location = Vector(origin)
    return root, x


A_FOLD, A_OPEN = 87.0, 34.0


def cover_angles(t_first, t_last):
    """앞표지는 첫 패널과, 뒤표지는 마지막 패널과 함께 펼쳐진다."""
    return lerp(A_FOLD + 4.0, 215.0, t_first), lerp(A_FOLD - 4.0, -35.0, t_last)


def chain_len(angles):
    return sum(K.PANEL[0] * math.cos(math.radians(a)) for a in angles) * MM


# ---------- 4. 병풍 펼침 (전체가 한 번에) ----------
def clip_acc_unfold(frames):
    N, HOLD0, OPEN = 132, 14, 92
    setup()
    cam = K.camera((0, -1, 0.3), (0, 0, 0.09), 50)
    for f in frames(N):
        t = ease((f - 1 - HOLD0) / OPEN)
        a = lerp(A_FOLD, A_OPEN, t)
        angles = [a] * 12
        L = chain_len(angles)
        clear_acc()
        cf, cb = cover_angles(t, t)
        build_acc_chain(angles, cf, cb, (-L / 2, 0.05, 0))
        span = L + 0.26 * (1 - t) + 0.12
        d = max(span / 0.72 * 1.02, 1.05)
        yc = 0.05 + K.PANEL[0] * math.sin(math.radians(a)) * MM / 2
        el = math.radians(lerp(16, 13, t))
        aim(cam, (0, yc - d * math.cos(el), 0.09 + d * math.sin(el)), (0, yc, 0.09))
        render_frame('acc_unfold', f)


# ---------- 5. 병풍 넘김 (한 장씩 차례로 젖혀지며 카메라가 따라감) ----------
def clip_acc_flip(frames):
    N, START, STEP, DUR = 216, 12, 15, 30
    setup(5.0)
    cam = K.camera((0, -1, 0.3), (0, 0, 0.09), 50)
    track = []
    for f in range(1, N + 1):
        ts = [ease((f - 1 - START - i * STEP) / DUR) for i in range(12)]
        angles = [lerp(A_FOLD, 40.0, t) for t in ts]
        # 지금 젖혀지는 패널의 바깥 끝 x
        x = 0.0
        for i, a in enumerate(angles):
            x += K.PANEL[0] * math.cos(math.radians(a)) * MM
            if ts[i] < 0.6:
                break
        track.append(x)
    # 카메라 x는 부드럽게(이동 평균)
    sm = []
    for i in range(N):
        win = track[max(0, i - 12): i + 13]
        sm.append(sum(win) / len(win))
    for f in frames(N):
        ts = [ease((f - 1 - START - i * STEP) / DUR) for i in range(12)]
        angles = [lerp(A_FOLD, 40.0, t) for t in ts]
        clear_acc()
        cf, cb = cover_angles(ts[0], ts[-1])
        x0 = -0.62
        build_acc_chain(angles, cf, cb, (x0, 0.05, 0))
        cx = x0 + sm[f - 1] - 0.06
        d = 0.78
        el = math.radians(12)
        yc = 0.09
        aim(cam, (cx + 0.10, yc - d * math.cos(el), 0.10 + d * math.sin(el)), (cx, yc, 0.085))
        render_frame('acc_flip', f)


# ---------- 6. 노트 펼침·넘김 (휘는 페이지) ----------
NW, NH, ND = K.NOTE
_note_objs = []


def page_mesh(name, theta, z_root, curl, thick, m_front, m_back, parent, seg=28):
    """책등(x=0)에 붙은 페이지. theta 0=오른쪽에 누움, pi=왼쪽으로 넘어감. curl: 끝이 뒤처지는 정도."""
    import bmesh
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new('UVMap')
    pts = []
    px, pz = 0.0, z_root
    ds = NW / seg
    for k in range(seg + 1):
        s = k / seg
        pts.append((px, pz))
        phi = theta - curl * math.sin(theta) * (s ** 1.4)
        px += ds * math.cos(phi)
        pz += ds * math.sin(phi)
    hy = NH / 2
    rows = []
    for (px_, pz_) in pts:
        rows.append((bm.verts.new(Vector((px_, -hy, pz_)) * MM), bm.verts.new(Vector((px_, hy, pz_)) * MM)))
    for k in range(seg):
        a0, a1 = rows[k]
        b0, b1 = rows[k + 1]
        f = bm.faces.new((a0, b0, b1, a1))     # 위에서 보면 반시계 → 법선 +Z (theta=0)
        for loop, (u, v) in zip(f.loops, [(k / seg, 0), ((k + 1) / seg, 0), ((k + 1) / seg, 1), (k / seg, 1)]):
            loop[uv].uv = (u, v)
    bm.normal_update()
    bm.to_mesh(me); bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    me.materials.append(m_front); me.materials.append(m_back)
    sm = ob.modifiers.new('solid', 'SOLIDIFY'); sm.thickness = thick * MM; sm.offset = -1
    sm.material_offset = 1; sm.material_offset_rim = 1
    ob.parent = parent
    _note_objs.append(ob)
    return ob


def clip_note_flip(frames):
    # 구간: 대기 → 표지 열림 → 1·2·3장 넘김 → 대기
    HOLD0, COVER, GAP, FLIP, NP = 14, 34, 10, 26, 3
    N = HOLD0 + COVER + GAP + NP * (FLIP + 8) + 30
    setup()
    paper = K.img_mat('paper_edge', None, rgb=(0.95, 0.94, 0.91), rough=0.8)
    cov = K.img_mat('note_cover', K.tex('note_cover'), rough=0.75, bump=0.2)
    covin = K.img_mat('note_in_cover', K.tex('note_in_cover'), rough=0.8)
    pg = {n: K.img_mat(n, K.tex(n), rough=0.85) for n in
          ('note_p1_front', 'note_p1_back', 'note_p2_front', 'note_p2_back', 'note_p3_front', 'note_p3_back', 'note_p4_front')}
    spine_m = K.img_mat('note_spine', None, rgb=(0.80, 0.77, 0.71), rough=0.8)
    g = K.empty('note_root', (0, 0.0, 0))
    g.rotation_euler = (0, 0, math.radians(-4))
    # 오른쪽 내지 블록(책등 x=0 에서 +X)
    blk_h = ND - 0.35 - 0.12 * 4 - 0.1
    K.box_obj('note_block', (NW - 1.0, NH - 1.0, blk_h), (NW / 2 + 0.5, 0, blk_h / 2), paper, parent=g)
    K.box_obj('note_spine', (0.6, NH, ND), (-0.3, 0, ND / 2), spine_m, parent=g)
    cam = K.camera((0.0, -0.36, 0.42), (0.0, 0.005, 0.0), 50)
    seq = [('cover', cov, covin, 0.35, 0.28)] + \
          [(f'p{j}', pg[f'note_p{j}_front'], pg[f'note_p{j}_back'], 0.12, 0.85) for j in (1, 2, 3)]
    for f in frames(N):
        for ob in _note_objs:
            me = ob.data; bpy.data.objects.remove(ob, do_unlink=True); bpy.data.meshes.remove(me)
        _note_objs.clear()
        t_cover = ease((f - 1 - HOLD0) / COVER)
        thetas = [math.pi * t_cover]
        base = HOLD0 + COVER + GAP
        for j in range(NP):
            thetas.append(math.pi * ease((f - 1 - base - j * (FLIP + 8)) / FLIP))
        for j, (nm, mf, mb, th, curl) in enumerate(seq):
            # 오른쪽: 두께가 아래로, 왼쪽(뒤집힘): 두께가 위로 쌓인다
            z_r = ND if j == 0 else ND - 0.35 - 0.12 * (j - 1) - 0.01 * j
            z_l = 0.02 if j == 0 else 0.02 + 0.35 + 0.12 * (j - 1) + 0.01 * j
            tt = thetas[j] / math.pi
            page_mesh(nm, thetas[j], lerp(z_r, z_l, tt), curl, th, mf, mb, g)
        # 넘어가지 않은 다음 장(4쪽)은 오른쪽 맨 위에 평평하게
        page_mesh('p4', 0.0, ND - 0.35 - 0.12 * 3 - 0.04, 0.0, 0.12, pg['note_p4_front'], paper, g)
        k = (f - 1) / (N - 1)
        aim(cam, (lerp(0.06, -0.02, k), lerp(-0.37, -0.33, k), lerp(0.44, 0.40, k)), (lerp(0.05, 0.0, ease(k * 1.6)), 0.005, 0.0))
        render_frame('note_flip', f)


CLIPS = {
    'rotate': clip_rotate,
    'lid_open': clip_lid_open,
    'acc_unfold': clip_acc_unfold,
    'acc_flip': clip_acc_flip,
    'note_flip': clip_note_flip,
}

if __name__ == '__main__':
    args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['all']
    preview = '--preview' in args
    args = [a for a in args if not a.startswith('--')]
    if preview:
        RES = (640, 360); SAMPLES = 16
        ANIM = os.path.join(K.ROOT, '3d', 'anim_preview')

        def frames(n):
            return sorted({1, n // 4, n // 2, 3 * n // 4, n})
    else:
        def frames(n):
            return range(1, n + 1)
    for a in (CLIPS if 'all' in args else args):
        CLIPS[a](frames)
        print('CLIP DONE', a)
