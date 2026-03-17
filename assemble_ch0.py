"""Assemble Chapter 0 v5 — Integrated layout.

Every panel has art with text overlaid as narration boxes or floating text.
No standalone white text panels. One continuous vertical strip.
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CH0_DIR = os.path.join(BASE_DIR, "panels", "ch0")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")

TARGET_W = 1080
FADE_H = 200
FONT_BANGERS = os.path.join(FONTS_DIR, "Bangers-Regular.ttf")

PURPLE = (139, 0, 255)
WHITE = (255, 255, 255)
BOX_BG = (0, 0, 0, 191)       # rgba(0,0,0,0.75)
BOX_BORDER_W = 3
BOX_PAD_Y = 12
BOX_PAD_X = 20
BOX_GAP = 6
SHADOW_COLOR = (0, 0, 0, 242)  # rgba(0,0,0,0.95)


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


def draw_shadow_text(draw, x, y, text, font, fill=WHITE, shadow_offset=2, shadow_blur=None):
    """Draw text with a dark shadow for readability over art."""
    for dx in range(-shadow_offset, shadow_offset + 1):
        for dy in range(-shadow_offset, shadow_offset + 1):
            if dx == 0 and dy == 0:
                continue
            draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 230))
    draw.text((x, y), text, font=font, fill=fill)


def draw_narration_boxes(draw, lines, x, y, font_size=36, max_w=None):
    """Draw stacked narration boxes with purple left border."""
    if max_w is None:
        max_w = int(TARGET_W * 0.85)
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
        cy += bh + BOX_GAP
    return cy - y


def draw_floating_lines(draw, lines, y_start, font_size=42, center=True,
                        x_offset=None, align="center"):
    """Draw floating text lines with shadow, no box."""
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


# ═══════════════════════════════════════════════════════════════
#  PANEL DEFINITIONS — v5 integrated layout
# ═══════════════════════════════════════════════════════════════

def render_panel_0():
    """City skyline with gates — chapter opener."""
    img = load_art("panel 0.jpg")
    if img is None:
        img = dark_panel(2400, (15, 5, 30))
    draw = ImageDraw.Draw(img)
    w, h = img.size

    font_sm = _font(38)
    font_md = _font(46)
    font_sm2 = _font(36)

    top_lines = [
        "Ten years ago Gates started cracking open in cities",
        "like cheap motel doors.",
    ]
    y = int(h * 0.06)
    for line in top_lines:
        tw, th = _text_size(line, font_sm)
        x = (w - tw) // 2
        draw_shadow_text(draw, x, y, line, font_sm)
        y += th + 14

    mid_lines = [
        "Monsters came flooding out.",
        "People awakened with powers and became Hunters.",
    ]
    y = int(h * 0.42)
    for line in mid_lines:
        tw, th = _text_size(line, font_md)
        x = (w - tw) // 2
        draw_shadow_text(draw, x, y, line, font_md)
        y += th + 16

    bot_lines = [
        "This ain't a story about one of those big-time Hunters.",
        "It's about me -- an E-rank who did things his own way.",
    ]
    y = int(h * 0.82)
    for line in bot_lines:
        tw, th = _text_size(line, font_sm2)
        x = (w - tw) // 2
        draw_shadow_text(draw, x, y, line, font_sm2)
        y += th + 14

    return img


def render_panel_1():
    """Character intro — Hollow's face."""
    img = load_art("panel 1.jpg")
    if img is None:
        img = dark_panel()
    draw = ImageDraw.Draw(img)
    w, h = img.size

    boxes = [
        "My name is Hollow Zounds.",
        "Yeah. That's my real government name.",
        "My mama named me that back in '07",
        "and ain't nobody in the family could pronounce it right.",
    ]
    draw_narration_boxes(draw, boxes, 40, int(h * 0.58))

    draw_floating_lines(draw, ["I still rock it like it's normal."],
                        int(h * 0.88), font_size=48)
    return img


def render_panel_2():
    """Gym scene — swordsmanship."""
    img = load_art("panel 2.jpg")
    if img is None:
        img = dark_panel()
    draw = ImageDraw.Draw(img)
    w, h = img.size

    boxes = [
        "I'm 18. Just graduated.",
        "I live with my grandma in the same apartment I grew up in.",
        "I taught myself swordsmanship off YouTube.",
        "My sensei quit after three months.",
        "I kept showing up every Tuesday anyway.",
    ]
    draw_narration_boxes(draw, boxes, 40, int(h * 0.05))

    float_lines = [
        "He eventually moved to another state",
        "and blocked my number.",
    ]
    draw_floating_lines(draw, float_lines, int(h * 0.85), font_size=44)
    return img


