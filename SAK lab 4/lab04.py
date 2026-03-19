import bpy
import math
import os

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def create_material(name, color, metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes

    bsdf = nodes.get("Principled BSDF")
    if bsdf is None:
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')

    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness

    return mat


def stworz_rosline(wysokosc=2.0, liczba_lisci=3, promien_lisci=0.3, liczba_korzeni=4, offset_x=0):

    mat_lodyga = create_material("Lodyga", (0.4, 0.25, 0.1, 1), metallic=0.8, roughness=0.3)
    mat_lisc = create_material("Lisc", (0.1, 0.8, 0.3, 1), metallic=0.2, roughness=0.4)

#łodyga
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.1,
        depth=wysokosc,
        location=(offset_x, 0, wysokosc / 2)
    )
    lodyga = bpy.context.active_object
    lodyga.data.materials.append(mat_lodyga)

#liscie
    for i in range(liczba_lisci):
        kat = (2 * math.pi / liczba_lisci) * i

        x = offset_x + math.cos(kat) * 0.5
        y = math.sin(kat) * 0.5
        z = wysokosc * 0.8

        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        lisc = bpy.context.active_object

        lisc.scale = (promien_lisci, promien_lisci, promien_lisci / 2)
        lisc.rotation_euler = (0.5, 0, kat)
        lisc.data.materials.append(mat_lisc)

#korzenie
    for i in range(liczba_korzeni):
        kat = (2 * math.pi / liczba_korzeni) * i

        x = offset_x + math.cos(kat) * 0.3
        y = math.sin(kat) * 0.3
        z = 0.1

        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        korzen = bpy.context.active_object
        korzen.scale = (0.1, 0.1, 0.1)
        korzen.data.materials.append(mat_lodyga)


stworz_rosline(1.5, 3, 0.2, 4, offset_x=-2)
stworz_rosline(2.5, 5, 0.3, 6, offset_x=0)
stworz_rosline(3.5, 7, 0.4, 8, offset_x=2)


bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
sun = bpy.context.active_object
sun.data.energy = 3


bpy.ops.object.camera_add(location=(6, -6, 4))
camera = bpy.context.active_object
camera.rotation_euler = (1.1, 0, 0.8)
bpy.context.scene.camera = camera


scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.filepath = os.path.abspath("rosliny.png")
scene.render.image_settings.file_format = 'PNG'
scene.render.resolution_x = 800
scene.render.resolution_y = 600

bpy.ops.render.render(write_still=True)

print("zapisano jako rosliny.png")