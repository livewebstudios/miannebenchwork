#!/usr/bin/env python3
"""Product image prep for the Mianne catalog.

1. Resizes the downloaded old-site kit diagrams (fetch-old-images.mjs) to 720px web JPEGs.
2. Draws plan-view diagrams for every model that never had an image on the old site
   (catalog-only starter and around-the-room sizes, expansion sections, parts).
3. Places the accessory illustrations cropped from the 2024 catalog (pass --acc DIR).

Requires Pillow. Usage: python3 scripts/make-diagrams.py [--acc path/to/crops]
"""
import json, math, os, re, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'public')
SIZE = 720
INK = (58, 42, 30)
GREEN = (168, 226, 160)
TAN = (217, 196, 163)
WOOD = (233, 211, 168)
WEB = (196, 170, 128)
FONT_DIR = '/System/Library/Fonts/Supplemental'


def font(size, bold=True):
    name = 'Times New Roman Bold.ttf' if bold else 'Times New Roman.ttf'
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()


F_HEAD, F_LABEL, F_NOTE, F_SUB = font(40), font(26), font(15), font(22, bold=False)


def canvas(model, subtitle=None, note=True):
    im = Image.new('RGB', (SIZE, SIZE), 'white')
    d = ImageDraw.Draw(im)
    d.text((24, 18), f'Model {model}', font=F_HEAD, fill=(0, 0, 0))
    if subtitle:
        d.text((26, 66), subtitle, font=F_SUB, fill=INK)
    if note:
        d.line([(20, SIZE - 46), (SIZE - 20, SIZE - 46)], fill=(0, 0, 0), width=2)
        msg = 'All pricing based on standard 40" height or lower. Taller legs are available.'
        w = d.textlength(msg, font=F_NOTE)
        d.text(((SIZE - w) / 2, SIZE - 38), msg, font=F_NOTE, fill=(0, 0, 0))
    return im, d


def label(d, xy, text, anchor='mm', f=None):
    d.text(xy, text, font=f or F_LABEL, fill=(0, 0, 0), anchor=anchor)


def fit(w_units, h_units, box=(70, 120, 650, 610)):
    bw, bh = box[2] - box[0], box[3] - box[1]
    s = min(bw / w_units, bh / h_units)
    x0 = box[0] + (bw - w_units * s) / 2
    y0 = box[1] + (bh - h_units * s) / 2
    return s, x0, y0


def ft(n):
    return f"{n:g}'"


def starter(model, w, l):
    im, d = canvas(model, f"{ft(w)} x {ft(l)} rectangular table")
    s, x0, y0 = fit(l, w, (90, 140, 640, 600))
    x1, y1 = x0 + l * s, y0 + w * s
    d.rectangle([x0, y0, x1, y1], fill=TAN, outline=INK, width=4)
    cols, rows = math.ceil(l / 2), math.ceil(w / 2)
    for i in range(1, cols):
        x = x0 + (x1 - x0) * i / cols
        d.line([(x, y0), (x, y1)], fill=INK, width=2)
    for j in range(1, rows):
        y = y0 + (y1 - y0) * j / rows
        d.line([(x0, y), (x1, y)], fill=INK, width=2)
    legs_x = max(2, math.ceil(l / 4) + 1)
    for i in range(legs_x):
        x = x0 + (x1 - x0) * i / (legs_x - 1)
        for y in (y0, y1):
            d.rectangle([x - 7, y - 7, x + 7, y + 7], fill=INK)
    label(d, ((x0 + x1) / 2, y1 + 30), ft(l))
    label(d, (x0 - 34, (y0 + y1) / 2), ft(w))
    return im


def ring_polygon(x0, y0, x1, y1, c):
    return [(x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1 - c),
            (x1 - c, y1), (x0 + c, y1), (x0, y1 - c), (x0, y0 + c)]


