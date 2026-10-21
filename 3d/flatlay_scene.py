"""취향의 권리 — 키트 전체 연출 컷(위에서 내려다본 플랫레이).

실행:  blender -b --python 3d/flatlay_scene.py -- [taste] [--test]
- 구성품 배치는 대표가 준 키트 실물 촬영(…142249431.jpg)의 위치를 mm로 환산한 것.
- 상자·노트·책갈피 카드는 kit_scene 의 실측 모델·텍스처, 파우치·원료 카드·사용 안내 엽서는
  make_flatlay_tex.py 가 실물 사진에서 펴서 만든 텍스처.
- 빛: 왼쪽 위 오후 햇빛 + 창틀 빛 띠 + 오른쪽 위 잎 그림자(카메라에는 안 보이는 가림판).
--test : 저해상도·저샘플 빠른 확인용
"""
import bpy, bmesh, math, os, sys
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_scene as K
from kit_scene import MM, img_mat, quad, box_obj, empty, tex

FL = os.path.join(K.ROOT, '3d', 'tex', 'flatlay')
U = 0.644                       # 실물 사진 축소 좌표(폭 900) 1칸 = 0.644 mm (상자 275 mm 기준)
C0 = (445, 645)                 # 배치 중심(사진 좌표)


def P(u, v):
    """사진 좌표 → 월드 mm (x 오른쪽, y 위쪽)."""
    return ((u - C0[0]) * U, -(v - C0[1]) * U)


def flt(name):
    return os.path.join(FL, name + '.png')


# ---------- 구성품 ----------
def flat_card(name, path, cx, cy, w, h, z, rot=0.0, rough=0.7, thick=0.35, uv_rot=0):
    """얇은 판(카드·엽서). uv_rot: 텍스처를 90° 단위로 돌려 붙임."""
    m = img_mat(name, path, rough=rough)
    back = img_mat('paper_back', None, rgb=(0.93, 0.92, 0.89), rough=0.85)
    g = empty(name + '_g', (cx, cy, z))
    hw, hh = w / 2, h / 2
    pts = [(-hw, hh, 0), (hw, hh, 0), (hw, -hh, 0), (-hw, -hh, 0)]
    pts = pts[uv_rot:] + pts[:uv_rot]          # UV(0,1)(1,1)(1,0)(0,0)이 붙는 꼭짓점을 돌림
    quad(name, pts, m, back, thick=thick, parent=g, out=(0, 0, 1))
    g.rotation_euler = (0, 0, math.radians(rot))
    return g


