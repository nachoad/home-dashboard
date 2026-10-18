"""Small icons drawn with Pillow primitives, using only the panel's six inks.

draw(img, name, x, y, size, color) paints icon `name` in the size×size box at (x, y).
A PNG in assets/<name>.png (RGBA, ideally already in the six colours) overrides it.
"""

import math
import os

from PIL import Image, ImageDraw

BLACK, WHITE, YELLOW = (0, 0, 0), (255, 255, 255), (255, 255, 0)
RED, BLUE, GREEN = (255, 0, 0), (0, 0, 255), (0, 255, 0)

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


class _Box:
    """Maps unit coordinates (0..1) inside the icon box to pixels."""

    def __init__(self, x, y, s):
        self.x, self.y, self.s = x, y, s

    def p(self, u, v):
        return (round(self.x + u * self.s), round(self.y + v * self.s))

    def r(self, u0, v0, u1, v1):
        return [*self.p(u0, v0), *self.p(u1, v1)]

    def w(self, k):
        return max(1, round(k * self.s))


def _calendar_blank(d, b, c, k=.09):
    d.rounded_rectangle(b.r(.06, .14, .94, .94), radius=b.w(.1), outline=c, width=b.w(k))
    d.rectangle(b.r(.06, .14, .94, .36 - (.09 - k) * 1.5), fill=c)
    for u in (.3, .7):
        d.rounded_rectangle(b.r(u - .05, .04, u + .05, .24), radius=b.w(.04), fill=c)


def _calendar(d, b, c):
    _calendar_blank(d, b, c)
    for u in (.25, .55):
        for v in (.5, .7):
            d.rounded_rectangle(b.r(u, v, u + .2, v + .1), radius=b.w(.03), fill=c)


def _sun(d, b, c, cx=.5, cy=.5, k=1.0):
    r = .2 * k
    for i in range(8):
        a = i * math.pi / 4
        d.line([b.p(cx + math.cos(a) * r * 1.45, cy + math.sin(a) * r * 1.45),
                b.p(cx + math.cos(a) * r * 2.05, cy + math.sin(a) * r * 2.05)],
               fill=c, width=b.w(.07 * k))
    d.ellipse(b.r(cx - r, cy - r, cx + r, cy + r), fill=c, outline=BLACK, width=b.w(.03))


def _cloud(d, b, c, dy=0.0, fill=WHITE):
    parts = [(.08, .42 + dy, .44, .78 + dy), (.28, .22 + dy, .70, .64 + dy),
             (.54, .38 + dy, .92, .76 + dy)]
    o = .06
    for u0, v0, u1, v1 in parts:  # outline pass, then fill pass on top
        d.ellipse(b.r(u0 - o / 2, v0 - o / 2, u1 + o / 2, v1 + o / 2), fill=c)
    d.rectangle(b.r(.23, .58 + dy - o / 2, .73, .78 + dy + o / 2), fill=c)
    for u0, v0, u1, v1 in parts:
        d.ellipse(b.r(u0 + o / 2, v0 + o / 2, u1 - o / 2, v1 - o / 2), fill=fill)
    d.rectangle(b.r(.25, .58 + dy, .71, .78 + dy - o / 2), fill=fill)


def _partly(d, b, c):
    _sun(d, b, YELLOW, .64, .34, .8)
    _cloud(d, b, c, dy=.08)


def _rain(d, b, c):
    _cloud(d, b, c, dy=-.12, fill=c)
    for u in (.3, .5, .7):
        d.line([b.p(u + .05, .74), b.p(u - .03, .92)], fill=c, width=b.w(.07))


def _snow(d, b, c):
    _cloud(d, b, c, dy=-.12)
    for u in (.3, .5, .7):
        d.ellipse(b.r(u - .05, .78, u + .05, .88), fill=c)


def _storm(d, b, c):
    _cloud(d, b, c, dy=-.12, fill=c)
    d.polygon([b.p(.52, .6), b.p(.36, .82), b.p(.5, .82), b.p(.42, 1.0), b.p(.66, .74),
               b.p(.52, .74), b.p(.6, .6)], fill=YELLOW, outline=BLACK)


def _drop(d, b, c):
    d.polygon([b.p(.5, .05), b.p(.22, .55), b.p(.78, .55)], fill=c)
    d.ellipse(b.r(.2, .35, .8, .95), fill=c)


