"""
Hollow Zounds - Panel Refiner
Uses Leonardo AI image-to-image to refine existing panel art.
"""

import requests
import time
import os
import sys
import json

API_KEY = os.environ.get("LEONARDO_API_KEY", "")
BASE_URL = "https://cloud.leonardo.ai/api/rest/v1"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "panels", "ch0")

HEADERS = {
    "accept": "application/json",
    "authorization": f"Bearer {API_KEY}"
}

HEADERS_JSON = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {API_KEY}"
}


def upload_init_image(image_path):
    """Upload an image to Leonardo AI and return the init image ID."""
    
    # Step 1: Get presigned URL
    filename = os.path.basename(image_path)
    ext = os.path.splitext(filename)[1].lstrip(".")
    
    payload = {"extension": ext}
    print(f"[*] Requesting upload URL for {filename}...")
    
    r = requests.post(f"{BASE_URL}/init-image", json=payload, headers=HEADERS_JSON)
    
    if r.status_code != 200:
        print(f"[!] Failed to get upload URL: {r.status_code} {r.text}")
        return None
    
    data = r.json()
    upload_url = data.get("uploadInitImage", {}).get("url")
    image_id = data.get("uploadInitImage", {}).get("id")
    fields_str = data.get("uploadInitImage", {}).get("fields")
    
    if not upload_url or not image_id:
        print(f"[!] Missing upload URL or image ID: {json.dumps(data, indent=2)}")
        return None
    
    print(f"[*] Init image ID: {image_id}")
    
    # Step 2: Upload the image to presigned URL
    # Parse the fields JSON string
    fields = json.loads(fields_str) if isinstance(fields_str, str) else fields_str
    
    print(f"[*] Uploading image...")
    with open(image_path, "rb") as f:
        files = {"file": (filename, f)}
        r2 = requests.post(upload_url, data=fields, files=files)
    
    if r2.status_code not in [200, 204]:
        print(f"[!] Upload failed: {r2.status_code} {r2.text[:200]}")
        return None
    
    print(f"[+] Image uploaded successfully.")
    
    # Give Leonardo a moment to process
    time.sleep(3)
    
    return image_id


def create_img2img_generation(prompt, init_image_id, negative_prompt="",
                               strength=0.3, width=864, height=1536):
    """Generate a refined image using img2img."""
    
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "num_images": 2,
        "init_image_id": init_image_id,
        "init_strength": strength,
        "alchemy": True,
        "presetStyle": "ANIME",
    }
    
    print(f"[*] Submitting img2img generation...")
    print(f"[*] Strength: {strength} (lower = closer to original)")
    print(f"[*] Prompt: {prompt[:120]}...")
    
    r = requests.post(f"{BASE_URL}/generations", json=payload, headers=HEADERS_JSON)
    
    if r.status_code != 200:
        print(f"[!] Error {r.status_code}: {r.text}")
        return None
    
    data = r.json()
    gen_id = data.get("sdGenerationJob", {}).get("generationId")
    
    if not gen_id:
        print(f"[!] No generation ID: {json.dumps(data, indent=2)}")
        return None
    
    print(f"[*] Generation ID: {gen_id}")
    return gen_id


def poll_generation(generation_id, max_wait=180, interval=5):
    """Poll until generation is complete."""
    
    url = f"{BASE_URL}/generations/{generation_id}"
    elapsed = 0
    
    while elapsed < max_wait:
        print(f"[*] Polling... ({elapsed}s elapsed)")
        r = requests.get(url, headers=HEADERS)
        
        if r.status_code != 200:
            time.sleep(interval)
            elapsed += interval
            continue
        
        data = r.json()
        gen_data = data.get("generations_by_pk", {})
        status = gen_data.get("status")
        
        if status == "COMPLETE":
            images = gen_data.get("generated_images", [])
            urls = [img.get("url") for img in images if img.get("url")]
            print(f"[+] Complete! {len(urls)} image(s)")
            return urls
        elif status == "FAILED":
            print(f"[!] Generation failed.")
            return []
        
        time.sleep(interval)
        elapsed += interval
    
    print(f"[!] Timed out after {max_wait}s")
    return []


def download_image(url, output_path):
    """Download image from URL."""
    print(f"[*] Downloading to {output_path}...")
    r = requests.get(url)
    if r.status_code == 200:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(r.content)
        print(f"[+] Saved: {output_path}")
        return True
    print(f"[!] Download failed: {r.status_code}")
    return False


# ============================================================
# PANEL 1 REFINEMENT
# ============================================================

REFINE_PROMPT = (
    "manhwa webtoon panel, dark night city scene, "
    "a jagged asymmetric CRACK tearing across the sky like shattered glass, "
    "the crack is an irregular diagonal slash not a centered circle, "
    "void darkness visible through the crack, "
    "purple-black energy and lightning radiating from the fracture, "
    "small realistic debris floating upward, "
    "7-Eleven convenience store on the left with glowing sign, "
    "parked car in foreground reflecting purple light, "
    "inner city American street at night, "
    "clean cel-shaded digital comic art, dark dramatic lighting, "
    "deep blacks, electric purple, manhwa illustration style"
)

REFINE_NEGATIVE = (
    "blurry, low quality, watermark, text, speech bubbles, "
    "symmetrical gate, circular portal, starburst shape, "
    "cartoonish, chibi, bright daylight"
)


if __name__ == "__main__":
    source = os.path.join(OUTPUT_DIR, "panel 1.jpg")
    
    if not os.path.exists(source):
        print(f"[!] Source image not found: {source}")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"  HOLLOW ZOUNDS - Refining Panel 1 via img2img")
    print(f"{'='*60}\n")
    
    # Upload the source image
    image_id = upload_init_image(source)
    if not image_id:
        print("[!] Failed to upload source image.")
        sys.exit(1)
    
    # Generate refined version (strength 0.3 = 70% original, 30% new)
    gen_id = create_img2img_generation(
        REFINE_PROMPT, image_id,
        negative_prompt=REFINE_NEGATIVE,
        strength=0.3
    )
    if not gen_id:
        print("[!] Failed to start generation.")
        sys.exit(1)
    
    # Poll and download
    urls = poll_generation(gen_id)
    if not urls:
        print("[!] No images returned.")
        sys.exit(1)
    
    saved = []
    for i, url in enumerate(urls):
        suffix = chr(97 + i)
        out_path = os.path.join(OUTPUT_DIR, f"panel_01_refined_{suffix}.png")
        if download_image(url, out_path):
            saved.append(out_path)
    
    print(f"\n[+] Done! {len(saved)} refined variation(s) saved:")
    for s in saved:
        print(f"    {s}")
