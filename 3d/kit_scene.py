"""취향의 권리 키트 3D 씬 — 메일러 박스(전개도 실측) + 칸막이 + 아코디언북 + 블렌딩 노트.

실행:  blender -b --python 3d/kit_scene.py -- <shot> [<shot> ...]
shot:  closed | open | accordion | all
치수(mm)는 docs/package-spec 전개도 벡터 측정값. 텍스처는 3d/tex/ (전개도 PDF에서 잘라 낸 실제 인쇄면).
"""
import bpy, bmesh, math, os, sys
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, '3d', 'tex')
OUT = os.path.join(ROOT, '3d', 'render')
MM = 0.001

# ---------- 치수 (mm) ----------
BX, BY, BZ = 275.0, 205.0, 74.0      # 베이스 바닥 275(폭 X) x 205(깊이 Y), 벽 높이 74
T = 1.6                               # 판지 두께
LID_Y = BY + 2 * T                    # 뚜껑 깊이
BOOK = (132.0, 176.0, 60.0)           # 아코디언북 접힌 상태 (폭, 높이, 두께)
NOTE = (126.0, 174.0, 11.0)
LEDGE = 25.0                          # 뒤쪽 'The Right To Taste' 선반 깊이
DUST_SPLAY = 35.0                     # 뚜껑 열렸을 때 측면 날개 벌어짐(도)
EAR_SPLAY = 30.0                      # 앞 턱 플랩 귀 벌어짐(도)
PANEL = (130.0, 180.0)


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    return sc


# ---------- 재질 ----------
_mats = {}


def img_mat(name, path=None, rgb=(0.92, 0.9, 0.86), rough=0.72, bump=0.0, alpha=False):
    key = (name, path)
    if key in _mats:
        return _mats[key]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    b.inputs['Roughness'].default_value = rough
    if path:
        tex = nt.nodes.new('ShaderNodeTexImage')
        tex.image = bpy.data.images.load(path, check_existing=True)
        tex.interpolation = 'Cubic'
        nt.links.new(tex.outputs['Color'], b.inputs['Base Color'])
        if bump > 0:
            bp = nt.nodes.new('ShaderNodeBump')
            bp.inputs['Strength'].default_value = bump
            bp.inputs['Distance'].default_value = 0.0004
            nt.links.new(tex.outputs['Color'], bp.inputs['Height'])
            nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    else:
        b.inputs['Base Color'].default_value = (*rgb, 1)
    _mats[key] = m
    return m


def tex(name):
    return os.path.join(TEX, name + '.png')


