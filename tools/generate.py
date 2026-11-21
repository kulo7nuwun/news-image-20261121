#!/usr/bin/env python3
"""Draw the front page of 'THE WORLD IN ONE DAY' for Saturday 21 November 2026.

A newspaper front page summing up the day's world news, drawn entirely with
Pillow: typography and simple geometric panels only, no photographs, no
invented quotes. Output: entry.png, 1024 x 1024.
"""

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
INK = (18, 18, 18)
PAPER = (250, 246, 238)
GREY = (96, 94, 88)
RED = (178, 34, 34)
DARK_BLUE = (28, 52, 96)
TEAL = (18, 110, 110)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_width, fill=INK, leading=None):
    """Draw wrapped text, return the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_font(draw, text, path, size, max_width):
    """Largest font size up to `size` at which text fits max_width."""
    while size > 12:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= max_width:
            return fnt
        size -= 2
    return font(path, size)


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_lead_panel(draw, x, y, w, h):
    """Stylised night-sky panel: red missile arcs over a dark landmass."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 30, 46))
    # stars
    for sx, sy, r in [(x + 30, y + 22, 2), (x + 90, y + 60, 1), (x + 150, y + 18, 2),
                      (x + 210, y + 48, 1), (x + 260, y + 26, 2), (x + 60, y + 90, 1)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(240, 240, 220))
    # landmass silhouette
    draw.polygon([(x, y + h), (x, y + h - 26), (x + 60, y + h - 44),
                  (x + 130, y + h - 30), (x + 200, y + h - 52),
                  (x + w, y + h - 34), (x + w, y + h)],
                 fill=(52, 66, 92))
    # missile arcs (kept inside the panel)
    for i, (cx, cy, rad) in enumerate([(x + 70, y + h - 14, 70),
                                       (x + 150, y + h - 12, 90),
                                       (x + 230, y + h - 14, 80)]):
        draw.arc([cx - rad, cy - rad, cx + rad, cy + rad],
                 start=200, end=330, fill=(232, 90, 70), width=4)
        draw.ellipse([cx - 4, cy - rad - 4, cx + 4, cy - rad + 4],
                     fill=(255, 210, 90))
    # impact marker
    draw.ellipse([x + w - 52, y + h - 62, x + w - 28, y + h - 38],
                 outline=(255, 210, 90), width=3)
    draw.text((x + 12, y + h - 26), "POLAND  •  21 NOV 2026",
              font=font(SANS_BOLD, 13), fill=(240, 240, 220))


def draw_chart_panel(draw, x, y, w, h, colour):
    """Falling market chart: axes plus a descending line with a red arrow."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                   outline=GREY, width=1)
    draw.line([(x + 14, y + h - 18), (x + w - 10, y + h - 18)],
              fill=GREY, width=1)
    draw.line([(x + 14, y + 12), (x + 14, y + h - 18)], fill=GREY, width=1)
    pts = [(x + 18, y + 22), (x + 55, y + 30), (x + 92, y + 28),
           (x + 129, y + 48), (x + 166, y + 44), (x + 203, y + 70),
           (x + 240, y + 66), (x + w - 16, y + h - 30)]
    draw.line(pts, fill=colour, width=4, joint="curve")
    draw.text((x + w - 72, y + 8), "-3.7%", font=font(SANS_BOLD, 20),
              fill=colour)


def draw_storm_panel(draw, x, y, w, h):
    """Cyclone spiral over a coastline, drawn with concentric arcs."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 230, 238),
                   outline=GREY, width=1)
    cx, cy = x + w // 2, y + h // 2
    for r in range(8, 40, 10):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
                 fill=TEAL, width=5)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=TEAL)
    # rain strokes in the top corners
    for rx in range(x + 14, x + 90, 24):
        draw.line([(rx, y + 10), (rx - 5, y + 22)], fill=(90, 130, 150),
                  width=2)
    for rx in range(x + w - 80, x + w - 8, 24):
        draw.line([(rx, y + 10), (rx - 5, y + 22)], fill=(90, 130, 150),
                  width=2)
    # coastline
    draw.line([(x, y + h - 20), (x + w, y + h - 34)], fill=(60, 70, 60),
              width=3)
    draw.text((x + 12, y + h - 18), "ODISHA COAST",
              font=font(SANS_BOLD, 13), fill=(40, 60, 70))


