"""
Hollow Zounds — Chapter 0 Panel Letterer (v3)
==============================================
Data-driven letterer for all 14 panels + end card of Chapter 0.
Generates text-only panels from scratch and letters art panels with
SFX, narration boxes, system UI, and floating monologue.

Usage:
    python letter_panel.py              # Process all panels found on disk
    python letter_panel.py 2            # Process just panel 2
    python letter_panel.py 1 2 5        # Process panels 1, 2, and 5

Panel types:
    "text"  — White background, centered black text (no source art needed)
    "art"   — Loads panels/ch0/panel N.jpg, applies overlays
    "dark"  — Dark void background (for system screens w/o art)
    "black" — Pure black background (for title cards)

Output:  panels/ch0/panel N lettered.png
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import sys
import os

# ═══════════════════════════════════════════════════════════════════════
#  Paths & Constants
# ═══════════════════════════════════════════════════════════════════════

PANELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "panels", "ch0")
FONTS_DIR = r"C:\Windows\Fonts"

# System font paths (replace with recommended fonts when available):
#   Text/Dialogue → Bangers-Regular.ttf (Google Fonts) or AnimeAce2.0.ttf
#   SFX           → Bangers or Impact
#   System UI     → VT323-Regular.ttf or ShareTechMono-Regular.ttf
#   Monologue     → Italic variant of your text font
FONT_TEXT = os.path.join(FONTS_DIR, "arialbd.ttf")
FONT_SFX = os.path.join(FONTS_DIR, "impact.ttf")
FONT_SYSTEM = os.path.join(FONTS_DIR, "consola.ttf")
FONT_ITALIC = os.path.join(FONTS_DIR, "ariali.ttf")
FONT_REGULAR = os.path.join(FONTS_DIR, "arial.ttf")

TARGET_W = 1080
TARGET_H = 1920
TARGET_RATIO = TARGET_W / TARGET_H

# ── Style Guide Colors ────────────────────────────────────────────────
BLACK_TEXT = (26, 26, 26)           # #1A1A1A
PURPLE = (139, 0, 255)             # #8B00FF
COLD_WHITE = (200, 224, 255)       # #C8E0FF
SYSTEM_BG = (13, 13, 26)          # #0D0D1A
VOID_BLACK = (10, 10, 15)         # #0A0A0F


# ═══════════════════════════════════════════════════════════════════════
#  Font Utilities
# ═══════════════════════════════════════════════════════════════════════

_font_cache = {}


def _font(path, size):
    key = (path, size)
    if key not in _font_cache:
        try:
            _font_cache[key] = ImageFont.truetype(path, size)
        except OSError:
            _font_cache[key] = ImageFont.truetype(FONT_TEXT, size)
    return _font_cache[key]


def load_fonts():
    s = TARGET_W
    return {
        "dialogue":       _font(FONT_TEXT, int(s * 0.030)),
        "dialogue_shout": _font(FONT_TEXT, int(s * 0.036)),
        "narration":      _font(FONT_TEXT, int(s * 0.026)),
        "monologue":      _font(FONT_ITALIC, int(s * 0.027)),
        "system":         _font(FONT_SYSTEM, int(s * 0.022)),
        "system_title":   _font(FONT_SYSTEM, int(s * 0.028)),
        "system_error":   _font(FONT_SYSTEM, int(s * 0.024)),
        "forum":          _font(FONT_REGULAR, int(s * 0.022)),
    }


# ═══════════════════════════════════════════════════════════════════════
#  Image Conversion
# ═══════════════════════════════════════════════════════════════════════

def convert_to_vertical(img, top_extend=500):
    """Extend top with blurred dark mirror, crop/resize to 9:16."""
    w, h = img.size
    img = img.convert("RGBA")

    mirror_h = min(top_extend + 100, h // 2)
    mirror_strip = img.crop((0, 0, w, mirror_h))
    mirror_strip = mirror_strip.transpose(Image.FLIP_TOP_BOTTOM)
    mirror_ext = mirror_strip.resize((w, top_extend), Image.LANCZOS)
    mirror_ext = mirror_ext.filter(ImageFilter.GaussianBlur(radius=40))

    dark = Image.new("RGBA", mirror_ext.size, (5, 2, 12, 170))
    mirror_ext = Image.alpha_composite(mirror_ext, dark)

    new_h = h + top_extend
    canvas = Image.new("RGBA", (w, new_h), (5, 2, 12, 255))
    canvas.paste(mirror_ext, (0, 0))
    canvas.paste(img, (0, top_extend))

    seam_margin = 80
    sy0 = max(0, top_extend - seam_margin)
    sy1 = min(new_h, top_extend + seam_margin)
    seam = canvas.crop((0, sy0, w, sy1))
    seam = seam.filter(ImageFilter.GaussianBlur(radius=30))

    sh = sy1 - sy0
    mask = Image.new("L", (w, sh), 0)
    md = ImageDraw.Draw(mask)
    for y in range(sh):
        t = 1.0 - abs(y - sh // 2) / (sh / 2)
        md.line([(0, y), (w, y)], fill=int(255 * t * t))
    canvas.paste(seam, (0, sy0), mask)

    crop_w = int(new_h * TARGET_RATIO)
    if crop_w > w:
        crop_h = int(w / TARGET_RATIO)
        yo = (new_h - crop_h) // 2
        cropped = canvas.crop((0, yo, w, yo + crop_h))
    else:
        xo = (w - crop_w) // 2
        cropped = canvas.crop((xo, 0, xo + crop_w, new_h))

    return cropped.resize((TARGET_W, TARGET_H), Image.LANCZOS)


def normalize_panel(img, top_extend=0):
    if top_extend > 0:
        return convert_to_vertical(img, top_extend)
    return img.convert("RGBA").resize((TARGET_W, TARGET_H), Image.LANCZOS)


# ═══════════════════════════════════════════════════════════════════════
#  Drawing Primitives
# ═══════════════════════════════════════════════════════════════════════

def draw_outlined_text(draw, xy, text, font, fill="white",
                       outline_fill="black", outline_width=4):
    x, y = xy
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx * dx + dy * dy <= outline_width * outline_width:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_fill)
    draw.text(xy, text, font=font, fill=fill)


def _text_size(text, font):
    bb = font.getbbox(text)
    return bb[2] - bb[0], bb[3] - bb[1]


def _text_block_size(lines, font):
    lh = int(font.size * 1.3)
    max_w = max((_text_size(ln, font)[0] for ln in lines), default=0)
    return max_w, lh * len(lines), lh


# ═══════════════════════════════════════════════════════════════════════
#  Text-Only Panel Renderer
# ═══════════════════════════════════════════════════════════════════════

def render_text_panel(config):
    """Generate a text-only panel: white bg, centered black text.

    Lines can be plain strings (scale=1.0) or tuples (text, scale).
    Empty strings create paragraph breaks.
    Optical centering shifts the block slightly below mathematical center
    so it looks visually centered on a tall 9:16 canvas.
    """
    img = Image.new("RGB", (TARGET_W, TARGET_H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    base_size = int(TARGET_W * 0.037)
    line_spacing = 2.0
    para_gap = int(base_size * 3.0)
    optical_offset = int(TARGET_H * 0.04)

    text_block = None
    for elem in config.get("elements", []):
        if elem["type"] == "text_block":
            text_block = elem
            break

    if text_block is None:
        return img.convert("RGBA")

    raw_lines = text_block["lines"]

    render_items = []
    total_h = 0

    for entry in raw_lines:
        if isinstance(entry, tuple):
            text, scale = entry
        else:
            text, scale = entry, 1.0

        if not text:
            render_items.append({"kind": "break", "h": para_gap})
            total_h += para_gap
        else:
            fsize = max(18, int(base_size * scale))
            font = _font(FONT_TEXT, fsize)
            lh = int(fsize * line_spacing)
            render_items.append({
                "kind": "text", "text": text, "font": font, "h": lh
            })
            total_h += lh

    y = (TARGET_H - total_h) // 2 + optical_offset

    for item in render_items:
        if item["kind"] == "break":
            y += item["h"]
        else:
            tw, _ = _text_size(item["text"], item["font"])
            x = (TARGET_W - tw) // 2
            draw.text((x, y), item["text"], fill=BLACK_TEXT, font=item["font"])
            y += item["h"]

    return img.convert("RGBA")


# ═══════════════════════════════════════════════════════════════════════
#  Title Card Renderer (black bg, white text)
# ═══════════════════════════════════════════════════════════════════════

def render_title_card(config):
    img = Image.new("RGB", (TARGET_W, TARGET_H), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    base_size = int(TARGET_W * 0.037)
    line_spacing = 1.8
    para_gap = int(base_size * 2.5)

    card_elem = None
    for elem in config.get("elements", []):
        if elem["type"] == "title_card":
            card_elem = elem
            break

    if card_elem is None:
        return img.convert("RGBA")

    raw_lines = card_elem["lines"]
    render_items = []
    total_h = 0

    for entry in raw_lines:
        if isinstance(entry, tuple):
            text, scale = entry
        else:
            text, scale = entry, 1.0

        if not text:
            render_items.append({"kind": "break", "h": para_gap})
            total_h += para_gap
        else:
            fsize = max(18, int(base_size * scale))
            font = _font(FONT_TEXT, fsize)
            lh = int(fsize * line_spacing)
            render_items.append({
                "kind": "text", "text": text, "font": font, "h": lh
            })
            total_h += lh

    y = (TARGET_H - total_h) // 2

    for item in render_items:
        if item["kind"] == "break":
            y += item["h"]
        else:
            tw, _ = _text_size(item["text"], item["font"])
            x = (TARGET_W - tw) // 2
            draw.text((x, y), item["text"], fill=(255, 255, 255), font=item["font"])
            y += item["h"]

    return img.convert("RGBA")


# ═══════════════════════════════════════════════════════════════════════
#  SFX Layer
# ═══════════════════════════════════════════════════════════════════════

def create_sfx_layer(size, text, font, position, rotation=0,
                     glow_color=(140, 0, 255), glow_radius=18):
    expand = 300
    layer = Image.new("RGBA", (size[0] + expand * 2, size[1] + expand * 2), (0, 0, 0, 0))
    drw = ImageDraw.Draw(layer)
    tx, ty = position[0] + expand, position[1] + expand

    glow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            gd.text((tx + dx, ty + dy), text, font=font,
                    fill=(*glow_color, 120))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=glow_radius))

    draw_outlined_text(drw, (tx, ty), text, font,
                       fill="white", outline_fill="black", outline_width=6)
    combined = Image.alpha_composite(glow, layer)
    if rotation:
        combined = combined.rotate(rotation, resample=Image.BICUBIC, expand=False)
    return combined.crop((expand, expand, expand + size[0], expand + size[1]))


def render_sfx(img, elem, w, h):
    scale = elem.get("font_scale", 0.085)
    font = _font(FONT_SFX, int(w * scale))
    text = elem["text"]
    tw, _ = _text_size(text, font)
    cx = int(elem["pos"][0] * w)
    ty = int(elem["pos"][1] * h)
    sx = cx - tw // 2

    layer = create_sfx_layer(
        img.size, text, font, position=(sx, ty),
        rotation=elem.get("rotation", 0),
        glow_color=elem.get("glow_color", (140, 0, 255)),
        glow_radius=elem.get("glow_radius", 20),
    )
    return Image.alpha_composite(img, layer)


# ═══════════════════════════════════════════════════════════════════════
#  Narration Boxes (transparent bg + purple border per typography guide)
# ═══════════════════════════════════════════════════════════════════════

def draw_narration_box(draw, position, text, font, box_width,
                       padding=12, border_width=3):
    """Sharp-cornered box: near-transparent bg, purple border, white text."""
    x, y = position
    _, th = _text_size(text, font)
    box_h = th + padding * 2

    coords = [x, y, x + box_width, y + box_h]
    draw.rectangle(coords, fill=(0, 0, 0, 50))
    draw.rectangle(coords, outline=(*PURPLE, 220), width=border_width)

    draw.text((x + padding + 2, y + padding - 1), text,
              font=font, fill=(255, 255, 255, 255))
    return box_h


def render_narration(draw, elem, fonts, w, h):
    font = fonts["narration"]
    bw = int(w * elem.get("width", 0.62))
    gap = 4
    px = int(elem["pos"][0] * w)
    py = int(elem["pos"][1] * h)
    cy = py
    for line in elem["lines"]:
        bh = draw_narration_box(draw, (px, cy), line, font, bw)
        cy += bh + gap


# ═══════════════════════════════════════════════════════════════════════
#  Speech Bubbles
# ═══════════════════════════════════════════════════════════════════════

def render_dialogue(draw, elem, fonts, w, h):
    shout = elem.get("shout", False)
    whisper = elem.get("whisper", False)
    font = fonts["dialogue_shout"] if shout else fonts["dialogue"]
    text = elem["text"]
    max_chars = elem.get("max_chars", 24)

    px = int(elem["pos"][0] * w)
    py = int(elem["pos"][1] * h)
    tx = int(elem["tail"][0] * w)
    ty = int(elem["tail"][1] * h)

    pad_x = int(w * 0.022)
    pad_y = int(w * 0.015)
    radius = int(w * 0.015) if not shout else int(w * 0.006)
    brd = max(2, int(w * 0.003))
    tail_sz = int(w * 0.018)

    fill = (255, 255, 255, 245)
    outline = (26, 26, 26, 255)

    lines = textwrap.wrap(text, width=max_chars)
    tw_px, th_px, lh = _text_block_size(lines, font)

    bw = tw_px + pad_x * 2
    bh = th_px + pad_y * 2
    bx = max(6, min(px - bw // 2, w - bw - 6))
    by = max(6, min(py - bh // 2, h - bh - 6))

    draw.rounded_rectangle([bx, by, bx + bw, by + bh],
                           radius=radius, fill=fill,
                           outline=outline, width=brd)

    if ty > by + bh:
        pts = [(tx, ty), (tx - tail_sz, by + bh - 1), (tx + tail_sz, by + bh - 1)]
        edge_y = by + bh
    elif ty < by:
        pts = [(tx, ty), (tx - tail_sz, by + 1), (tx + tail_sz, by + 1)]
        edge_y = by
    elif tx > bx + bw:
        pts = [(tx, ty), (bx + bw - 1, ty - tail_sz), (bx + bw - 1, ty + tail_sz)]
        edge_y = None
    else:
        pts = [(tx, ty), (bx + 1, ty - tail_sz), (bx + 1, ty + tail_sz)]
        edge_y = None

    draw.polygon(pts, fill=fill, outline=outline, width=brd)
    if edge_y is not None:
        cx1 = min(pts[1][0], pts[2][0]) + brd
        cx2 = max(pts[1][0], pts[2][0]) - brd
        draw.rectangle([cx1, edge_y - brd, cx2, edge_y + brd], fill=fill)

    text_y = by + pad_y
    for ln in lines:
        lw, _ = _text_size(ln, font)
        draw.text((bx + (bw - lw) // 2, text_y), ln,
                  fill=(26, 26, 26, 255), font=font)
        text_y += lh


# ═══════════════════════════════════════════════════════════════════════
#  Internal Monologue (floating italic, no bubble)
# ═══════════════════════════════════════════════════════════════════════

def render_monologue(draw, elem, fonts, w, h):
    font = fonts["monologue"]
    max_chars = elem.get("max_chars", 30)
    px = int(elem["pos"][0] * w)
    py = int(elem["pos"][1] * h)

    all_lines = []
    for line in elem["lines"]:
        all_lines.extend(textwrap.wrap(line, width=max_chars))

    tw, th, lh = _text_block_size(all_lines, font)
    bx = max(6, min(px - tw // 2, w - tw - 6))

    text_y = py
    for ln in all_lines:
        lw, _ = _text_size(ln, font)
        draw.text((bx + (tw - lw) // 2, text_y), ln,
                  fill=(220, 210, 240, 255), font=font)
        text_y += lh


# ═══════════════════════════════════════════════════════════════════════
#  System Screen (dark bg, cold blue-white glow, monospace)
# ═══════════════════════════════════════════════════════════════════════

def render_system(draw, elem, fonts, w, h):
    font = fonts["system"]
    title_font = fonts["system_title"]
    error_font = fonts["system_error"]
    lines = elem["lines"]
    box_w = int(w * elem.get("width", 0.78))
    pad = int(w * 0.025)
    brd = max(2, int(w * 0.003))

    px = int(elem["pos"][0] * w)
    py = int(elem["pos"][1] * h)

    lh = int(font.size * 1.5)
    total_h = lh * len(lines) + pad * 2
    bx = px - box_w // 2
    by = py

    draw.rectangle([bx, by, bx + box_w, by + total_h],
                   fill=(*SYSTEM_BG, 230),
                   outline=(*COLD_WHITE, 180), width=brd)

    accent = int(w * 0.03)
    for cx, cy in [(bx, by), (bx + box_w, by),
                   (bx, by + total_h), (bx + box_w, by + total_h)]:
        dx = 1 if cx == bx else -1
        dy = 1 if cy == by else -1
        draw.line([(cx, cy), (cx + accent * dx, cy)],
                  fill=(*COLD_WHITE, 255), width=2)
        draw.line([(cx, cy), (cx, cy + accent * dy)],
                  fill=(*COLD_WHITE, 255), width=2)

    ty = by + pad
    for i, line in enumerate(lines):
        is_title = (i == 0)
        has_error = "ERROR" in line or "???" in line or "UNREADABLE" in line
        f = title_font if is_title else (error_font if has_error else font)
        color = (*PURPLE, 255) if has_error else (*COLD_WHITE, 255)
        draw.text((bx + pad, ty), line, font=f, fill=color)
        ty += lh


# ═══════════════════════════════════════════════════════════════════════
#  Forum Posts
# ═══════════════════════════════════════════════════════════════════════

def render_forum(draw, elem, fonts, w, h):
    font = fonts["forum"]
    box_w = int(w * elem.get("width", 0.88))
    pad = int(w * 0.012)
    brd = max(1, int(w * 0.002))

    px = int(elem["pos"][0] * w)
    py = int(elem["pos"][1] * h)

    lines = textwrap.wrap(elem["text"], width=50)
    lh = int(font.size * 1.3)
    total_h = lh * len(lines) + pad * 2

    bx = px - box_w // 2
    by = py

    draw.rounded_rectangle([bx, by, bx + box_w, by + total_h],
                           radius=int(w * 0.008),
                           fill=(18, 18, 24, 220),
                           outline=(60, 60, 80, 180), width=brd)

    ty = by + pad
    for ln in lines:
        draw.text((bx + pad + 4, ty), ln, font=font,
                  fill=(200, 200, 210, 255))
        ty += lh
    return total_h


# ═══════════════════════════════════════════════════════════════════════
#  Floating Narrator Text (Hollow's voice, no box — art panels only)
# ═══════════════════════════════════════════════════════════════════════

def render_floating(draw, elem, fonts, w, h):
    font = _font(FONT_ITALIC, int(TARGET_W * elem.get("font_scale", 0.038)))
    text = elem["text"]
    px = int(elem["pos"][0] * w)
    py = int(elem["pos"][1] * h)

    tw, _ = _text_size(text, font)
    x = px - tw // 2
    x = max(6, min(x, w - tw - 6))

    draw_outlined_text(draw, (x, py), text, font,
                       fill=(255, 255, 255), outline_fill=(0, 0, 0),
                       outline_width=3)


# ═══════════════════════════════════════════════════════════════════════
#  PANEL CONFIGS — Chapter 0 (v3), 14 panels + end card
#
#  "base":     "text" | "art" | "dark" | "black"
#  "top_extend": pixels to extend for vertical conversion (art only)
#  "elements":  list of overlay elements
#
#  Text-only panels use "text_block" elements where lines are either
#  plain strings (scale=1.0) or tuples ("text", scale).
#  Empty strings create paragraph breaks.
#
#  Positions are fractions 0-1 of the 1080x1920 canvas.
# ═══════════════════════════════════════════════════════════════════════

PANELS = {

    # ── PANEL 1: TEXT ONLY — "My name is Hollow Zounds." ─────────────
    1: {
        "base": "text",
        "elements": [{
            "type": "text_block",
            "lines": [
                "My name is Hollow Zounds.",
                "",
                "Yeah. That's a real-ass name, nigga.",
                "I looked that shit up.",
                "It's a whole thing.",
                "",
                ("Anyway.", 1.5),
            ],
        }],
    },

    # ── PANEL 2: ART — Hollow close-up, deadpan eye contact ─────────
    2: {
        "base": "art",
        "top_extend": 0,
        "elements": [],
    },

    # ── PANEL 3: TEXT ONLY — Background / sword training ─────────────
    3: {
        "base": "text",
        "elements": [{
            "type": "text_block",
            "lines": [
                "I'm 18. Just graduated.",
                "I live with my grandma.",
                "I do sword shit. Self-taught.",
                "My sensei quit after three months",
                "'cause my form was actual dog ass.",
                "",
                ("I kept going.", 1.2),
                "Sensei made the right call honestly.",
                ("That nigga was scared.", 1.15),
            ],
        }],
    },

    # ── PANEL 4: ART — Hollow in empty gym, cancelled sign ──────────
    4: {
        "base": "art",
        "top_extend": 0,
        "elements": [],
    },

    # ── PANEL 5: TEXT ONLY — Programmer brag ─────────────────────────
    5: {
        "base": "text",
        "elements": [{
            "type": "text_block",
            "lines": [
                "I'm also a programmer.",
                "Built my own hunter stat tracker app.",
                "",
                "It's advanced as fuck.",
                "You probably wouldn't understand",
                ("the UI, dumbass.", 1.15),
            ],
        }],
    },

    # ── PANEL 6: ART — Cracked phone, terrible app ──────────────────
    6: {
        "base": "art",
        "top_extend": 0,
        "elements": [],
    },

    # ── PANEL 7: TEXT ONLY — The luck stat ───────────────────────────
    7: {
        "base": "text",
        "elements": [{
            "type": "text_block",
            "lines": [
                "Oh right. The luck stat.",
                "",
                "So here's the thing.",
                "After the incident \u2014",
                "which I'll get to \u2014",
                "the system gave me a stat screen.",
                "",
                "Every other stat came back normal.",
                "Luck just said ERROR,",
                ("that dumb bitch.", 1.2),
                "Still does.",
            ],
        }],
    },

    # ── PANEL 8: DARK/ART — System stat screen ──────────────────────
    8: {
        "base": "dark",
        "elements": [{
            "type": "system",
            "pos": (0.50, 0.18),
            "width": 0.82,
            "lines": [
                "HOLLOW ZOUNDS",
                "RANK: E",
                "",
                "STRENGTH     \u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591  F",
                "AGILITY      \u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591  F",
                "ENDURANCE    \u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591  F",
                "INTELLIGENCE \u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591  D",
                "LUCK         ??????????  ERROR",
                "",
                "WARNING: STAT UNREADABLE",
                "RECOMMENDATION: DO NOT ALLOCATE",
            ],
        }],
    },

    # ── PANEL 9: TEXT ONLY — "I did that shit anyway" ────────────────
    9: {
        "base": "text",
        "elements": [{
            "type": "text_block",
            "lines": [
                "Every scanner I walk past",
                "freezes the fuck up.",
                "System said DO NOT ALLOCATE.",
                "",
                ("I did that shit anyway.", 1.25),
                "",
                "I've been dumping every point",
                "in Luck ever since.",
                ("Fuck what they say.", 1.15),
            ],
        }],
    },

    # ── PANEL 10: TEXT ONLY — The 7-Eleven gate ─────────────────────
    10: {
        "base": "text",
        "elements": [{
            "type": "text_block",
            "lines": [
                ("Anyway.", 1.15),
                "",
                "Three weeks after graduation,",
                "I stopped at a 7-Eleven",
                "on the way home from practice.",
                "",
                "And a Gate opened up.",
                "Right there. On my block.",
                "Just cracked open",
                "like some lazy-ass motherfucker",
                "forgot to close the refrigerator door",
                ("to another fucking dimension.", 1.4),
            ],
        }],
    },

    # ── PANEL 11: ART — Gate ripping open above 7-Eleven ────────────
    11: {
        "base": "art",
        "top_extend": 500,
        "elements": [
            {"type": "sfx", "text": "KKRRRAAAACK",
             "pos": (0.50, 0.10), "font_scale": 0.115, "rotation": -5},
            {"type": "narration", "pos": (0.04, 0.82), "width": 0.62,
             "lines": [
                 "11:47 PM.",
                 "Class-D Gate. Unregistered.",
                 "Three B-rank hunters in the area.",
                 "One civilian. E-rank. Luck stat: ERROR.",
             ]},
        ],
    },

    # ── PANEL 12: TEXT ONLY — Gate aftermath recap ───────────────────
    12: {
        "base": "text",
        "elements": [{
            "type": "text_block",
            "lines": [
                "Three B-rank hunters",
                "got pulled in with me.",
                ("Two didn't make it out.", 1.1),
                ("Weak-ass bitches.", 1.15),
                "",
                "I came out with a monster core,",
                "an empty sandwich wrapper,",
                "and a level up notification.",
                "",
                "I put the point in Luck, obviously.",
                "Darius \u2014 the one hunter",
                "who survived \u2014",
                "hasn't looked me in the eye since.",
                ("I respect that shit.", 1.1),
                "Nigga probably still traumatized.",
            ],
        }],
    },

    # ── PANEL 13: TEXT ONLY — Name hits the internet ─────────────────
    #    Typography note: text gets progressively larger toward bottom
    13: {
        "base": "text",
        "elements": [{
            "type": "text_block",
            "lines": [
                ("By midnight my name", 0.85),
                ("was everywhere.", 0.85),
                "",
                ("Hunter forums. News sites.", 0.95),
                ("Twelve guild masters", 0.95),
                ("got the same notification.", 0.95),
                ("Simultaneously.", 1.0),
                "",
                ("Nobody knew who the fuck I was.", 1.25),
                "",
                ("They were about to make it", 1.15),
                ("weird as hell.", 1.45),
            ],
        }],
    },

    # ── PANEL 14: ART — Chapter closer, Hollow walking away ─────────
    14: {
        "base": "art",
        "top_extend": 0,
        "elements": [
            {"type": "narration", "pos": (0.04, 0.72), "width": 0.70,
             "lines": [
                 "Rank E. Luck stat: ERROR. One level.",
                 "First gate cleared. First point spent.",
                 "Operation Get Lucky. Day 1.",
             ]},
            {"type": "floating",
             "text": "Day 1, nigga.",
             "pos": (0.50, 0.92), "font_scale": 0.042},
        ],
    },

    # ── PANEL 15: END CARD — Black bg, chapter tease ────────────────
    15: {
        "base": "black",
        "elements": [{
            "type": "title_card",
            "lines": [
                ("\u201cI started as nobody.\u201d", 1.0),
                "",
                ("\u201cThis is how that changed.\u201d", 1.0),
                "",
                "",
                ("HOLLOW ZOUNDS", 1.8),
                "",
                ("Chapter 1: \u201cThat's Crazy. Anyway.\u201d", 0.85),
                ("\u2192 Starts Now", 0.75),
            ],
        }],
    },
}


# ═══════════════════════════════════════════════════════════════════════
#  Lettering Engine
# ═══════════════════════════════════════════════════════════════════════

def letter_panel(panel_num):
    config = PANELS.get(panel_num)
    if config is None:
        print(f"[!] No config for panel {panel_num}")
        return None

    base = config.get("base", "art")
    source = os.path.join(PANELS_DIR, f"panel {panel_num}.jpg")
    output = os.path.join(PANELS_DIR, f"panel {panel_num} lettered.png")

    # Build the base image
    if base == "text":
        img = render_text_panel(config)
        print(f"[*] Panel {panel_num}: text-only ({TARGET_W}x{TARGET_H})")
    elif base == "black":
        img = render_title_card(config)
        print(f"[*] Panel {panel_num}: title card ({TARGET_W}x{TARGET_H})")
    elif base == "dark":
        if os.path.exists(source):
            img = Image.open(source).convert("RGBA")
            img = normalize_panel(img, config.get("top_extend", 0))
            print(f"[*] Panel {panel_num}: dark+art {img.size[0]}x{img.size[1]}")
        else:
            img = Image.new("RGBA", (TARGET_W, TARGET_H), (*SYSTEM_BG, 255))
            print(f"[*] Panel {panel_num}: dark bg ({TARGET_W}x{TARGET_H})")
    elif base == "art":
        if not os.path.exists(source):
            print(f"[skip] panel {panel_num}.jpg not found")
            return None
        img = Image.open(source).convert("RGBA")
        img = normalize_panel(img, config.get("top_extend", 0))
        print(f"[*] Panel {panel_num}: art {img.size[0]}x{img.size[1]}")
    else:
        print(f"[!] Unknown base type '{base}' for panel {panel_num}")
        return None

    w, h = img.size

    # Apply overlay elements
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    fonts = load_fonts()

    for elem in config.get("elements", []):
        t = elem["type"]
        if t == "text_block" or t == "title_card":
            continue
        elif t == "sfx":
            img = render_sfx(img, elem, w, h)
        elif t == "narration":
            render_narration(odraw, elem, fonts, w, h)
        elif t == "dialogue":
            render_dialogue(odraw, elem, fonts, w, h)
        elif t == "monologue":
            render_monologue(odraw, elem, fonts, w, h)
        elif t == "system":
            render_system(odraw, elem, fonts, w, h)
        elif t == "forum":
            render_forum(odraw, elem, fonts, w, h)
        elif t == "floating":
            render_floating(odraw, elem, fonts, w, h)

    img = Image.alpha_composite(img, overlay)
    img.convert("RGB").save(output, quality=95)
    print(f"[+] Saved: {output}")
    return output


def letter_all(panel_nums=None):
    if panel_nums is None:
        panel_nums = sorted(PANELS.keys())
    results = {}
    for n in panel_nums:
        results[n] = letter_panel(n)
    found = sum(1 for v in results.values() if v)
    skipped = sum(1 for v in results.values() if v is None)
    print(f"\n[done] Lettered {found} panel(s), skipped {skipped}")
    return results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        nums = [int(x) for x in sys.argv[1:]]
    else:
        nums = None
    letter_all(nums)
