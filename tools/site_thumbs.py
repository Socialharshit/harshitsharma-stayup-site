"""Make the Work page's website tiles (site/work/sites/<key>.webp) from screenshots.

Each tile is a 3:4 card on the StayUp navy: the desktop site in a browser
window, the mobile site on a phone in front of it, the site's name, and a
glow tinted by the site's own colours.

Put two screenshots per site in tools/shots/ (they are not published):

    <key>-desk.png   1440 x 900 viewport (any 16:10 capture works)
    <key>-mob.png    390 x 844 viewport, optional (no phone without it)

then run:

    python3 tools/site_thumbs.py            # all sites in SITES
    python3 tools/site_thumbs.py minikin    # just one
"""
import argparse, colorsys, pathlib, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITES = {
    'minikin': ('Minikin', 'Online store', 'minikin.shop'),
    'spexy': ('Spexy Studio', 'Studio website', 'spexy-studio.pages.dev'),
    'prashant': ('Prashant Dhakad', 'Personal brand', 'prashant-dhakad.dhakadprashant06.workers.dev'),
    'cafepress': ('CafePress', 'E-commerce', 'cafepress.com'),
}
W, H, S = 900, 1200, 2  # output size; drawn at S x and scaled down for clean edges
NAVY, DEEP, BLUE, CYAN = (10, 18, 88), (0, 3, 31), (31, 63, 255), (18, 216, 250)
FONTS = pathlib.Path('/usr/share/fonts/opentype/inter')


def font(name, size):
    try:
        return ImageFont.truetype(str(FONTS / name), size * S)
    except OSError:
        return ImageFont.truetype('DejaVuSans.ttf', size * S)


def px(*v):
    return tuple(round(x * S) for x in v)


def accent(shot):
    """The site's most vivid colour, pulled toward StayUp blue so every tile sits in one family."""
    best, score = BLUE, 0
    raw = shot.convert('RGB').resize((48, 48)).tobytes()
    for r, g, b in zip(raw[0::3], raw[1::3], raw[2::3]):
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if s * v > score and v > .35:
            best, score = (r, g, b), s * v
    if score < .25:
        return BLUE
    return tuple(round(.65 * a + .35 * b) for a, b in zip(best, BLUE))


def glow(size, xy, radius, color, alpha):
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    x, y = xy
    ImageDraw.Draw(layer).ellipse(px(x - radius, y - radius * .8, x + radius, y + radius * .8), fill=color + (alpha,))
    return layer.filter(ImageFilter.GaussianBlur(radius * S * .45))


def shadow(size, box, r, blur, color, dy=0):
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    x0, y0, x1, y1 = box
    ImageDraw.Draw(layer).rounded_rectangle(px(x0, y0 + dy, x1, y1 + dy), px(r)[0], fill=color)
    return layer.filter(ImageFilter.GaussianBlur(blur * S))


def rounded(img, r):
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, img.width - 1, img.height - 1), r, fill=255)
    img.putalpha(mask)
    return img


def fit(shot, w, h):
    """Cover w x h from the top of the screenshot."""
    k = max(w / shot.width, h / shot.height)
    s = shot.convert('RGB').resize((round(shot.width * k), round(shot.height * k)), Image.LANCZOS)
    x = (s.width - w) // 2
    return s.crop((x, 0, x + w, h))


def background(tint):
    size = px(W, H)
    bg = Image.new('RGBA', size)
    d = ImageDraw.Draw(bg)
    for y in range(size[1]):
        t = y / size[1]
        d.line((0, y, size[0], y), fill=tuple(round(a + (b - a) * t ** 1.4) for a, b in zip(NAVY, DEEP)) + (255,))
    bg.alpha_composite(glow(size, (450, 300), 520, tint, 150))
    bg.alpha_composite(glow(size, (820, 1080), 380, CYAN, 55))
    bg.alpha_composite(glow(size, (40, 1150), 300, BLUE, 70))
    # faint blueprint grid that fades out away from the devices
    grid = Image.new('RGBA', size, (0, 0, 0, 0))
    g = ImageDraw.Draw(grid)
    for k in range(0, W + 1, 60):
        g.line(px(k, 0, k, H), fill=(255, 255, 255, 14), width=S)
    for k in range(0, H + 1, 60):
        g.line(px(0, k, W, k), fill=(255, 255, 255, 14), width=S)
    fade = Image.new('L', size, 0)
    ImageDraw.Draw(fade).ellipse(px(-150, 40, 1050, 1000), fill=255)
    grid.putalpha(Image.composite(grid.getchannel('A'), Image.new('L', size, 0), fade.filter(ImageFilter.GaussianBlur(120 * S))))
    bg.alpha_composite(grid)
    return bg


