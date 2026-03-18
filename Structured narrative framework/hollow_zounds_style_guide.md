# HOLLOW ZOUNDS — VISUAL STYLE GUIDE
## Prompt Bible & Consistency Reference

---

## THE ANCHOR PROMPT (Panel 1 — Verified, Publication Quality)

Use this as the baseline reference for every background/environment panel.

```
Create a single vertical webtoon/manhwa panel (9:16 aspect ratio). 
Scene: A low-angle shot from street level looking up at the night sky 
over an inner-city American block. A massive jagged crack is tearing 
open the sky — not a circle or a beam, but like broken glass shattering 
reality itself, revealing pure void darkness behind it. Purple-black 
energy and lightning arc outward from the fracture. Small debris (trash, 
a newspaper, gravel) floats upward toward the rift, defying gravity. 
On the left side of the street, a 7-Eleven convenience store with its 
iconic lit sign is the only warm light source. A parked sedan sits in 
the foreground, its hood reflecting the purple glow from above. The 
street is empty, dark, and still — the moment right after the crack 
appeared. Style: Dark, dramatic Korean manhwa / webtoon illustration. 
Clean ink linework with cel-shaded coloring. Think Solo Leveling 
background art — highly detailed environments, deep blacks, dramatic 
rim lighting, and saturated purple energy effects against a dark palette. 
This is a full-bleed vertical panel with no borders. No characters 
visible. No text, no speech bubbles, no sound effects, no watermarks. 
Color palette: Midnight black, deep indigo, electric purple, magenta 
highlights. The only non-purple light is the warm yellow-green glow 
of the 7-Eleven sign.
```

**Generated in:** Grok (base image) → Leonardo AI (upscale + fixes)
**Final rating:** 9/10 — publication quality

---

## CORE STYLE RULES (Apply to Every Panel)

These rules must be present in every prompt you write.

### Always Include:
- `single vertical webtoon/manhwa panel, 9:16 aspect ratio`
- `dark dramatic Korean manhwa illustration`
- `clean ink linework with cel-shaded coloring`
- `Solo Leveling background art style`
- `highly detailed environments, deep blacks, dramatic rim lighting`
- `saturated purple energy effects against dark palette`
- `full-bleed vertical panel, no borders`
- `no text, no speech bubbles, no sound effects, no watermarks`

### Always Specify What It's NOT:
This is what made Panel 1 work. Tell the AI what to avoid:
- `not a circle, not a beam` (for the gate)
- `no splotches on the car` (for vehicle panels)
- `no AI artifacts on signage` (for real-world location panels)
- `no symmetrical composition` (for city/environment panels)

### Color Palette (Lock These):
| Color | Use |
|-------|-----|
| Midnight black `#0a0a0f` | Shadows, backgrounds, void |
| Deep indigo `#1a0533` | Sky, dungeon atmosphere |
| Electric purple `#8b00ff` | Gate energy, lightning, accents |
| Magenta highlight `#ff00cc` | Rim lighting, energy peaks |
| Warm yellow-green `#c8d400` | 7-Eleven sign, real-world warmth |
| Cold white `#e8f0ff` | Lightning cracks, system UI glow |

---

## TWO-TOOL PIPELINE

**Step 1 — Grok** (base image generation)
- Use for: initial panel generation
- Strengths: follows complex scene descriptions well, good composition

**Step 2 — Leonardo AI** (upscale + fixes)
- Use for: upscaling, fixing AI text artifacts, removing splotches, sharpening linework
- Always upscale to: `1080x1920px` (9:16 vertical)
- Use img2img for targeted fixes (sign text, car surface, faces)

---

## PROMPT TEMPLATES BY PANEL TYPE

### Environment Panel (No Characters)
```
Create a single vertical webtoon/manhwa panel (9:16 aspect ratio).
Scene: [DESCRIBE THE LOCATION AND ACTION].
Style: Dark, dramatic Korean manhwa illustration. Clean ink linework 
with cel-shaded coloring. Solo Leveling background art style. 
Highly detailed environments, deep blacks, dramatic rim lighting, 
saturated purple energy effects against dark palette.
Full-bleed vertical panel, no borders.
No characters visible. No text, no speech bubbles, no sound effects, 
no watermarks.
Color palette: Midnight black, deep indigo, electric purple, magenta 
highlights.
[ADD ANY NEGATIVE INSTRUCTIONS SPECIFIC TO THIS PANEL]
```