def draw_chip_panel(draw, x, y, w, h):
    """Server racks behind a red ban bar: overseas data-centre story."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 236, 228),
                   outline=GREY, width=1)
    for i in range(3):
        rx = x + 24 + i * 78
        draw.rectangle([rx, y + 14, rx + 54, y + h - 42], fill=(255, 255, 255),
                       outline=GREY, width=1)
        for j in range(2):
            ry = y + 20 + j * 12
            draw.rectangle([rx + 8, ry, rx + 46, ry + 8], fill=(180, 190, 200))
            draw.ellipse([rx + 40, ry + 1, rx + 44, ry + 7], fill=(40, 160, 90))
    # ban bar
    draw.rectangle([x + 8, y + h - 32, x + w - 8, y + h - 10], fill=RED)
    draw.text((x + 16, y + h - 29), "BAN THREATENED",
              font=font(SANS_BOLD, 14), fill=(255, 255, 255))


def draw_nvidia_panel(draw, x, y, w, h):
    """A green chip mark falling, with a magnifier: SEC probe story."""
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                   outline=GREY, width=1)
    cx, cy = x + w // 2 - 30, y + h // 2
    # chip eye
    draw.ellipse([cx - 34, cy - 22, cx + 34, cy + 22], outline=(30, 120, 60),
                 width=5)
    draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(30, 120, 60))
    # falling arrow
    draw.line([(x + w - 70, y + 22), (x + w - 30, y + h - 34)], fill=RED,
              width=5)
    draw.polygon([(x + w - 30, y + h - 34), (x + w - 48, y + h - 40),
                  (x + w - 34, y + h - 18)], fill=RED)
    # magnifier
    draw.ellipse([x + 18, y + h - 52, x + 52, y + h - 18],
                 outline=DARK_BLUE, width=4)
    draw.line([(x + 48, y + h - 22), (x + 66, y + h - 6)], fill=DARK_BLUE,
              width=4)
    draw.text((x + 14, y + 12), "52-WEEK LOW", font=font(SANS_BOLD, 15),
              fill=RED)


def story(draw, x, y, col_w, kicker, kicker_colour, headline, body, panel_fn,
          panel_y):
    """One two-column story block; its panel sits at the fixed row panel_y."""
    draw.text((x, y), kicker, font=font(SANS_BOLD, 15), fill=kicker_colour)
    y += 22
    y = draw_wrapped(draw, headline, font(SERIF_BOLD, 28), x, y, col_w,
                     leading=33)
    y += 6
    y = draw_wrapped(draw, body, font(SERIF, 19), x, y, col_w, leading=23)
    panel_fn(draw, x, panel_y, col_w, 84)
    return panel_y + 84


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN
    col_w = (x1 - x0 - 24) // 2
    cx = x0 + col_w + 24

    # ---------- masthead ----------
    draw.text((x0, 18), "THE WORLD IN ONE DAY",
              font=font(SERIF_BOLD, 62), fill=INK)
    rule(draw, x0, x1, 96, 3)
    rule(draw, x0, x1, 102, 1)
    draw.text((x0, 112), "Saturday, 21 November 2026",
              font=font(SERIF_BOLD, 24), fill=INK)
    draw.text((x1 - draw.textlength("ONE DAY  •  ONE PAGE  •  THE WHOLE WORLD",
                                    font=font(SANS_BOLD, 15)), 118),
              "ONE DAY  •  ONE PAGE  •  THE WHOLE WORLD",
              font=font(SANS_BOLD, 15), fill=GREY)
    rule(draw, x0, x1, 146, 2)

    # ---------- lead story ----------
    y = 156
    draw.text((x0, y), "LEAD STORY", font=font(SANS_BOLD, 16), fill=RED)
    y += 26
    y = draw_wrapped(draw, "RUSSIAN MISSILES HIT POLAND",
                     font(SERIF_BOLD, 44), x0, y, 560, leading=52)
    y += 6
    draw_wrapped(
        draw,
        "Poland calls it a deliberate provocation. NATO calls it a grave "
        "violation of its airspace.",
        font(SERIF, 21), x0, y, 560, leading=26)
    draw_lead_panel(draw, x0 + 590, 182, 362, 146)
    rule(draw, x0, x1, 350, 1)

    # ---------- second row: markets + cyclone ----------
    y = 364
    left_end = story(
        draw, x0, y, col_w, "MARKETS", RED, "Wall Street slump",
        "The S&P 500 and the Dow enter correction territory as AI stocks "
        "plunge, falling about 3.7%.",
        lambda d, px, py, pw, ph: draw_chart_panel(d, px, py, pw, ph, RED),
        500)
    right_end = story(
        draw, cx, y, col_w, "WEATHER", TEAL, "Cyclone Akvan hits India",
        "The cyclone crosses the Odisha coast with strong winds and heavy "
        "rain, forcing mass evacuations.",
        draw_storm_panel, 500)
    rule(draw, x0, x1, 596, 1)

    # ---------- third row: Trump AI ban + Nvidia ----------
    y = 610
    left_end = story(
        draw, x0, y, col_w, "TECH POLICY", RED,
        "Trump threatens overseas AI ban",
        "The US president threatens to ban American firms from building AI "
        "data centres overseas.",
        draw_chip_panel, 756)
    right_end = story(
        draw, cx, y, col_w, "TECH", RED, "Nvidia sinks to 52-week low",
        "Shares fall to a 52-week low after a report that the SEC is "
        "probing the chipmaker's accounting.",
        draw_nvidia_panel, 756)
    rule(draw, x0, x1, 852, 2)

    # ---------- the week in brief ----------
    y = 866
    draw.text((x0, y), "THE WEEK IN BRIEF", font=font(SANS_BOLD, 17),
              fill=DARK_BLUE)
    y += 26
    briefs = [
        "ICJ rules Myanmar committed genocide against the Rohingya.",
        "UK and EU sign deals on food trade, carbon markets and youth mobility.",
        "Trump\u2013Xi\u2013Putin trilateral summit in Shenzhen ends with few concrete results.",
        "EU adopts \u20ac1bn in military aid for Ukraine.",
        "UK pledges 1,000+ drones for Ukraine.",
    ]
    for item in briefs:
        draw.text((x0, y), "\u25aa", font=font(SANS_BOLD, 15), fill=DARK_BLUE)
        y = draw_wrapped(draw, item, font(SERIF, 17), x0 + 22, y, x1 - x0 - 22,
                         leading=20)
        y += 1
    rule(draw, x0, x1, 998, 1)
    draw.text((x0, 1005), "Drawn illustration \u2014 no photographs. Sources: wire reports, 21 November 2026.",
              font=font(SANS, 11), fill=GREY)

    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, "PNG")
    print(f"saved {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
