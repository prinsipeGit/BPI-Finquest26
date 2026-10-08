# Master Instructions: Firsts Fund 30-Second Motion Graphics Ad

**Version:** 2.0 (2026-10-08). Replaces the first draft. Changes are listed at the end.
**Output folder:** `07 Marketing video/` (Remotion project in `remotion/`, audio in `remotion/public/audio/`, final render in `render/`).

---

## 1. Role and objective

You are a motion graphics director, creative strategist and Remotion developer. Produce a finished 30-second ad for **Firsts Fund**, a proposed actively managed global equity UITF under BPI Wealth, entered in BPI Wealth FinQuest 2026 by Team Los Angeles 76ers.

Tools:
- **Remotion** (React + TypeScript) for composition, animation and rendering.
- **ElevenLabs** for the voiceover. Sound effects too, if the connector supports them.
- Custom SVGs, typography and programmatic motion for every visual.

The deliverable is a **rendered MP4**. A storyboard, script or code sample alone doesn't count.

The ad plays at the Final Showdown right before the team's pitch. Judges score cohesion and originality, so the ad has to look like *this* fund's ad, not a generic investing ad. It should feel art-directed by an agency, not like an AI-made slideshow.

## 2. Campaign

| Item | Spec |
| --- | --- |
| Product name | **Firsts Fund** (never "The Firsts Fund") |
| Institution | BPI Wealth (text wordmark only, see Section 3A) |
| Tagline | **FUND YOUR FIRSTS.** This is the one line viewers should remember |
| Supporting line | "Every first begins somewhere." Optional, opening only |
| Duration | Exactly 30.0 s = **900 frames** |
| Format | 1920 × 1080, 16:9, 30 fps, H.264 MP4, AAC stereo 48 kHz |
| Audience | Young Filipinos aged 21–30: graduating students, fresh graduates, early-career professionals |

**Core insight:** You're just starting out, but you already have big firsts ahead of you.