# ---------- 기하 유틸 ----------
def quad(name, corners, mat_front, mat_back=None, thick=T, parent=None, out=None):
    """corners: 이미지 TL, TR, BR, BL 순서의 3D 점(mm).
    out: 인쇄면이 보여야 할 방향(로컬). 면 법선을 이 방향으로 맞춘다(인쇄면 = 법선 쪽)."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new(Vector(c) * MM) for c in corners]
    f = bm.faces.new(vs)
    uv = bm.loops.layers.uv.new('UVMap')
    for loop, (u, v) in zip(f.loops, [(0, 1), (1, 1), (1, 0), (0, 0)]):
        loop[uv].uv = (u, v)
    f.normal_update()
    if out is not None and f.normal.dot(Vector(out)) < 0:
        bmesh.ops.reverse_faces(bm, faces=[f])
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    me.materials.append(mat_front)
    me.materials.append(mat_back or mat_front)
    if thick:
        s = ob.modifiers.new('solid', 'SOLIDIFY')
        s.thickness = thick * MM
        s.offset = -1
        s.material_offset = 1
        s.material_offset_rim = 1
    if parent:
        ob.parent = parent
    return ob


def rounded(pts, r, seg=8):
    """2D 다각형 꼭짓점마다 반지름 r(목록 또는 값) 필렛."""
    rs = r if isinstance(r, (list, tuple)) else [r] * len(pts)
    out = []
    n = len(pts)
    for i in range(n):
        p0, p1, p2 = Vector(pts[i - 1]), Vector(pts[i]), Vector(pts[(i + 1) % n])
        ri = rs[i]
        if ri <= 0:
            out.append(tuple(p1)); continue
        d0, d1 = (p0 - p1).normalized(), (p2 - p1).normalized()
        ang = d0.angle(d1)
        t = ri / math.tan(ang / 2)
        a, b = p1 + d0 * t, p1 + d1 * t
        bis = (d0 + d1).normalized()
        c = p1 + bis * (ri / math.sin(ang / 2))
        va, vb = a - c, b - c
        sa, sb = math.atan2(va.y, va.x), math.atan2(vb.y, vb.x)
        da = sb - sa
        while da > math.pi: da -= 2 * math.pi
        while da < -math.pi: da += 2 * math.pi
        for k in range(seg + 1):
            th = sa + da * k / seg
            out.append((c.x + ri * math.cos(th), c.y + ri * math.sin(th)))
    return out


def ngon(name, pts3d, mat_front, mat_back=None, thick=T, parent=None, out=None):
    """임의 다각형 판. UV는 바운딩 박스 평면 투영(무늬 재질용)."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new(Vector(c) * MM) for c in pts3d]
    f = bm.faces.new(vs)
    f.normal_update()
    uv = bm.loops.layers.uv.new('UVMap')
    import itertools
    co = [Vector(c) for c in pts3d]
    span = [max(c[i] for c in co) - min(c[i] for c in co) for i in range(3)]
    ax = sorted(range(3), key=lambda i: -span[i])[:2]
    mn = [min(c[i] for c in co) for i in range(3)]
    for loop in f.loops:
        c = loop.vert.co / MM
        loop[uv].uv = ((c[ax[0]] - mn[ax[0]]) / max(span[ax[0]], 1e-6), (c[ax[1]] - mn[ax[1]]) / max(span[ax[1]], 1e-6))
    if out is not None and f.normal.dot(Vector(out)) < 0:
        bmesh.ops.reverse_faces(bm, faces=[f])
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    me.materials.append(mat_front); me.materials.append(mat_back or mat_front)
    if thick:
        sm = ob.modifiers.new('solid', 'SOLIDIFY'); sm.thickness = thick * MM; sm.offset = -1
        sm.material_offset = 1; sm.material_offset_rim = 1
    if parent:
        ob.parent = parent
    return ob


def box_obj(name, size, loc, mat, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=Vector(loc) * MM)
    ob = bpy.context.object
    ob.name = name
    ob.scale = Vector(size) * MM
    bpy.ops.object.transform_apply(scale=True)
    ob.data.materials.append(mat)
    if parent:
        ob.parent = parent
    return ob


