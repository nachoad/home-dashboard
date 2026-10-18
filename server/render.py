"""Draw the dashboard. Edit this file to change the layout; data is a dict (see fixture()).

    python render.py --fixture [--estilo comic] [out.png]   # sample data

Styles (`data["style"]`): each Theme subclass changes fonts, colours and how cards and
the header are drawn; the layout is shared.
"""

import math
import os
import random
import sys
from datetime import datetime, timedelta

from PIL import Image, ImageChops, ImageDraw, ImageFont

import icons
from epaper import HEIGHT, WIDTH

BLACK, WHITE, YELLOW = icons.BLACK, icons.WHITE, icons.YELLOW
RED, BLUE, GREEN = icons.RED, icons.BLUE, icons.GREEN
GREY = (1, 2, 3)  # not a panel ink: grey() swaps it for a dot pattern

SUPP = "/System/Library/Fonts/Supplemental/"
SYS = "/System/Library/Fonts/"

DAYS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
          "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

# Card colour -> (fill, text on fill, text/accents on white)
COLORS = {
    "amarillo": (YELLOW, BLACK, BLACK),
    "rojo": (RED, WHITE, RED),
    "azul": (BLUE, WHITE, BLUE),
    "verde": (GREEN, WHITE, BLACK),
    "gris": (GREY, BLACK, BLACK),  # placeholder ink, replaced by grey()
}
KID_COLORS = ["amarillo", "rojo", "verde"]

# Vertical layout
HEADER_BOTTOM = 82
TOP_BOTTOM = 222  # shared calendar (left) and "Importante" box (right)
KIDS = (230, 474)
MOTTO_X = 628  # motto area: MOTTO_X..WIDTH - 8
MOTTO_CX = (MOTTO_X + WIDTH - 8) // 2


class Theme:
    """The original look ("clasico"). Subclasses override what they restyle."""

    fonts = {
        "regular": [(SUPP + "Arial.ttf", 0), ("/Library/Fonts/Arial.ttf", 0)],
        "bold": [(SUPP + "Arial Bold.ttf", 0), ("/Library/Fonts/Arial Bold.ttf", 0)],
        "italic": [(SUPP + "Arial Italic.ttf", 0)],
    }
    header_fg = BLACK
    calendar_color = BLUE
    weather_color = BLUE
    max_color, min_color, rain_color = RED, BLUE, BLUE
    motto_color = BLUE
    divider = BLACK
    tomorrow_fill, tomorrow_fg = RED, WHITE

    def __init__(self):
        self._fonts = {}

    def font(self, size: int, style: str = "regular") -> ImageFont.FreeTypeFont:
        key = (size, style)
        if key not in self._fonts:
            for path, index in self.fonts.get(style, []) + self.fonts["regular"]:
                if os.path.exists(path):
                    self._fonts[key] = ImageFont.truetype(path, size, index=index)
                    break
            else:
                self._fonts[key] = ImageFont.load_default(size)
        return self._fonts[key]

    def background(self, img, d):
        pass

    def header_background(self, img, d):
        pass

    border = 2  # card outline width; grey() keeps the title dots inside it

    def card(self, img, d, box, color, header_h):
        """Draw the card frame; return the colour for text in the header strip."""
        fill, on_fill, _ = COLORS[color]
        x0, y0, x1, y1 = box
        d.rounded_rectangle(box, radius=10, fill=WHITE, outline=fill, width=self.border)
        d.rounded_rectangle([x0, y0, x1, y0 + header_h], radius=10, fill=fill)
        d.rectangle([x0, y0 + header_h - 10, x1, y0 + header_h], fill=fill)
        if fill == YELLOW or fill == GREEN:  # light inks need a dark edge to read as a card
            d.rounded_rectangle(box, radius=10, outline=BLACK, width=1)
        return on_fill

    def kid_name(self, img, d, box, name, title_color):
        x0, y0, x1, _ = box
        f = self.font(30, "bold")
        d.text((x0 + 58, y0 + 7), fit(d, name, f, x1 - x0 - 66), font=f, fill=title_color)

    def motto(self, img, d, text):
        f = self.font(17, "italic")
        for i, line in enumerate(wrap(d, text, f, WIDTH - 8 - MOTTO_X, 3)):
            d.text((MOTTO_X, 3 + i * 18), line, font=f, fill=self.motto_color)


