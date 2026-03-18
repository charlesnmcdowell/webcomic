"""Assemble Chapter 0 v6.3 — SNF Compliant integrated layout.

24 panels: 17 art panels + 7 Cursor-generated design panels.
One continuous vertical strip, seamless transitions.
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
CH0_DIR = os.path.join(PROJECT_DIR, "panels", "ch0")
FONTS_DIR = os.path.join(PROJECT_DIR, "fonts")

TARGET_W = 1080
FADE_H = 200
FONT_BANGERS = os.path.join(FONTS_DIR, "Bangers-Regular.ttf")

PURPLE = (139, 0, 255)
WHITE = (255, 255, 255)
BOX_BG = (0, 0, 0, 191)
BOX_BORDER_W = 3
BOX_PAD_Y = 12
BOX_PAD_X = 20
BOX_GAP = 6

DARK_PURPLE = (26, 10, 46)
CRIMSON = (139, 0, 0)


# ===================================================================
#  UTILITY FUNCTIONS
# ===================================================================

def _font(size):
    return ImageFont.truetype(FONT_BANGERS, size)


def _text_size(text, font):
    bb = font.getbbox(text)
    return bb[2] - bb[0], bb[3] - bb[1]


def load_art(filename):
    path = os.path.join(CH0_DIR, filename)
    if not os.path.exists(path):
        return None
    img = Image.open(path).convert("RGBA")
    if img.width != TARGET_W:
        ratio = TARGET_W / img.width
        new_h = int(img.height * ratio)
        img = img.resize((TARGET_W, new_h), Image.LANCZOS)
    return img


def dark_panel(height=1920, color=(10, 8, 20)):
    return Image.new("RGBA", (TARGET_W, height), (*color, 255))


def linear_gradient(w, h, top_color, bot_color):
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    for row in range(h):
        t = row / max(h - 1, 1)
        for c in range(3):
            arr[row, :, c] = int(top_color[c] * (1 - t) + bot_color[c] * t)
    return Image.fromarray(arr).convert("RGBA")


def radial_gradient(w, h, center_color, edge_color):
    y_grid, x_grid = np.mgrid[:h, :w]
    cx, cy = w // 2, h // 2
    max_dist = np.sqrt(cx ** 2 + cy ** 2)
    dist = np.sqrt((x_grid - cx) ** 2 + (y_grid - cy) ** 2) / max_dist
    dist = np.clip(dist, 0, 1)
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    for c in range(3):
        arr[:, :, c] = (center_color[c] * (1 - dist) + edge_color[c] * dist).astype(np.uint8)
    return Image.fromarray(arr).convert("RGBA")


def draw_shadow_text(draw, x, y, text, font, fill=WHITE, shadow_offset=2):
    for dx in range(-shadow_offset, shadow_offset + 1):
        for dy in range(-shadow_offset, shadow_offset + 1):
            if dx == 0 and dy == 0:
                continue
            draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 230))
    draw.text((x, y), text, font=font, fill=fill)


def draw_outlined_text(draw, x, y, text, font, fill=WHITE,
                       outline=(0, 0, 0, 255), outline_w=4):
    for dx in range(-outline_w, outline_w + 1):
        for dy in range(-outline_w, outline_w + 1):
            if dx == 0 and dy == 0:
                continue
            draw.text((x + dx, y + dy), text, font=font, fill=outline)
    draw.text((x, y), text, font=font, fill=fill)


def draw_narration_boxes(draw, lines, x, y, font_size=36, max_w=None, gap=None):
    if max_w is None:
        max_w = int(TARGET_W * 0.85)
    if gap is None:
        gap = BOX_GAP
    font = _font(font_size)
    cy = y
    for line in lines:
        tw, th = _text_size(line, font)
        bw = min(tw + BOX_PAD_X * 2 + BOX_BORDER_W, max_w)
        bh = th + BOX_PAD_Y * 2
        draw.rectangle([x, cy, x + bw, cy + bh], fill=BOX_BG)
        draw.rectangle([x, cy, x + BOX_BORDER_W, cy + bh], fill=(*PURPLE, 255))
        draw.text((x + BOX_BORDER_W + BOX_PAD_X, cy + BOX_PAD_Y),
                  line, font=font, fill=WHITE)
        cy += bh + gap
    return cy - y


def draw_floating_lines(draw, lines, y_start, font_size=48, center=True,
                        x_offset=None):
    font = _font(font_size)
    cy = y_start
    for line in lines:
        tw, th = _text_size(line, font)
        if center:
            x = (TARGET_W - tw) // 2
        elif x_offset is not None:
            x = x_offset
        else:
            x = 40
        draw_shadow_text(draw, x, cy, line, font)
        cy += th + 12
    return cy - y_start


# ===================================================================
#  ART PANEL RENDERERS
# ===================================================================

def render_panel_0():
    """World establishment -- Void Holes over city."""
    img = load_art("panel 0.jpg")
    if img is None:
        img = dark_panel(2400, (15, 5, 30))
    draw = ImageDraw.Draw(img)
    draw_narration_boxes(draw, [
        "Ten years ago Void Holes started opening.",
        "Creatures came out.",
        "People with abilities became Anoms.",
    ], 40, int(img.height * 0.15))
    return img


def render_panel_1():
    """Civilian behavior -- street level, nobody cares."""
    img = load_art("Panel 1.jpg")
    if img is None:
        img = dark_panel()
    draw = ImageDraw.Draw(img)
    w, h = img.size

    font_sm = _font(34)
    font_lg = _font(38)
    draw_shadow_text(draw, 80, int(h * 0.52), '"Another one."', font_sm)
    draw_shadow_text(draw, 320, int(h * 0.60), '"Third this week."', font_sm)

    text = '"You want mustard or not?"'
    tw, _ = _text_size(text, font_lg)
    draw_shadow_text(draw, w - tw - 50, int(h * 0.74), text, font_lg)
    return img


def render_panel_2a():
    """Void is dangerous -- shadow creatures."""
    img = load_art("PANEL 2A.jpg")
    if img is None:
        img = dark_panel(2400, (8, 5, 15))
    draw = ImageDraw.Draw(img)
    draw_narration_boxes(draw, ["Not everyone makes it out."],
                         40, int(img.height * 0.88))
    return img


def render_panel_2b():
    """Anoms in action -- competent team clearing Void."""
    img = load_art("panel 2b.jpg")
    if img is None:
        img = dark_panel(2400)
    draw = ImageDraw.Draw(img)
    draw_narration_boxes(draw, [
        "Anoms run Voids for a living.",
        "Good ones make serious money.",
    ], 40, int(img.height * 0.15))
    return img


def render_panel_3():
    """Character intro -- Hollow portrait."""
    img = load_art("panel 3.jpg")
    if img is None:
        img = dark_panel()
    draw = ImageDraw.Draw(img)
    w, h = img.size

    draw_narration_boxes(draw, [
        "My name is Hollow Zounds.",
        "E-rank. Basically a regular person with paperwork.",
    ], 40, int(h * 0.62))

    stat_font = _font(22)
    stat_color = (255, 255, 255, 90)
    draw.text((w - 180, h - 80), "RANK: E", font=stat_font, fill=stat_color)
    draw.text((w - 180, h - 52), "LUCK: ???", font=stat_font, fill=stat_color)
    return img


def render_panel_4():
    """Stakes -- bills on table, Anom card."""
    img = load_art("panel 4.jpg")
    if img is None:
        img = dark_panel()
    draw = ImageDraw.Draw(img)
    draw_narration_boxes(draw, [
        "I awakened three months ago.",
        "Haven't been approved for a contract yet.",
        "Haven't run a single Void.",
    ], 40, int(img.height * 0.15))
    return img


def render_panel_6a():
    """Void Hole opening -- all text baked into art. No overlay."""
    img = load_art("panel 6a.jpg")
    if img is None:
        img = dark_panel(2400)
    return img


def render_panel_6b():
    """Apex arrives -- carries narration from 6A + 6B."""
    img = load_art("panel 6b.jpg")
    if img is None:
        img = dark_panel(2400)
    draw = ImageDraw.Draw(img)
    h = img.height

    draw_narration_boxes(draw, [
        "Three weeks after graduation.",
        "Stopped at the 7-Eleven on the way home from practice.",
        "Faction response team showed up two minutes later.",
        "Then the Void Hole pulled us all in.",
    ], 40, int(h * 0.15))

    draw_floating_lines(draw, [
        "Like somebody forgot to close the refrigerator door",
        "to another dimension.",
    ], int(h * 0.82), font_size=38)
    return img


def render_panel_7():
    """Silent -- battle scene inside Void. No text."""
    img = load_art("panel 7a.jpg")
    if img is None:
        img = dark_panel(2400, (12, 10, 22))
    return img


def render_panel_7b():
    """Boss kill -- spider queen climax. Image carries everything."""
    img = load_art("panel 7b.jpg")
    if img is None:
        img = dark_panel(2400, (12, 10, 22))
    return img


def render_panel_7c():
    """Hero status notification -- text baked into art."""
    img = load_art("panel 7c.jpg")
    if img is None:
        img = dark_panel()
    return img


def render_panel_7d():
    """Hollow with sword and core -- accepted Hero Status."""
    img = load_art("panel 7d.jpg")
    if img is None:
        img = dark_panel()
    draw = ImageDraw.Draw(img)
    draw_narration_boxes(draw, ["Obviously said yes."],
                         40, int(img.height * 0.15))
    return img


def render_panel_7e():
    """Inventory discovery -- items dissolving."""
    img = load_art("panel 7e.jpg")
    if img is None:
        img = dark_panel()
    draw = ImageDraw.Draw(img)
    h = img.height

    draw_narration_boxes(draw, [
        "Then my stuff disappeared into thin air.",
    ], 40, int(h * 0.15))

    draw_floating_lines(draw, ['"Oh no. My precious loot."'],
                        int(h * 0.88), font_size=46)
    return img


def render_panel_8():
    """Aftermath -- walking out of Void. Glitch text in art."""
    img = load_art("panel 8.jpg")
    if img is None:
        img = dark_panel()
    draw = ImageDraw.Draw(img)
    draw_narration_boxes(draw, [
        "Found my snacks from the 7-Eleven.",
        "Started making my way home.",
        "Trying to understand my level up notification.",
    ], 40, int(img.height * 0.15))
    return img


def render_panel_9():
    """World reacts -- news aftermath."""
    img = load_art("panel 9.jpg")
    if img is None:
        img = dark_panel()
    draw = ImageDraw.Draw(img)
    h = img.height

    draw_narration_boxes(draw, [
        "By midnight the news was everywhere.",
        "Gate incident on the lower east side.",
        "Two survivors. Identities not released.",
    ], 40, int(h * 0.15))

    draw_floating_lines(draw, ['"I was one of them."'],
                        int(h * 0.88), font_size=46)
    return img


def render_panel_10():
    """Silent closer -- no text."""
    img = load_art("panel 10.jpg")
    if img is None:
        img = dark_panel()
    return img


def render_panel_11():
    """Title card -- always generated to match latest script text."""
    img = Image.new("RGBA", (TARGET_W, 1920), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    lines = [
        ('"That was a weird night."', 62),
        ("", 0),
        ('"Anyway."', 62),
        ("", 0),
        ('"At least I still had my snacks."', 52),
        ("", 0),
        ("HOLLOW ZOUNDS", 130),
        ('Chapter 1: "That\'s Crazy. Anyway."', 42),
        (">> Starts Now", 36),
    ]
    y = 400
    for text, size in lines:
        if not text:
            y += 100
            continue
        font = _font(size)
        tw, th = _text_size(text, font)
        x = (TARGET_W - tw) // 2
        draw.text((x, y), text, font=font, fill=WHITE)
        y += th + 40
    return img


# ===================================================================
#  CURSOR-GENERATED DESIGN PANELS
# ===================================================================

def render_panel_7_i():
    """Black panel -- agent deaths. Quiet. Respectful."""
    w, h = TARGET_W, 600
    img = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    line1 = "Two agents didn't make it to the boss room."
    line2 = "They knew the risk."

    f1 = _font(52)
    f2 = _font(36)
    tw1, th1 = _text_size(line1, f1)
    tw2, th2 = _text_size(line2, f2)

    total_block = th1 + 50 + 2 + 30 + th2
    y_start = (h - total_block) // 2

    draw.text(((w - tw1) // 2, y_start), line1, font=f1, fill=WHITE)

    line_y = y_start + th1 + 50
    line_w = max(tw1, tw2) + 40
    draw.line([(w - line_w) // 2, line_y, (w + line_w) // 2, line_y],
              fill=(255, 255, 255, 80), width=1)

    draw.text(((w - tw2) // 2, line_y + 30), line2, font=f2,
              fill=(136, 136, 136))
    return img


def render_panel_7_ii():
    """Red BANG panel -- explosive transition."""
    w, h = TARGET_W, 800
    img = radial_gradient(w, h, (255, 0, 0), CRIMSON)
    draw = ImageDraw.Draw(img)

    cx, cy = w // 2, h // 2
    for i in range(6):
        r = 180 + i * 55
        alpha = int(140 * (1 - i / 6))
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)],
                     outline=(255, 255, 255, alpha), width=2)

    font = _font(280)
    text = "BANG"
    tw, th = _text_size(text, font)
    tx, ty = (w - tw) // 2, (h - th) // 2

    for dx, dy in [(4, 4), (6, 6), (8, 8)]:
        draw.text((tx + dx, ty + dy), text, font=font, fill=(0, 0, 0, 180))
    draw.text((tx, ty), text, font=font, fill=WHITE)
    return img


def render_panel_7_iii():
    """Sound effects panel -- chain reaction."""
    w, h = TARGET_W, 900
    img = Image.new("RGBA", (w, h), (*DARK_PURPLE, 255))
    draw = ImageDraw.Draw(img)

    f1 = _font(96)
    t1 = "CRAAACK"
    tw1, _ = _text_size(t1, f1)
    draw_outlined_text(draw, (w - tw1) // 2 - 80, 90,
                       t1, f1, fill=(192, 192, 192), outline_w=3)

    f2 = _font(140)
    t2 = "SKKRRRRCH"
    tw2, th2 = _text_size(t2, f2)
    pad = 50
    txt_canvas = Image.new("RGBA", (tw2 + pad * 2, th2 + pad * 2), (0, 0, 0, 0))
    txt_draw = ImageDraw.Draw(txt_canvas)
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            txt_draw.text((pad + dx, pad + dy), t2, font=f2,
                          fill=(139, 0, 0, 200))
    txt_draw.text((pad, pad), t2, font=f2, fill=WHITE)
    rotated = txt_canvas.rotate(3, expand=True, resample=Image.BICUBIC)
    img.paste(rotated, ((w - rotated.width) // 2, (h - rotated.height) // 2 - 20), rotated)

    draw = ImageDraw.Draw(img)

    f3 = _font(88)
    t3 = "KSSSSREEEEEE"
    tw3, th3 = _text_size(t3, f3)
    draw_outlined_text(draw, (w - tw3) // 2 + 60, h - th3 - 100,
                       t3, f3, fill=(*CRIMSON, 255), outline_w=3)
    return img


def render_panel_7_iv():
    """White fade -- dark SFX to bright boss kill."""
    return linear_gradient(TARGET_W, 300, DARK_PURPLE, (255, 255, 255))


def render_panel_7_v():
    """Portal exit fade -- white to black."""
    return linear_gradient(TARGET_W, 300, (255, 255, 255), (0, 0, 0))


def render_panel_7_vi():
    """Narration panel -- item value + FINAL NOTICE callback."""
    w, h = TARGET_W, 700
    img = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    box_x = (w - int(w * 0.8)) // 2
    box_h = draw_narration_boxes(draw, [
        "The core was still in my inventory.",
        "So was the sword.",
        "No idea what either was worth.",
    ], box_x, 80, gap=12, max_w=int(w * 0.8))

    punch_y = 80 + box_h + 60
    draw_floating_lines(draw, [
        "But I had a FINAL NOTICE on my kitchen table.",
        "So.",
    ], punch_y, font_size=48)
    return img


def render_panel_7_vii():
    """Night sky fade -- black to dark purple-blue."""
    return linear_gradient(TARGET_W, 400, (0, 0, 0), DARK_PURPLE)


# ===================================================================
#  PANEL ORDER -- 24 panels
# ===================================================================

PANEL_RENDERERS = [
    render_panel_0,        # 0  - World establishment
    render_panel_1,        # 1  - Civilian behavior
    render_panel_2a,       # 2  - Void is dangerous
    render_panel_2b,       # 3  - Anoms in action
    render_panel_3,        # 4  - Character intro
    render_panel_4,        # 5  - Stakes / bills
    render_panel_6a,       # 6  - Void Hole opening (narration + baked text)
    render_panel_6b,       # 7  - Apex arrives
    render_panel_7,        # 8  - Silent battle scene
    render_panel_7_i,      # 9  - Black death panel (CURSOR)
    render_panel_7_ii,     # 10 - Red BANG (CURSOR)
    render_panel_7_iii,    # 11 - SFX chain reaction (CURSOR)
    render_panel_7_iv,     # 12 - White fade (CURSOR)
    render_panel_7b,       # 13 - Boss kill
    render_panel_7c,       # 14 - Hero notification (silent)
    render_panel_7d,       # 15 - Sword + core
    render_panel_7e,       # 16 - Inventory discovery
    render_panel_7_v,      # 17 - Portal exit fade (CURSOR)
    render_panel_7_vi,     # 18 - Narration / FINAL NOTICE (CURSOR)
    render_panel_7_vii,    # 19 - Night sky fade (CURSOR)
    render_panel_8,        # 20 - Aftermath
    render_panel_9,        # 21 - World reacts
    render_panel_10,       # 22 - Silent closer
    render_panel_11,       # 23 - Title card
]


# ===================================================================
#  ASSEMBLY
# ===================================================================

def blend_edge(top_img, bot_img, fade_h):
    top_arr = np.array(top_img.convert("RGB"))
    bot_arr = np.array(bot_img.convert("RGB"))
    top_strip = top_arr[-fade_h:]
    bot_strip = bot_arr[:fade_h]
    blended = np.zeros_like(top_strip, dtype=np.float32)
    for row in range(fade_h):
        t = row / fade_h
        t = t * t * (3 - 2 * t)
        blended[row] = top_strip[row] * (1 - t) + bot_strip[row] * t
    return Image.fromarray(blended.astype(np.uint8)).convert("RGBA")


def assemble():
    print("[*] Rendering v6.3 panels (24 total)...")
    panels = []
    for i, renderer in enumerate(PANEL_RENDERERS):
        name = renderer.__name__.replace("render_", "")
        print(f"  [{i:2d}] {name}: ", end="")
        img = renderer()
        panels.append(img)
        print(f"{img.width}x{img.height}")

    fades = []
    for i in range(len(panels) - 1):
        f = min(FADE_H, panels[i].height // 3, panels[i + 1].height // 3)
        fades.append(f)

    print(f"\n[*] Assembling {len(panels)} panels with adaptive blend transitions...")

    segments = []
    for i, panel in enumerate(panels):
        bot_fade = fades[i] if i < len(fades) else 0
        top_fade = fades[i - 1] if i > 0 else 0

        if i == 0:
            cropped = panel.crop((0, 0, panel.width, panel.height - bot_fade))
            segments.append(cropped)
        else:
            blend = blend_edge(panels[i - 1], panel, top_fade)
            segments.append(blend)
            bottom_cut = bot_fade if i < len(panels) - 1 else 0
            cropped = panel.crop((0, top_fade, panel.width, panel.height - bottom_cut))
            segments.append(cropped)

    total_h = sum(s.height for s in segments)
    print(f"[*] Total strip: {TARGET_W}x{total_h}px")

    strip = Image.new("RGB", (TARGET_W, total_h), (0, 0, 0))
    y = 0
    for seg in segments:
        strip.paste(seg.convert("RGB"), (0, y))
        y += seg.height

    out = os.path.join(CH0_DIR, "hollow_zounds_ch0_final.png")
    strip.save(out, "PNG")
    print(f"[+] Saved: {out}")
    print("\n[done]")


if __name__ == "__main__":
    assemble()