def pouch(name, path, cx, cy, z, w=88.0, h=116.0, bulge=3.2):
    """파우치: 헤더(얇은 판지) + 유산지 봉투 볼록. 텍스처 알파로 봉투 외곽."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    b = nt.nodes['Principled BSDF']
    b.inputs['Roughness'].default_value = 0.5
    tx = nt.nodes.new('ShaderNodeTexImage')
    tx.image = bpy.data.images.load(path, check_existing=True)
    tx.interpolation = 'Cubic'
    nt.links.new(tx.outputs['Color'], b.inputs['Base Color'])
    nt.links.new(tx.outputs['Alpha'], b.inputs['Alpha'])
    # 격자 메시: 봉투 창 부분만 볼록하게
    nx, ny = 32, 42
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    uvl = bm.loops.layers.uv.new('UVMap')
    vs = [[None] * (nx + 1) for _ in range(ny + 1)]
    for j in range(ny + 1):
        for i in range(nx + 1):
            u, v = i / nx, j / ny                       # v=0 아래, v=1 위
            # 볼록: 텍스처 창(위에서 40~84% 아래쪽) 안에서 부드럽게
            t_ = 1 - v                                   # 0 = 위
            bx = max(0.0, math.sin(math.pi * min(max((u - 0.04) / 0.92, 0), 1)))
            by = max(0.0, math.sin(math.pi * min(max((t_ - 0.40) / 0.46, 0), 1)))
            zz = bulge * (bx * by) ** 0.6
            vs[j][i] = bm.verts.new(Vector(((u - .5) * w, (v - .5) * h, zz)) * MM)
    for j in range(ny):
        for i in range(nx):
            f = bm.faces.new([vs[j][i], vs[j][i + 1], vs[j + 1][i + 1], vs[j + 1][i]])
            for loop in f.loops:
                co = loop.vert.co / MM
                loop[uvl].uv = (co.x / w + .5, co.y / h + .5)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    me.materials.append(mat)
    for p_ in me.polygons:
        p_.use_smooth = True
    s = ob.modifiers.new('solid', 'SOLIDIFY'); s.thickness = 0.5 * MM; s.offset = -1
    ob.location = (cx * MM, cy * MM, z * MM)
    return ob


def note(cx, cy, w, h, d, rot):
    paper = img_mat('paper_edge', None, rgb=(0.95, 0.94, 0.91), rough=0.8)
    cov = img_mat('note_cover', tex('note_cover'), rough=0.75, bump=0.2)
    g = empty('note_g', (cx, cy, 0))
    box_obj('note_block', (w - 1, h - 1, d), (0, 0, d / 2), paper, parent=g)
    quad('note_cover', [(-w / 2, h / 2, d + .1), (w / 2, h / 2, d + .1), (w / 2, -h / 2, d + .1), (-w / 2, -h / 2, d + .1)],
         cov, thick=0.4, parent=g, out=(0, 0, 1))
    g.rotation_euler = (0, 0, math.radians(rot))
    return g


def bookmarks(px, py):
    """책갈피 카드 6장 부채꼴: 오른쪽 아래 모서리를 축으로 왼쪽으로 펼침(맨 위가 세로)."""
    w, h = 50.0, 150.0
    order = ['postcard_5', 'postcard_0', 'postcard_3', 'postcard_2', 'postcard_4', 'postcard_1']   # 아래 → 위
    angs = [68, 54, 41, 28, 15, 2]
    for k, (nm, a) in enumerate(zip(order, angs)):
        g = empty(f'bm_{k}', (px, py, 0.4 + k * 0.45))
        quad(f'bm_card_{k}', [(-w, h, 0), (0, h, 0), (0, 0, 0), (-w, 0, 0)],
             img_mat(nm, tex(nm), rough=0.55), img_mat('paper_back', None, rgb=(0.93, 0.92, 0.89), rough=0.85),
             thick=0.35, parent=g, out=(0, 0, 1))
        g.rotation_euler = (0, 0, math.radians(a))


def infuser(top, ball, r_ball=23.5):
    """슬라이딩 스테인리스 인퓨저(TREE 304 실물 기준): 위아래 반구가 조개처럼 맞물리고 테두리 플랜지,
    몸체 전체 타공, 손잡이는 테두리에 붙고 가운데 나팔꼴 슬라이딩 칼라, 끝은 납작한 원판 손잡이.
    바닥에 눕히면 맞물림 선이 바닥과 평행 → 위에서 보면 돔 + 테두리 링."""
    def steel_mat(name, holes=False):
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        nt = m.node_tree
        b = nt.nodes['Principled BSDF']
        b.inputs['Base Color'].default_value = (0.80, 0.80, 0.80, 1)
        b.inputs['Metallic'].default_value = 1.0
        b.inputs['Roughness'].default_value = 0.3
        if holes:
            # 타공: 2.4mm 간격 점 → 구멍 안은 어둡고 거칠게
            tc = nt.nodes.new('ShaderNodeTexCoord')
            vor = nt.nodes.new('ShaderNodeTexVoronoi'); vor.feature = 'F1'
            vor.inputs['Scale'].default_value = 1 / 0.0021
            vor.inputs['Randomness'].default_value = 0.08
            nt.links.new(tc.outputs['Object'], vor.inputs['Vector'])
            ramp = nt.nodes.new('ShaderNodeValToRGB')
            ramp.color_ramp.elements[0].position = 0.30; ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
            ramp.color_ramp.elements[1].position = 0.34; ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
            nt.links.new(vor.outputs['Distance'], ramp.inputs['Fac'])
            mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
            mix.inputs['A'].default_value = (0.05, 0.045, 0.04, 1)
            mix.inputs['B'].default_value = (0.80, 0.80, 0.80, 1)
            nt.links.new(ramp.outputs['Color'], mix.inputs['Factor'])
            nt.links.new(mix.outputs['Result'], b.inputs['Base Color'])
            nt.links.new(ramp.outputs['Color'], b.inputs['Metallic'])
        return m
    steel, mesh = steel_mat('steel'), steel_mat('steel_mesh', holes=True)
    bx, by = ball
    r = r_ball
    zc = r * 0.95                      # 맞물림 높이
    # 위·아래 반구(타공)
    for sgn in (1, -1):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r * MM, location=(bx * MM, by * MM, zc * MM), segments=64, ring_count=32)
        h = bpy.context.object
        h.scale = (1, 1, 0.92 if sgn > 0 else 0.95)
        bm = bmesh.new(); bm.from_mesh(h.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z * sgn < -1e-6], context='VERTS')
        bm.to_mesh(h.data); bm.free()
        h.data.materials.append(mesh)
        bpy.ops.object.shade_smooth()
        so = h.modifiers.new('solid', 'SOLIDIFY'); so.thickness = 0.5 * MM
    # 테두리 플랜지(바닥과 평행한 납작한 링)
    bpy.ops.mesh.primitive_torus_add(major_radius=(r + 1.3) * MM, minor_radius=1.4 * MM, location=(bx * MM, by * MM, zc * MM))
    fl = bpy.context.object; fl.scale = (1, 1, 0.6); fl.data.materials.append(steel)
    bpy.ops.object.shade_smooth()
    # 손잡이 막대: 테두리(위쪽)에서 top 까지
    tx, ty = top
    dirv = Vector((tx - bx, ty - by, 0)).normalized()               # 손잡이 쪽 테두리에서 시작
    p0 = Vector((bx, by, zc)) + dirv * (r + 1.5); p1 = Vector((tx, ty, 4.5))
    d = p1 - p0
    rot = d.to_track_quat('Z', 'Y').to_euler()

    def along(t_):
        return (p0 + d * t_) * MM

    bpy.ops.mesh.primitive_cylinder_add(radius=2.4 * MM, depth=d.length * MM, location=along(.5), vertices=32)
    o = bpy.context.object; o.rotation_euler = rot; o.data.materials.append(steel); bpy.ops.object.shade_smooth()
    # 나팔꼴 슬라이딩 칼라(손잡이 2/3 지점, 넓은 쪽이 끝 방향)
    bpy.ops.mesh.primitive_cone_add(radius1=3.2 * MM, radius2=7.5 * MM, depth=8 * MM, location=along(.66), vertices=48)
    o = bpy.context.object; o.rotation_euler = rot; o.data.materials.append(steel); bpy.ops.object.shade_smooth()
    # 끝 손잡이: 짧은 나팔 + 납작한 원판
    bpy.ops.mesh.primitive_cone_add(radius1=2.6 * MM, radius2=5.0 * MM, depth=6 * MM, location=along(.975), vertices=48)
    o = bpy.context.object; o.rotation_euler = rot; o.data.materials.append(steel); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_cylinder_add(radius=7.2 * MM, depth=2.0 * MM, location=(p1 + d.normalized() * 1.5) * MM, vertices=48)
    o = bpy.context.object; o.rotation_euler = rot; o.data.materials.append(steel); bpy.ops.object.shade_smooth()


def box_closed(cx, cy, rot_z, z=0.0):
    root, _ = K.build_box(0.0, with_contents=False)
    root.location = (cx * MM, cy * MM, z * MM)
    root.rotation_euler = (0, 0, math.radians(rot_z))
    return root


# ---------- 무대·빛 ----------
def floor_and_light():
    # 바닥: 아이보리 미장에 오후빛 베이지를 곱함
    mat = bpy.data.materials.new('floor_warm')
    mat.use_nodes = True
    nt = mat.node_tree
    b = nt.nodes['Principled BSDF']
    b.inputs['Roughness'].default_value = 0.92
    tx = nt.nodes.new('ShaderNodeTexImage')
    tx.image = bpy.data.images.load(os.path.join(K.ROOT, 'wadiz', 'assets', 'photo', 'plaster-eu-1.jpg'))
    mapn = nt.nodes.new('ShaderNodeMapping'); mapn.inputs['Scale'].default_value = (1.6, 1.6, 1)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    nt.links.new(tc.outputs['UV'], mapn.inputs['Vector']); nt.links.new(mapn.outputs['Vector'], tx.inputs['Vector'])
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'
    mix.inputs['Factor'].default_value = 1.0
    mix.inputs['B'].default_value = (1.0, 0.91, 0.82, 1)
    nt.links.new(tx.outputs['Color'], mix.inputs['A'])
    nt.links.new(mix.outputs['Result'], b.inputs['Base Color'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.25; bp.inputs['Distance'].default_value = 0.001
    nt.links.new(tx.outputs['Color'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    bpy.ops.mesh.primitive_plane_add(size=2.4, location=(0, 0, -0.0005))
    bpy.context.object.data.materials.append(mat)

    w = bpy.data.worlds.new('W'); bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (1.0, 0.9, 0.78, 1)
    w.node_tree.nodes['Background'].inputs[1].default_value = 0.24
    # 오후 햇빛(왼쪽 위에서) → 그림자는 오른쪽 아래
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 5.5; sun.angle = math.radians(2.5)
    sun.color = (1.0, 0.86, 0.68)
    so = bpy.data.objects.new('sun', sun); bpy.context.scene.collection.objects.link(so)
    so.rotation_euler = (math.radians(38), 0, math.radians(-128))   # 고도 52°, 왼쪽 위에서
    # 부드러운 채움빛
    fill = bpy.data.lights.new('fill', 'AREA'); fill.energy = 10; fill.size = 1.6; fill.color = (1.0, 0.95, 0.9)
    fo = bpy.data.objects.new('fill', fill); bpy.context.scene.collection.objects.link(fo)
    fo.location = (0.2, -0.3, 1.4)
    return so


def occluders(sun, hw=0.39, hh=0.26):
    """카메라에는 안 보이고 그림자만 드리우는 가림판: 창틀(빛 띠) + 잎 가지."""
    def hidden(ob):
        ob.visible_camera = False
        ob.visible_glossy = False
        ob.visible_diffuse = False
    black = img_mat('occ', None, rgb=(0, 0, 0), rough=1)
    bpy.context.view_layer.update()                                   # 회전값을 matrix_world 에 반영
    sd = sun.matrix_world.to_quaternion() @ Vector((0, 0, -1))      # 햇빛 진행 방향
    def above(x, y, H=0.9):
        """바닥 (x, y)에 그림자를 떨어뜨리려면 높이 H 의 어디에 둬야 하는지.
        높을수록 그림자 가장자리가 번진다(창틀은 높게, 잎은 낮게)."""
        t = H / -sd.z
        return Vector((x, y, 0)) - sd * t
    # 창틀: 왼쪽 바깥의 큰 판에 비스듬한 틈 두 줄 → 왼쪽 가장자리에 밝은 띠, 나머지는 살짝 그늘
    # (판을 여러 띠로 쪼개 틈을 만든다)
    o = above(-hw * 1.2, hh * 0.2)
    for k, (a, b) in enumerate([(-0.40, -0.16), (-0.10, -0.02), (0.06, 0.40)]):
        bpy.ops.mesh.primitive_plane_add(size=1, location=o)
        pl = bpy.context.object
        pl.scale = (0.30, b - a, 1)
        pl.location = o + Vector((-0.02, (a + b) / 2, 0))
        pl.rotation_euler = (0, 0, math.radians(-32))
        pl.data.materials.append(black); hidden(pl)
    # 잎 가지: 오른쪽 위 모서리
    import random
    rnd = random.Random(7)
    base = above(hw * 0.85, hh * 0.92, H=0.26)

    def leaf(p, ang, L):
        bpy.ops.mesh.primitive_plane_add(size=1, location=p)
        lf = bpy.context.object
        lf.scale = (L, L * 0.36, 1)
        lf.rotation_euler = (0, 0, ang)
        lf.data.materials.append(black); hidden(lf)

    def branch(p, ang, length, depth):
        q = p + Vector((math.cos(ang), math.sin(ang), 0)) * length
        n = 6
        for i in range(1, n + 1):
            c = p + (q - p) * (i / n)
            for s in (-1, 1):
                a2 = ang + s * rnd.uniform(.6, 1.0)
                L = rnd.uniform(.035, .055) * (1 - depth * .2)
                leaf(c + Vector((math.cos(a2), math.sin(a2), 0)) * L * .55, a2, L)
        # 가지 줄기
        bpy.ops.mesh.primitive_plane_add(size=1, location=(p + q) / 2)
        st = bpy.context.object; st.scale = (length, 0.004, 1); st.rotation_euler = (0, 0, ang)
        st.data.materials.append(black); hidden(st)
        if depth < 2:
            for _ in range(2):
                branch(q, ang + rnd.uniform(-.55, .55), length * .6, depth + 1)
    branch(base + Vector((0.12, 0.10, 0)), math.radians(205), 0.22, 0)
    branch(base + Vector((0.16, -0.02, 0)), math.radians(190), 0.14, 1)


# ---------- 키트 배치 ----------
# 오른쪽 위 묶음(mm, 회전°): 스쿱 종이 · 일러카드(전체 시트 116 x 166) · 노트
SCOOP = (98.0, 86.0, 1.5)
CARD = (114.0, 90.0, -0.8)
NOTE = (234.0, 89.0, -2.5)

KITS = {
    'taste': {'card': 'card_taste_full', 'row1': ['teabag', 'lemon_balm', 'chamomile', 'hibiscus'],
              'row2': ['peppermint', 'yuza', 'rose']},
    'depth': {'card': 'card_depth_full', 'row1': ['teabag', 'brown_rice', 'dandelion_root', 'sorghum'],
              'row2': ['barley', 'red_bean', 'solomons_seal']},
}


def place_kit(ver='taste', dx=0.0, dy=0.0, marks=True, infuser_on=True):
    """키트 하나(실물 촬영 배치 그대로)를 (dx, dy) mm 만큼 옮겨 놓는다."""
    kit = KITS[ver]

    def Q(u, v):
        x, y = P(u, v)
        return x + dx, y + dy
    bx, by = Q(307, 470); box_closed(bx, by, BOX_ROT)
    # 스쿱 종이 위에 일러카드(전체 시트) — 실물 상자처럼 왼쪽에 흰 종이가 살짝 보이게. 노트는 그 오른쪽
    flat_card(f'postcard_use_{ver}', flt('postcard_use'), SCOOP[0] + dx, SCOOP[1] + dy, 104, 146, 0.0, uv_rot=3, rot=SCOOP[2])
    flat_card(kit['card'] + '_c', flt(kit['card']), CARD[0] + dx, CARD[1] + dy, 116, 166, 0.45, rot=CARD[2])
    note(NOTE[0] + dx, NOTE[1] + dy, 115, 152, 11, NOTE[2])
    for (u, key, z) in zip((361.5, 497.5, 631.5, 769.5), kit['row1'], (0.2, 0.25, 0.3, 0.35)):
        x, y = Q(u, 741.5); pouch(f'pouch_{key}_{ver}', flt('pouch_' + key), x, y, z)
    for (u, key, z) in zip((421, 560, 699.5), kit['row2'], (4.2, 4.3, 4.4)):
        x, y = Q(u, 887); pouch(f'pouch_{key}_{ver}', flt('pouch_' + key), x, y, z)
    if marks:
        px, py = Q(222, 948); bookmarks(px, py)
    if infuser_on:
        infuser(Q(285, 694), Q(283, 905))


def danpatt(cx, cy, z, rot, w=74.0):
    """단팥차 샘플 티백(누끼 PNG 알파)."""
    iw, ih = bpy.data.images.load(flt('danpatt'), check_existing=True).size
    pouch('danpatt', flt('danpatt'), cx, cy, z, w=w, h=w * ih / iw, bulge=2.0).rotation_euler = (0, 0, math.radians(rot))


def random_packs(x0, y0):
    """원료 랜덤 3팩: 라벨 비운 파우치 세 장을 비스듬히 겹쳐 놓음."""
    for i in range(3):
        ob = pouch(f'pouch_blank_{i + 1}', flt(f'pouch_blank_{i + 1}'), x0 + 22 * i, y0 - 38 * i, 6 + 0.6 * i)
        ob.rotation_euler = (0, 0, math.radians(-9 + 9 * i))


def set_two():
    """2개 세트: 키트 2(Taste·Depth) + 노트 2 + 인퓨저 2 + 단팥차 샘플. 화면 1.0 m 폭에 맞춘 전용 배치."""
    box_closed(-300, 150, BOX_ROT - 3)
    box_closed(-245, 112, BOX_ROT + 4, z=K.BZ + 2.5)            # 위에 포갠 상자
    flat_card('postcard_use_set', flt('postcard_use'), -40, 150, 104, 146, 0.0, uv_rot=3, rot=1.0)
    flat_card('card_taste_set', flt('card_taste_full'), -10, 150, 116, 166, 0.45, rot=-1.0)
    flat_card('card_depth_set', flt('card_depth_full'), 112, 146, 116, 166, 0.9, rot=2.0)
    note(240, 158, 115, 152, 11, -3.0)
    note(365, 150, 115, 152, 11, 2.0)
    rows = [('taste', -45, 0.2, -300), ('depth', -140, 4.4, -255)]
    for ver, y, z, x0 in rows:
        keys = KITS[ver]['row1'] + KITS[ver]['row2']
        for i, key in enumerate(keys):
            pouch(f'pouch_{key}_{ver}_s', flt('pouch_' + key), x0 + 86 * i, y, z + 0.05 * i)
    danpatt(410, -105, 0.3, 9)
    bookmarks(-290, -250)
    # 인퓨저 2개: 아래 가운데에 손잡이를 마주 보게 눕힘
    infuser((70, -262), (-120, -268))
    infuser((140, -262), (330, -256))


# ---------- 샷 ----------
SHOTS = {
    # 이름: (만들기, 화면 폭 m, 카메라 이동 x, y)
    # 키트 단품 컷 = 언박싱 마지막 장면과 같은 배열(단팥차 샘플 포함). 'super' = 슈퍼 얼리버드(키트 + 인퓨저만)
    'taste': (lambda: (place_kit('taste'), danpatt(330, -205, 0.3, 9)), 0.78, 0.0, 0.0),
    'depth': (lambda: (place_kit('depth'), danpatt(330, -205, 0.3, 9)), 0.78, 0.0, 0.0),
    'super': (lambda: place_kit('taste'), 0.78, 0.0, 0.0),
    'ultra': (lambda: (place_kit('taste'), random_packs(300, -112)), 0.86, 0.035, -0.01),
    'set': (set_two, 1.0, 0.0, -0.01),
}


BOX_ROT = 0.0


def render(name, build, width=0.78, sx=0.0, sy=0.0, test=False):
    K.reset(); K._mats.clear()
    sun = floor_and_light()
    occluders(sun, hw=width / 2 + sx, hh=width / 3 + sy)
    build()
    cam = bpy.data.cameras.new('cam'); cam.type = 'ORTHO'; cam.ortho_scale = width
    co = bpy.data.objects.new('cam', cam); bpy.context.scene.collection.objects.link(co)
    co.location = (sx, sy, 1.5); co.rotation_euler = (0, 0, 0)
    bpy.context.scene.camera = co
    res = (900, 600) if test else (2400, 1600)
    K.render_setup(*res, samples=32 if test else 256)
    sc = bpy.context.scene
    sc.view_settings.view_transform = 'Standard'
    sc.view_settings.exposure = -0.45
    K.save(name + ('_test' if test else ''))


if __name__ == '__main__':
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    test = '--test' in argv
    for a in argv:
        if a.startswith('--boxrot='):
            BOX_ROT = float(a.split('=')[1])
    names = [a for a in argv if not a.startswith('--')] or ['taste']
    for n in names:
        build, width, sx, sy = SHOTS[n]
        render('flatlay_' + n, build, width, sx, sy, test)
