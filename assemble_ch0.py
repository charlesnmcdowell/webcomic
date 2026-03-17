"""Assemble Chapter 0 vertical webtoon strip from panel images.

Stacks panels top-to-bottom at 1080px wide, zero gap.
Adds narration overlay to panel 14.
Splits into <=3000px slices at clean panel boundaries.
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CH0_DIR = os.path.join(BASE_DIR, "panels", "ch0")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")

TARGET_W = 1080
MAX_SLICE_H = 10000
TEXT_PANEL_PAD = 150  # breathing room above and below content on text panels

FONT_BANGERS = os.path.join(FONTS_DIR, "Bangers-Regular.ttf")

TEXT_PANELS = {
    "panel 1 lettered.png",
    "panel 3 lettered.png",
    "panel 5 lettered.png",
    "panel 7 lettered.png",
    "panel 9 lettered.png",
    "panel 10 lettered.png",
    "panel 12 lettered.png",
    "panel 13 lettered.png",
}

PANEL_ORDER = [
    "panel 1 lettered.png",
    "panel 2.jpg",
    "panel 3 lettered.png",
    "panel 4.jpg",
    "panel 5 lettered.png",
    "panel 6.jpg",
    "panel 7 lettered.png",
    "panel 8 lettered.png",
    "panel 9 lettered.png",
    "panel 9.5.jpg",
    "panel 10 lettered.png",
    "panel 11.jpg",
    "panel 12 lettered.png",
    "panel 12.5.jpg",
    "panel 13 lettered.png",
    "panel 14.jpg",
    "panel 15 lettered.png",
]


def load_panel(filename):
    path = os.path.join(CH0_DIR, filename)
    img = Image.open(path).convert("RGBA")
    if img.width != TARGET_W:
        ratio = TARGET_W / img.width
        new_h = int(img.height * ratio)
        img = img.resize((TARGET_W, new_h), Image.LANCZOS)
    return img


def trim_text_panel(img, pad=TEXT_PANEL_PAD):
    """Crop a white-background text panel to its content + padding."""
    arr = np.array(img.convert("RGB"))
    # A row is "content" if any pixel isn't near-white
    row_has_content = np.any(arr < 240, axis=(1, 2))
    content_rows = np.where(row_has_content)[0]
    if len(content_rows) == 0:
        return img
    top = max(0, content_rows[0] - pad)
    bottom = min(img.height, content_rows[-1] + pad)
    return img.crop((0, top, img.width, bottom))


def overlay_panel_14(img):
    """Add narration boxes and floating text to panel 14."""
    draw = ImageDraw.Draw(img)
    font_box = ImageFont.truetype(FONT_BANGERS, 32)
    font_float = ImageFont.truetype(FONT_BANGERS, 48)

    purple = (139, 0, 255)
    white = (255, 255, 255)

    box_texts = [
        "Rank E. Luck stat: ERROR. One level.",
        "First gate cleared. First point spent.",
        "Operation Get Lucky. Day 1.",
    ]

    pad_x, pad_y = 16, 12
    box_gap = 14
    margin_left = 40
    margin_bottom = 120

    boxes = []
    for text in box_texts:
        bbox = font_box.getbbox(text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        boxes.append({"text": text, "tw": tw, "th": th})

    total_boxes_h = sum(b["th"] + pad_y * 2 for b in boxes) + box_gap * (len(boxes) - 1)
    float_text = "Day 1, nigga."
    float_bbox = font_float.getbbox(float_text)
    float_tw = float_bbox[2] - float_bbox[0]
    float_th = float_bbox[3] - float_bbox[1]
    float_gap = 24

    total_h = total_boxes_h + float_gap + float_th
    start_y = img.height - margin_bottom - total_h

    y = start_y
    for b in boxes:
        bw = b["tw"] + pad_x * 2
        bh = b["th"] + pad_y * 2
        x = margin_left

        draw.rectangle([x, y, x + bw, y + bh], fill=(0, 0, 0, 0), outline=purple, width=2)

        inner_fill = (0, 0, 0, 120)
        draw.rectangle([x + 2, y + 2, x + bw - 2, y + bh - 2], fill=inner_fill)

        draw.rectangle([x, y, x + bw, y + bh], outline=purple, width=2)

        text_y_offset = (bbox[1] if bbox[1] < 0 else 0)
        draw.text((x + pad_x, y + pad_y), b["text"], fill=white, font=font_box)
        y += bh + box_gap

    y += float_gap
    float_x = (img.width - float_tw) // 2
    draw.text((float_x, y), float_text, fill=white, font=font_float)

    return img


def assemble():
    print("[*] Loading panels...")
    panels = []
    cumulative_heights = []
    running_h = 0

    for i, filename in enumerate(PANEL_ORDER, 1):
        print(f"  [{i:2d}] {filename}", end="")
        img = load_panel(filename)
        orig_h = img.height

        if filename in TEXT_PANELS:
            img = trim_text_panel(img)
            print(f"  (trimmed {orig_h} >> {img.height})", end="")

        panels.append(img)
        cumulative_heights.append(running_h)
        running_h += img.height
        print(f"  >> {img.width}x{img.height}")

    total_h = running_h
    print(f"\n[*] Total strip: {TARGET_W}x{total_h}px")

    strip = Image.new("RGBA", (TARGET_W, total_h))
    y = 0
    for img in panels:
        strip.paste(img, (0, y))
        y += img.height
    out = os.path.join(CH0_DIR, "hollow_zounds_ch0_assembled.png")
    strip.convert("RGB").save(out, "PNG")
    print(f"[+] Saved: {out}")

    print("\n[done]")


if __name__ == "__main__":
    assemble()
