"""
Hollow Zounds - Panel Generator
Calls Leonardo AI API to generate webcomic panel art from script descriptions.
"""

import requests
import time
import os
import sys
import json

# --- CONFIG ---
API_KEY = os.environ.get("LEONARDO_API_KEY", "")
BASE_URL = "https://cloud.leonardo.ai/api/rest/v1"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "panels", "ch0")

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {API_KEY}"
}


def create_generation(prompt, negative_prompt="", width=864, height=1536,
                      num_images=4, preset="DYNAMIC", model_id=None):
    """Submit an image generation request to Leonardo AI."""

    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "num_images": num_images,
        "alchemy": True,
        "highResolution": True,
        "presetStyle": preset,
        "photoReal": False,
    }

    if model_id:
        payload["modelId"] = model_id

    url = f"{BASE_URL}/generations"
    print(f"[*] Submitting generation request...")
    print(f"[*] Preset: {preset}")
    print(f"[*] Images: {num_images}")
    print(f"[*] Prompt: {prompt[:150]}...")
    if negative_prompt:
        print(f"[*] Negative: {negative_prompt[:100]}...")

    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code != 200:
        print(f"[!] Error {response.status_code}: {response.text}")
        return None

    data = response.json()
    generation_id = data.get("sdGenerationJob", {}).get("generationId")

    if not generation_id:
        print(f"[!] No generation ID returned. Response: {json.dumps(data, indent=2)}")
        return None

    print(f"[*] Generation ID: {generation_id}")
    return generation_id


def poll_generation(generation_id, max_wait=180, interval=5):
    """Poll until the generation is complete and return image URLs."""

    url = f"{BASE_URL}/generations/{generation_id}"
    elapsed = 0

    while elapsed < max_wait:
        print(f"[*] Polling... ({elapsed}s elapsed)")
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"[!] Poll error {response.status_code}: {response.text}")
            time.sleep(interval)
            elapsed += interval
            continue

        data = response.json()
        gen_data = data.get("generations_by_pk", {})
        status = gen_data.get("status")

        if status == "COMPLETE":
            images = gen_data.get("generated_images", [])
            urls = [img.get("url") for img in images if img.get("url")]
            print(f"[+] Generation complete! {len(urls)} image(s) ready.")
            return urls
        elif status == "FAILED":
            print(f"[!] Generation failed.")
            return []

        time.sleep(interval)
        elapsed += interval

    print(f"[!] Timed out after {max_wait}s")
    return []


def download_image(url, output_path):
    """Download an image from URL and save it."""
    print(f"[*] Downloading to {output_path}...")
    response = requests.get(url)

    if response.status_code == 200:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"[+] Saved: {output_path}")
        return True
    else:
        print(f"[!] Download failed: {response.status_code}")
        return False


def generate_panel(panel_num, prompt, negative_prompt="", output_dir=OUTPUT_DIR,
                   num_images=4, preset="DYNAMIC"):
    """Full pipeline: generate images from prompt and save to disk."""

    gen_id = create_generation(prompt, negative_prompt=negative_prompt,
                               num_images=num_images, preset=preset)
    if not gen_id:
        return []

    urls = poll_generation(gen_id)
    if not urls:
        return []

    saved = []
    for i, url in enumerate(urls):
        suffix = chr(97 + i)  # a, b, c, d
        filename = f"panel_{panel_num:02d}_{suffix}.png"
        output_path = os.path.join(output_dir, filename)
        if download_image(url, output_path):
            saved.append(output_path)

    return saved


# ============================================================
# PANEL 1 — COLD OPEN: THE GATE
# ============================================================

PANEL_1_PROMPT = (
    "dramatic manhwa illustration, dark urban night scene, "
    "low angle looking up from street level, "
    "a huge jagged crack tearing open the night sky like shattered glass, "
    "purple-black void energy pouring through the crack, lightning arcing from it, "
    "small debris floating upward toward the rift, "
    "inner city American street below with a 7-Eleven store glowing on one side, "
    "a parked car in the foreground reflecting purple light, "
    "dark cinematic atmosphere, deep shadows, rim lighting from the portal, "
    "cel-shaded digital art, clean linework, Korean webtoon style, "
    "Solo Leveling inspired, detailed background art, vertical composition"
)

PANEL_1_NEGATIVE = (
    "text, words, speech bubbles, watermark, signature, "
    "blurry, low quality, photograph, 3D render, "
    "daylight, bright, happy, cute, chibi"
)


if __name__ == "__main__":
    panel_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    if panel_num == 1:
        prompt = PANEL_1_PROMPT
        negative = PANEL_1_NEGATIVE
    else:
        print(f"[!] Panel {panel_num} prompt not defined yet.")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  HOLLOW ZOUNDS - Generating Panel {panel_num} (2 variations)")
    print(f"{'='*60}\n")

    results = generate_panel(panel_num, prompt, negative_prompt=negative,
                             num_images=2, preset="ILLUSTRATION")

    if results:
        print(f"\n[+] SUCCESS! {len(results)} variations saved:")
        for r in results:
            print(f"    {r}")
    else:
        print(f"\n[!] FAILED to generate panel {panel_num}")
        sys.exit(1)