def browser(card, shot, domain, box, tint):
    x0, y0, x1, y1 = box
    bar, r = 40, 16
    card.alpha_composite(shadow(card.size, box, r, 46, (0, 0, 0, 200), dy=40))
    card.alpha_composite(shadow(card.size, box, r, 60, tint + (90,)))
    win = Image.new('RGBA', px(x1 - x0, y1 - y0), (16, 22, 64, 255))
    win.paste(fit(shot, *px(x1 - x0, y1 - y0 - bar)), (0, bar * S))
    d = ImageDraw.Draw(win)
    d.rectangle((0, 0, win.width, bar * S), fill=(20, 27, 78))
    for k, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse(px(18 + k * 20, 15, 28 + k * 20, 25), fill=c)
    d.rounded_rectangle(px(110, 9, x1 - x0 - 110, 31), 11 * S, fill=(9, 13, 44))
    f = font('Inter-Medium.otf', 13)
    d.text((win.width // 2, 20 * S), domain, font=f, fill=(214, 224, 255), anchor='mm')
    d.line((0, bar * S, win.width, bar * S), fill=(255, 255, 255, 30), width=S)
    rounded(win, r * S)
    card.alpha_composite(win, px(x0, y0))
    ImageDraw.Draw(card).rounded_rectangle(px(x0, y0, x1, y1), r * S, outline=(255, 255, 255, 46), width=S)


def phone(card, shot, box):
    x0, y0, x1, y1 = box
    bezel, r = 11, 42
    card.alpha_composite(shadow(card.size, box, r, 34, (0, 0, 0, 220), dy=30))
    body = Image.new('RGBA', px(x1 - x0, y1 - y0), (8, 10, 26, 255))
    screen = rounded(fit(shot, *px(x1 - x0 - 2 * bezel, y1 - y0 - 2 * bezel)).convert('RGBA'), (r - bezel) * S)
    body.alpha_composite(screen, px(bezel, bezel))
    d = ImageDraw.Draw(body)
    mid = (x1 - x0) / 2
    d.rounded_rectangle(px(mid - 38, bezel + 9, mid + 38, bezel + 31), 11 * S, fill=(0, 0, 0))
    rounded(body, r * S)
    card.alpha_composite(body, px(x0, y0))
    rim = ImageDraw.Draw(card)
    rim.rounded_rectangle(px(x0, y0, x1, y1), r * S, outline=(255, 255, 255, 70), width=S)
    rim.rounded_rectangle(px(x0 + 3, y0 + 3, x1 - 3, y1 - 3), (r - 3) * S, outline=(0, 0, 0, 160), width=S)


def title(card, name, kicker, has_phone):
    d = ImageDraw.Draw(card)
    room = 520 if has_phone else 780
    size = 66
    while size > 36 and d.textlength(name, font=font('InterDisplay-SemiBold.otf', size)) > room * S:
        size -= 2
    d.text(px(62, 806), kicker.upper(), font=font('Inter-SemiBold.otf', 15), fill=(127, 239, 255))
    d.text(px(60, 836), name, font=font('InterDisplay-SemiBold.otf', size), fill=(255, 255, 255))
    d.line(px(62, 836 + size + 26, 122, 836 + size + 26), fill=CYAN + (255,), width=2 * S)


def grain(card):
    rnd = random.Random(7)
    noise = Image.new('L', (W, H))
    noise.putdata([rnd.randint(0, 255) for _ in range(W * H)])
    tex = Image.merge('RGBA', [noise] * 3 + [Image.new('L', (W, H), 9)])
    card.alpha_composite(tex)


def make(key, shots, out):
    name, kicker, domain = SITES[key]
    desk = Image.open(shots / f'{key}-desk.png')
    mob_path = shots / f'{key}-mob.png'
    mob = Image.open(mob_path) if mob_path.exists() else None
    tint = accent(desk)
    card = background(tint)
    if mob:
        browser(card, desk, domain, (60, 170, 840, 690), tint)
        phone(card, mob, (612, 520, 852, 1040))
    else:
        browser(card, desk, domain, (40, 190, 860, 735), tint)
    title(card, name, kicker, bool(mob))
    card = card.resize((W, H), Image.LANCZOS)
    grain(card)
    out.mkdir(parents=True, exist_ok=True)
    card.convert('RGB').save(out / f'{key}.webp', quality=86, method=6)
    print('wrote', (out / f'{key}.webp').relative_to(ROOT) if out.is_relative_to(ROOT) else out / f'{key}.webp')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('keys', nargs='*', default=list(SITES))
    ap.add_argument('--shots', type=pathlib.Path, default=ROOT / 'tools' / 'shots')
    ap.add_argument('--out', type=pathlib.Path, default=ROOT / 'site' / 'work' / 'sites')
    a = ap.parse_args()
    for k in a.keys:
        if not (a.shots / f'{k}-desk.png').exists():
            print('skipped', k, '(no', f'{k}-desk.png in {a.shots})')
            continue
        make(k, a.shots, a.out)
