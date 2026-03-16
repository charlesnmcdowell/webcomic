# HOLLOW ZOUNDS — TYPOGRAPHY & TEXT STYLE GUIDE
## Version 1.0

---

## CORE PHILOSOPHY

- The art is dark, dramatic, and saturated. The text should feel **clean and intentional** against it.
- Emphasis is handled through **size, weight, and spacing** — not color. White is the only text color except where noted.
- Every text element should feel like it belongs in the world — not pasted on top of it.
- When in doubt: **less is more.** Solo Leveling's text works because it breathes.

---

## 1. TEXT-ONLY PANELS

Used for: Hollow's narration, world-building exposition, emotional beats

**Background:** Pure white `#FFFFFF`
**Text color:** Black `#1A1A1A`
**Font style:** Clean, slightly stylized sans-serif — recommended fonts:
- **Bangers** (Google Font) — high energy, reads like a comic without being too loud
- **CC Astro City** — professional comic lettering feel
- **Anime Ace** — free, webtoon-appropriate

**Layout rules:**
- Text centered horizontally
- Generous line spacing — let it breathe
- Short lines. Never more than 6 words per line if you can help it.
- Single most important word or phrase on its own line

**Emphasis:**
- Important words: **larger font size** (not a different color)
- Punchline or final beat of a text panel: **largest text on the page, sometimes all caps**
- Never use bold as emphasis — use SIZE

**Example — Panel 1:**
```
My name is Hollow Zounds.

Yeah. That's a real name.
I looked it up. It's a whole thing.

Anyway.
```
*"Anyway." should be noticeably larger than the lines above it.*

**Example — Panel 10:**
```
Just cracked open like somebody
forgot to close the refrigerator door

TO ANOTHER DIMENSION.
```
*"TO ANOTHER DIMENSION." is the biggest text in that panel.*

---

## 2. NARRATION BOXES

Used for: System-style world narration, timestamps, statistics, third-person context

**Style:** Transparent background with a **purple border**
**Border color:** Electric purple `#8B00FF` — 2–3px solid line
**Text color:** White `#FFFFFF`
**Font:** Same comic font as text-only panels, slightly smaller
**Shape:** Rectangular, sharp corners (not rounded — rounded = dialogue)
**Placement:** Top-left or bottom-left corner of panel. Never centered.
**Padding:** 8–12px inside the border on all sides

**Visual reference:**
```
┌─────────────────────────────────────┐  ← purple border
│ Somewhere in the city. 11:47 PM.    │  ← white text
└─────────────────────────────────────┘
```

**Stacked narration boxes** (like Panel 1 of Chapter 1):
- Stack vertically with 4px gap between boxes
- Each box is its own separate statement
- Do NOT combine multiple thoughts in one box

**Example — Chapter 1 Panel 1:**
```
┌──────────────────────────────────────────┐
│ Somewhere in the city. 11:47 PM.         │
└──────────────────────────────────────────┘
┌──────────────────────────────────────────┐
│ A Class-D Gate. Unexpected. Unregistered.│
└──────────────────────────────────────────┘
┌──────────────────────────────────────────┐
│ Population within blast radius: 34.      │
└──────────────────────────────────────────┘
┌──────────────────────────────────────────┐
│ Hunters in the area: 3.                  │
└──────────────────────────────────────────┘
```

---

## 3. DIALOGUE BUBBLES

Used for: Character speech

**Shape:** Rounded oval/circle — classic comic bubble
**Background:** White `#FFFFFF`
**Border:** Black `#1A1A1A`, 2px
**Text color:** Black `#1A1A1A`
**Font:** Same comic font, medium weight
**Tail:** Points directly toward the speaker's mouth

**SHOUTING / HIGH EMOTION:**
- Jagged/spiked bubble border instead of smooth oval
- Text in ALL CAPS
- Slightly larger font size
- Example: *"IT'S EXPANDING — EVERYONE RU—"*

**WHISPERING / QUIET SPEECH:**
- Dashed border instead of solid
- Slightly smaller font
- Example: *"...They see us."*

**INTERNAL MONOLOGUE:**
- NO bubble — text floats with NO border
- Italics
- Slightly smaller than dialogue
- Example: *[ I got absolutely nothing. ]*

---

## 4. SFX (SOUND EFFECTS)

Used for: KKRRRAAAACK, BONK, BOOM, DING, etc.

**Philosophy:** SFX should feel PART of the art, not sitting on top of it.
Integrate into the panel — let it overlap the art slightly.

**Style rules:**
- Large, bold, heavy weight font — recommended: **Bangers** or **Impact**
- White text `#FFFFFF` with a **black outline** (3–5px stroke)
- For BIG sounds: add a subtle **purple glow** behind the text
- For IMPACT sounds: slight diagonal tilt (5–15 degrees)
- For QUIET/eerie sounds: smaller, lighter weight, no outline