def _umbrella(d, b, c):
    for u, v in ((.12, .1), (.86, .16), (.2, .62), (.84, .7)):  # rain drops around it
        _drop(d, _Box(*b.p(u - .05, v), b.w(.1)), BLUE)
    d.line([b.p(.5, .06), b.p(.5, .16)], fill=BLACK, width=b.w(.04))
    d.pieslice(b.r(.06, .14, .94, .86), 180, 360, fill=c, outline=BLACK, width=b.w(.02))
    for u in (.21, .5, .79):  # scalloped edge
        d.ellipse(b.r(u - .15, .44, u + .15, .56), fill=WHITE)
    for u in (.36, .64):  # ribs
        d.line([b.p(.5, .16), b.p(u, .46)], fill=BLACK, width=b.w(.02))
    d.line([b.p(.5, .44), b.p(.5, .86)], fill=BLACK, width=b.w(.05))
    d.arc(b.r(.34, .76, .52, .94), 0, 180, fill=BLACK, width=b.w(.05))


def _person(d, b, c):
    d.ellipse(b.r(.3, .06, .7, .46), outline=c, width=b.w(.1))
    d.chord(b.r(.12, .52, .88, 1.3), 180, 360, outline=c, width=b.w(.1))
    d.line([b.p(.12, .9), b.p(.88, .9)], fill=c, width=b.w(.1))


def _cutlery(d, b, c):
    # fork
    # whole-pixel tines and gaps, so they stay apart at small sizes
    tw = max(1, round(b.s * .07))
    x0 = b.p(.28, 0)[0] - (5 * tw) // 2
    top, base = b.p(0, .06)[1], b.p(0, .38)[1]
    for i in range(3):
        d.rectangle([x0 + 2 * i * tw, top, x0 + 2 * i * tw + tw - 1, base], fill=c)
    d.rounded_rectangle([x0, base - 1, x0 + 5 * tw - 1, b.p(0, .5)[1]], radius=b.w(.08), fill=c)
    d.line([b.p(.28, .4), b.p(.28, .94)], fill=c, width=b.w(.11))
    # knife
    d.pieslice(b.r(.56, .06, .86, .9), 270, 360, fill=c)
    d.rectangle(b.r(.66, .06, .71, .48), fill=c)
    d.line([b.p(.69, .45), b.p(.69, .94)], fill=c, width=b.w(.11))


def _ball(d, b, c):
    w = b.w(.07)
    d.ellipse(b.r(.08, .08, .92, .92), outline=c, width=w)
    d.line([b.p(.5, .08), b.p(.5, .92)], fill=c, width=w)
    d.line([b.p(.08, .5), b.p(.92, .5)], fill=c, width=w)
    d.arc(b.r(-.25, .2, .32, .8), -60, 60, fill=c, width=w)
    d.arc(b.r(.68, .2, 1.25, .8), 120, 240, fill=c, width=w)


def _star(d, b, c):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        r = .48 if i % 2 == 0 else .2
        pts.append(b.p(.5 + r * math.cos(a), .53 + r * math.sin(a)))
    d.polygon(pts, fill=c, outline=BLACK if c in (YELLOW, GREEN) else c)


def _pikachu(d, b, c):
    ol = b.w(.035)
    # ears (yellow with black tips), drawn first so the head covers their base
    for sign in (-1, 1):
        base_in, base_out = .5 + sign * .1, .5 + sign * .3
        tip = (.5 + sign * .46, .0)
        d.polygon([b.p(base_in, .36), b.p(*tip), b.p(base_out, .42)], fill=YELLOW,
                  outline=BLACK)
        mid_in = (base_in + (tip[0] - base_in) * .6, .36 * .4)
        mid_out = (base_out + (tip[0] - base_out) * .6, .42 * .4)
        d.polygon([b.p(*mid_in), b.p(*tip), b.p(*mid_out)], fill=BLACK)
    d.ellipse(b.r(.1, .28, .9, .98), fill=YELLOW, outline=BLACK, width=ol)
    # eyes with highlight
    for u in (.34, .66):
        d.ellipse(b.r(u - .07, .5, u + .07, .64), fill=BLACK)
        d.ellipse(b.r(u - .04, .515, u, .555), fill=WHITE)
    # cheeks
    for u in (.2, .8):
        d.ellipse(b.r(u - .08, .68, u + .08, .82), fill=RED)
    # nose and mouth
    d.ellipse(b.r(.485, .66, .515, .68), fill=BLACK)
    d.arc(b.r(.38, .66, .5, .78), 20, 160, fill=BLACK, width=ol)
    d.arc(b.r(.5, .66, .62, .78), 20, 160, fill=BLACK, width=ol)


