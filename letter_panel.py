"""
Hollow Zounds - Panel Letterer
Adds SFX text and narration boxes to panel art in Solo Leveling manhwa style.
Converts square panels to vertical webtoon format (1080x1920).
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor
import os
import numpy as np

PANELS_DIR = os.path.join(os.path.dirname(__file__), "panels", "ch0")
FONTS_DIR = r"C:\Windows\Fonts"

IMPACT = os.path.join(FONTS_DIR, "impact.ttf")
ARIAL_BOLD = os.path.join(FONTS_DIR, "arialbd.ttf")

TARGET_W = 1080
TARGET_H = 1920
TARGET_RATIO = TARGET_W / TARGET_H  # 0.5625


def convert_to_vertical(img, top_extend=500):
    """Convert a square image to 9:16 vertical webtoon format.
    Extends the top with a heavily blurred, darkened mirror of the sky area.
    Blends the seam by Gaussian-blurring a strip around the join point.
    """
    w, h = img.size
    img = img.convert("RGBA")

    # Take a generous top chunk, flip and blur it for a soft dark sky
    mirror_h = min(top_extend + 100, h // 2)
    mirror_strip = img.crop((0, 0, w, mirror_h))
    mirror_strip = mirror_strip.transpose(Image.FLIP_TOP_BOTTOM)
    mirror_ext = mirror_strip.resize((w, top_extend), Image.LANCZOS)
    mirror_ext = mirror_ext.filter(ImageFilter.GaussianBlur(radius=40))

    dark_overlay = Image.new("RGBA", mirror_ext.size, (5, 2, 12, 170))
    mirror_ext = Image.alpha_composite(mirror_ext, dark_overlay)

    new_h = h + top_extend
    canvas = Image.new("RGBA", (w, new_h), (5, 2, 12, 255))
    canvas.paste(mirror_ext, (0, 0))
    canvas.paste(img, (0, top_extend))

    # Blur the seam zone: extract a strip across the join, blur it, paste back
    seam_margin = 80
    seam_y0 = max(0, top_extend - seam_margin)
    seam_y1 = min(new_h, top_extend + seam_margin)
    seam_strip = canvas.crop((0, seam_y0, w, seam_y1))
    seam_strip = seam_strip.filter(ImageFilter.GaussianBlur(radius=30))

    # Create a vertical gradient mask so the blur fades at edges of the strip
    strip_h = seam_y1 - seam_y0
    seam_mask = Image.new("L", (w, strip_h), 0)
    seam_mask_draw = ImageDraw.Draw(seam_mask)
    for y in range(strip_h):
        dist_from_center = abs(y - strip_h // 2)
        t = 1.0 - (dist_from_center / (strip_h / 2))
        seam_mask_draw.line([(0, y), (w, y)], fill=int(255 * t * t))

    canvas.paste(seam_strip, (0, seam_y0), seam_mask)

    crop_w = int(new_h * TARGET_RATIO)
    if crop_w > w:
        crop_w = w
        crop_h = int(w / TARGET_RATIO)
        y_offset = (new_h - crop_h) // 2
        cropped = canvas.crop((0, y_offset, w, y_offset + crop_h))
    else:
        x_offset = (w - crop_w) // 2
        cropped = canvas.crop((x_offset, 0, x_offset + crop_w, new_h))

    result = cropped.resize((TARGET_W, TARGET_H), Image.LANCZOS)
    print(f"[*] Converted to vertical: {result.size}")
    return result


def draw_outlined_text(draw, xy, text, font, fill="white", outline_fill="black",
                       outline_width=4):
    """Draw text with a thick outline by stamping the text in offsets."""
    x, y = xy
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx * dx + dy * dy <= outline_width * outline_width:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_fill)
    draw.text(xy, text, font=font, fill=fill)


def create_sfx_layer(size, text, font, position, rotation=0,
                     glow_color=(140, 0, 255), glow_radius=18):
    """Create an SFX text layer with purple glow, outline, and optional rotation."""
    expand = 300
    layer = Image.new("RGBA", (size[0] + expand * 2, size[1] + expand * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    bbox = font.getbbox(text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    tx = position[0] + expand
    ty = position[1] + expand

    glow_layer = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            glow_draw.text((tx + dx, ty + dy), text, font=font,
                           fill=(*glow_color, 120))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=glow_radius))

    draw_outlined_text(draw, (tx, ty), text, font,
                       fill="white", outline_fill="black", outline_width=6)

    combined = Image.alpha_composite(glow_layer, layer)

    if rotation != 0:
        combined = combined.rotate(rotation, resample=Image.BICUBIC, expand=False)

    result = combined.crop((expand, expand, expand + size[0], expand + size[1]))
    return result


def draw_narration_box(draw, position, text, font, box_width,
                       bg_color=(10, 5, 18, 210),
                       border_color=(120, 50, 200, 180),
                       text_color=(220, 225, 240, 255),
                       padding=16, border_width=2):
    """Draw a Solo Leveling-style narration box with dark bg and subtle purple border."""
    x, y = position

    bbox = font.getbbox(text)
    text_h = bbox[3] - bbox[1]
    box_h = text_h + padding * 2

    box_coords = [x, y, x + box_width, y + box_h]
    draw.rectangle(box_coords, fill=bg_color)
    draw.rectangle(box_coords, outline=border_color, width=border_width)

    accent_coords = [x, y, x + 3, y + box_h]
    draw.rectangle(accent_coords, fill=(140, 60, 220, 230))

    draw.text((x + padding + 4, y + padding - 2), text, font=font, fill=text_color)
    return box_h


def letter_panel_1():
    source_path = os.path.join(PANELS_DIR, "panel 1.jpg")
    output_path = os.path.join(PANELS_DIR, "panel 1 lettered.png")

    img = Image.open(source_path).convert("RGBA")
    print(f"[*] Original image: {img.size}")

    img = convert_to_vertical(img, top_extend=500)
    w, h = img.size
    print(f"[*] Working canvas: {w}x{h}")

    # --- SFX: KKRRRAAAACK ---
    sfx_font_size = int(w * 0.115)
    sfx_font = ImageFont.truetype(IMPACT, sfx_font_size)

    sfx_text = "KKRRRAAAACK"
    sfx_bbox = sfx_font.getbbox(sfx_text)
    sfx_w = sfx_bbox[2] - sfx_bbox[0]

    sfx_x = (w - sfx_w) // 2
    sfx_y = int(h * 0.10)

    sfx_layer = create_sfx_layer(
        img.size, sfx_text, sfx_font,
        position=(sfx_x, sfx_y),
        rotation=-5,
        glow_color=(140, 0, 255),
        glow_radius=20
    )
    img = Image.alpha_composite(img, sfx_layer)

    # --- NARRATION BOXES ---
    narration_lines = [
        "Somewhere in the city. 11:47 PM.",
        "A Class-D Gate. Unexpected. Unregistered.",
        "Population within blast radius: 34.",
        "Hunters in the area: 3.",
    ]

    narr_font_size = int(w * 0.028)
    narr_font = ImageFont.truetype(ARIAL_BOLD, narr_font_size)

    box_width = int(w * 0.62)
    box_margin = int(w * 0.04)
    box_spacing = int(h * 0.006)
    start_y = int(h * 0.82)

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    current_y = start_y
    for line in narration_lines:
        box_h = draw_narration_box(
            overlay_draw,
            position=(box_margin, current_y),
            text=line,
            font=narr_font,
            box_width=box_width,
        )
        current_y += box_h + box_spacing

    img = Image.alpha_composite(img, overlay)

    img_rgb = img.convert("RGB")
    img_rgb.save(output_path, quality=95)
    print(f"[+] Saved lettered panel: {output_path} ({w}x{h})")
    return output_path


if __name__ == "__main__":
    letter_panel_1()
