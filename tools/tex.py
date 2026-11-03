"""Deterministic pixel-art materials for Create: Stagg Field.

Textures borrow muted zinc, copper, and brass values from Create's 1.21.1 palette.
Run: python3 tools/tex.py <output-directory>
"""
import os, struct, sys, zlib


def png(path, px):
    h, w = len(px), len(px[0])
    channels = len(px[0][0])
    color_type = 6 if channels == 4 else 2
    raw = b"".join(b"\x00" + bytes(c for p in row for c in p) for row in px)
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, color_type, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def canvas(w, h, color):
    return [[color for _ in range(w)] for _ in range(h)]


def rect(px, x0, y0, x1, y1, color):
    for y in range(y0, y1):
        for x in range(x0, x1):
            px[y][x] = color


def dots(px, entries):
    for x, y, color in entries:
        px[y][x] = color


def graphite():
    p = canvas(16, 16, (55, 59, 60))
    rect(p, 0, 0, 16, 1, (37, 41, 42))
    rect(p, 0, 0, 1, 16, (37, 41, 42))
    rect(p, 1, 15, 16, 16, (82, 86, 84))
    rect(p, 15, 1, 16, 16, (82, 86, 84))
    rect(p, 2, 2, 6, 4, (63, 67, 67))
    rect(p, 7, 3, 11, 5, (48, 52, 53))
    rect(p, 10, 7, 14, 9, (62, 66, 65))
    rect(p, 3, 10, 7, 12, (48, 52, 53))
    rect(p, 8, 12, 12, 14, (63, 67, 67))
    dots(p, [(3, 5, (91, 94, 91)), (4, 5, (69, 73, 72)), (12, 3, (87, 90, 87)),
             (13, 4, (44, 48, 49)), (2, 8, (77, 81, 79)), (8, 7, (96, 99, 94)),
             (6, 9, (42, 46, 47)), (11, 11, (92, 94, 90)), (13, 12, (45, 49, 49)),
             (5, 13, (78, 81, 78)), (8, 2, (79, 82, 79)), (2, 13, (45, 49, 49))])
    return p


def bore():
    p = canvas(16, 16, (34, 38, 39))
    rect(p, 0, 0, 16, 2, (46, 50, 50))
    rect(p, 0, 14, 16, 16, (27, 31, 32))
    for x in (2, 6, 10, 14):
        rect(p, x, 2, x + 1, 14, (25, 29, 30))
        rect(p, x + 1, 2, x + 2, 14, (65, 69, 68))
    rect(p, 0, 6, 16, 7, (42, 46, 47))
    rect(p, 0, 11, 16, 12, (30, 34, 35))
    dots(p, [(4, 4, (91, 94, 91)), (12, 9, (82, 85, 82)), (8, 3, (74, 78, 77)),
             (3, 10, (24, 28, 29)), (13, 5, (24, 28, 29))])
    return p


def rod(edge, shade, body, highlight, cap, band):
    p = canvas(16, 16, body)
    rect(p, 0, 0, 16, 16, shade)
    rect(p, 2, 0, 14, 16, body)
    rect(p, 4, 0, 6, 16, highlight)
    rect(p, 6, 0, 11, 16, body)
    rect(p, 11, 0, 13, 16, shade)
    rect(p, 0, 0, 2, 16, edge)
    rect(p, 14, 0, 16, 16, edge)
    rect(p, 0, 1, 16, 3, cap)
    rect(p, 0, 13, 16, 15, cap)
    rect(p, 2, 5, 14, 7, band)
    rect(p, 2, 8, 14, 9, shade)
    rect(p, 1, 0, 15, 1, highlight)
    rect(p, 1, 15, 15, 16, edge)
    dots(p, [(3, 3, highlight), (12, 3, edge), (3, 11, edge), (12, 11, highlight)])
    return p


def steel():
    p = canvas(32, 32, (93, 98, 85))
    # A broad, inset steel plate with rolled ribs and a narrow brass safety stripe.
    rect(p, 0, 0, 32, 2, (47, 52, 49))
    rect(p, 0, 30, 32, 32, (47, 52, 49))
    for x in (0, 1, 8, 9, 22, 23, 30, 31):
        rect(p, x, 2, x + 1, 30, (75, 82, 73) if x % 2 == 0 else (126, 128, 108))
    rect(p, 3, 4, 29, 28, (126, 128, 108))
    rect(p, 4, 5, 28, 27, (111, 119, 101))
    rect(p, 5, 6, 27, 26, (126, 128, 108))
    rect(p, 3, 4, 29, 5, (170, 181, 157))
    rect(p, 3, 27, 29, 28, (75, 82, 73))
    rect(p, 0, 13, 32, 14, (58, 36, 17))
    rect(p, 0, 14, 32, 16, (255, 235, 140))
    rect(p, 0, 16, 32, 17, (114, 71, 49))
    # Split the stripe into dark registration marks so it reads as worn safety paint.
    for x in (4, 12, 20, 28):
        rect(p, x, 14, x + 2, 16, (58, 36, 17))
    for x, y in ((5, 7), (25, 7), (5, 24), (25, 24)):
        rect(p, x - 1, y - 1, x + 2, y + 2, (47, 52, 49))
        p[y][x] = (181, 209, 186)
    dots(p, [(11, 9, (170, 181, 157)), (12, 9, (75, 82, 73)), (19, 22, (75, 82, 73)),
             (20, 22, (170, 181, 157)), (15, 4, (82, 97, 93)), (16, 26, (82, 97, 93))])
    return p