def empty(name, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    e.location = Vector(loc) * MM
    bpy.context.scene.collection.objects.link(e)
    return e


# ---------- 키트 ----------
def build_box(lid_angle_deg=0.0, origin=(0, 0, 0), with_contents=True, band='taste', flap=None, dust=None, ear=None):
    """flap: 앞 턱 플랩 접힘(90=뚜껑과 직각, 0=평평하게 펼침). dust/ear: 측면 날개·귀 벌어짐(0=접힘, 90=평평).
    열린 상태 기본값은 실물 사진(10/19, 뚜껑 열린 정면) 기준: 앞 턱은 반쯤 펴지고, 귀와 측면 날개는 각각 바깥으로 벌어진다."""
    is_open = lid_angle_deg >= 5
    if flap is None:
        flap = 20.0 if is_open else 90.0
    if dust is None:
        dust = 40.0 if is_open else 0.0
    if ear is None:
        ear = 72.0 if is_open else 0.0
    plaster_in = img_mat('plaster_in', tex('plaster_patch'), rough=0.85, bump=0.25)
    white_in = img_mat('board_white', None, rgb=(0.93, 0.93, 0.91), rough=0.9)
    root = empty('kit', origin)
    hx, hy = BX / 2, BY / 2
    # 바닥(안쪽은 미장 인서트)
    quad('floor', [(-hx, hy, T), (hx, hy, T), (hx, -hy, T), (-hx, -hy, T)], plaster_in, white_in, parent=root, out=(0, 0, 1))
    # 앞벽(-Y) "Taste / Depth": 이미지 위 = +X, 왼쪽 = 위
    m = img_mat('base_front', tex('base_front'), bump=0.2)
    quad('wall_front', [(hx, -hy, BZ), (hx, -hy, 0), (-hx, -hy, 0), (-hx, -hy, BZ)], m, plaster_in, parent=root, out=(0, -1, 0))
    # 뒷벽(+Y, 힌지)
    m = img_mat('base_back', tex('base_back'), bump=0.2)
    quad('wall_back', [(hx, hy, 0), (hx, hy, BZ), (-hx, hy, BZ), (-hx, hy, 0)], m, plaster_in, parent=root, out=(0, 1, 0))
    # 끝벽 +X (문단) / -X (www · With Thanks, 원고에서 거꾸로 배치)
    m = img_mat('base_end_a', tex('base_end_a'), bump=0.2)
    quad('wall_endA', [(hx, -hy, BZ), (hx, hy, BZ), (hx, hy, 0), (hx, -hy, 0)], m, plaster_in, parent=root, out=(1, 0, 0))
    m = img_mat('base_end_b', tex('base_end_b'), bump=0.2)
    quad('wall_endB', [(-hx, -hy, 0), (-hx, hy, 0), (-hx, hy, BZ), (-hx, -hy, BZ)], m, plaster_in, parent=root, out=(-1, 0, 0))
    # 뚜껑: 뒷벽 위 모서리 힌지
    hinge = empty('lid_hinge', (0, hy, BZ))
    hinge.parent = root
    lid_top = img_mat('lid_top', tex('lid_top'), bump=0.2)
    ly = LID_Y
    # 뚜껑 이미지: 왼쪽 = 힌지(+Y), 위 = +X
    quad('lid_top', [(hx + T, 0, T), (hx + T, -ly, T), (-hx - T, -ly, T), (-hx - T, 0, T)], lid_top, white_in, parent=hinge, out=(0, 0, 1))
    lid_front = img_mat('lid_front', tex('lid_front'), bump=0.2)
    flap_piv = empty('flap_pivot', (0, -ly, 0)); flap_piv.parent = hinge
    quad('lid_flap', [(hx - 2, 0, 0), (hx - 2, 0, -BZ + 6), (-hx + 2, 0, -BZ + 6), (-hx + 2, 0, 0)], lid_front, white_in, parent=flap_piv, out=(0, -1, 0))
    flap_piv.rotation_euler = (math.radians(-(90.0 - flap)), 0, 0)
    hinge.rotation_euler = (math.radians(-lid_angle_deg), 0, 0)
    # 칸막이 (X=0, 엄지 구멍)
    div = box_obj('divider', (T, BY - 2 * T, BZ - 6), (0, 0, (BZ - 6) / 2 + T), plaster_in, parent=root)
    bpy.ops.mesh.primitive_cylinder_add(radius=14 * MM, depth=10 * MM, location=(0, 0, (BZ - 4) * MM), rotation=(0, math.radians(90), 0))
    cut = bpy.context.object
    bo = div.modifiers.new('hole', 'BOOLEAN')
    bo.object = cut
    bo.operation = 'DIFFERENCE'
    bpy.context.view_layer.objects.active = div
    bpy.ops.object.modifier_apply(modifier='hole')
    bpy.data.objects.remove(cut)
    # 측면에 끼우는 날개: 뚜껑 좌우 변 전체를 따라 붙고, 닫으면 측벽 안쪽으로 들어간다.
    # 앞쪽은 귀와 칼선 틈(6mm)으로 떨어지고 모서리가 비스듬히 잘림, 힌지 쪽은 살짝만 비낌.
    plaster_out = img_mat('lid_plaster_out', tex('plaster_patch'), rough=0.85, bump=0.2)
    fd = 68.0
    front_in, front_free, rear_in, rear_free = 6.0, 24.0, 2.0, 12.0
    for sgn in (1, -1):
        xw = sgn * (hx - T - 0.6)
        piv = empty(f'dust_pivot_{sgn:+d}', (xw, 0, 0)); piv.parent = hinge
        tr = [(-ly + front_in, 0), (-rear_in, 0), (-rear_free, -fd), (-ly + front_free, -fd)]
        pts2 = rounded(tr, [0, 0, 5, 8])
        ngon(f'lid_dustflap_{sgn:+d}', [(0, y_, z_) for (y_, z_) in pts2], plaster_out, white_in, parent=piv, out=(sgn, 0, 0))
        piv.rotation_euler = (0, math.radians(-sgn * dust), 0)
    # 윗면 틈새에 끼우는 귀: 앞 턱 플랩 양끝 세로 접선에 붙어, 닫으면 측벽 위 틈새로 들어간다.
    # 플랩 끝(자유단) 쪽 모서리는 크게 둥글고, 뚜껑 접선 쪽 모서리는 작게 둥글다(실물 사진).
    ear_len, ear_h = 48.0, BZ - 8
    for sgn in (1, -1):
        xe = sgn * (hx - 2)
        piv = empty(f'ear_pivot_{sgn:+d}', (xe, 0, 0)); piv.parent = flap_piv
        ear_pts = [(0, 0), (ear_len, 0), (ear_len, -ear_h), (0, -ear_h)]
        pts2 = rounded(ear_pts, [0, 8, 36, 0], seg=12)
        ngon(f'lid_ear_{sgn:+d}', [(0, y_, z_) for (y_, z_) in pts2], lid_front, white_in, parent=piv, out=(sgn, 0, 0))
        piv.rotation_euler = (0, 0, math.radians(-sgn * ear))
    # 뒤쪽 인서트: 등판 + 'The Right To Taste' 선반
    ledge = img_mat('back_ledge', tex('back_ledge'), rough=0.8, bump=0.2)
    panel = img_mat('back_panel', tex('back_panel'), rough=0.8, bump=0.2)
    lz = BZ - 2.0
    yb = hy - T
    quad('back_ledge', [(-hx + T, yb, lz), (hx - T, yb, lz), (hx - T, yb - LEDGE, lz), (-hx + T, yb - LEDGE, lz)], ledge, white_in, thick=1.2, parent=root, out=(0, 0, 1))
    quad('back_panel', [(-hx + T, yb - LEDGE, lz), (hx - T, yb - LEDGE, lz), (hx - T, yb - LEDGE, T), (-hx + T, yb - LEDGE, T)], panel, white_in, thick=1.2, parent=root, out=(0, -1, 0))
    if with_contents:
        cy = -LEDGE / 2 - 1
        build_closed_book(root, (-BX / 4, cy, T), band=band)
        # 노트 밑 받침(실물 확인 전): 노트 윗면을 아코디언북 윗면과 맞춘다
        riser = BOOK[2] + 1.8 - NOTE[2] - 0.1
        box_obj('note_riser', (NOTE[0] - 4, NOTE[1] - 4, riser), (BX / 4, cy, T + riser / 2), white_in, parent=root)
        build_note(root, (BX / 4, cy, T + riser))
    return root, hinge


def build_closed_book(parent, loc, band='taste'):
    w, h, d = BOOK
    paper = img_mat('paper_edge', None, rgb=(0.95, 0.94, 0.91), rough=0.8)
    g = empty('book', loc)
    g.parent = parent
    box_obj('book_block', (w - 3, h - 3, d - 3), (0, 0, d / 2), paper, parent=g)
    front = img_mat('acc_front_cover', tex('acc_front_cover'), rough=0.6)
    back = img_mat('acc_back_cover', tex('acc_back_cover'), rough=0.6)
    spine = img_mat('acc_spine', tex('acc_spine'), rough=0.6)
    hw, hh = w / 2, h / 2
    quad('cover_front', [(-hw, hh, d), (hw, hh, d), (hw, -hh, d), (-hw, -hh, d)], front, thick=1.8, parent=g, out=(0, 0, 1))
    quad('cover_back', [(hw, hh, 0), (-hw, hh, 0), (-hw, -hh, 0), (hw, -hh, 0)], back, thick=1.8, parent=g, out=(0, 0, -1))
    # 책등 (-X 쪽), 글자는 세로
    quad('spine', [(-hw, hh, 0), (-hw, hh, d), (-hw, -hh, d), (-hw, -hh, 0)], spine, thick=1.8, parent=g, out=(-1, 0, 0))
    if band:
        bm_ = img_mat('band_' + band, tex('band_' + band), rough=0.55)
        brown = img_mat('band_col_' + band, None, rgb=((0.33, 0.29, 0.17) if band == 'taste' else (0.20, 0.13, 0.09)), rough=0.55)
        bh_ = 46.0
        y0, y1 = -bh_ / 2 - 15, bh_ / 2 - 15
        quad('band_front', [(-hw - 1, y1, d + 2.2), (hw + 1, y1, d + 2.2), (hw + 1, y0, d + 2.2), (-hw - 1, y0, d + 2.2)], bm_, brown, thick=0.4, parent=g, out=(0, 0, 1))
        quad('band_side', [(hw + 1, y1, d + 2.2), (hw + 1, y1, -0.6), (hw + 1, y0, -0.6), (hw + 1, y0, d + 2.2)], brown, thick=0.4, parent=g, out=(1, 0, 0))
        quad('band_spine', [(-hw - 1, y1, -0.6), (-hw - 1, y1, d + 2.2), (-hw - 1, y0, d + 2.2), (-hw - 1, y0, -0.6)], brown, thick=0.4, parent=g, out=(-1, 0, 0))
    return g


def build_note(parent, loc):
    w, h, d = NOTE
    paper = img_mat('paper_edge', None, rgb=(0.95, 0.94, 0.91), rough=0.8)
    cov = img_mat('note_cover', tex('note_cover'), rough=0.75, bump=0.2)
    g = empty('note', loc)
    g.parent = parent
    box_obj('note_block', (w, h, d), (0, 0, d / 2), paper, parent=g)
    quad('note_cover', [(-w / 2, h / 2, d + 0.1), (w / 2, h / 2, d + 0.1), (w / 2, -h / 2, d + 0.1), (-w / 2, -h / 2, d + 0.1)], cov, thick=0.3, parent=g, out=(0, 0, 1))
    return g


def build_accordion(origin=(0, 0, 0), fold_deg=38.0, n=12):
    """펼친 아코디언: 패널 12장을 세워 지그재그. 안쪽 면(텍스처)이 앞(-Y)을 본다."""
    pw, ph = PANEL
    faces = ['acc_in_01', 'acc_in_02', 'acc_in_03_win', 'acc_in_04', 'acc_in_05_win', 'acc_in_06',
             'acc_in_07_win', 'acc_in_08', 'acc_in_09_win', 'acc_in_10', 'acc_in_11_win', 'acc_in_12']
    pouch_faces = {1, 3, 5, 7, 9, 11}
    back = img_mat('paper_back', None, rgb=(0.95, 0.94, 0.91), rough=0.8)
    pouch = img_mat('pouch', tex('pouch'), rough=0.45)
    root = empty('accordion', origin)
    a = math.radians(fold_deg)
    x = 0.0
    y = 0.0
    for i in range(n):
        sgn = 1 if i % 2 == 0 else -1
        dx, dy = pw * math.cos(a), sgn * pw * math.sin(a)
        p0 = (x, y)
        p1 = (x + dx, y + dy)
        m = img_mat(faces[i], tex(faces[i]), rough=0.75, bump=0.1)
        quad(f'panel_{i+1:02d}', [(p0[0], p0[1], ph), (p1[0], p1[1], ph), (p1[0], p1[1], 0), (p0[0], p0[1], 0)], m, back, thick=0.9, parent=root, out=(0, -1, 0))
        if i in pouch_faces:
            # 파우치: 패널 위쪽 가운데, 패널 면에서 2.5mm 앞으로
            nx, ny = -(p1[1] - p0[1]) / pw, (p1[0] - p0[0]) / pw   # 패널 법선(앞쪽 -Y 방향 성분)
            if ny > 0:
                nx, ny = -nx, -ny
            off = 2.5
            u0, u1 = 0.07, 0.93
            q0 = (p0[0] + dx * u0 + nx * off, p0[1] + dy * u0 + ny * off)
            q1 = (p0[0] + dx * u1 + nx * off, p0[1] + dy * u1 + ny * off)
            top, bot = ph * 0.86, ph * 0.86 - pw * 0.86
            quad(f'pouch_{i+1:02d}', [(q0[0], q0[1], top), (q1[0], q1[1], top), (q1[0], q1[1], bot), (q0[0], q0[1], bot)], pouch, back, thick=1.5, parent=root, out=(0, -1, 0))
        x, y = p1
    # 앞·뒤 하드커버 (양 끝에 세움)
    w, h = BOOK[0], BOOK[1]
    front = img_mat('acc_front_cover', tex('acc_front_cover'), rough=0.6)
    backc = img_mat('acc_back_cover', tex('acc_back_cover'), rough=0.6)
    ca = math.radians(70)
    quad('cover_front_open', [(-w * math.cos(ca), -w * math.sin(ca), h), (0, 0, h), (0, 0, 0), (-w * math.cos(ca), -w * math.sin(ca), 0)], front, back, thick=2.2, parent=root, out=(0, -1, 0))
    quad('cover_back_open', [(x, y, h), (x + w * math.cos(ca), y - w * math.sin(ca), h), (x + w * math.cos(ca), y - w * math.sin(ca), 0), (x, y, 0)], backc, back, thick=2.2, parent=root, out=(0, -1, 0))
    return root, x


# ---------- 무대 ----------
def stage(size=5.0):
    plaster = img_mat('backdrop', os.path.join(ROOT, 'wadiz', 'assets', 'photo', 'plaster-eu-1.jpg'), rough=0.95, bump=0.15)
    # 바닥 + 뒷벽 (곡면 없는 L자, 넓게)
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0.3, 0))
    fl = bpy.context.object
    fl.name = 'floor_backdrop'
    fl.data.materials.append(plaster)
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0.9, size / 2), rotation=(math.radians(90), 0, 0))
    wall = bpy.context.object
    wall.name = 'wall_backdrop'
    wall.data.materials.append(plaster)
    w = bpy.data.worlds.new('W')
    bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (0.95, 0.92, 0.86, 1)
    w.node_tree.nodes['Background'].inputs[1].default_value = 0.12
    # 창가 빛: 왼쪽 위 큰 면광 + 오른쪽 약한 반사
    key = bpy.data.lights.new('key', 'AREA')
    key.energy = 60
    key.size = 1.2
    key.color = (1.0, 0.95, 0.88)
    ko = bpy.data.objects.new('key', key)
    ko.location = (-1.1, -0.6, 1.2)
    bpy.context.scene.collection.objects.link(ko)
    ko.rotation_euler = (Vector((0, 0, 0.05)) - ko.location).to_track_quat('-Z', 'Y').to_euler()
    fill = bpy.data.lights.new('fill', 'AREA')
    fill.energy = 14
    fill.size = 1.5
    fo = bpy.data.objects.new('fill', fill)
    fo.location = (1.2, -0.9, 0.7)
    bpy.context.scene.collection.objects.link(fo)
    fo.rotation_euler = (Vector((0, 0, 0.05)) - fo.location).to_track_quat('-Z', 'Y').to_euler()


