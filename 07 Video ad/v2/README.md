# Firsts Fund ad, v2 (Remotion)

A 30-second ad. v1 felt too slow, so v2 cuts on the beat (124 BPM, a cut roughly every 1–2 seconds).
It tells the viewer two things: whether the fund is for them, and how to start. Holdings and technical details are left out.

**Message:** fund your firsts, and keep the habit, because there is always a new first.
**Audience:** early-career Filipinos with a goal at least five years away.

## Storyboard (beats in `src/timeline.json`; 1 beat = 0.48 s)

| Time | Scene | On screen |
|---|---|---|
| 0.0–1.9 | Hook | Payroll notification · **First paycheck? Fund your next firsts.** |
| 1.9–7.7 | Montage, 6 × 1 s | Firsts that take 5+ years: trip abroad with Ma & Pa · kotse · condo · "I do" · negosyo · first school year of your child. Counter First #1–#6; a coin drops into a ring that fills a little more each time (the habit motif) |
| 7.7–8.7 | Turn | **Paano magsimula?** |
| 8.7–21.3 | Onboarding calculator | 1 Name your first (*Japan with Ma & Pa*) · 2 Magkano? (₱150,000) · 3 Kailan? (slider dragged to 2 years snaps back to the **5-year minimum**) · **₱2,500 / buwan** (₱150,000 ÷ 60, contributions only) · Start with as little as ₱100 · + Add your next first (car, condo DP, retirement trip) |
| 21.3–22.3 | Silence | Black, music stops |
| 22.3–24.2 | Payoff | #7 → ∞ · **There's always a new first.** (the beat drops) |
| 24.2–27.1 | Logo | Firsts Fund · **Fund your firsts.** · Start with as little as ₱100 |
| 27.1–30.0 | Legal | Proposed-fund and UITF disclaimers |

The calculator matches how the real one (still being built) works: monthly contribution = amount ÷ months, with a 5-year minimum.
The ad shows **contributions only, with no assumed return**, so it promises no growth.

## Run it

```bash
npm install
npm run audio            # regenerate placeholder music + SFX (python3 + numpy)
npm run studio           # preview / edit in the browser
npm run render           # out/FirstsFund_Ad_v2.mp4      (1920×1080)
npm run render:vertical  # out/FirstsFund_Ad_v2_9x16.mp4 (1080×1920, Reels/TikTok)
```

If Chrome won't launch (e.g. in a cloud container), point Remotion at a headless shell: `REMOTION_BROWSER=/path/to/headless_shell npm run render`.
Fonts (Poppins, OFL) are bundled in `public/fonts`, so rendering needs no network.

## Files

| File | What it does |
|---|---|
| `src/timeline.json` | Tempo and every scene boundary, in beats. Change timing here; video and music both follow it |
| `src/Ad.tsx` | Puts the scenes and sound cues on the timeline |
| `src/Scenes.tsx` | Hook, montage cards, "Paano magsimula?", silence, payoff, logo, legal |
| `src/Phone.tsx` | The onboarding calculator on the phone, plus its sound cues |
| `src/icons.tsx` | Line icons for each first (drawn in code, no image assets) |
| `scripts/make_audio.py` | Synthesises a placeholder beat and SFX that follow `timeline.json` |

## Before release

- [ ] **Music:** `public/audio/music.wav` is a synthesised placeholder. Replace it with a licensed 120–128 BPM track (Artlist, Epidemic, Uppbeat, YouTube Audio Library), keep the file name, and line its drop up with 23.3 s. If the tempo differs, change `bpm` in `timeline.json`.
- [ ] SFX (`public/audio/*.wav`) are synthesised and free to use. Swap in better ones if you have a library.
- [ ] Team check: Taglish lines, the example first (Japan, ₱150,000, 5 years), and the legal text.
- [ ] Keep calculator wording in line with the real calculator once it is built.