def concrete():
    p = canvas(32, 32, (145, 143, 132))
    # Cast panel seams, old runoff, and grime at both exposed edges.
    rect(p, 0, 0, 32, 2, (105, 106, 98))
    rect(p, 0, 30, 32, 32, (105, 106, 98))
    rect(p, 0, 8, 32, 9, (113, 113, 103))
    rect(p, 0, 9, 32, 10, (166, 162, 146))
    rect(p, 0, 22, 32, 23, (113, 113, 103))
    rect(p, 0, 23, 32, 24, (166, 162, 146))
    rect(p, 0, 2, 1, 30, (123, 124, 114))
    rect(p, 31, 2, 32, 30, (123, 124, 114))
    rect(p, 15, 2, 16, 8, (128, 128, 116))
    rect(p, 16, 10, 17, 22, (128, 128, 116))
    rect(p, 15, 24, 16, 30, (128, 128, 116))
    # Water and soot run below panel joints in short, broken streaks.
    for x, y1, y2 in ((4, 10, 15), (6, 10, 13), (20, 10, 17), (27, 10, 14),
                      (2, 24, 28), (11, 24, 27), (23, 24, 29), (29, 24, 26)):
        rect(p, x, y1, x + 1, y2, (118, 119, 108))
    rect(p, 20, 11, 22, 13, (132, 128, 115))
    rect(p, 23, 25, 25, 27, (130, 126, 114))
    dots(p, [(3, 5, (176, 171, 154)), (9, 4, (119, 120, 111)), (12, 6, (159, 157, 141)),
             (21, 5, (176, 171, 154)), (26, 6, (119, 120, 111)), (8, 16, (176, 171, 154)),
             (13, 18, (119, 120, 111)), (24, 19, (173, 168, 151)), (5, 26, (176, 171, 154)),
             (18, 27, (119, 120, 111)), (26, 29, (169, 164, 148))])
    return p


def uraninite_ore(deep=False):
    base = (48, 52, 53) if deep else (101, 104, 98)
    edge = (35, 38, 39) if deep else (73, 76, 71)
    light = (69, 73, 72) if deep else (132, 130, 112)
    p = canvas(16, 16, base)
    for x, y, color in ((1, 1, edge), (4, 2, light), (8, 1, edge), (12, 3, light),
                        (2, 6, light), (6, 5, edge), (10, 7, light), (14, 6, edge),
                        (4, 10, edge), (8, 12, light), (13, 11, edge), (2, 14, light)):
        p[y][x] = color
    inclusion = (157, 145, 83) if deep else (186, 173, 94)
    seam = (92, 111, 85) if deep else (124, 142, 99)
    for x, y in ((4, 4), (5, 4), (6, 4), (5, 5), (11, 9), (12, 9), (11, 10), (10, 10)):
        p[y][x] = inclusion
    for x, y in ((6, 6), (12, 10), (3, 5), (9, 11)):
        p[y][x] = seam
    return p


def item_gem(colors, shape):
    """Small transparent pixel icons; shape points are grouped as body, shade, highlight."""
    p = canvas(16, 16, (0, 0, 0, 0))
    for color, points in zip(colors, shape):
        for x, y in points:
            p[y][x] = color
    return p


def uranium_concentrate():
    body = [(x, y) for y, xs in ((8, range(4, 12)), (9, range(3, 13)), (10, range(2, 14)),
                                 (11, range(3, 13)), (12, range(4, 12))) for x in xs]
    shade = [(3, 10), (4, 11), (5, 12), (10, 12), (11, 11), (12, 10), (6, 10), (9, 9)]
    highlight = [(5, 8), (6, 8), (8, 9), (9, 10)]
    return item_gem([(117, 89, 47, 255), (76, 61, 39, 255), (197, 166, 92, 255)],
                    (body, shade, highlight))


def washed_uraninite():
    body = [(x, y) for y, xs in ((7, range(6, 10)), (8, range(4, 12)), (9, range(3, 13)),
                                 (10, range(4, 12)), (11, range(6, 10))) for x in xs]
    shade = [(4, 9), (5, 10), (6, 11), (9, 11), (10, 10), (11, 9)]
    highlight = [(6, 7), (7, 7), (8, 8), (9, 9)]
    return item_gem([(167, 151, 92, 255), (108, 103, 71, 255), (215, 204, 145, 255)],
                    (body, shade, highlight))


