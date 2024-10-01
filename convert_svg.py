import bpy
import re


def svg_circles_to_vertices(filename, scale):
    verts = []
    add_vert = verts.append

    pattern = 'cx="(.*)" cy="(.*)" '

    with open(filename) as f:
        for l in f:
            stripped = l.strip()
            if stripped.startswith("<circle"):
                m = re.search(pattern, stripped)
                if m:
                    x, y = m.group(1, 2)
                    x, y = float(x) * scale, -float(y) * scale
                    add_vert([x, y, 0])

    # print(verts)

    mesh = bpy.data.meshes.new("mesh_name")
    mesh.from_pydata(verts, [], [])
    mesh.update()

    obj = bpy.data.objects.new("obj_name", mesh)

    scene = bpy.context.scene
    scene.objects.link(obj)


filename = "10978611521529652583.svg"
svg_circles_to_vertices(filename, 0.01)
