"""Generate the Stagg Pile block-state JSON models.

Run: python3 tools/geom.py <outdir>

Curved machine OBJ models are authored and exported from Blender by
tools/model_blender.py. This script intentionally writes only the four pile
variants so it cannot replace Blender-authored machine geometry.
"""
import json
import os
import sys


def block_json(elements, textures):
    els = []
    for element in elements:
        tex = element.get("tex", "main")
        face_textures = element.get("face_textures", {})
        faces = {
            direction: {
                "texture": f"#{face_textures.get(direction, tex)}",
                "uv": element.get("uv", [0, 0, 16, 16]),
            }
            for direction in ("north", "east", "south", "west", "up", "down")
        }
        els.append({"from": element["from"], "to": element["to"], "faces": faces})
    return {"textures": textures, "elements": els}


def pile_parts(rod=None):
    """Four graphite slabs around a 4x4 px Y-channel, optionally filled by a rod."""
    elements = [
        {"from": [0, 0, 0], "to": [16, 16, 6], "face_textures": {"south": "bore"}},
        {"from": [0, 0, 10], "to": [16, 16, 16], "face_textures": {"north": "bore"}},
        {"from": [0, 0, 6], "to": [6, 16, 10], "face_textures": {"east": "bore"}},
        {"from": [10, 0, 6], "to": [16, 16, 10], "face_textures": {"west": "bore"}},
    ]
    if rod:
        elements.append({"from": [6, 0, 6], "to": [10, 15, 10], "tex": rod})
    return elements


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    for rod in (None, "fuel", "source", "absorber"):
        textures = {
            "main": "staggfield:block/graphite_drilled",
            "bore": "staggfield:block/graphite_bore",
            "particle": "staggfield:block/graphite_drilled",
        }
        if rod:
            textures[rod] = f"staggfield:block/pile_rod_{rod}"
        path = os.path.join(out, f"pile_{rod or 'empty'}.json")
        with open(path, "w", encoding="utf-8") as model_file:
            json.dump(block_json(pile_parts(rod), textures), model_file, indent=1)
    print("Wrote four Stagg Pile JSON variants to", out)