def render_panel_3():
    """Phone screen — programmer brag."""
    img = load_art("panel 3.jpg")
    if img is None:
        img = dark_panel()
    draw = ImageDraw.Draw(img)
    w, h = img.size

    boxes_top = [
        "I'm also a programmer.",
        "Built my own hunter stat tracker app",
        "on my cracked phone in my grandma's kitchen.",
        "It's advanced as hell.",
    ]
    draw_narration_boxes(draw, boxes_top, 40, int(h * 0.04))

    draw_floating_lines(draw,
                        ["Some dude left a review that said",
                         "'UI is straight ass.'"],
                        int(h * 0.48), font_size=36)

    draw_narration_boxes(draw,
                         ["I replied at 2am: 'It kicks ass tho, my guy.'"],
                         40, int(h * 0.66))

    draw_floating_lines(draw, ["He ain't say nothing back."],
                        int(h * 0.86), font_size=38)
    return img


def render_panel_4():
    """Stat screen — luck stat."""
    img = load_art("panel 4.png")
    if img is None:
        img = dark_panel()
    draw = ImageDraw.Draw(img)
    w, h = img.size

    boxes = [
        "Oh right. The luck stat.",
        "After the incident the System gave me my stat screen.",
        "Everything else was normal.",
        "But Luck came back ERROR.",
        "Warning said: DO NOT ALLOCATE.",
    ]
    draw_narration_boxes(draw, boxes, 40, int(h * 0.04))

    float_lines = [
        "I put the point in anyway.",
        "I'm tryna get lucky out here.",
        "You already know what I mean.",
        "Been maxing that stat ever since.",
    ]
    draw_floating_lines(draw, float_lines, int(h * 0.72), font_size=42)
    return img


def render_panel_5():
    """Agent scanner scene."""
    img = load_art("panel 5.jpg")
    if img is None:
        img = dark_panel()
    draw = ImageDraw.Draw(img)
    w, h = img.size

    boxes = [
        "Every scanner I walk past starts glitching and smoking.",
        "Three agents filed official reports on government letterhead",
        'about "severe equipment malfunction."',
        "They eventually pulled me in for questioning.",
    ]
    draw_narration_boxes(draw, boxes, 40, int(h * 0.04))

    draw_floating_lines(draw,
                        ["This high-ranking dude looked at me and asked:"],
                        int(h * 0.42), font_size=36)

    draw_floating_lines(draw,
                        ['"What did you do to your Luck stat?"'],
                        int(h * 0.50), font_size=42)

    float_lines = [
        "I just shrugged and said:",
        '"I live with my grandma, bro."',
    ]
    draw_floating_lines(draw, float_lines, int(h * 0.64), font_size=44)

    draw_floating_lines(draw, ["He ain't say nothing back."],
                        int(h * 0.82), font_size=36)

    draw_floating_lines(draw, ["I respect that."],
                        int(h * 0.90), font_size=40)
    return img


def render_panel_6():
    """Gate opening — the big one."""
    img = load_art("panel 6.jpg")
    if img is None:
        img = dark_panel(2400)
    draw = ImageDraw.Draw(img)
    w, h = img.size

    boxes_top = [
        "Three weeks after graduation",
        "I stopped at the 7-Eleven on the way home from practice.",
        "Bought a sandwich and some chips. Minding my business.",
    ]
    draw_narration_boxes(draw, boxes_top, 40, int(h * 0.04))

    boxes_bot = [
        "Then a whole Gate cracked open right on my block.",
    ]
    draw_narration_boxes(draw, boxes_bot, 40, int(h * 0.72))

    float_lines = [
        "Like somebody forgot to close",
        "the refrigerator door",
        "to another dimension.",
    ]
    draw_floating_lines(draw, float_lines, int(h * 0.84), font_size=44)
    return img


