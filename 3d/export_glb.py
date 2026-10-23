"""홈페이지(three.js)용 GLB 내보내기 테스트 — 기존 Blender 모델을 그대로 쓸 수 있는지 확인.

  blender -b --python 3d/export_glb.py
출력: 3d/web/kit_open.glb (뚜껑 연 상자 + 아코디언북 + 노트), 3d/web/pouches.glb (Taste 파우치 6 + 빈 티백)
- 피벗(empty) 이름을 그대로 남겨 three.js 에서 lid_hinge.rotation.x 로 뚜껑을 열고 닫을 수 있게 한다.
- 텍스처는 GLB 안에 묶고(JPEG, 1024px 이하로 줄임), 용량과 폴리곤 수를 출력한다.
"""
import bpy, os, sys, math

os.environ['BOARD_T'] = '2.6'      # 웹은 판지를 두껍게(두께감)
os.environ['WEB_EXPORT'] = '1'     # 모서리 베벨
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_scene as K
import flatlay_scene as F

OUT = os.path.join(K.ROOT, '3d', 'web')
os.makedirs(OUT, exist_ok=True)


def shrink_textures(max_px=1024):
    for im in bpy.data.images:
        if im.size[0] > max_px or im.size[1] > max_px:
            s = max_px / max(im.size)
            im.scale(int(im.size[0] * s), int(im.size[1] * s))


def export(path):
    shrink_textures()
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', export_image_format='JPEG', export_jpeg_quality=80,
                              export_apply=True, export_yup=True, export_cameras=False, export_lights=False,
                              use_selection=True, export_texcoords=True, export_normals=True)
    tris = sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')
    print(f'EXPORTED {os.path.basename(path)} {os.path.getsize(path) / 1e6:.2f}MB polys={tris} '
          f'empties={[o.name for o in bpy.data.objects if o.type == "EMPTY"]}')


def build_accordion_hinged(n=12):
    """힌지 체인 아코디언북: acc_h00..11 을 돌리면 접히고 펼쳐진다(three.js 에서 스크롤로 구동).
    평평할 때 한 줄, 힌지 i 를 (-1)^i·(180-2a)° 돌리면 접힘각 a 의 병풍."""
    pw, ph = K.PANEL
    faces = ['acc_in_01', 'acc_in_02', 'acc_in_03_win', 'acc_in_04', 'acc_in_05_win', 'acc_in_06',
             'acc_in_07_win', 'acc_in_08', 'acc_in_09_win', 'acc_in_10', 'acc_in_11_win', 'acc_in_12']
    pouch_faces = {1, 3, 5, 7, 9, 11}
    back = K.img_mat('paper_back', None, rgb=(0.95, 0.94, 0.91), rough=0.8)
    pouch = K.img_mat('pouch', K.tex('pouch'), rough=0.45)
    root = K.empty('acc_root')
    parent = root
    for i in range(n):
        h = K.empty(f'acc_h{i:02d}', (pw if i > 0 else 0, 0, 0)); h.parent = parent
        m = K.img_mat(faces[i], K.tex(faces[i]), rough=0.75)
        K.quad(f'acc_p{i:02d}', [(0, 0, ph), (pw, 0, ph), (pw, 0, 0), (0, 0, 0)], m, back, thick=0.9, parent=h, out=(0, -1, 0))
        if i in pouch_faces:
            off, u0, u1 = 2.5, pw * .07, pw * .93
            top, bot = ph * .86, ph * .86 - pw * .86
            K.quad(f'acc_pouch{i:02d}', [(u0, -off, top), (u1, -off, top), (u1, -off, bot), (u0, -off, bot)], pouch, back, thick=1.5, parent=h, out=(0, -1, 0))
        parent = h
    w, hh = K.BOOK[0], K.BOOK[1]
    front = K.img_mat('acc_front_cover', K.tex('acc_front_cover'), rough=0.6)
    backc = K.img_mat('acc_back_cover', K.tex('acc_back_cover'), rough=0.6)
    cf = K.empty('acc_cov_f', (0, 0, 0)); cf.parent = root
    K.quad('acc_cover_f', [(-w, 0, hh), (0, 0, hh), (0, 0, 0), (-w, 0, 0)], front, back, thick=2.2, parent=cf, out=(0, -1, 0))
    cb = K.empty('acc_cov_b', (pw, 0, 0)); cb.parent = parent
    K.quad('acc_cover_b', [(0, 0, hh), (w, 0, hh), (w, 0, 0), (0, 0, 0)], backc, back, thick=2.2, parent=cb, out=(0, -1, 0))