**SFX by type:**

| SFX | Size | Color | Effect |
|-----|------|-------|--------|
| KKRRRAAAACK | Massive, top of panel | White + black outline | Purple glow behind |
| BWOOOOOOM | Massive, radiating outward | White + black outline | Purple glow |
| BONK | Large but slightly smaller than BOOM | White + black outline | Slight tilt, comedic placement |
| BOOM | Large | White + black outline | Standard |
| SHHK / CRACK | Medium, sharp | White + black outline | Diagonal tilt |
| DING | Small, clean | White, thin outline | Subtle glow, floats near character |
| grrrrrrrr | Small, lowercase | White, no outline | Scattered across panel |
| CLICK | Small | White, thin outline | Near the finger/button |

**BONK specifically:**
The BONK is a comedy moment. The font should be slightly rounder and friendlier than the action SFX — same Bangers font but the placement should feel almost embarrassed, like even the sound effect knows this is ridiculous.

---

## 5. SYSTEM SCREEN TEXT

Used for: Level up notifications, stat screens, anomaly alerts

**Background:** Dark `#0D0D1A` — near black with slight blue tint
**Border:** Cold blue-white `#C8E0FF` glow effect, 2px
**Text color:** Cold blue-white `#C8E0FF`
**Font:** Monospace — recommended: **Courier New**, **Share Tech Mono**, or **VT323**
**Special:** The `ERROR` / `???` text on the Luck stat should pulse or glow slightly brighter than the rest — electric purple `#8B00FF`

**Layout:** Always centered in the panel, floating in darkness

---

## 6. CHAPTER TITLE CARDS

Used for: Chapter 0 opening text card, chapter end cards

**Background:** Full black `#000000`
**Text color:** White `#FFFFFF`
**Chapter number:** Small, light weight, all caps — sits above the title
**Chapter title:** Large, bold, centered
**Subtitle/tagline:** Small italics below

**Example:**
```
HOLLOW ZOUNDS

CHAPTER 0
"Let Me Explain."

→ Chapter 1 Starts Now
```

---

## 7. FONT STACK SUMMARY

| Element | Recommended Font | Weight | Case |
|---------|-----------------|--------|------|
| Text-only panel narration | Bangers / Anime Ace | Regular | Mixed |
| Narration boxes | Bangers / Anime Ace | Regular | Mixed |
| Dialogue | Anime Ace / CC Wild Words | Regular | Mixed |
| SFX | Bangers / Impact | Bold | ALL CAPS |
| System screen | VT323 / Share Tech Mono | Regular | Mixed |
| Chapter titles | Bangers | Bold | ALL CAPS |

**All fonts listed are free:**
- Bangers — Google Fonts
- Anime Ace — Blambot (free for personal use)
- VT323 — Google Fonts
- Share Tech Mono — Google Fonts

---

## 8. WHAT NOT TO DO

- ❌ Never use red text — that's Solo Leveling's brand
- ❌ Never use yellow/gold text — reserved for potential future special ability reveals
- ❌ Never use rounded narration boxes — rounded = dialogue only
- ❌ Never center dialogue bubbles — they follow the speaker
- ❌ Never put SFX in a box or bubble — it floats free in the art
- ❌ Never use more than 2 font sizes in a single text-only panel
- ❌ Never crowd text to the edges — always leave safe margins (10–15% from panel edge)
- ❌ Never use a drop shadow on narration box text — the purple border does that job

---

## 9. LETTERING TOOLS

| Tool | Use | Cost |
|------|-----|------|
| **Clip Studio Paint** | Full lettering suite, comic bubbles, SFX integration | Paid (one-time) |
| **Canva** | Quick text panels, title cards, narration boxes | Free tier works |
| **Adobe Illustrator** | Most precise, full control | Subscription |
| **Photoshop** | Good for SFX integration into art | Subscription |
| **Procreate** | Good for hand-lettered SFX if you want organic feel | iPad only |

**Recommended starting setup:**
Canva for text-only panels and title cards → Clip Studio Paint for dialogue and SFX on art panels. This keeps the workflow fast and cheap.

---

## 10. PANEL 1 LETTERING REFERENCE (ALREADY DONE ✅)

Your existing Panel 1 lettering established a baseline:
- KKRRRAAAACK — white, black outline, large, top of panel ✅
- Narration boxes — dark background, white text, stacked ✅

**One update for future panels:** Switch narration box background from solid dark to **transparent with purple border** as decided. Panel 1 can stay as-is for now — update in a future pass if needed.