def camera(loc, target, lens=50):
    cam = bpy.data.cameras.new('cam')
    cam.lens = lens
    co = bpy.data.objects.new('cam', cam)
    bpy.context.scene.collection.objects.link(co)
    co.location = loc
    co.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = co
    return co


def render_setup(w, h, samples=128):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    prefs = bpy.context.preferences.addons['cycles'].preferences
    for dt in ('OPTIX', 'CUDA'):
        try:
            prefs.compute_device_type = dt
            prefs.get_devices()
            if any(d.type == dt for d in prefs.devices):
                for d in prefs.devices:
                    d.use = d.type in (dt, 'CPU') and d.type != 'CPU'
                sc.cycles.device = 'GPU'
                break
        except Exception:
            pass
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.image_settings.file_format = 'PNG'
    sc.view_settings.view_transform = 'Standard'
    sc.view_settings.exposure = -0.6
    sc.view_settings.gamma = 1.0
    sc.render.film_transparent = False


def save(name):
    sc = bpy.context.scene
    os.makedirs(OUT, exist_ok=True)
    sc.render.filepath = os.path.join(OUT, name + '.png')
    bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, name + '.blend'))
    print('RENDERED', name, sc.cycles.device)


# ---------- 샷 ----------
def _shot(name, build, cam_loc, cam_target, lens=50, res=(1600, 1200), transparent=False, backdrop=True, shift=(0.0, 0.0), sensor_w=None):
    """shift·sensor_w: 같은 카메라·같은 픽셀 배율로 캔버스만 넓힐 때(누끼 여백). sensor_w = 36 × 새 폭 / 원래 폭."""
    reset(); _mats.clear()
    if backdrop:
        stage()
    else:
        stage(); [bpy.data.objects.remove(bpy.data.objects[n]) for n in ('floor_backdrop', 'wall_backdrop')]
    build()
    cam = camera(cam_loc, cam_target, lens=lens)
    cam.data.shift_x, cam.data.shift_y = shift
    if sensor_w:
        cam.data.sensor_fit = 'HORIZONTAL'      # 가로 기준 고정 → 해상도를 키워도 픽셀 배율 유지
        cam.data.sensor_width = sensor_w
    render_setup(*res)
    bpy.context.scene.render.film_transparent = transparent
    if transparent:
        bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    save(name)


