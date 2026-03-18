"""Overlay narration boxes and floating text on panel 14."""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CH0_DIR = os.path.join(BASE_DIR, "panels", "ch0")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
FONT_BANGERS = os.path.join(FONTS_DIR, "Bangers-Regular.ttf")

SRC = os.path.join(CH0_DIR, "panel 14.jpg")
OUT = os.path.join(CH0_DIR, "panel_14_lettered.png")

REFERENCE_W = 1080

img = Image.open(SRC).convert("RGBA")
W, H = img.size
S = W / REFERENCE_W  # scale factor for all pixel values

# --- Fonts ---
font_box = ImageFont.truetype(FONT_BANGERS, int(36 * S))
font_float = ImageFont.truetype(FONT_BANGERS, int(52 * S))

# --- Colors ---
purple = (139, 0, 255, 255)
white = (255, 255, 255, 255)
box_bg = (0, 0, 0, int(0.7 * 255))

# --- Dimensions (scaled) ---
pad_top = int(10 * S)
pad_side = int(16 * S)
border_w = int(3 * S)
box_gap = int(6 * S)
margin_left = int(40 * S)
from_bottom = int(200 * S)
float_from_bottom = int(60 * S)

# --- Box content ---
box_texts = [
    "Rank E. Luck stat: ERROR. One level.",
    "First gate cleared. First point spent.",
    "Operation Get Lucky. Day 1.",
]

overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Measure boxes
boxes = []
for text in box_texts:
    bbox = font_box.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    bw = tw + pad_side * 2 + border_w
    bh = th + pad_top * 2
    boxes.append({"text": text, "tw": tw, "th": th, "bw": bw, "bh": bh})

total_stack_h = sum(b["bh"] for b in boxes) + box_gap * (len(boxes) - 1)

# Stack upward from `from_bottom` px above the bottom
stack_bottom_y = H - from_bottom
stack_top_y = stack_bottom_y - total_stack_h

y = stack_top_y
for b in boxes:
    x = margin_left
    bw, bh = b["bw"], b["bh"]

    # Semi-transparent black background
    draw.rectangle([x, y, x + bw, y + bh], fill=box_bg)

    # Left purple border
    draw.rectangle([x, y, x + border_w, y + bh], fill=purple)

    # White text
    text_x = x + border_w + pad_side
    text_y = y + pad_top
    draw.text((text_x, text_y), b["text"], fill=white, font=font_box)

    y += bh + box_gap

# --- Floating voice line ---
float_text = "Day 1, nigga."
float_bbox = font_float.getbbox(float_text)
float_tw = float_bbox[2] - float_bbox[0]
float_th = float_bbox[3] - float_bbox[1]
float_x = (W - float_tw) // 2
float_y = H - float_from_bottom - float_th
draw.text((float_x, float_y), float_text, fill=white, font=font_float)

# Composite and save
result = Image.alpha_composite(img, overlay)
result.convert("RGB").save(OUT, "PNG")
print(f"[+] Saved: {OUT}  ({W}x{H})")
