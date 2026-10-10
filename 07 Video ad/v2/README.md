# Firsts Fund ad, v2 (Remotion)

A 30-second ad. v1 felt too slow, so v2 cuts on the beat (124 BPM, a cut roughly every 1–2 seconds).
It tells the viewer two things: whether the fund is for them, and how to start. Holdings and technical details are left out.
English only. The look is clean and modern: warm off-white paper, ink, one emerald accent, Geist throughout (small labels in uppercase with wide spacing),
masked text reveals, and thin line graphics.

**Message:** fund your firsts, and keep the habit, because there will always be a new first.
**Audience:** early-career Filipinos with a goal at least five years away.

## Storyboard (beats in `src/timeline.json`; 1 beat = 0.48 s)

| Time | Scene | What happens |
|---|---|---|
| 0.0–2.9 | Intro | "SALARY CREDITED" chip · **You just got your first paycheck.** → **What do you do first?** The text clears and leaves one green dot |
| 2.9–11.6 | Five firsts, 1.7 s each | Each has its own graphic, and each starts from the last frame of the one before (see below) |
| 11.6–13.5 | Message | The notebook lines retract; five dots (the five firsts) gather into a ring · **Fund your firsts.** (underlined) |
| 13.5–21.8 | Calculator | Step 01 name your first · 02 amount (₱150,000) · 03 when (slider dragged to 2 years snaps back to the 5-year minimum) · ₱2,500 / month (contributions only) · Start with ₱100 · the card shrinks into a list and three next firsts stack under it |
| 21.8–24.2 | Payoff | Counter FIRST 06 → 99 → ∞ · **There will always be a new first.** |
| 24.2–27.1 | Logo | Dark panel rises · ring draws · Firsts Fund · Fund your firsts. · Start with as little as ₱100 |
| 27.1–30.0 | Legal | Proposed-fund and UITF disclaimers |

### The five firsts and their transitions

| # | First | Motion graphic | How it enters |
|---|---|---|---|
| 01 | Take Mom & Dad abroad. | Dotted flight path MNL → TYO on a dot grid; the plane follows the curve | The intro's green dot becomes Manila |
| 02 | Buy your first car. | Car drives in with speed lines; wheels spin; lane dashes scroll | The flight path straightens into the road |
| 03 | Get your first home. | Building stacks up floor by floor; one window lights up | The car speeds off, the ground line stays |
| 04 | Open your first business. | Storefront draws itself, shutter rolls up, OPEN sign swings | Zoom through the lit window; the green folds down into the shop's awning |
| 05 | Their first day of school. | Notebook page; "ABC" and a star are drawn by hand | The OPEN sign flips over and becomes the page |

The small ring next to each "FIRST 0n" label fills by one fifth each time. That's the habit motif, and it returns as the logo.

The calculator matches how the real one (still being built) works: monthly contribution = amount ÷ months, with a 5-year minimum.
The ad shows **contributions only, with no assumed return**, so it promises no growth.

## Sound

| Layer | Source | Notes |
|---|---|---|
| Voice-over | ElevenLabs, voice **Justin Case - Warm, Trustworthy, Clear**, model eleven_v4 | One take of the whole script (`assets/elevenlabs/vo_justin_case_take3.mp3`), cut into 16 lines by `scripts/prepare_audio.py` and placed on the cuts (`src/vo.json`) |
| Sound effects | ElevenLabs Sound Effects v2 | Notification, whoosh, plane, car, stacking blocks, shutter, page flip, pencil, typing, click, success chime, boom, riser (`assets/elevenlabs/sfx/`) |
| Music | Placeholder, synthesised (`scripts/make_audio.py`) | The ElevenLabs connector here has no music generation. Dips automatically under the voice |

Voice-over script (timings in `src/vo.json`):

> You just got your first paycheck. So… what do you do first?
> Take Mom and Dad abroad. Your first car. Your first home. Your first business. Their first day of school.
> Fund your firsts.
> Name your first. Set the amount. Pick a date five years or more away. See what to set aside each month… and start with as little as one hundred pesos.
> Because there will always be a new first.
> Firsts Fund. Fund your firsts.

## Run it

```bash
npm install
npm run audio            # regenerate the placeholder music bed (python3 + numpy)
python3 scripts/prepare_audio.py   # re-cut the voice-over and clean the SFX (needs ffmpeg)
npm run studio           # preview / edit in the browser
npm run render           # out/FirstsFund_Ad_v2.mp4      (1920×1080)
npm run render:vertical  # out/FirstsFund_Ad_v2_9x16.mp4 (1080×1920, Reels/TikTok)
```

If Chrome won't launch (e.g. in a cloud container), point Remotion at a headless shell: `REMOTION_BROWSER=/path/to/headless_shell npm run render`.
Fonts (Geist Sans, plus Inter for the ₱ sign; both OFL) are bundled in `public/fonts`, so rendering needs no network.

## Files

| File | What it does |
|---|---|
| `src/timeline.json` | Tempo and every scene boundary, in beats. Change timing here; video and music both follow it |
| `src/Ad.tsx` | Puts the scenes and sound cues on the timeline |
| `src/lib.tsx` | Fonts, colours, easing, layout (the shared 1000 × 600 stage), text reveal, caption |
| `src/Firsts.tsx` | The five firsts and their chained transitions |
| `src/Story.tsx` | Intro, "Fund your firsts.", pause, payoff, logo, legal |
| `src/Calc.tsx` | The onboarding calculator and its sound cues |
| `scripts/make_audio.py` | Synthesises the placeholder music bed, following `timeline.json` |
| `scripts/prepare_audio.py` | Cuts the ElevenLabs voice-over into lines (writes `src/vo.json`) and cleans the ElevenLabs SFX |
| `assets/elevenlabs/` | Original ElevenLabs downloads (voice take and SFX) |

## Before release

- [x] Voice-over (ElevenLabs, Justin Case) and sound effects (ElevenLabs).
- [ ] **Music:** `public/audio/music.wav` is a synthesised placeholder. Replace it with a licensed 120–128 BPM track (Artlist, Epidemic, Uppbeat, YouTube Audio Library), keep the file name, and line its drops up with 11.6 s ("Fund your firsts.") and 22.7 s. If the tempo differs, change `bpm` in `timeline.json`.
- [ ] Team check: the lines, the example first (Japan, ₱150,000, 5 years), and the legal text.
- [ ] Keep calculator wording in line with the real calculator once it is built.