def _princesa(d, b, c):
    ol = b.w(.035)
    hair = YELLOW
    # hair behind the face
    d.ellipse(b.r(.1, .2, .9, .98), fill=hair, outline=BLACK, width=ol)
    d.rectangle(b.r(.1, .58, .9, .98), fill=hair)
    d.line([b.p(.1, .58), b.p(.1, .98)], fill=BLACK, width=ol)
    d.line([b.p(.9, .58), b.p(.9, .98)], fill=BLACK, width=ol)
    # face
    d.ellipse(b.r(.22, .34, .78, .92), fill=WHITE, outline=BLACK, width=ol)
    # fringe
    d.chord(b.r(.2, .26, .8, .62), 180, 360, fill=hair, outline=BLACK, width=ol)
    # crown
    d.polygon([b.p(.26, .3), b.p(.26, .08), b.p(.38, .2), b.p(.5, .02), b.p(.62, .2),
               b.p(.74, .08), b.p(.74, .3)], fill=YELLOW, outline=BLACK, width=ol)
    d.ellipse(b.r(.46, .17, .54, .25), fill=RED)
    # eyes, cheeks, smile
    for u in (.39, .61):
        d.ellipse(b.r(u - .045, .56, u + .045, .66), fill=BLACK)
    for u in (.3, .7):
        d.ellipse(b.r(u - .05, .69, u + .05, .76), fill=RED)
    d.arc(b.r(.41, .64, .59, .8), 20, 160, fill=BLACK, width=ol)


def _chupete(d, b, c):
    """Front view: butterfly-shaped shield with air holes, teat button and ring handle."""
    ol = b.w(.04)
    # shield: two lobes joined in the middle
    for u0, u1 in ((.02, .56), (.44, .98)):
        d.ellipse(b.r(u0, .2, u1, .74), fill=c, outline=BLACK, width=ol)
    d.rectangle(b.r(.3, .28, .7, .66), fill=c)
    d.arc(b.r(.02, .2, .56, .74), 300, 340, fill=BLACK, width=ol)
    d.arc(b.r(.44, .2, .98, .74), 200, 240, fill=BLACK, width=ol)
    d.arc(b.r(.02, .2, .56, .74), 20, 60, fill=BLACK, width=ol)
    d.arc(b.r(.44, .2, .98, .74), 120, 160, fill=BLACK, width=ol)
    # air holes
    for u in (.18, .82):
        d.ellipse(b.r(u - .06, .41, u + .06, .53), fill=WHITE, outline=BLACK, width=ol)
    # ring handle hanging from the button
    d.ellipse(b.r(.3, .46, .7, .98), outline=BLACK, width=b.w(.13))
    d.ellipse(b.r(.32, .48, .68, .96), outline=YELLOW, width=b.w(.07))
    # button in the centre
    d.ellipse(b.r(.36, .3, .64, .58), fill=WHITE, outline=BLACK, width=ol)
    d.ellipse(b.r(.44, .38, .56, .5), fill=c)


def _top(d, b, c, ol):
    """Long-sleeved top outline shared by the clothes icons."""
    d.polygon([b.p(.32, .06), b.p(.68, .06), b.p(.96, .26), b.p(.96, .6), b.p(.8, .6),
               b.p(.8, .96), b.p(.2, .96), b.p(.2, .6), b.p(.04, .6), b.p(.04, .26)],
              fill=c, outline=BLACK, width=ol)
    d.line([b.p(.2, .6), b.p(.2, .36)], fill=BLACK, width=ol)
    d.line([b.p(.8, .6), b.p(.8, .36)], fill=BLACK, width=ol)


def _uniforme(d, b, c):
    """Shirt with collar and tie."""
    ol = b.w(.05)
    _top(d, b, c, ol)
    d.polygon([b.p(.32, .06), b.p(.5, .24), b.p(.36, .34)], fill=WHITE, outline=BLACK, width=ol)
    d.polygon([b.p(.68, .06), b.p(.5, .24), b.p(.64, .34)], fill=WHITE, outline=BLACK, width=ol)
    tie = BLUE if c != BLUE else RED
    d.polygon([b.p(.5, .24), b.p(.58, .34), b.p(.54, .78), b.p(.5, .86), b.p(.46, .78),
               b.p(.42, .34)], fill=tie, outline=BLACK)


