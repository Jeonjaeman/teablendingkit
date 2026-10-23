"""export_glb*.py 공용: 텍스처 축소 + GLB 내보내기."""
import bpy, os


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