def build_note_hinged():
    """노트: 바닥 블록 + 힌지 달린 표지·내지 4장(note_cov_h, note_pg_h0..3). 등은 -X 쪽."""
    w, h, d = K.NOTE
    paper = K.img_mat('paper_edge', None, rgb=(0.95, 0.94, 0.91), rough=0.8)
    root = K.empty('note_root')
    K.box_obj('note_block', (w, h, d * .7), (0, 0, d * .35), paper, parent=root)
    pages = [('note_p1_front', 'note_p1_back'), ('note_p2_front', 'note_p2_back'), ('note_p3_front', 'note_p3_back'), ('note_p4_front', 'note_back')]
    for k, (f, b) in enumerate(pages):
        z = d * .7 + .3 * (len(pages) - k)
        hp = K.empty(f'note_pg_h{k}', (-w / 2, 0, z)); hp.parent = root
        K.quad(f'note_page{k}', [(0, h / 2, 0), (w, h / 2, 0), (w, -h / 2, 0), (0, -h / 2, 0)],
               K.img_mat(f, K.tex(f), rough=.85), K.img_mat(b, K.tex(b), rough=.85), thick=0.25, parent=hp, out=(0, 0, 1))
    hc = K.empty('note_cov_h', (-w / 2, 0, d * .7 + .3 * (len(pages) + 1))); hc.parent = root
    K.quad('note_cover_top', [(0, h / 2, 0), (w, h / 2, 0), (w, -h / 2, 0), (0, -h / 2, 0)],
           K.img_mat('note_cover', K.tex('note_cover'), rough=.75), K.img_mat('note_in_cover', K.tex('note_in_cover'), rough=.85),
           thick=1.2, parent=hc, out=(0, 0, 1))


# 1) 닫힌 상자 + 내용물(아코디언북·노트). three.js 에서 lid_hinge / flap_pivot / dust_pivot / ear_pivot 을 돌려 연다
K.reset(); K._mats.clear()
K.build_box(0.0, with_contents=True, band='taste')
export(os.path.join(OUT, 'kit_closed.glb'))

# 2) 파우치 7개(Taste 6 + 빈 티백) — 알파 텍스처라 PNG 로 묶이므로 512px 로 줄인다
K.reset(); K._mats.clear()
for i, key in enumerate(['teabag', 'lemon_balm', 'chamomile', 'hibiscus', 'peppermint', 'yuza', 'rose']):
    F.pouch('pouch_' + key, F.flt('pouch_' + key), (i - 3) * 95.0, 0, 0)
shrink_textures(512)
export(os.path.join(OUT, 'pouches_taste.glb'))

# 3) Depth 파우치 6개
K.reset(); K._mats.clear()
for i, key in enumerate(['brown_rice', 'dandelion_root', 'sorghum', 'barley', 'red_bean', 'solomons_seal']):
    F.pouch('pouch_' + key, F.flt('pouch_' + key), (i - 2.5) * 95.0, 0, 0)
shrink_textures(512)
export(os.path.join(OUT, 'pouches_depth.glb'))

# 4) 부속: 일러카드·스쿱 종이·엽서 6장·인퓨저
K.reset(); K._mats.clear()
F.flat_card('card_taste', F.flt('card_taste_full'), 0, 0, 116, 166, 0)
F.flat_card('scoop_paper', F.flt('postcard_use'), 140, 0, 104, 146, 0, uv_rot=3)
F.bookmarks(-120, 80)
F.infuser((-200, 60), (-200, -120))
shrink_textures(768)
export(os.path.join(OUT, 'extras.glb'))

# 5) 힌지 아코디언북 · 노트
K.reset(); K._mats.clear()
build_accordion_hinged()
shrink_textures(768)
export(os.path.join(OUT, 'accordion.glb'))
K.reset(); K._mats.clear()
build_note_hinged()
shrink_textures(768)
export(os.path.join(OUT, 'note.glb'))