### Character Panel (With Hollow)
```
Create a single vertical webtoon/manhwa panel (9:16 aspect ratio).
Scene: [DESCRIBE THE SCENE AND HOLLOW'S POSITION/ACTION].
Character: Black American male, 18 years old, 5'4", slightly athletic 
build. Long dreadlocks with purple accent streaks. Wearing oversized 
anime graphic tee and joggers. Cheap practice sword strapped to back. 
Expression: [DESCRIBE EXPRESSION — deadpan / mildly inconvenienced / 
confident / zoning out].
Style: Dark, dramatic Korean manhwa illustration. Clean ink linework 
with cel-shaded coloring. Solo Leveling character art style. 
Dramatic rim lighting, deep blacks, saturated purple energy accents.
Full-bleed vertical panel, no borders.
No text, no speech bubbles, no sound effects, no watermarks.
Color palette: Midnight black, deep indigo, electric purple, magenta 
highlights, warm skin tones.
```

### Reaction/Close-Up Panel
```
Create a single vertical webtoon/manhwa panel (9:16 aspect ratio).
Scene: Extreme close-up on [CHARACTER]'s face. Expression: [DESCRIBE].
[DESCRIBE WHAT THEY ARE REACTING TO — visible in background or implied].
Style: Dark, dramatic Korean manhwa illustration. Clean ink linework 
with cel-shaded coloring. Dramatic rim lighting from [DIRECTION]. 
Deep blacks, saturated purple energy in background.
Full-bleed vertical panel, no borders.
No text, no speech bubbles, no sound effects, no watermarks.
```

### System Screen Panel
```
Create a single vertical webtoon/manhwa panel (9:16 aspect ratio).
Scene: A dark holographic system notification screen floating in 
mid-air, glowing with cold blue-white light. Dark background. 
The screen has a rectangular border with geometric UI elements.
Center of screen is dark/blank — text will be added in post.
Style: Korean manhwa UI design, Solo Leveling system screen aesthetic.
Glowing edges, dark void background, subtle purple atmospheric glow.
Full-bleed vertical panel, no borders.
No pre-existing text on the screen. No watermarks.
```

---

## HOLLOW ZOUNDS — CHARACTER REFERENCE NOTES

Lock these details for every panel he appears in:

| Feature | Description |
|---------|-------------|
| Hair | Long dreadlocks, purple accent streaks throughout |
| Build | 5'4", slightly athletic — not intimidating looking |
| Default outfit | Oversized anime graphic tee, joggers, beat-up sneakers |
| Weapon | Cheap practice sword on back (breaks frequently) |
| Expression default | Deadpan / mildly unbothered |
| Eye quality | Looks like he's either deep in thought or completely checked out |
| Vibe | Looks like the LAST person who should be in a dungeon |

---

## PANEL SIZE REFERENCE

| Panel Type | Script Label | Approximate Height |
|------------|--------------|-------------------|
| Tall reveal | FULL | 2000–2500px |
| Standard | HALF | 1000–1400px |
| Quick beat | THIRD | 600–900px |
| Cinematic slice | WIDE | 500–700px |

All panels: **1080px wide**
Export slices: **max 3000px tall per slice** for webtoon platform loading

---

## WHAT TO FIX IN LEONARDO (RECURRING AI ISSUES)

| Problem | Leonardo Fix |
|---------|--------------|
| Sign text garbled | Use img2img, mask the sign, re-prompt with exact text |
| Purple splotches on surfaces | Inpaint the affected area, re-prompt clean surface |
| Hands/fingers wrong | Inpaint hands, use "correct hand anatomy" in prompt |
| Face looks off | Inpaint face region, increase face detail slider |
| Square output from Grok | Upscale and extend canvas to 1080x1920 in Leonardo |

---

## FILES IN THIS PROJECT

| File | Description |
|------|-------------|
| `hollow_zounds_character_sheet_v3.md` | Full character bible |
| `hollow_zounds_ch0_script_v2.md` | Chapter 0 full script, 33 panels |
| `hollow_zounds_style_guide.md` | This file — prompt bible |
| `panel_1_upscale_v2.jpg` | Anchor panel — visual reference for all future panels |

---

> **Rule #1:** When in doubt, go back to the Panel 1 prompt and modify from there.
> It works. Don't reinvent it. Just adapt it.
