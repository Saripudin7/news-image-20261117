#!/usr/bin/env python3
"""Render the 17 November 2026 world-news infographic (1024x1024 PNG).

All artwork is drawn with PIL primitives: no photos, no external assets.
Run:  python3 draw_news.py   -> writes entry.png next to this script.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024

# Palette: newsprint paper, dark navy masthead, strong accent per story.
PAPER = (244, 241, 234)
NAVY = (16, 34, 64)
NAVY_LIGHT = (28, 52, 92)
INK = (24, 28, 36)
MUTED = (92, 96, 104)
WHITE = (255, 255, 255)
GOLD = (214, 164, 32)
FOOTER_BG = (226, 222, 212)

ACCENTS = {
    "red": (178, 34, 34),
    "orange": (204, 102, 0),
    "blue": (24, 90, 160),
    "teal": (0, 128, 128),
    "purple": (104, 64, 152),
    "green": (34, 128, 64),
}


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 74)
F_SUB = font("DejaVuSans-Bold.ttf", 30)
F_TAG = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 28)
F_BODY = font("DejaVuSans.ttf", 22)
F_FOOT = font("DejaVuSans.ttf", 18)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_explosion(d, cx, cy, r, color):
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)
    d.ellipse([cx - r * 0.28, cy - r * 0.28, cx + r * 0.28, cy + r * 0.28],
              fill=(255, 236, 160))


def draw_bridge(d, cx, cy, r, color):
    # Deck, arch and hangers of a suspension bridge.
    d.line([cx - r, cy + r * 0.35, cx + r, cy + r * 0.35], fill=color, width=7)
    d.arc([cx - r, cy - r * 0.9, cx + r, cy + r * 0.9], 180, 360, fill=color, width=6)
    for fx in (-0.6, -0.3, 0.0, 0.3, 0.6):
        x = cx + fx * r
        top = cy - math.sqrt(max(0.0, r * r - (fx * r) ** 2)) * 0.9
        d.line([x, top, x, cy + r * 0.35], fill=color, width=3)
    # A broken gap in the deck, right of centre.
    d.line([cx + r * 0.35, cy + r * 0.35, cx + r * 0.62, cy + r * 0.75],
           fill=(178, 34, 34), width=6)


def draw_chip(d, cx, cy, r, color):
    s = r * 1.15
    for i in range(3):
        off = -r * 0.55 + i * r * 0.55
        d.line([cx + off, cy - s - 12, cx + off, cy - s], fill=color, width=5)
        d.line([cx + off, cy + s, cx + off, cy + s + 12], fill=color, width=5)
        d.line([cx - s - 12, cy + off, cx - s, cy + off], fill=color, width=5)
        d.line([cx + s, cy + off, cx + s + 12, cy + off], fill=color, width=5)
    d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], radius=10,
                        fill=color)
    d.rounded_rectangle([cx - s * 0.45, cy - s * 0.45, cx + s * 0.45,
                         cy + s * 0.45], radius=6, fill=(255, 255, 255))
    d.text((cx, cy), "$", font=F_TAG, fill=color, anchor="mm")


def draw_globe(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=6)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=color, width=4)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=4)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360,
          fill=color, width=4)
    d.ellipse([cx - r * 0.28, cy - r * 0.3, cx + r * 0.1, cy + r * 0.08],
              fill=color)


def draw_megaphone(d, cx, cy, r, color):
    d.polygon([(cx - r * 0.9, cy - r * 0.35), (cx + r * 0.1, cy - r * 0.75),
               (cx + r * 0.1, cy + r * 0.75), (cx - r * 0.9, cy + r * 0.35)],
              fill=color)
    d.rectangle([cx - r * 1.05, cy - r * 0.35, cx - r * 0.85, cy + r * 0.35],
                fill=color)
    for k, rr in enumerate((0.45, 0.7, 0.95)):
        d.arc([cx + r * 0.1, cy - r * rr, cx + r * (0.1 + 2 * rr),
               cy + r * rr], -55, 55, fill=color, width=5)


def draw_virus(d, cx, cy, r, color):
    for i in range(8):
        ang = math.pi * i / 4
        x1 = cx + r * 0.75 * math.cos(ang)
        y1 = cy + r * 0.75 * math.sin(ang)
        x2 = cx + r * 1.05 * math.cos(ang)
        y2 = cy + r * 1.05 * math.sin(ang)
        d.line([x1, y1, x2, y2], fill=color, width=6)
        d.ellipse([x2 - 6, y2 - 6, x2 + 6, y2 + 6], fill=color)
    d.ellipse([cx - r * 0.75, cy - r * 0.75, cx + r * 0.75, cy + r * 0.75],
              fill=color)
    d.ellipse([cx - r * 0.35, cy - r * 0.4, cx - r * 0.05, cy - r * 0.1],
              fill=(255, 255, 255))
    d.ellipse([cx + r * 0.1, cy + r * 0.15, cx + r * 0.4, cy + r * 0.45],
              fill=(255, 255, 255))


ICONS = {
    "explosion": draw_explosion,
    "bridge": draw_bridge,
    "chip": draw_chip,
    "globe": draw_globe,
    "megaphone": draw_megaphone,
    "virus": draw_virus,
}

# (tag, accent, icon, headline, body)
STORIES = [
    ("CONFLICT", "red", "explosion",
     "US and Iran trade fire",
     "US jets hit an Iranian missile site on Qeshm Island after Iran fired "
     "drones at a US radar base in Bahrain."),
    ("WAR IN UKRAINE", "orange", "bridge",
     "Kerch Bridge hit again",
     "Ukrainian drones struck the Crimea bridge a second day; a road "
     "section fell into the strait."),
    ("TECH", "blue", "chip",
     "Nvidia: record $115bn quarter",
     "Record revenue, about double a year earlier \u2014 but ousted CEO "
     "Jensen Huang will not return."),
    ("SUMMIT", "teal", "globe",
     "Trump heads to APEC in Shenzhen",
     "A rare three-way meeting with China's Xi and Russia's Putin is "
     "planned for Thursday."),
    ("FRANCE", "purple", "megaphone",
     "146,000 march in France",
     "Unions strike over living costs; 28,000 protest in Paris alone."),
    ("HEALTH", "green", "virus",
     "US loses measles-free status",
     "After 26 years: 5,400+ cases and 10 deaths in a record outbreak."),
]


def draw_panel(d, x, y, w, h, story):
    tag, accent_key, icon, head, body = story
    accent = ACCENTS[accent_key]
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=WHITE,
                        outline=(210, 206, 196), width=2)
    # Accent bar on top.
    d.rounded_rectangle([x, y, x + w, y + 10], radius=5, fill=accent)
    d.rectangle([x, y + 5, x + w, y + 10], fill=accent)
    # Tag.
    d.text((x + 22, y + 26), tag, font=F_TAG, fill=accent)
    # Icon in a soft circle, top right.
    cx, cy, r = x + w - 52, y + 58, 34
    d.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6],
              fill=(238, 236, 230))
    ICONS[icon](d, cx, cy, 26, accent)
    # Headline, wrapped to leave the icon clear.
    lines = wrap(d, head, F_HEAD, w - 44 - 78)
    ty = y + 56
    for ln in lines:
        d.text((x + 22, ty), ln, font=F_HEAD, fill=INK)
        ty += 36
    # Body text.
    by = ty + 10
    for ln in wrap(d, body, F_BODY, w - 44):
        d.text((x + 22, by), ln, font=F_BODY, fill=MUTED)
        by += 30


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.rectangle([0, 168, W, 174], fill=GOLD)
    d.text((32, 22), "17 NOVEMBER 2026", font=F_TITLE, fill=WHITE)
    d.text((34, 112), "WORLD NEWS IN ONE IMAGE", font=F_SUB, fill=GOLD)
    d.text((W - 34, 118), "TUESDAY", font=F_TAG, fill=(180, 196, 220),
           anchor="ra")

    # Story grid: 2 columns x 3 rows.
    margin, gap = 16, 16
    pw = (W - 2 * margin - gap) // 2
    ph = 240
    gy = 190
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (pw + gap)
        y = gy + row * (ph + gap)
        draw_panel(d, x, y, pw, ph, story)

    # Footer.
    fy = gy + 3 * ph + 2 * gap + 8
    d.rectangle([0, fy, W, H], fill=FOOTER_BG)
    d.text((W // 2, fy + 10),
           "All events reported on 17 November 2026",
           font=F_FOOT, fill=MUTED, anchor="ma")
    d.text((W // 2, fy + 34),
           "Sources: BBC  \u00b7  CBS News  \u00b7  NPR  \u00b7  Al Jazeera",
           font=F_FOOT, fill=MUTED, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
