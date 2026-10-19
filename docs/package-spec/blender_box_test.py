# Blender headless smoke test: build tray + lid + accordion from the measured dieline numbers (mm → m)
import bpy, math, sys, os
out = sys.argv[sys.argv.index('--') + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
S = 0.001
def box(name, w, d, h, loc, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object; o.name = name; o.scale = (w*S, d*S, h*S); o.data.materials.append(mat); return o
def mat(name, rgb, rough=0.85):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Roughness'].default_value = rough; return m
ivory = mat('ivory_plaster', (0.90, 0.86, 0.78)); brown = mat('brown_band', (0.28, 0.20, 0.14)); paper = mat('paper', (0.96, 0.94, 0.90))
T = 1.5  # board thickness mm
# TRAY: inner 285 x 275, wall 75 (from dieline: V 77.5-285.5 / 361.5; H 90.5-167 / 448 / 520.5)
L, Wd, H = 285.0, 275.0, 75.0
box('tray_floor', L, Wd, T, (0, 0, T/2*S), ivory)
box('tray_wall_L', T, Wd, H, (-(L/2 - T/2)*S, 0, H/2*S), ivory)
box('tray_wall_R', T, Wd, H, ((L/2 - T/2)*S, 0, H/2*S), ivory)
box('tray_wall_F', L, T, H, (0, -(Wd/2 - T/2)*S, H/2*S), ivory)
box('tray_wall_B', L, T, H, (0, (Wd/2 - T/2)*S, H/2*S), ivory)
# LID (small dieline 297x249, walls 60 → top 177 x 129): this is NOT the tray lid; model separately offset to the side as "lid_small"
lt, ld, lh = 177.0, 129.0, 60.0
box('lid_small_top', lt, ld, T, (0.45, 0, (lh - T/2)*S), ivory)
for nm, sc, lc in [('lid_small_L', (T, ld, lh), (0.45 - (lt/2 - T/2)*S, 0, lh/2*S)), ('lid_small_R', (T, ld, lh), (0.45 + (lt/2 - T/2)*S, 0, lh/2*S)),
                   ('lid_small_F', (lt, T, lh), (0.45, -(ld/2 - T/2)*S, lh/2*S)), ('lid_small_B', (lt, T, lh), (0.45, (ld/2 - T/2)*S, lh/2*S))]:
    box(nm, *sc, lc, ivory)
# ACCORDION: 12 panels, 130 x 180 mm, zigzag at 35° like a spring
pw, ph, ang = 130.0, 180.0, math.radians(35)
x = -0.0
for i in range(12):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    p = bpy.context.object; p.name = f'acc_{i+1:02d}'; p.scale = (pw*S, ph*S, 1)
    p.rotation_euler = (math.radians(90), 0, (ang if i % 2 == 0 else -ang))
    dx = pw*S*math.cos(ang); p.location = (-0.75 + x + dx/2, 0, ph/2*S + 0.002); x += dx
    p.data.materials.append(paper)
# camera + light + render
cam = bpy.data.cameras.new('cam'); co = bpy.data.objects.new('cam', cam); bpy.context.scene.collection.objects.link(co)
co.location = (0.0, -1.05, 0.62); co.rotation_euler = (math.radians(62), 0, 0); bpy.context.scene.camera = co; cam.lens = 40
li = bpy.data.lights.new('sun', 'SUN'); li.energy = 3.0; lo = bpy.data.objects.new('sun', li); bpy.context.scene.collection.objects.link(lo); lo.rotation_euler = (math.radians(50), math.radians(10), math.radians(-30))
w = bpy.context.scene.world or bpy.data.worlds.new('W'); bpy.context.scene.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.92, 0.90, 0.86, 1); w.node_tree.nodes['Background'].inputs[1].default_value = 0.8
sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE' if hasattr(bpy.types, 'SceneEEVEE') else 'BLENDER_EEVEE_NEXT'
try: sc.render.engine = 'BLENDER_EEVEE_NEXT'
except Exception: sc.render.engine = 'BLENDER_EEVEE'
sc.render.resolution_x, sc.render.resolution_y = 1400, 900; sc.render.filepath = os.path.join(out, 'box_test.png'); sc.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'box_test.blend'))
print('OBJECTS', len(bpy.data.objects), 'ENGINE', sc.render.engine)