def _chandal(d, b, c):
    """Tracksuit jacket: two white stripes down sleeves and sides, zip and high collar."""
    ol = b.w(.05)
    _top(d, b, c, ol)
    stripe = BLUE if c == YELLOW else WHITE
    for u in (.09, .15, .85, .91):
        d.line([b.p(u, .3), b.p(u, .58)], fill=stripe, width=b.w(.04))
    for u in (.26, .32, .68, .74):
        d.line([b.p(u, .4), b.p(u, .94)], fill=stripe, width=b.w(.04))
    d.rectangle(b.r(.34, .02, .66, .14), fill=c, outline=BLACK, width=ol)
    d.line([b.p(.5, .04), b.p(.5, .96)], fill=BLACK, width=ol)
    d.rectangle(b.r(.44, .16, .56, .3), fill=WHITE, outline=BLACK)


def _warning(d, b, c):
    d.polygon([b.p(.5, .04), b.p(.97, .92), b.p(.03, .92)], fill=YELLOW, outline=BLACK,
              width=b.w(.06))
    d.rounded_rectangle(b.r(.44, .3, .56, .66), radius=b.w(.04), fill=BLACK)
    d.ellipse(b.r(.43, .72, .57, .85), fill=BLACK)


def battery_segments(level: int) -> tuple[int, tuple]:
    """(squares, colour): >= 90 % 4 green, >= 40 % 3 yellow (no orange ink), >= 20 % 2 red,
    >= 5 % 1 red, below that empty."""
    for limit, n, color in ((90, 4, GREEN), (40, 3, YELLOW), (20, 2, RED), (5, 1, RED)):
        if level >= limit:
            return n, color
    return 0, RED


def battery(img: Image.Image, x: int, y: int, level: int | None, usb: bool) -> None:
    """48x14 battery: outline with up to 4 square 8 px segments (battery_segments) and a
    lightning bolt when on USB. level None = unknown."""
    d = ImageDraw.Draw(img)
    seg, gap = 8, 2
    bx1, by1 = x + 3 + 4 * seg + 3 * gap + 2, y + 3 + seg + 2  # 2 px outline, 1 px margin
    d.rounded_rectangle([x, y, bx1, by1], radius=3, fill=WHITE, outline=BLACK, width=2)
    d.rectangle([bx1 + 1, y + 4, bx1 + 4, by1 - 4], fill=BLACK)
    if level is not None:
        n, color = battery_segments(level)
        for i in range(n):
            sx = x + 3 + i * (seg + gap)
            d.rectangle([sx, y + 3, sx + seg - 1, y + 3 + seg - 1], fill=color)
    cx, cy = (x + bx1) / 2, (y + by1) / 2
    if usb:
        k = (by1 - y) / 15
        bolt = [(cx + 2 * k, cy - 7 * k), (cx - 5 * k, cy + 1 * k), (cx - 0 * k, cy + 1 * k),
                (cx - 2 * k, cy + 7 * k), (cx + 5 * k, cy - 1 * k), (cx + 0 * k, cy - 1 * k)]
        d.polygon([(round(px), round(py)) for px, py in bolt], fill=YELLOW, outline=BLACK)
    elif level is None:
        d.text((cx, cy), "?", fill=BLACK, anchor="mm")


ICONS = {
    "calendar": _calendar, "calendar_blank": lambda d, b, c: _calendar_blank(d, b, c, .04), "sun": lambda d, b, c: _sun(d, b, YELLOW), "partly": _partly,
    "cloud": _cloud, "rain": _rain, "snow": _snow, "storm": _storm, "drop": _drop,
    "person": _person, "cutlery": _cutlery, "ball": _ball, "star": _star,
    "pikachu": _pikachu, "princesa": _princesa, "chupete": _chupete, "warning": _warning,
    "umbrella": _umbrella,
    "uniforme": _uniforme, "chandal": _chandal,
}


def draw(img: Image.Image, name: str, x: int, y: int, size: int, color=BLACK) -> None:
    path = os.path.join(ASSETS_DIR, f"{name}.png")
    if os.path.exists(path):
        icon = Image.open(path).convert("RGBA").resize((size, size), Image.Resampling.NEAREST)
        img.paste(icon, (x, y), icon)
        return
    fn = ICONS.get(name)
    if fn:
        fn(ImageDraw.Draw(img), _Box(x, y, size), color)