class Comic(Theme):
    """Comic book: yellow halftone dots, thick outlines, hard shadows, speech bubbles."""

    border = 3
    fonts = {
        "regular": [(SUPP + "Comic Sans MS.ttf", 0)] + Theme.fonts["regular"],
        "bold": [(SUPP + "Comic Sans MS Bold.ttf", 0)] + Theme.fonts["bold"],
        "italic": [(SUPP + "Comic Sans MS Bold.ttf", 0)],
    }
    motto_color = BLACK
    tomorrow_fill, tomorrow_fg = BLUE, WHITE

    def background(self, img, d):
        for y in range(4, HEIGHT, 12):
            for x in range(4 + (6 if (y // 12) % 2 else 0), WIDTH, 12):
                d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=YELLOW)

    def header_background(self, img, d):
        d.rectangle([6, 4, 660, 76], fill=WHITE)

    def card(self, img, d, box, color, header_h):
        fill, on_fill, _ = COLORS[color]
        x0, y0, x1, y1 = box
        x1, y1 = x1 - 5, y1 - 5
        d.rectangle([x0 + 5, y0 + 5, x1 + 5, y1 + 5], fill=BLACK)
        d.rectangle([x0, y0, x1, y1], fill=WHITE, outline=BLACK, width=self.border)
        d.rectangle([x0, y0, x1, y0 + header_h], fill=fill, outline=BLACK, width=self.border)
        return on_fill

    def kid_name(self, img, d, box, name, title_color):
        x0, y0, x1, _ = box
        f = self.font(22, "bold")
        name = fit(d, name, f, x1 - x0 - 110)
        w = d.textlength(name, font=f)
        bx0, by0 = x0 + 64, y0 + 6
        bx1, by1 = bx0 + w + 24, y0 + 38
        d.polygon([(bx0 + 6, by1 - 8), (x0 + 55, y0 + 30), (bx0 + 14, by1 - 2)],
                  fill=WHITE, outline=BLACK)
        d.rounded_rectangle([bx0, by0, bx1, by1], radius=14, fill=WHITE, outline=BLACK, width=2)
        d.line([(bx0 + 7, by1 - 7), (bx0 + 13, by1 - 3)], fill=WHITE, width=3)
        d.text(((bx0 + bx1) / 2, (by0 + by1) / 2), name, font=f, fill=BLACK, anchor="mm")
        burst(d, x1 - 30, y0 + 23, 17, 13, WHITE if title_color == BLACK else YELLOW)

    def motto(self, img, d, text):
        burst(d, MOTTO_CX, 31, 80, 32, WHITE, spikes=14, outline=3)
        f = self.font(11, "bold")
        lines = wrap(d, text, f, 100, 3)
        top = 31 - (len(lines) - 1) * 6.5
        for i, line in enumerate(lines):
            d.text((MOTTO_CX, top + i * 13), line, font=f, fill=RED, anchor="mm")


class Pizarra(Theme):
    """Blackboard header with chalk, paper notes with tape and hand-drawn edges."""

    fonts = {
        "regular": [(SUPP + "ChalkboardSE.ttc", 1)] + Theme.fonts["regular"],
        "bold": [(SUPP + "ChalkboardSE.ttc", 2)] + Theme.fonts["bold"],
        "italic": [(SUPP + "ChalkboardSE.ttc", 1)],
    }
    header_fg = WHITE
    calendar_color = YELLOW
    weather_color = YELLOW
    max_color, min_color, rain_color = YELLOW, GREEN, GREEN
    motto_color = YELLOW
    divider = WHITE
    tomorrow_fill, tomorrow_fg = YELLOW, BLACK

    def header_background(self, img, d):
        d.rectangle([0, 0, WIDTH, 78], fill=BLACK)
        d.rectangle([0, 76, WIDTH, 79], fill=YELLOW)  # chalk tray
        rnd = random.Random(7)
        for _ in range(60):  # chalk dust
            d.point((rnd.randrange(WIDTH), rnd.randrange(74)), fill=WHITE)

    def card(self, img, d, box, color, header_h):
        fill, _, accent = COLORS[color]
        x0, y0, x1, y1 = box
        d.rectangle(box, fill=WHITE)
        sketch(d, box, BLACK, seed=x0 + y0)
        cx = (x0 + x1) // 2  # tape strip across the top edge
        d.polygon([(cx - 34, y0 - 5), (cx + 30, y0 - 9), (cx + 34, y0 + 7), (cx - 30, y0 + 11)],
                  fill=fill, outline=BLACK)
        rnd = random.Random(x0)  # hand-drawn underline below the title
        pts = [(x, y0 + header_h - 3 + rnd.choice((-1, 0, 1))) for x in range(x0 + 10, x1 - 8, 12)]
        d.line(pts, fill=BLACK if fill == YELLOW else fill, width=3)
        return accent


class Arcoiris(Theme):
    """Rainbow: big rounded bubbles, polka-dot headers, sticker names, rainbow arc."""

    border = 4
    fonts = {
        "regular": [(SUPP + "Trebuchet MS.ttf", 0)] + Theme.fonts["regular"],
        "bold": [(SUPP + "Arial Rounded Bold.ttf", 0)] + Theme.fonts["bold"],
        "italic": [(SUPP + "Trebuchet MS Italic.ttf", 0)],
    }
    tomorrow_fill, tomorrow_fg = GREEN, BLACK

    def card(self, img, d, box, color, header_h):
        fill, on_fill, _ = COLORS[color]
        x0, y0, x1, y1 = box
        d.rounded_rectangle(box, radius=18, fill=WHITE, outline=fill, width=self.border)
        d.rounded_rectangle([x0, y0, x1, y0 + header_h], radius=18, fill=fill)
        d.rectangle([x0, y0 + header_h - 18, x1, y0 + header_h], fill=fill)
        dot = RED if fill == YELLOW else WHITE
        for i, x in enumerate(range(x0 + 170, x1 - 12, 16)):
            y = y0 + 10 + (i % 2) * 14
            if y < y0 + header_h - 6:
                d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=dot)
        if fill in (YELLOW, GREEN):
            d.rounded_rectangle(box, radius=18, outline=BLACK, width=1)
        return on_fill

    def kid_name(self, img, d, box, name, title_color):
        x0, y0, x1, _ = box
        f = self.font(22, "bold")
        name = fit(d, name, f, x1 - x0 - 110)
        w = d.textlength(name, font=f)
        sx0, sy0 = x0 + 56, y0 + 9
        d.rounded_rectangle([sx0, sy0, sx0 + w + 22, sy0 + 30], radius=15, fill=WHITE,
                            outline=BLACK, width=2)
        d.text((sx0 + 11 + w / 2, sy0 + 15), name, font=f, fill=BLACK, anchor="mm")

    def motto(self, img, d, text):
        cx, cy = MOTTO_CX, 28
        for r, c in zip((26, 22, 18, 14), (RED, YELLOW, GREEN, BLUE)):
            d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=c, width=4)
        for dx in (-20, 20):  # little clouds at the ends
            d.ellipse([cx + dx - 9, cy - 6, cx + dx + 9, cy + 5], fill=WHITE, outline=BLUE, width=2)
        f = self.font(12, "italic")
        for i, line in enumerate(wrap(d, text, f, WIDTH - 8 - MOTTO_X, 2)):
            d.text((cx, cy + 5 + i * 12), line, font=f, fill=BLUE, anchor="mt")