def _box(angle, contents=True, **kw):
    return lambda: build_box(angle, with_contents=contents, **kw)


def _acc(fold=36.0, y=0.05):
    def f():
        root, length = build_accordion(fold_deg=fold)
        root.location = (-length / 2 * MM, y, 0)
    return f


def _acc_detail():
    root, length = build_accordion(fold_deg=24.0)
    root.location = (-length * 0.42 * MM, 0.05, 0)


def _book():
    g = empty('stage_root')
    build_closed_book(g, (-0.075 / MM, 0, 0), band='taste')
    build_note(g, (0.07 / MM, 0.01 / MM, 0))


SHOTS = {
    'closed':        lambda: _shot('closed', _box(0, False), (-0.42, -0.52, 0.42), (0, 0, 0.03), 55),
    'closed_top':    lambda: _shot('closed_top', _box(0, False), (0.0, -0.06, 0.95), (0, 0, 0.0), 50, (1400, 1400)),
    'closed_end':    lambda: _shot('closed_end', _box(0, False), (-0.62, -0.08, 0.26), (0, 0, 0.035), 55),
    'open':          lambda: _shot('open', _box(172, flap=8, dust=82, ear=80), (0.0, -0.05, 1.22), (0, 0.15, 0.03), 50, (1200, 1600)),
    'open_front':    lambda: _shot('open_front', _box(108), (0.02, -0.76, 0.80), (0, 0.08, 0.13), 50),
    'open_34':       lambda: _shot('open_34', _box(112), (0.56, -0.70, 0.68), (0, 0.06, 0.13), 50),
    'open_top':      lambda: _shot('open_top', _box(150), (0.0, -0.06, 1.12), (0, 0.07, 0.0), 50, (1400, 1400)),
    'open_half':     lambda: _shot('open_half', _box(48), (-0.42, -0.64, 0.38), (0, 0.02, 0.07), 55),
    'accordion':     lambda: _shot('accordion', _acc(36), (0.0, -2.05, 0.55), (0, 0.05, 0.08), 50, (1800, 1000)),
    'accordion_detail': lambda: _shot('accordion_detail', _acc_detail, (0.0, -0.62, 0.16), (0, 0.06, 0.09), 50, (1600, 1100)),
    'books':         lambda: _shot('books', _book, (0.0, -0.32, 0.55), (0, 0.0, 0.0), 50),
    'ref_front':     lambda: _shot('ref_front', _box(104), (0.0, -0.36, 0.78), (0, 0.06, 0.06), 50, (1200, 1600), transparent=True, backdrop=False),
    'closed_cut':    lambda: _shot('closed_cut', _box(0, False), (-0.42, -0.52, 0.42), (0, 0, 0.03), 55, transparent=True, backdrop=False),
    # 원래 open_34 카메라(1600×1200) 그대로, 위 600px·오른쪽 500px만 넓혀 뚜껑·귀까지 담는다(원 픽셀 + (0, 600))
    'open_cut':      lambda: _shot('open_cut', _box(112), (0.40, -0.48, 0.46), (0, 0.02, 0.03), 50, (2100, 1800), transparent=True, backdrop=False, shift=(250 / 2100, 300 / 2100), sensor_w=36 * 2100 / 1600),
}

if __name__ == '__main__':
    args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['all']
    for a in (SHOTS if 'all' in args else args):
        SHOTS[a]()
