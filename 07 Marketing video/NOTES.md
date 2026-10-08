# Firsts Fund 30-second ad: build notes

**Current cut:** `render/FirstsFund_30s_music.mp4`, with music and sound effects but **no voiceover yet**. The script lines appear as on-screen text.

| Setting | Value |
| --- | --- |
| Video | H.264, 1920 × 1080, 30 fps, **900 frames (30.0 s)**, CRF 16, yuv420p |
| Audio | AAC stereo 48 kHz. Integrated loudness −15.7 LUFS, peak −2.7 dBFS |
| Font | Plus Jakarta Sans 500/700/800 (SIL Open Font License), bundled in `remotion/public/fonts/` |
| Palette | Fact sheet tokens (`src/theme.ts`) |

## Storyboard (frames at 30 fps; source of truth is `remotion/src/timing.ts`)
| Time | On screen |
| --- | --- |
| 0–3.5 s | A "Salary credited" notification springs in. **"Your first paycheck."** / "Small. But it's a start." The card shrinks into the amber dot, which pulses |
| 3.9–10.9 s | The dot moves left and draws a path, which branches. Condo tower (**First home**) and storefront (**First business**) draw in, with a Manila skyline along the bottom. **"Bigger firsts are coming."** |
| 11.5–17.9 s | **"Your firsts run on the world's essentials."** Lines link each first to Power, Networks, Ports and Hospitals |
| 18.3–25.3 s | The six icons collapse into nodes on one steady line (Today → 5 years, no rising curve). **"Firsts Fund invests in the companies behind them."** The dot becomes a **Start with ₱100** pill, which is tapped. The dot travels the line, lighting each node. **"Think 5 years ahead."** |
| 25.4–30 s | The line retracts into the dot, which moves to the centre and expands into a green wipe. End card: FIRSTS FUND / **FUND YOUR FIRSTS** (the amber dot becomes the period) / BPI Wealth, with the disclaimer on screen for the last 3.1 s |

## Rerun
```bash
cd "07 Marketing video/audio" && python3 make_audio.py          # music + SFX (needs numpy)
cd ../remotion && npm install
npx remotion studio                                              # live preview
npm run render                                                   # → ../render/FirstsFund_30s_music.mp4
# Cloud container only: export REMOTION_CHROME=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
```

## Open items
- [ ] Add the ElevenLabs voiceover (script in `MASTER_INSTRUCTIONS.md` §4). Retime `timing.ts` to the word timestamps and duck the music about 12 dB under speech.
- [ ] Listen through on real speakers. The synthesised mix was checked by meter only (no clipping), not by ear.
- [ ] Team review of icon choices (hospital for "business" links is symbolic) and of the Manila skyline (generic silhouette, not specific buildings).