def around(model, a, b, depth_in):
    dft = depth_in / 12
    im, d = canvas(model, f"{ft(a)} x {ft(b)} room, {depth_in}\" sections")
    s, x0, y0 = fit(b, a, (90, 130, 630, 600))
    x1, y1 = x0 + b * s, y0 + a * s
    d.rectangle([x0, y0, x1, y1], fill=GREEN, outline=INK, width=4)
    ix0, iy0, ix1, iy1 = x0 + dft * s, y0 + dft * s, x1 - dft * s, y1 - dft * s
    c = min(1.5 * s, (ix1 - ix0) / 3, (iy1 - iy0) / 3)
    # cross members every 2 ft along each run
    for i in range(1, int(b // 2)):
        x = x0 + i * 2 * s
        d.line([(x, y0), (x, iy0 + 2)], fill=INK, width=2)
        d.line([(x, iy1 - 2), (x, y1)], fill=INK, width=2)
    for j in range(1, int(a // 2)):
        y = y0 + j * 2 * s
        d.line([(x0, y), (ix0 + 2, y)], fill=INK, width=2)
        d.line([(ix1 - 2, y), (x1, y)], fill=INK, width=2)
    d.polygon(ring_polygon(ix0, iy0, ix1, iy1, c), fill='white', outline=INK, width=4)
    label(d, ((x0 + x1) / 2, y0 - 24), ft(b))
    label(d, (x1 + 34, (y0 + y1) / 2), ft(a))
    # depth arrow at top run
    ax = (x0 + x1) / 2
    d.line([(ax, y0 + 6), (ax, iy0 - 6)], fill=INK, width=2)
    for yy, sg in ((y0 + 6, 1), (iy0 - 6, -1)):
        d.polygon([(ax, yy), (ax - 6, yy + 10 * sg), (ax + 6, yy + 10 * sg)], fill=INK)
    label(d, (ax + 30, (y0 + iy0) / 2), f'{depth_in}"', f=font(20))
    return im


def section(model, depth, length, legs=True):
    im, d = canvas(model, f'{depth}" x {length}" straight section', note=False)
    s, x0, y0 = fit(length, depth, (110, 170, 620, 560))
    x1, y1 = x0 + length * s, y0 + depth * s
    d.rectangle([x0, y0, x1, y1], fill=GREEN, outline=INK, width=4)
    n = max(1, round(length / 12))
    for i in range(1, n):
        x = x0 + (x1 - x0) * i / n
        d.line([(x, y0), (x, y1)], fill=INK, width=2)
    if legs:
        for y in (y0, y1):
            d.rectangle([x1 - 8, y - 8, x1 + 8, y + 8], fill=INK)
    label(d, ((x0 + x1) / 2, y1 + 30), f'{length}"')
    label(d, (x0 - 36, (y0 + y1) / 2), f'{depth}"')
    d.text((SIZE / 2, SIZE - 50), 'Bolts onto any Mianne layout. Legs included.', font=F_SUB, fill=INK, anchor='mm')
    return im


def corner(model, depth):
    im, d = canvas(model, f'{depth}" deep 48" x 48" corner', note=False)
    s, x0, y0 = fit(48, 48, (150, 140, 590, 580))
    D = depth * s
    x1, y1 = x0 + 48 * s, y0 + 48 * s
    ch = D * 0.35
    pts = [(x0, y0), (x1, y0), (x1, y0 + D), (x0 + D + ch, y0 + D),
           (x0 + D, y0 + D + ch), (x0 + D, y1), (x0, y1)]
    d.polygon(pts, fill=GREEN, outline=INK, width=4)
    for k in range(1, 3):
        x = x0 + D + (x1 - x0 - D) * k / 3
        d.line([(x, y0), (x, y0 + D)], fill=INK, width=2)
        y = y0 + D + (y1 - y0 - D) * k / 3
        d.line([(x0, y), (x0 + D, y)], fill=INK, width=2)
    d.line([(x0, y0), (x0 + D, y0 + D)], fill=INK, width=2)
    label(d, ((x0 + x1) / 2, y0 - 24), '48"')
    label(d, (x0 - 34, (y0 + y1) / 2), '48"')
    label(d, (x1 + 34, y0 + D / 2), f'{depth}"', f=font(22))
    d.text((SIZE / 2, SIZE - 50), 'Turns any Mianne layout a corner. Legs included.', font=F_SUB, fill=INK, anchor='mm')
    return im


def leg(d, cx, top, bottom, w=26):
    d.polygon([(cx - w * .9, top), (cx + w * .9, top), (cx + w * 1.2, top + 10),
               (cx - w * 1.2, top + 10)], fill=WOOD, outline=INK)
    d.rectangle([cx - w / 2, top + 10, cx + w / 2, bottom - 14], fill=WOOD, outline=INK, width=3)
    d.rectangle([cx - 4, bottom - 14, cx + 4, bottom - 6], fill=(150, 150, 150), outline=INK)
    d.rectangle([cx - 14, bottom - 6, cx + 14, bottom], fill=(90, 90, 90), outline=INK)


def legset(model, depth):
    im, d = canvas(model, f'Leg set for {depth}" sections', note=False)
    w = 140 + depth * 8
    cx0, cx1 = SIZE / 2 - w / 2, SIZE / 2 + w / 2
    top, bot = 170, 600
    beam_y = top + 40
    d.rectangle([cx0, beam_y, cx1, beam_y + 34], fill=WOOD, outline=INK, width=3)
    d.rectangle([cx0 + 8, beam_y + 9, cx1 - 8, beam_y + 25], fill=WEB, outline=INK)
    leg(d, cx0, top, bot)
    leg(d, cx1, top, bot)
    label(d, (SIZE / 2, beam_y - 26), f'{depth}"')
    label(d, (cx1 + 70, (top + bot) / 2), '40"')
    d.text((SIZE / 2, SIZE - 50), 'Add to any section to make it free-standing.', font=F_SUB, fill=INK, anchor='mm')
    return im


def ibeam(model, length, angled=False, subtitle=None):
    im, d = canvas(model, subtitle or (f'{length}" 45° I-beam' if angled else f'{length}" I-beam'), note=False)
    maxlen = 48
    w = 160 + 420 * length / maxlen
    x0, x1 = SIZE / 2 - w / 2, SIZE / 2 + w / 2
    y0, y1 = 250, 330
    off = 40 if angled else 0
    d.polygon([(x0, y0), (x1, y0), (x1 - off, y1), (x0 + off, y1)], fill=WOOD, outline=INK, width=3)
    d.polygon([(x0 + 14 + off * .2, y0 + 16), (x1 - 14 - off * .2, y0 + 16),
               (x1 - 14 - off * .8, y1 - 16), (x0 + 14 + off * .8, y1 - 16)], fill=WEB, outline=INK)
    for hx in (x0 + 26 + off * .5, x1 - 26 - off * .5):
        d.ellipse([hx - 7, (y0 + y1) / 2 - 7, hx + 7, (y0 + y1) / 2 + 7], fill='white', outline=INK, width=2)
    d.line([(x0, y0 - 30), (x1, y0 - 30)], fill=INK, width=2)
    for xx in (x0, x1):
        d.line([(xx, y0 - 40), (xx, y0 - 20)], fill=INK, width=2)
    label(d, (SIZE / 2, y0 - 54), f'{length}"')
    # cross-section inset
    cx, cy = SIZE / 2, 480
    d.rectangle([cx - 34, cy - 60, cx + 34, cy - 44], fill=WOOD, outline=INK, width=3)
    d.rectangle([cx - 6, cy - 44, cx + 6, cy + 44], fill=WEB, outline=INK, width=2)
    d.rectangle([cx - 34, cy + 44, cx + 34, cy + 60], fill=WOOD, outline=INK, width=3)
    d.text((cx, cy + 92), 'Hardwood frame, hardboard web', font=F_SUB, fill=INK, anchor='mm')
    return im


def block(model, name, kind):
    im, d = canvas(model, name, note=False)
    cx, cy = SIZE / 2, 380
    def cube(x, y, w, h, dep, fill=WOOD):
        d.polygon([(x, y), (x + w, y), (x + w + dep, y - dep), (x + dep, y - dep)], fill=tuple(min(255, c + 14) for c in fill), outline=INK)
        d.polygon([(x + w, y), (x + w + dep, y - dep), (x + w + dep, y + h - dep), (x + w, y + h)], fill=tuple(max(0, c - 24) for c in fill), outline=INK)
        d.rectangle([x, y, x + w, y + h], fill=fill, outline=INK, width=3)
    if kind == 'connector':
        cube(cx - 90, cy - 60, 180, 120, 50)
        for hx in (cx - 45, cx + 45):
            d.ellipse([hx - 12, cy - 12, hx + 12, cy + 12], fill='white', outline=INK, width=2)
    elif kind == 'full':
        cube(cx - 150, cy - 60, 300, 120, 50)
        for hx in (cx - 110, cx - 40, cx + 40, cx + 110):
            d.ellipse([hx - 11, cy - 11, hx + 11, cy + 11], fill='white', outline=INK, width=2)
    elif kind == 'adapter':
        cube(cx - 70, cy - 70, 140, 140, 40)
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill='white', outline=INK, width=2)
    elif kind == 'double':
        cube(cx - 160, cy - 70, 140, 140, 40)
        cube(cx + 20, cy - 70, 140, 140, 40)
        for hx in (cx - 90, cx + 90):
            d.ellipse([hx - 14, cy - 14, hx + 14, cy + 14], fill='white', outline=INK, width=2)
    elif kind == 'top':
        cube(cx - 60, cy - 30, 120, 60, 30)
        for i, hx in enumerate((cx - 150, cx + 150)):
            d.line([(hx, cy - 50), (hx, cy + 40)], fill=INK, width=6)
            d.polygon([(hx - 14, cy - 56), (hx + 14, cy - 56), (hx + 8, cy - 46), (hx - 8, cy - 46)], fill=INK)
            d.polygon([(hx - 4, cy + 40), (hx + 4, cy + 40), (hx, cy + 54)], fill=INK)
        d.text((cx, cy + 110), 'Screws included', font=F_SUB, fill=INK, anchor='mm')
    return im


def legpart(model, name, height):
    im, d = canvas(model, name, note=False)
    top, bot = 140, 140 + 440 * min(1, (height if isinstance(height, int) else 46) / 58)
    leg(d, SIZE / 2 - 40, top, bot, w=34)
    d.line([(SIZE / 2 + 40, top), (SIZE / 2 + 40, bot)], fill=INK, width=2)
    for yy in (top, bot):
        d.line([(SIZE / 2 + 30, yy), (SIZE / 2 + 50, yy)], fill=INK, width=2)
    label(d, (SIZE / 2 + 100, (top + bot) / 2), f'{height}"' if isinstance(height, int) else height)
    d.text((SIZE / 2, SIZE - 50), 'Solid hardwood, built-in leveling foot', font=F_SUB, fill=INK, anchor='mm')
    return im


def caster(model, name):
    im, d = canvas(model, name, note=False)
    cx, cy = SIZE / 2, 360
    d.rectangle([cx - 90, cy - 130, cx + 90, cy - 112], fill=(150, 150, 150), outline=INK, width=3)
    d.polygon([(cx - 40, cy - 112), (cx + 40, cy - 112), (cx + 56, cy + 10), (cx - 56, cy + 10)], fill=(190, 190, 190), outline=INK)
    d.ellipse([cx - 80, cy - 40, cx + 80, cy + 120], fill=(70, 70, 70), outline=INK, width=3)
    d.ellipse([cx - 26, cy + 14, cx + 26, cy + 66], fill=(200, 200, 200), outline=INK, width=2)
    label(d, (cx + 150, cy + 40), '2"')
    d.text((cx, SIZE - 70), 'Locking or non-locking', font=F_SUB, fill=INK, anchor='mm')
    return im


def place_crop(model, src):
    im, d = canvas(model, note=False)
    art = Image.open(src).convert('RGB')
    art.thumbnail((SIZE - 60, SIZE - 150), Image.LANCZOS)
    im.paste(art, ((SIZE - art.width) // 2, 110 + (SIZE - 150 - art.height) // 2))
    return im


def save(im, rel):
    im.save(os.path.join(OUT, rel), quality=82, optimize=True, progressive=True)


def main():
    acc_dir = sys.argv[sys.argv.index('--acc') + 1] if '--acc' in sys.argv else None
    data = json.load(open(os.path.join(ROOT, 'src/data/products.json')))
    old = json.load(open(os.path.join(ROOT, 'scripts/old-image-map.json')))
    made = []
    for p in data['products']:
        m, rel = p['model'], p['image']
        dest = os.path.join(OUT, rel)
        if m in old:
            if os.path.exists(dest):
                im = Image.open(dest).convert('RGB')
                if im.width > SIZE:
                    im = im.resize((SIZE, SIZE * im.height // im.width), Image.LANCZOS)
                    save(im, rel)
            continue
        im = None
        if (g := re.fullmatch(r'ST-(\d+)x(\d+)TSR', m)):
            im = starter(m, int(g[1]), int(g[2]))
        elif (g := re.fullmatch(r'AR(8|9|10|12)(12|16|20|24)-(\d+)', m)):
            im = around(m, int(g[1]), int(g[2]), int(g[3]))
        elif (g := re.fullmatch(r'(24|30|36)([A-H]|LS)', m)):
            dep = int(g[1])
            if g[2] == 'A':
                im = corner(m, dep)
            elif g[2] == 'LS':
                im = legset(m, dep)
            else:
                im = section(m, dep, int(re.match(r'\d+', p['dimensions'].split('x')[1].strip())[0]))
        elif m in ('0012', '0018', '0024', '0030', '0036', '0042', '0048'):
            im = ibeam(m, int(m))
        elif m in ('1245', '1845', '2445', '3045'):
            im = ibeam(m, int(re.match(r'\d+', p['dimensions'])[0]), angled=True)
        elif m == '1005':
            im = block(m, p['dimensions'], 'connector')
        elif m == '1010':
            im = block(m, p['dimensions'], 'full')
        elif m == '2001':
            im = block(m, p['dimensions'], 'adapter')
        elif m == '2002':
            im = block(m, p['dimensions'], 'double')
        elif m == '3001':
            im = block(m, 'Top Attachment Block', 'top')
        elif m == '1040':
            im = legpart(m, '40" Leg', 40)
        elif m == '1048':
            im = legpart(m, '42" to 48" Leg', '42-48"')
        elif m == '1058':
            im = legpart(m, '58" Two-Level Leg', 58)
        elif m == 'CAS-1':
            im = caster(m, '2" Adjustable Height Caster')
        elif acc_dir and os.path.exists(os.path.join(acc_dir, f'{m.lower()}.png')):
            im = place_crop(m, os.path.join(acc_dir, f'{m.lower()}.png'))
        if im is None:
            print('NO IMAGE:', m)
            continue
        save(im, rel)
        made.append(m)
    print(f'generated {len(made)} diagrams')


if __name__ == '__main__':
    main()
