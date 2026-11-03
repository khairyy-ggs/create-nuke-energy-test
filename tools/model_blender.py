"""Build and export the Stagg Field tier-2/3 machinery in Blender 5.2.

Run from the project root:
  blender -b --python tools/model_blender.py -- --preview-dir <directory>

The scene is stored in tools/blender/StaggFieldModels.blend. OBJ output keeps the
existing NeoForge loader, single-material mapping, block-unit scale, and Y-up axis.
"""
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/assets/staggfield"
MODEL_DIR = ASSETS / "models/block"
TEXTURE_DIR = ASSETS / "textures/block"
BLEND_PATH = ROOT / "tools/blender/StaggFieldModels.blend"


def preview_path():
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if "--preview-dir" in args:
        return Path(args[args.index("--preview-dir") + 1]).resolve()
    return ROOT / "tools/blender/previews"


class MeshBuilder:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.face_uvs = []

    def vertex(self, point):
        self.vertices.append(tuple(float(v) for v in point))
        return len(self.vertices) - 1

    def face(self, indices, uvs, normal_hint=None):
        indices = list(indices)
        uvs = list(uvs)
        if normal_hint is not None and len(indices) >= 3:
            p0, p1, p2 = (Vector(self.vertices[indices[i]]) for i in range(3))
            normal = (p1 - p0).cross(p2 - p0)
            hint = Vector(normal_hint)
            if normal.length > 1e-9 and hint.length > 1e-9 and normal.dot(hint) < 0:
                indices.reverse()
                uvs.reverse()
        self.faces.append(indices)
        self.face_uvs.append(uvs)

    def box(self, x0, y0, z0, x1, y1, z1):
        points = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                  (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        ids = [self.vertex(p) for p in points]
        square = [(0, 0), (1, 0), (1, 1), (0, 1)]
        for face, normal in [
            ([0, 3, 2, 1], (0, 0, -1)), ([4, 5, 6, 7], (0, 0, 1)),
            ([0, 1, 5, 4], (0, -1, 0)), ([1, 2, 6, 5], (1, 0, 0)),
            ([2, 3, 7, 6], (0, 1, 0)), ([3, 0, 4, 7], (-1, 0, 0)),
        ]:
            self.face([ids[i] for i in face], square, normal)

    def lathe(self, profile, segments=24, uv_height=1.0, center=(0.0, 0.0)):
        """Revolve (radius, z) points around Z. Close hollow profiles explicitly."""
        cx, cy = center
        rings = []
        for radius, z in profile:
            if radius <= 1e-8:
                rings.append([self.vertex((cx, cy, z))])
            else:
                rings.append([
                    self.vertex((cx + radius * math.cos(2 * math.pi * i / segments),
                                 cy + radius * math.sin(2 * math.pi * i / segments), z))
                    for i in range(segments)
                ])
        for row in range(len(profile) - 1):
            r0, z0 = profile[row]
            r1, z1 = profile[row + 1]
            dr, dz = r1 - r0, z1 - z0
            hint_scale = math.hypot(dz, dr) or 1.0
            for i in range(segments):
                angle = 2 * math.pi * (i + 0.5) / segments
                hint = (math.cos(angle) * dz / hint_scale,
                        math.sin(angle) * dz / hint_scale,
                        -dr / hint_scale)
                u0, u1 = i / segments, (i + 1) / segments
                v0, v1 = z0 / uv_height, z1 / uv_height
                if abs(v1 - v0) < 1e-5:
                    v1 = v0 + max(1 / 32, 0.02 / uv_height)
                if len(rings[row]) == 1 and len(rings[row + 1]) > 1:
                    self.face([rings[row][0], rings[row + 1][(i + 1) % segments], rings[row + 1][i]],
                              [((u0 + u1) / 2, v0), (u1, v1), (u0, v1)], hint)
                elif len(rings[row]) > 1 and len(rings[row + 1]) == 1:
                    self.face([rings[row][i], rings[row][(i + 1) % segments], rings[row + 1][0]],
                              [(u0, v0), (u1, v0), ((u0 + u1) / 2, v1)], hint)
                else:
                    self.face([rings[row][i], rings[row][(i + 1) % segments],
                               rings[row + 1][(i + 1) % segments], rings[row + 1][i]],
                              [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], hint)

    def ring(self, inner, outer, z0, z1, segments=32, uv_height=1.0, center=(0.0, 0.0)):
        self.lathe([(inner, z0), (outer, z0), (outer, z1), (inner, z1), (inner, z0)],
                   segments=segments, uv_height=uv_height, center=center)

    def beam(self, start, end, radial, tangent, width0, width1, depth0, depth1):
        start, end = Vector(start), Vector(end)
        radial, tangent = Vector(radial).normalized(), Vector(tangent).normalized()
        points = []
        for center, width, depth in ((start, width0, depth0), (end, width1, depth1)):
            points.extend([
                center - tangent * width / 2 - radial * depth / 2,
                center + tangent * width / 2 - radial * depth / 2,
                center + tangent * width / 2 + radial * depth / 2,
                center - tangent * width / 2 + radial * depth / 2,
            ])
        ids = [self.vertex(p) for p in points]
        face_uvs = [(0, 0), (1, 0), (1, 1), (0, 1)]
        faces = [([0, 3, 2, 1], (0, 0, -1)), ([4, 5, 6, 7], (0, 0, 1)),
                 ([0, 1, 5, 4], -radial), ([1, 2, 6, 5], -tangent),
                 ([2, 3, 7, 6], radial), ([3, 0, 4, 7], tangent)]
        for face, hint in faces:
            self.face([ids[i] for i in face], face_uvs, hint)

    def cylinder_between(self, start, end, radius, segments=12):
        start, end = Vector(start), Vector(end)
        axis = (end - start).normalized()
        helper = Vector((0, 0, 1)) if abs(axis.z) < 0.92 else Vector((0, 1, 0))
        u = helper.cross(axis).normalized()
        v = axis.cross(u).normalized()
        bottom, top = [], []
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            radial = u * math.cos(angle) + v * math.sin(angle)
            bottom.append(self.vertex(start + radial * radius))
            top.append(self.vertex(end + radial * radius))
        bottom_center, top_center = self.vertex(start), self.vertex(end)
        for i in range(segments):
            nxt = (i + 1) % segments
            mid = 2 * math.pi * (i + 0.5) / segments
            radial = u * math.cos(mid) + v * math.sin(mid)
            self.face([bottom[i], bottom[nxt], top[nxt], top[i]],
                      [(i / segments, 0), ((i + 1) / segments, 0),
                       ((i + 1) / segments, 1), (i / segments, 1)], radial)
            self.face([bottom_center, bottom[nxt], bottom[i]],
                      [(0.5, 0.5), (0.5 + 0.5 * math.cos(2 * math.pi * (i + 1) / segments),
                                    0.5 + 0.5 * math.sin(2 * math.pi * (i + 1) / segments)),
                       (0.5 + 0.5 * math.cos(2 * math.pi * i / segments),
                        0.5 + 0.5 * math.sin(2 * math.pi * i / segments))], -axis)
            self.face([top_center, top[i], top[nxt]],
                      [(0.5, 0.5), (0.5 + 0.5 * math.cos(2 * math.pi * i / segments),
                                    0.5 + 0.5 * math.sin(2 * math.pi * i / segments)),
                       (0.5 + 0.5 * math.cos(2 * math.pi * (i + 1) / segments),
                        0.5 + 0.5 * math.sin(2 * math.pi * (i + 1) / segments))], axis)

    def pipe_between(self, start, end, outer, inner, segments=16):
        start, end = Vector(start), Vector(end)
        axis = (end - start).normalized()
        helper = Vector((0, 0, 1)) if abs(axis.z) < 0.92 else Vector((0, 1, 0))
        u = helper.cross(axis).normalized()
        v = axis.cross(u).normalized()
        rings = []
        for center, radius in ((start, outer), (end, outer), (start, inner), (end, inner)):
            rings.append([self.vertex(center + radius * (u * math.cos(2 * math.pi * i / segments) +
                                                           v * math.sin(2 * math.pi * i / segments)))
                          for i in range(segments)])
        outer0, outer1, inner0, inner1 = rings
        for i in range(segments):
            nxt = (i + 1) % segments
            mid = 2 * math.pi * (i + 0.5) / segments
            radial = u * math.cos(mid) + v * math.sin(mid)
            u0, u1 = i / segments, (i + 1) / segments
            self.face([outer0[i], outer0[nxt], outer1[nxt], outer1[i]],
                      [(u0, 0), (u1, 0), (u1, 1), (u0, 1)], radial)
            self.face([inner0[i], inner0[nxt], inner1[nxt], inner1[i]],
                      [(u0, 0), (u1, 0), (u1, 1), (u0, 1)], -radial)
            self.face([outer0[i], outer0[nxt], inner0[nxt], inner0[i]],
                      [(u0, 0), (u1, 0), (u1, 1), (u0, 1)], -axis)
            self.face([outer1[i], inner1[i], inner1[nxt], outer1[nxt]],
                      [(u0, 0), (u0, 1), (u1, 1), (u1, 0)], axis)


def build_centrifuge():
    b = MeshBuilder()
    b.box(0.08, 0.08, 0.015, 0.92, 0.92, 0.12)
    b.lathe([(0, 0.10), (0.41, 0.10), (0.47, 0.15), (0.47, 0.20),
             (0.39, 0.20), (0.39, 0.29), (0.45, 0.29), (0.45, 0.34),
             (0.37, 0.34), (0.37, 0.43), (0.44, 0.43), (0.44, 0.48),
             (0.36, 0.48), (0.36, 0.57), (0.44, 0.57), (0.44, 0.62),
             (0.37, 0.62), (0.37, 0.71), (0.45, 0.71), (0.45, 0.76),
             (0.38, 0.76), (0.38, 0.84), (0.45, 0.84), (0.45, 0.90),
             (0.33, 0.90), (0.33, 0.96), (0.13, 0.96), (0.13, 1.0), (0, 1.0)],
            segments=24, uv_height=1.0, center=(0.5, 0.5))
    # Four stage tie rods and two gas-transfer ports make the cascade read at block scale.
    for angle in (0, math.pi / 2, math.pi, 3 * math.pi / 2):
        radial = Vector((math.cos(angle), math.sin(angle), 0))
        tangent = Vector((-math.sin(angle), math.cos(angle), 0))
        point = Vector((0.5, 0.5, 0)) + radial * 0.355
        b.cylinder_between(point + Vector((0, 0, 0.19)), point + Vector((0, 0, 0.82)), 0.021, 10)
        b.box(point.x - tangent.x * 0.05 - radial.x * 0.035 - 0.03,
              point.y - tangent.y * 0.05 - radial.y * 0.035 - 0.03, 0.12,
              point.x + tangent.x * 0.05 + radial.x * 0.035 + 0.03,
              point.y + tangent.y * 0.05 + radial.y * 0.035 + 0.03, 0.17)
    for angle, z in ((-math.pi / 4, 0.38), (3 * math.pi / 4, 0.59)):
        radial = Vector((math.cos(angle), math.sin(angle), 0))
        start = Vector((0.5, 0.5, z)) + radial * 0.42
        end = start + radial * 0.11
        b.pipe_between(start, end, 0.075, 0.04, 12)
        b.pipe_between(end - radial * 0.03, end + radial * 0.025, 0.095, 0.04, 12)
    return b


def build_vessel():
    b = MeshBuilder()
    center = Vector((1.5, 1.5, 0))
    b.lathe([(0, 0.20), (1.25, 0.20), (1.43, 0.32), (1.45, 0.48),
             (1.45, 2.28), (1.38, 2.60), (1.22, 2.86), (0.82, 3.18), (0, 3.30)],
            segments=32, uv_height=3.45, center=(1.5, 1.5))
    b.ring(1.35, 1.53, 0.16, 0.31, segments=32, uv_height=3.45, center=(1.5, 1.5))
    b.ring(1.22, 1.42, 2.70, 2.82, segments=32, uv_height=3.45, center=(1.5, 1.5))
    for i in range(8):
        angle = 2 * math.pi * i / 8
        radial = Vector((math.cos(angle), math.sin(angle), 0))
        tangent = Vector((-math.sin(angle), math.cos(angle), 0))
        start = center + radial * 1.40 + Vector((0, 0, 0.18))
        end = center + radial * 1.30 + Vector((0, 0, 0.72))
        b.beam(start, end, radial, tangent, 0.22, 0.14, 0.22, 0.15)
    # Gas inlet/outlet ducts leave the vessel at different elevations and angles.
    for angle, z, radius, length in ((-math.pi / 4, 2.12, 0.22, 0.55),
                                     (3 * math.pi / 4, 1.02, 0.19, 0.48)):
        radial = Vector((math.cos(angle), math.sin(angle), 0))
        start = center + radial * 1.40 + Vector((0, 0, z))
        end = start + radial * length
        b.pipe_between(start, end, radius, radius * 0.56, 20)
        flange_start = end - radial * 0.10
        b.pipe_between(flange_start, end + radial * 0.03, radius * 1.36, radius * 0.55, 20)
        # Six visible flange bolts around each duct mouth.
        tangent = Vector((-math.sin(angle), math.cos(angle), 0))
        vertical = Vector((0, 0, 1))
        for bolt in range(8):
            a = 2 * math.pi * bolt / 8
            pos = end + tangent * (math.cos(a) * radius * 1.08) + vertical * (math.sin(a) * radius * 1.08)
            b.cylinder_between(pos - radial * 0.025, pos + radial * 0.025, 0.025, 8)
    # A 3x3 charging/control-rod cap pattern is visible on the vessel head.
    for x in (-0.36, 0, 0.36):
        for y in (-0.36, 0, 0.36):
            r = math.hypot(x, y)
            z0 = 3.13 - max(0, r - 0.2) * 0.55
            pos = center + Vector((x, y, z0))
            b.cylinder_between(pos, pos + Vector((0, 0, 0.16)), 0.085, 12)
            b.cylinder_between(pos + Vector((0, 0, 0.13)), pos + Vector((0, 0, 0.20)), 0.105, 12)
    # A shallow instrument panel sits between the two main gas connections.
    b.box(1.30, 0.02, 1.43, 1.70, 0.13, 1.86)
    b.box(1.36, 0.00, 1.50, 1.64, 0.03, 1.78)
    return b


def build_tower():
    b = MeshBuilder()
    height, base, throat, throat_y, wall, segments = 8.0, 2.5, 1.5, 5.5, 0.14, 32
    k = (base * base - throat * throat) / (throat_y * throat_y)

    def radius(z):
        return math.sqrt(throat * throat + k * (z - throat_y) ** 2)

    ys = [height * i / 24 for i in range(25)]
    outer = [(radius(z), z) for z in ys]
    inner = [(max(0.05, radius(z) - wall), z) for z in reversed(ys)]
    b.lathe(outer + inner + [outer[0]], segments=segments, uv_height=height, center=(2.5, 2.5))
    # Ring beams stiffen the shell at the footing, throat, and crown.
    for z, thickness, extra in ((0.12, 0.12, 0.10), (5.48, 0.12, 0.11), (7.82, 0.14, 0.12)):
        r = radius(z)
        b.ring(max(0.05, r - 0.035), r + extra, z, z + thickness,
               segments=segments, uv_height=height, center=(2.5, 2.5))
    # Repeating lower piers transfer the shell load to the circular foundation ring.
    pier_count = 16
    for i in range(pier_count):
        angle = 2 * math.pi * i / pier_count
        radial = Vector((math.cos(angle), math.sin(angle), 0))
        tangent = Vector((-math.sin(angle), math.cos(angle), 0))
        z0, z1 = 0.12, 1.45
        center = Vector((2.5, 2.5, 0))
        start = center + radial * (radius(z0) + 0.055) + Vector((0, 0, z0))
        end = center + radial * (radius(z1) + 0.025) + Vector((0, 0, z1))
        b.beam(start, end, radial, tangent, 0.19, 0.12, 0.16, 0.13)
    # A narrow throat gallery gives the tower a human-scale maintenance point.
    z = 5.65
    r = radius(z)
    b.ring(r - 0.04, r + 0.24, z, z + 0.10, segments=segments, uv_height=height,
           center=(2.5, 2.5))
    return b


def texture_material(name, image_path):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    shader = nodes.get("Principled BSDF")
    image = bpy.data.images.load(str(image_path), check_existing=True)
    image.pack()
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = image
    tex.interpolation = "Closest"
    tex.extension = "REPEAT"
    links.new(tex.outputs["Color"], shader.inputs["Base Color"])
    shader.inputs["Roughness"].default_value = 0.84
    return material


def make_object(name, builder, material, collection):
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(builder.vertices, [], builder.faces)
    mesh.update()
    uv_layer = mesh.uv_layers.new(name="UVMap")
    for polygon, face_uvs in zip(mesh.polygons, builder.face_uvs):
        for loop_index, uv in zip(polygon.loop_indices, face_uvs):
            uv_layer.data[loop_index].uv = uv
    mesh.materials.append(material)
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    return obj


def export_obj(obj, name):
    path = MODEL_DIR / (name + ".obj")
    mesh = obj.data
    uv_layer = mesh.uv_layers.active
    lines = [f"mtllib {name}.mtl", f"o {name}", "usemtl main"]
    for vertex in mesh.vertices:
        x, y, z = vertex.co
        # Blender Z-up to the project's Minecraft Y-up OBJ coordinates.
        lines.append(f"v {x:.5f} {z:.5f} {y:.5f}")
    texture_index = 1
    for polygon in mesh.polygons:
        refs = []
        for loop_index in polygon.loop_indices:
            uv = uv_layer.data[loop_index].uv
            lines.append(f"vt {uv.x:.6f} {uv.y:.6f}")
            refs.append((mesh.loops[loop_index].vertex_index + 1, texture_index))
            texture_index += 1
        # Swapping Blender Y/Z reverses handedness; reverse each polygon once on export.
        lines.append("f " + " ".join(f"{vi}/{ti}" for vi, ti in reversed(refs)))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (MODEL_DIR / (name + ".mtl")).write_text("newmtl main\nKd 1 1 1\nmap_Kd #main\n", encoding="utf-8")
    return path


def point_camera(camera, location, target):
    camera.location = location
    camera.rotation_euler = (Vector(target) - Vector(location)).to_track_quat("-Z", "Y").to_euler()


def setup_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights, bpy.data.materials):
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 320
    scene.render.resolution_y = 320
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "Medium High Contrast"
    world = bpy.data.worlds.new("Stagg Field Studio") if not bpy.data.worlds else bpy.data.worlds[0]
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.035, 0.045, 0.05, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.55
    for name, location, energy, size in (
        ("Key", (4, -8, 13), 1800, 8), ("Fill", (-8, -1, 7), 1100, 7), ("Rim", (12, 7, 10), 1600, 6)
    ):
        data = bpy.data.lights.new(name, "AREA")
        data.energy = energy
        data.shape = "DISK"
        data.size = size
        light = bpy.data.objects.new(name, data)
        scene.collection.objects.link(light)
        light.location = location
        light.rotation_euler = (Vector((5, 0, 3)) - light.location).to_track_quat("-Z", "Y").to_euler()
    floor_mat = bpy.data.materials.new("Studio floor")
    floor_mat.diffuse_color = (0.10, 0.12, 0.13, 1)
    bpy.ops.mesh.primitive_plane_add(size=50, location=(5, 0, -0.06))
    floor = bpy.context.object
    floor.name = "StudioGround"
    floor.data.materials.append(floor_mat)
    camera_data = bpy.data.cameras.new("ReviewCamera")
    camera = bpy.data.objects.new("ReviewCamera", camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    camera.data.type = "ORTHO"
    return scene, camera, floor


def render_reviews(scene, camera, objects, centers, scales, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    for obj in objects:
        center = Vector(centers[obj.name]) + obj.location
        scale = scales[obj.name]
        camera.data.ortho_scale = scale
        for view, direction in (("front", Vector((0, -1, 0.10))),
                                ("threequarter", Vector((1.15, -1.55, 0.78)))):
            for other in objects:
                other.hide_render = other != obj
            direction.normalize()
            point_camera(camera, center + direction * scale * 2.3, center)
            scene.render.filepath = str(out_dir / f"{obj.name.lower()}_{view}.png")
            bpy.ops.render.render(write_still=True)
    for obj in objects:
        obj.hide_render = False


def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    BLEND_PATH.parent.mkdir(parents=True, exist_ok=True)
    scene, camera, floor = setup_scene()
    models_collection = bpy.data.collections.new("Stagg Field Wave 1 Models")
    scene.collection.children.link(models_collection)
    materials = {
        "Cascade_Centrifuge": texture_material("Casing Steel", TEXTURE_DIR / "casing_steel.png"),
        "Magnox_Vessel": texture_material("Casing Steel Vessel", TEXTURE_DIR / "casing_steel.png"),
        "Cooling_Tower": texture_material("Cast Concrete", TEXTURE_DIR / "concrete.png"),
    }
    builders = {
        "Cascade_Centrifuge": build_centrifuge(),
        "Magnox_Vessel": build_vessel(),
        "Cooling_Tower": build_tower(),
    }
    offsets = {"Cascade_Centrifuge": (0, 0, 0), "Magnox_Vessel": (4.5, 0, 0), "Cooling_Tower": (10, 0, 0)}
    for name in builders:
        obj = make_object(name, builders[name], materials[name], models_collection)
        obj.location = offsets[name]
        export_obj(obj, name.lower())
    objects = [bpy.data.objects[name] for name in builders]
    centers = {"Cascade_Centrifuge": (0.5, 0.5, 0.5),
               "Magnox_Vessel": (1.5, 1.5, 1.75),
               "Cooling_Tower": (2.5, 2.5, 4.0)}
    scales = {"Cascade_Centrifuge": 1.45, "Magnox_Vessel": 4.8, "Cooling_Tower": 9.0}
    render_reviews(scene, camera, objects, centers, scales, preview_path())
    # Save with all three editable models arranged as a study, not over the user's open scene.
    for obj in objects:
        obj.hide_render = False
    camera.data.ortho_scale = 18.0
    point_camera(camera, (15, -19, 15), (6, 0, 3.5))
    scene.render.resolution_x, scene.render.resolution_y = 1280, 720
    scene.render.filepath = str(preview_path() / "staggfield_model_overview.png")
    bpy.ops.render.render(write_still=True)
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    print("Exported:", ", ".join(str(MODEL_DIR / (name.lower() + ".obj")) for name in builders))
    print("Blender source:", BLEND_PATH)
    print("Preview directory:", preview_path())


if __name__ == "__main__":
    main()