def render_panel_7():
    """Walking out of gate aftermath."""
    img = dark_panel(1600, (12, 10, 22))
    draw = ImageDraw.Draw(img)
    w, h = img.size

    boxes = [
        "Three B-rank hunters got sucked in with me.",
        "Two of them didn't make it.",
        "I walked out with a monster core,",
        "an empty sandwich wrapper,",
        "and a level-up notification.",
    ]
    draw_narration_boxes(draw, boxes, 40, int(h * 0.08))

    draw_floating_lines(draw,
                        ["Obviously put the point in Luck."],
                        int(h * 0.75), font_size=52)
    return img


def render_panel_8():
    """Waiting room — Darius callback."""
    img = load_art("panel 8.jpg")
    if img is None:
        img = dark_panel()
    draw = ImageDraw.Draw(img)
    w, h = img.size

    boxes = [
        "Darius -- the only survivor --",
        "still won't look me in the eye.",
        "We've been called in for questioning three times.",
        "Three times in that same waiting room.",
    ]
    draw_narration_boxes(draw, boxes, 40, int(h * 0.04))

    float_lines = [
        "I respect it.",
        "He saw some things in there.",
    ]
    draw_floating_lines(draw, float_lines, int(h * 0.84), font_size=44)
    return img


def render_panel_9():
    """News aftermath."""
    img = load_art("panel 9.jpg")
    if img is None:
        img = dark_panel()
    draw = ImageDraw.Draw(img)
    w, h = img.size

    boxes = [
        "By midnight my name was everywhere.",
        "Hunter forums blowing up.",
        "News sites posted my blurry picture.",
        "Twelve guild masters got the same notification",
        "at the same time.",
    ]
    draw_narration_boxes(draw, boxes, 40, int(h * 0.04))

    draw_floating_lines(draw,
                        ["Nobody knew who I was."],
                        int(h * 0.78), font_size=50)

    draw_floating_lines(draw,
                        ["They were about to make it weird."],
                        int(h * 0.90), font_size=38)
    return img


def render_panel_10():
    """Cinematic closer — no text."""
    img = load_art("panel 10.jpg")
    if img is None:
        img = dark_panel()
    return img


def render_panel_11():
    """Title card — black bg."""
    img = load_art("panel 11.png")
    if img is not None:
        return img

    img = Image.new("RGBA", (TARGET_W, 1920), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    lines = [
        ('"I started as nobody."', 62),
        ('"This is how that changed."', 62),
        ("", 0),
        ("HOLLOW ZOUNDS", 130),
        ('Chapter 1: "That\'s Crazy. Anyway."', 42),
        (">> Starts Now", 36),
    ]
    y = 600
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


PANEL_RENDERERS = [
    render_panel_0,
    render_panel_1,
    render_panel_2,
    render_panel_3,
    render_panel_4,
    render_panel_5,
    render_panel_6,
    render_panel_7,
    render_panel_8,
    render_panel_9,
    render_panel_10,
    render_panel_11,
]


def blend_edge(top_img, bot_img, fade_h=FADE_H):
    """Create a gradient blend between the bottom of top_img and top of bot_img."""
    top_arr = np.array(top_img.convert("RGB"))
    bot_arr = np.array(bot_img.convert("RGB"))

    top_strip = top_arr[-fade_h:]
    bot_strip = bot_arr[:fade_h]

    blended = np.zeros_like(top_strip, dtype=np.float32)
    for row in range(fade_h):
        t = row / fade_h
        t = t * t * (3 - 2 * t)  # smoothstep
        blended[row] = top_strip[row] * (1 - t) + bot_strip[row] * t

    return Image.fromarray(blended.astype(np.uint8)).convert("RGBA")


def assemble():
    print("[*] Rendering v5 integrated panels...")
    panels = []
    for i, renderer in enumerate(PANEL_RENDERERS):
        print(f"  Panel {i}: ", end="")
        img = renderer()
        panels.append(img)
        print(f"{img.width}x{img.height}")

    print(f"\n[*] Assembling with {FADE_H}px blend transitions...")

    segments = []
    for i, panel in enumerate(panels):
        if i == 0:
            top_crop = panel.crop((0, 0, panel.width, panel.height - FADE_H))
            segments.append(top_crop)
        else:
            prev = panels[i - 1]
            blend = blend_edge(prev, panel, FADE_H)
            segments.append(blend)

            is_last = (i == len(panels) - 1)
            if is_last:
                cropped = panel.crop((0, FADE_H, panel.width, panel.height))
            else:
                cropped = panel.crop((0, FADE_H, panel.width, panel.height - FADE_H))
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