def carbon_fines():
    grains = [(4, 10), (5, 9), (6, 10), (7, 11), (8, 9), (9, 10), (10, 11), (11, 9), (12, 10)]
    shade = [(5, 11), (7, 12), (9, 11), (11, 10)]
    highlight = [(5, 9), (8, 9), (11, 9)]
    return item_gem([(75, 80, 79, 255), (42, 47, 48, 255), (138, 143, 135, 255)],
                    (grains, shade, highlight))


def fuel_mix():
    body = [(x, y) for y, xs in ((8, range(5, 11)), (9, range(4, 12)), (10, range(3, 13)),
                                 (11, range(4, 12)), (12, range(6, 10))) for x in xs]
    shade = [(4, 10), (5, 11), (6, 12), (9, 12), (10, 11), (11, 10)]
    highlight = [(6, 8), (7, 8), (9, 9)]
    return item_gem([(123, 112, 75, 255), (69, 67, 55, 255), (182, 171, 128, 255)],
                    (body, shade, highlight))


def pellet(body, band):
    outline = [(6, 3), (7, 3), (8, 3), (9, 3), (5, 4), (10, 4), (5, 5), (10, 5),
               (5, 6), (10, 6), (5, 7), (10, 7), (5, 8), (10, 8), (5, 9), (10, 9),
               (5, 10), (10, 10), (6, 11), (7, 11), (8, 11), (9, 11)]
    face = [(6, y) for y in range(4, 11)] + [(7, y) for y in range(4, 11)] + [(8, y) for y in range(4, 11)] + [(9, y) for y in range(4, 11)]
    band_points = [(x, 7) for x in range(6, 10)]
    return item_gem([(42, 46, 44, 255), body, band], (outline, face, band_points))


def boron_powder():
    body = [(x, y) for y, xs in ((9, range(6, 10)), (10, range(4, 12)), (11, range(3, 13)),
                                 (12, range(5, 11))) for x in xs]
    shade = [(4, 11), (5, 12), (6, 12), (10, 12), (11, 11)]
    highlight = [(6, 9), (7, 9), (9, 10)]
    return item_gem([(85, 115, 106, 255), (49, 72, 68, 255), (137, 177, 158, 255)],
                    (body, shade, highlight))


def boron_pellet():
    body = [(x, y) for y, xs in ((6, range(6, 10)), (7, range(5, 11)), (8, range(5, 11)),
                                 (9, range(5, 11)), (10, range(6, 10))) for x in xs]
    shade = [(5, 8), (6, 10), (9, 10), (10, 8)]
    highlight = [(7, 6), (8, 6), (7, 7)]
    return item_gem([(43, 59, 57, 255), (28, 39, 38, 255), (122, 149, 133, 255)],
                    (body, shade, highlight))


def rotor_warning():
    p = canvas(16, 16, (55, 58, 54))
    rect(p, 0, 0, 16, 2, (39, 42, 39))
    rect(p, 0, 14, 16, 16, (39, 42, 39))
    for x in range(0, 16, 4):
        rect(p, x, 3, min(x + 2, 16), 13, (198, 166, 80))
        rect(p, min(x + 2, 16), 3, min(x + 4, 16), 13, (73, 59, 37))
    dots(p, [(1, 4, (232, 210, 138)), (9, 9, (232, 210, 138)),
             (13, 5, (37, 40, 38)), (5, 11, (37, 40, 38))])
    return p


TEXTURES = {
    "graphite_drilled": graphite(),
    "graphite_bore": bore(),
    "pile_rod_fuel": rod((75, 64, 42), (93, 98, 85), (126, 116, 82), (181, 209, 186), (158, 105, 71), (114, 71, 49)),
    "pile_rod_source": rod((75, 73, 72), (154, 80, 56), (178, 98, 71), (214, 123, 91), (255, 235, 140), (75, 73, 72)),
    "pile_rod_absorber": rod((47, 58, 56), (75, 82, 73), (82, 110, 105), (181, 209, 186), (126, 128, 108), (47, 52, 49)),
    "casing_steel": steel(),
    "concrete": concrete(),
    "uraninite_ore": uraninite_ore(),
    "deepslate_uraninite_ore": uraninite_ore(deep=True),
    "uraninite_concentrate": uranium_concentrate(),
    "washed_uraninite": washed_uraninite(),
    "carbon_fines": carbon_fines(),
    "fuel_mix": fuel_mix(),
    "fuel_pellet": pellet((143, 141, 112, 255), (184, 160, 83, 255)),
    "boron_powder": boron_powder(),
    "boron_pellet": boron_pellet(),
    "rotor_warning": rotor_warning(),
}


if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    if not args:
        raise SystemExit("usage: tex.py <output-directory>")
    out = args[0]
    os.makedirs(out, exist_ok=True)
    for name, pixels in TEXTURES.items():
        png(os.path.join(out, name + ".png"), pixels)