THEMES = {"clasico": Theme, "comic": Comic, "pizarra": Pizarra, "arcoiris": Arcoiris}
T = Theme()  # theme being drawn; set by render()


def font(size: int, style: str = "regular") -> ImageFont.FreeTypeFont:
    return T.font(size, style)


def burst(d, cx, cy, rx, ry, fill, spikes=10, outline=2):
    pts = []
    for i in range(spikes * 2):
        a = i * math.pi / spikes
        k = 1.0 if i % 2 == 0 else 0.72
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    d.polygon(pts, fill=fill, outline=BLACK, width=outline)


def sketch(d, box, color, seed=0):
    """Slightly wobbly double outline, like a felt-tip drawing."""
    x0, y0, x1, y1 = box
    rnd = random.Random(seed)
    for _ in range(2):
        def j():
            return rnd.choice((-1, 0, 1))
        pts = [(x0 + j(), y0 + j()), (x1 + j(), y0 + j()), (x1 + j(), y1 + j()),
               (x0 + j(), y1 + j()), (x0 + j(), y0 + j())]
        d.line(pts, fill=color, width=2, joint="curve")


def grey(img, box, header_h):
    """Turn the GREY placeholder that T.card() drew into a grey title strip. The panel has no
    grey ink, so it is a grid of black dots on white; GREY outside the strip (borders, tape,
    underlines) becomes black."""
    x0, y0, x1, y1 = box
    region = img.crop(box)
    mask = ImageChops.difference(region, Image.new("RGB", region.size, GREY)).convert("L")
    mask = mask.point(lambda v: 255 if v == 0 else 0)
    fill = Image.new("RGB", region.size, BLACK)
    b = T.border
    dots = Image.new("RGB", (x1 - x0 - 2 * b, header_h - b), WHITE)
    dd = ImageDraw.Draw(dots)
    for y in range(0, dots.height, 2):
        for x in range(y // 2 % 2, dots.width, 2):
            dd.point((x, y), fill=BLACK)
    fill.paste(dots, (b, b))
    region.paste(fill, mask=mask)
    img.paste(region, box[:2])


def fit(d: ImageDraw.ImageDraw, text: str, f, width: int) -> str:
    """Truncate with an ellipsis so the text fits in `width` px."""
    if d.textlength(text, font=f) <= width:
        return text
    while text and d.textlength(text + "…", font=f) > width:
        text = text[:-1]
    return text.rstrip() + "…"


def wrap(d: ImageDraw.ImageDraw, text: str, f, width: int, lines: int) -> list[str]:
    """Word-wrap into at most `lines` lines; the last one is truncated if needed."""
    out, words = [], text.split()
    while words and len(out) < lines:
        line = words.pop(0)
        while words and d.textlength(f"{line} {words[0]}", font=f) <= width:
            line += " " + words.pop(0)
        out.append(line)
    if words and out:
        out[-1] = fit(d, f"{out[-1]} {' '.join(words)}", f, width)
    return [fit(d, line, f, width) for line in out]


def battery_level(device: dict) -> int | None:
    bat = str(device.get("bat", ""))
    return int(bat) if bat.isdigit() else None  # "-1" = no battery connected


def draw_header(img, d, data):
    day, weather = data["day"], data["weather"]
    tomorrow = day != data["now"].date()
    T.header_background(img, d)
    fg = T.header_fg

    # Date
    icons.draw(img, "calendar_blank", 6, 4, 74, T.calendar_color)
    d.text((43, 51), str(day.day), font=font(42, "bold"), fill=T.calendar_color, anchor="mm")
    name = DAYS[day.weekday()].capitalize()
    d.text((84, 6), name, font=font(34, "bold"), fill=fg)
    if tomorrow:
        x = 84 + d.textlength(name, font=font(34, "bold")) + 3
        w = d.textlength("MAÑANA", font=font(12, "bold")) + 6
        d.rounded_rectangle([x, 14, x + w, 38], radius=6, fill=T.tomorrow_fill)
        d.text((x + w / 2, 26), "MAÑANA", font=font(12, "bold"), fill=T.tomorrow_fg, anchor="mm")
    d.text((84, 46), f"{MONTHS[day.month - 1]} de {day.year}", font=font(20), fill=fg)
    d.line([310, 10, 310, 70], fill=T.divider, width=1)

    # Weather
    if weather:
        icons.draw(img, weather["icon"] if not tomorrow else weather["day_icon"], 320, 10, 60,
                   T.weather_color)
        big = weather["temp"] if weather["temp"] is not None else weather["tmax"]
        d.text((388, 2), f"{big}°", font=font(44, "bold"), fill=fg)
        d.text((390, 50), fit(d, weather["desc"], font(18), 110), font=font(18), fill=fg)
        x = 510
        d.line([x - 8, 10, x - 8, 70], fill=T.divider, width=1)
        half = (MOTTO_X - 8 - (x - 8)) / 2  # centred between the two dividers: max left, min right
        for i, (label, temp, color) in enumerate((("Máx", weather["tmax"], T.max_color),
                                                  ("Mín", weather["tmin"], T.min_color))):
            cx = x - 8 + half + (i - .5) * 48
            d.text((cx, 8), f"{temp}°", font=font(28, "bold"), fill=color, anchor="mt")
            d.text((cx, 33), label, font=font(12), fill=fg, anchor="mt")
        if weather["rain"] is not None:
            pct = f"{weather['rain']}%"
            rx = round(x - 8 + half - (22 + d.textlength(pct, font=font(18, "bold"))) / 2)
            icons.draw(img, "drop", rx, 52, 18, T.rain_color)
            d.text((rx + 22, 52), pct, font=font(18, "bold"), fill=T.rain_color)
    else:
        d.text((322, 24), "Sin datos del tiempo", font=font(22), fill=RED)
    d.line([MOTTO_X - 8, 10, MOTTO_X - 8, 70], fill=T.divider, width=1)

    # Motto, time and battery
    T.motto(img, d, data.get("frase", ""))
    d.text((MOTTO_X, 60), f"{data['now']:%H:%M}", font=font(13), fill=fg)
    if data.get("show_battery", True):
        dev = data.get("device", {})
        level, usb = battery_level(dev), dev.get("usb") == "1"
        icons.battery(img, 702, 61, level, usb)
        if level is not None:
            d.text((754, 60), f"{level}%", font=font(13, "bold"), fill=RED if level < 20 else fg)


def rainy(weather) -> bool:
    """Rain likely on the shown day: forecast says rain/storm or probability >= 50 %."""
    if not weather:
        return False
    return weather.get("day_icon") in ("rain", "storm") or (weather.get("rain") or 0) >= 50


def draw_important(img, d, box, messages, umbrella=False):
    x0, y0, x1, y1 = box
    title_color = T.card(img, d, box, "gris", 34)
    grey(img, box, 34)
    icons.draw(img, "warning", x0 + 10, y0 + 5, 24, title_color)
    d.text((x0 + 42, y0 + 4), "Importante", font=font(23, "bold"), fill=title_color)
    if umbrella:  # big umbrella behind the messages when rain is likely
        size = 80
        icons.draw(img, "umbrella", (x0 + x1 - size) // 2, y1 - size - 4, size, RED)
    text_w = x1 - x0 - 50
    if not messages:
        d.text((x0 + 14, y0 + 46), "Sin avisos", font=font(18), fill=BLACK)
        return
    f, row_h, y = font(18), 23, y0 + 39
    max_rows = (y1 - y - 2) // row_h
    for msg in messages:
        lines = wrap(d, msg, f, text_w, max_rows)
        if not lines:
            break
        d.text((x0 + 16, y), "•", font=font(18, "bold"), fill=RED)
        for line in lines:
            d.text((x0 + 34, y), line, font=f, fill=BLACK,  # white halo over the umbrella
                   stroke_width=2 if umbrella else 0, stroke_fill=WHITE)
            y += row_h
        max_rows -= len(lines)


def agenda_when(on, hhmm, day) -> str:
    """'10:00' for the shown day; 'Sáb 10:00' for the following ones; all-day: just 'Sáb'."""
    if on == day and hhmm:
        return hhmm
    return f"{DAYS[on.weekday()][:3].capitalize()} {hhmm}".strip()


def draw_agenda(img, d, box, title, items, day):
    x0, y0, x1, y1 = box
    _, _, accent = COLORS["azul"]
    title_color = T.card(img, d, box, "gris", 34)
    grey(img, box, 34)
    icons.draw(img, "calendar", x0 + 10, y0 + 5, 24, title_color)
    d.text((x0 + 42, y0 + 4), title, font=font(23, "bold"), fill=title_color)
    if items is None:
        d.text((x0 + 14, y0 + 46), "Calendario no disponible", font=font(18), fill=RED)
        return
    if not items:
        d.text((x0 + 14, y0 + 46), "Nada en la agenda", font=font(18), fill=BLACK)
        return
    row_h, top = 23, y0 + 39
    max_rows = (y1 - top - 2) // row_h
    shown = items if len(items) <= max_rows else items[:max_rows - 1]
    whens = [agenda_when(on, hhmm, day) for on, hhmm, _ in shown]
    tx = x0 + max([76] + [24 + int(d.textlength(w, font=font(18, "bold"))) for w in whens])
    for i, ((_, _, text), when) in enumerate(zip(shown, whens)):
        y = top + i * row_h
        d.text((x0 + 14, y), when, font=font(18, "bold"), fill=accent)
        d.text((tx, y), fit(d, text, font(18), x1 - tx - 14), font=font(18), fill=BLACK)
    if len(shown) < len(items):
        d.text((tx, top + len(shown) * row_h), f"+{len(items) - len(shown)} más",
               font=font(18, "italic"), fill=BLACK)


def menu_lines(menu) -> list[str]:
    """First and second course, one per line (no side dish or dessert, to fit the card)."""
    return [p for p in ((menu or {}).get("primero"), (menu or {}).get("segundo")) if p]


def draw_kid(img, d, box, kid, color, menu, day):
    x0, y0, x1, y1 = box
    fill, _, accent = COLORS[color]
    title_color = T.card(img, d, box, color, 48)
    icons.draw(img, kid["icon"] or "star", x0 + 5, y0 + 2, 46, BLUE)
    T.kid_name(img, d, box, kid["name"], title_color)
    if day.weekday() >= 5:  # weekend: big icon and a message instead of school details
        size, cx = 112, (x0 + x1) // 2
        icons.draw(img, kid["icon"] or "star", cx - size // 2, y0 + 56, size, BLUE)
        for j, line in enumerate(("¡Es fin de semana!", "¡A jugar!")):
            d.text((cx, y0 + 56 + size + 12 + j * 28), line, font=font(22, "bold"), fill=accent,
                   anchor="mt")
        return

    clothes = kid.get("clothes")
    sections = [("chandal" if clothes == "Chándal" else "uniforme" if clothes else "star",
                 clothes or "—", ["Piscina" if kid.get("pool") else ""], 1, 22)]
    dishes = menu_lines(menu) or ["Sin cole" if day.weekday() >= 5 else "—"]
    sections.append(("cutlery", "Comida", dishes, 3, 18))
    acts = [f"{t}  {what}".strip() for t, what in kid["activities"]]
    if acts:  # no title: the activity itself is the label
        sections.append(("ball", None, acts, 2, 18))

    width, top = x1 - x0 - 50, y0 + 51
    wrapped = []
    for icon, title, lines, max_lines, size in sections:  # size: font px of the section
        out = []
        for line in lines:
            out += wrap(d, line, font(size), width, max_lines - len(out))
            if len(out) >= max_lines:
                break
        wrapped.append((icon, title, out or [""], size))
    # each section takes only the lines it uses (title size + 3, line size + 2);
    # spare room goes between sections
    used = sum((size + 3 if title else 0) + len(out) * (size + 2)
               for _, title, out, size in wrapped)
    gap = max(2, min(10, (y1 - 8 - top - used) // (len(wrapped) - 1)))
    y = top
    for icon, title, out, size in wrapped:
        body, label = font(size), font(size, "bold")
        icons.draw(img, icon, x0 + 9, y + 2, 26, accent if icon in ("cutlery", "ball") else fill)
        if title:
            d.text((x0 + 42, y), title, font=label, fill=accent)
            y += size + 3
        for j, line in enumerate(out):
            d.text((x0 + 42, y + j * (size + 2)), line, font=body if title else label, fill=BLACK)
        y += len(out) * (size + 2) + gap


def render(data: dict) -> Image.Image:
    """data: see server.collect(); every source may be None/empty when unavailable."""
    global T
    T = THEMES.get(data.get("style", "clasico"), Theme)()
    img = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    d = ImageDraw.Draw(img)
    d.fontmode = "1"  # no antialiasing: grey edges would dither into noise on the panel

    T.background(img, d)
    draw_header(img, d, data)

    umbrella = rainy(data.get("weather"))
    messages = list(data.get("importante") or [])
    if umbrella:
        tomorrow = data["day"] != data["now"].date()
        messages.insert(0, "Mañana llueve!" if tomorrow else "Hoy llueve!")
    draw_important(img, d, [536, HEADER_BOTTOM, 796, TOP_BOTTOM], messages, umbrella)
    draw_agenda(img, d, [8, HEADER_BOTTOM, 528, TOP_BOTTOM],
                data.get("calendar_title") or "Calendario común", data.get("agenda"), data["day"])

    for i, kid in enumerate(data.get("kids", [])[:3]):
        x0 = 8 + i * 264
        color = kid["color"] if kid.get("color") in COLORS else KID_COLORS[i]
        draw_kid(img, d, [x0, KIDS[0], x0 + 256, KIDS[1]], kid, color, data.get("menu"), data["day"])
    return img


def fixture(now: datetime | None = None) -> dict:
    """Sample data for the demo mode and for design work. Dates follow `now`."""
    now = now or datetime(2026, 10, 14, 16, 0)
    day = now.date()
    return {
        "now": now, "day": day, "frase": "Hoy también es un gran día",
        "device": {"bat": "78", "usb": "0"},
        "weather": {"today": True, "code": 61, "desc": "Lluvia ligera", "icon": "rain",
                    "day_icon": "rain", "temp": 12, "tmax": 16, "tmin": 9, "rain": 70},
        "importante": ["Llevar la autorización firmada de la excursión", "Papá cena fuera"],
        "calendar_title": "Calendario común",
        "agenda": [(day, "", "Cumpleaños de la abuela"), (day, "08:30", "Reunión proyecto"),
                   (day, "16:30", "Recoger a niño1"),
                   (day + timedelta(days=1), "", "Excursión al campo"),
                   (day + timedelta(days=1), "19:30", "Cena en casa")],
        "menu": {"primero": "Crema de calabacín", "segundo": "Pollo asado", "guarnicion": "Patatas",
                 "postre": "Fruta de temporada"},
        "kids": [
            {"name": "niño1", "icon": "pikachu", "color": "amarillo",
             "activities": [("16:30", "Inglés"), ("18:00", "Fútbol")],
             "notes": [(day + timedelta(days=3), "Excursión al museo")]},
            {"name": "niño2", "icon": "princesa", "color": "rojo",
             "activities": [("17:30", "Baile moderno")], "notes": []},
            {"name": "niño3", "icon": "chupete", "color": "verde",
             "activities": [], "notes": [(day, "Traer ropa de cambio")]},
        ],
    }


if __name__ == "__main__":
    import epaper

    args = sys.argv[1:]
    style = args[args.index("--estilo") + 1] if "--estilo" in args else "clasico"
    files = [a for i, a in enumerate(args)
             if not a.startswith("--") and (i == 0 or args[i - 1] != "--estilo")]
    out = files[0] if files else "preview.png"
    if "--fixture" in args:
        data = fixture()
        data["style"] = style
        epaper.preview(render(data)).save(out)
        print(f"wrote {out}")