**What makes this fund different (use it, don't explain it):** Firsts Fund invests in listed companies around the world that own, run or supply the essentials everyday life depends on: **power, water, telecom networks, ports, airports and hospitals**. The creative bridge is simple. *Your future firsts run on these essentials, and the fund invests in the companies behind them.*

**How firsts are used in the ad (this keeps it consistent with the fact sheet):**
- **First paycheck = the starting point.** It's the money you invest *with*, not a goal you invest toward.
- **Firsts the fund saves toward = goals five or more years away:** a first home, a first business, further study, a first big family milestone. The fact sheet says the fund is "not suitable for money needed within five years."
- **Don't use short-term goals** as things to invest for. That rules out a first trip, a first gadget and a first car bought next year.

## 3. Creative and visual direction

### A. Aesthetic
Clean, contemporary, premium fintech motion design: minimal compositions, generous negative space, kinetic typography, elegant vector line art, light parallax and depth, strong continuity between scenes.

**Palette** (matches the Phase 2 fact sheet so the ad, deck and fact sheet look like one set):

| Token | Hex | Use |
| --- | --- | --- |
| `green` | `#0F7A45` | Primary brand color, end card |
| `greenDeep` | `#142019` | Dark backgrounds, text on light |
| `greenLight` | `#5FC48C` | Highlights, active paths |
| `mist` | `#C9D6CE` | Secondary lines, inactive nodes |
| `paper` | `#F5F4EE` | Warm-white backgrounds |
| `amber` | `#C9761F` | One accent only: the "first step" dot and the CTA |
| `grey` | `#9AA39D` | Disclaimer text |

**Typography:** one modern sans-serif loaded through `@remotion/google-fonts` (Inter or Plus Jakarta Sans), in two weights at most. Minimum on-screen text size is **36 px for supers and 28 px for the disclaimer**. Keep all text inside a 96 px safe margin.

**Brand marks:** don't redraw or imitate the official BPI or BPI Wealth logo. Set "BPI Wealth" as plain text in the ad's typeface. Nothing on screen may claim that BPI has approved or launched the product.

**Filipino grounding:** include one or two local cues as line art, such as a Manila or BGC skyline silhouette, a condo window or a jeepney. A peso sign (₱) is the only currency symbol on screen.

**Avoid:** stock footage, random 3D objects, clutter, inconsistent illustration styles, rising line or bar charts, upward-arrow "growth" graphics, coins piling up, and any number other than ₱100 and "5 years."

### B. Animation philosophy
Every scene grows out of the one before it. Avoid cuts that look like slides being swapped, and don't use fades as the main transition.

**The motif chain, which holds the whole ad together:**
1. An amber **dot** (the first paycheck, the first step)
2. The dot draws a **path**
3. The path **branches** into several future firsts (home, business, study, family)
4. Each first's line art **traces back** to an essential: power line, water pipe, signal tower, port crane, runway, hospital cross
5. The branches **gather** into one steady line: a journey contributed to over time, drawn as even spaced nodes rather than a rising curve
6. The line **resolves** into the end card wordmark

Use real easing (spring, `Easing.bezier`), staggered reveals, matching geometry between morphs, masks and stroke-dash drawing.

### C. Remotion requirements
- Use `useCurrentFrame`, `useVideoConfig`, `interpolate` (always clamp extrapolation), `spring` and `Easing`.
- Use `<Sequence>` or `<Series>` for scenes, with one shared `timing.ts` that holds every frame number taken from the voiceover timestamps.
- SVG paths, `strokeDasharray`/`strokeDashoffset`, masks and `clipPath` for line art.
- Keep everything deterministic. Use `random(seed)` from Remotion, never `Math.random`, `Date` or CSS animations/transitions.
- Shared components: `PathLine`, `Node`, `MilestoneIcon`, `EssentialIcon`, `KineticText`, `EndCard`, `Disclaimer`.
- Load audio through `staticFile` and `<Audio>`, and set volume with frame-based ducking.
- Keep dependencies to `remotion`, `@remotion/cli`, `@remotion/google-fonts`, `@remotion/media-utils`, and optionally `@remotion/paths` and `@remotion/shapes`. Use one version for every Remotion package.

## 4. Story structure and locked script

The script is **locked at 56 words**. Small edits for natural delivery are fine, but keep the meaning, keep it under 60 words, and keep "Fund your firsts" as the last spoken line.

| Time | Beat | Voiceover | On-screen / motion |
| --- | --- | --- | --- |
| 0–4 s | **Hook: the first paycheck** | "Your first paycheck. It's small, but it's a start." | A phone notification "Salary credited" shrinks into the amber dot. The dot pulses once, then starts drawing a path |
| 4–11 s | **Dreams: bigger firsts** | "Because bigger firsts are coming: your first home, your first business." | The path branches. Line art of a condo window over a Manila skyline, then a small storefront. Each word lands with its icon. Supers "First home", "First business" |
| 11–18 s | **The idea: the essentials** | "They'll run on the things the world can't do without: power, networks, ports, hospitals." | Each milestone traces back to an essential: a power line, a signal tower, a port crane, a hospital cross. A small world grid links them. The four words appear as kinetic type |
| 18–25 s | **The step** | "Firsts Fund invests in the companies behind them. Start with one hundred pesos. Think five years ahead." | The branches gather into one calm line with evenly spaced contribution nodes (no rising curve). The amber dot returns as a "Start with ₱100" button that gets tapped. Super "Think 5 years ahead" |
| 25–30 s | **Resolution** | "Fund your firsts." (around 26 s, then music only) | The line resolves into the end card on `green`: **FIRSTS FUND** / **FUND YOUR FIRSTS.** / BPI Wealth. The disclaimer is visible for at least the last 3 s |

**End card disclaimer (required, verbatim, 28 px minimum, `paper` text at 80% opacity):**
> Proposed fund concept for BPI Wealth FinQuest 2026. ₱100 minimum is proposed. A UITF is not a deposit and is not insured by PDIC. Its value can fall as well as rise, and you may get back less than you invest. For goals at least five years away.

Timings shift to match the real voiceover (Section 5). The total runtime is fixed at 900 frames.

## 5. ElevenLabs voiceover

**Voice:** a young adult (mid-20s) who sounds warm, calm and confident, like a slightly older friend. Natural English with a light Filipino accent is preferred. Pick a voice from `creative_list_voices` (never a remembered ID) and say which one you picked and why. If no suitable Filipino-accented voice exists, use a neutral, warm young voice and note it in the technical notes.

**Delivery:** conversational, unhurried, with real pauses after "It's a start." and before "Fund your firsts." No hype, no theatrical swell, no announcer tone.

**Pronunciation checks** (listen to each, then re-generate or respell if wrong):
- "Firsts" must keep the final *-sts* and must not become "First" or "Firs".
- "one hundred pesos" stays as written. Don't send "₱100" to the voice.
- "BPI" is never spoken, so the end card carries it.

**Workflow:**
1. Generate the locked script once with the default number of variations. Don't call generation again just to retry, because each call spends credits.
2. Listen to every variation and pick the best one on pronunciation, warmth and pacing. Pin it.
3. Export it to `remotion/public/audio/vo.mp3`. Spoken audio must end by **27.5 s**. If it runs long, ask for a slightly faster read or trim pauses. Don't speed it up in post by more than 5%.
4. Get word-level timestamps by transcribing the chosen take with `creative_transcribe_audio`, then write them to `remotion/src/vo-timings.json`.
5. Build `timing.ts` from those timestamps so that each listed word triggers its visual within ±2 frames: "paycheck", "home", "business", "power", "networks", "ports", "hospitals", "one hundred pesos", "five years", "Fund your firsts".

Placeholder or system TTS must never appear in the final render.

## 6. Music and sound design

- **Music:** subtle and modern. It starts curious, builds momentum and resolves warmly on the end card. The ElevenLabs connector here can't make music, so use a track the team has a clear license for (for example the YouTube Audio Library or Pixabay Music), saved at `remotion/public/audio/music.mp3`, with its source and license recorded in `07 Marketing video/AUDIO_CREDITS.md`. **If no licensed track is provided, render without music and say so in the technical notes. Never use an unlicensed track.**
- **Sound effects (optional):** a soft tick on the dot, a light whoosh on path draws, a gentle chime on the end card. Generate them with ElevenLabs if the connector supports it, or use licensed files, and record them in the same credits file.
- **Mix:** voice peaks around −6 dBFS, and music is ducked about 12 dB under speech using frame-based volume. Music rises only after "Fund your firsts." Avoid clipping, and fade out cleanly by frame 900.

## 7. Production workflow

1. **Creative lock:** confirm the script, write the storyboard (one frame description per beat) and the motif map.
2. **Visual system:** tokens, type scale, a 12-column grid, the icon set (4 milestones + 6 essentials, same stroke width) and the shared components.
3. **Voice:** generate, choose, transcribe and save the timings (Section 5).
4. **Build:** implement every scene as real animation. Use no still placeholders.
5. **Sync:** wire every reveal to `timing.ts` and place music and sound effects.
6. **Render and review:** `npx remotion render` to `render/FirstsFund_30s.mp4`. Then check:
   - `ffprobe` shows 30.000 s, 900 frames, 1920×1080, 30 fps.
   - Still frames exported at 0, 3, 8, 15, 22, 27 and 29.9 s have no blank frames, clipping or cut-off text.
   - Every super stays on screen long enough to read (at least 1 s per 3 words).
   - The audio doesn't clip, and the voice is clear over the music.
   - The disclaimer can be read on a laptop screen.
   - Fix any problems and render again.

## 8. Quality standards (non-negotiable)

1. **Motion first.** Something purposeful moves in every second.
2. **One continuous story,** told through the dot → path → firsts → essentials → line → end card chain.
3. **Premium simplicity** over effects.
4. **Feeling before mechanics.** Fund mechanics, holdings and returns never appear.
5. **Voice-led timing,** per Section 5.
6. **A strong first 3 seconds** (the paycheck notification hook).
7. **A memorable last 5 seconds:** FUND YOUR FIRSTS. is the biggest, last and longest-held line.
8. **One identity,** with the same palette and type as the fact sheet.
9. **Responsible claims.**
   - No performance figures, growth curves, guarantees or promises that goals will be met.
   - No claims of regulatory approval or launch.
   - Only goals five or more years away count as "firsts to fund". Never short-term goals.
   - The ₱100 minimum is always marked "proposed" in the disclaimer.
   - The disclaimer is required.
10. **Finish the job.** Deliver a rendered MP4, not a plan.

## 9. Deliverables (all in `07 Marketing video/`)

- `SCRIPT.md`: the final voiceover script with its word count and the chosen voice
- `STORYBOARD.md`: scene-by-scene timestamps, matching `timing.ts`
- `remotion/`: the complete source, with `public/audio/vo.mp3` and `src/vo-timings.json`
- `AUDIO_CREDITS.md`: the source and license for the music and any sound effects
- `render/FirstsFund_30s.mp4`: the final render
- `NOTES.md`: video settings, the `ffprobe` output, the voice used, and any open limitations (for example, no music)

## 10. Final creative instruction

A dot becomes a path.
A path becomes your firsts.
Your firsts run on the world's essentials.
The essentials become one steady line, and the line becomes the name.

Every transition serves the story, and every word has something to show.
The viewer should leave remembering one line: **FUND YOUR FIRSTS.**

Take creative initiative within these rules. Choose a polished, complete video over stopping to ask about small design choices.

---

### Changes from the first draft
- Name changed to **Firsts Fund**, as used across the project.
- Main memorable line changed to **FUND YOUR FIRSTS.**; "Every first begins somewhere" is kept as an optional opener.
- "First international trip" removed. The paycheck is now the starting point, and the goals are five or more years away, to match the fact sheet's suitability section.
- Added the fund's own idea: firsts run on essential capacity (power, networks, ports, hospitals).
- Replaced the "investment growth illustration" with a line of steady contributions. Growth graphics are now banned.
- Added the CTA "Start with ₱100", a required verbatim disclaimer, and "proposed" labels.
- Palette now uses the fact sheet's hex values. The BPI logo is not recreated.
- Locked a 56-word script with word-level sync points.
- ElevenLabs steps now match the connector: voice picked from the list, no repeated generation, timings taken from transcription, no music generation.
- Music must be licensed and credited. If no track is provided, the video renders without music.
- Added measurable QA checks (`ffprobe`, still frames, text size and time on screen).
