# Firsts Fund 30-second ad: build notes

**Final cut:** `render/FirstsFund_30s.mp4`, with ElevenLabs voiceover, music and sound effects.
`render/FirstsFund_30s_music.mp4` is the earlier version without a voiceover (music and sound effects only).

| Setting | Value |
| --- | --- |
| Video | H.264, 1920 × 1080, 30 fps, **900 frames (30.0 s)**, CRF 16, yuv420p |
| Audio | AAC 256 kbps stereo 48 kHz, normalised to −13.5 LUFS integrated, −1.5 dBFS peak (two-pass loudnorm after render) |
| Voice | ElevenLabs "Hope - upbeat and clear" (`tnSpp4vdxKPjI9w0GnoV`), eleven_multilingual_v2, take 3 of 4. Cut into 8 phrases placed on the visual beats; music ducked about 10 dB under speech |
| Font | Plus Jakarta Sans 500/700/800 (SIL Open Font License), bundled in `remotion/public/fonts/` |
| Palette | Fact sheet tokens (`src/theme.ts`) |

## Storyboard (source of truth: `remotion/src/timing.ts`; voice word frames noted there)
| Time | Voiceover | On screen |
| --- | --- | --- |
| 0–3.6 s | "Your first paycheck. It's small… but it's a start." | The "Salary credited" notification shrinks into the amber dot on "start" |
| 3.8–9.0 s | "Because bigger firsts are coming: your first home, your first business." | Path branches. **First home** lands on "home" and **First business** on "business", with the Manila skyline below |
| 9.4–15.5 s | "They'll run on the things the world can't do without. Power. Networks. Ports. Hospitals." | **"Your firsts run on the world's essentials."** Each essential's label lands on its spoken word |
| 15.9–21.8 s | "Firsts Fund invests in the companies behind them. Start with one hundred pesos. Think five years ahead." | Icons collapse onto the Today → 5 years line. The **Start with ₱100** pill opens with "one hundred pesos" and is tapped. The dot travels the line |
| 22.4–30 s | "Fund your firsts." (24.1–25.3 s) | Green wipe at 23.1 s (music resolves). FUND / YOUR / FIRSTS rise with each spoken word. BPI Wealth and the disclaimer stay on screen for 6 s |

## Voiceover
Script (55 words, spoken 22.5 s): *Your first paycheck. It's small… but it's a start. Because bigger firsts are coming: your first home, your first business. They'll run on the things the world can't do without. Power. Networks. Ports. Hospitals. Firsts Fund invests in the companies behind them. Start with one hundred pesos. Think five years ahead. Fund your firsts.*

- All 4 takes are in `audio/vo_takes/`. Take 3 was chosen on pacing (clear pauses after "start" and before the tagline). A Scribe transcript matched the script word for word, including "firsts".
- Phrase cuts (seconds in take 3): A 0–1.40 · B 1.40–3.85 · C 3.85–8.55 · D 8.55–11.36 · E 11.36–14.62 · F 14.62–17.15 · G 17.15–20.25 · I 21.30–22.62 (+3 dB). Regenerate a phrase with the same ffmpeg cut if you swap takes. Word timestamps are in `audio/vo_words.json`.
- ElevenLabs flow: "Firsts Fund 30s ad voiceover" (4 takes × 339 credits, transcription free).

## Rerun
```bash
cd "07 Marketing video/audio" && python3 make_audio.py          # music + SFX (needs numpy)
cd ../remotion && npm install
npx remotion studio                                              # live preview
npx remotion render src/index.ts FirstsFund ../render/FirstsFund_30s.mp4
# then loudness-normalise to -14 LUFS (ffmpeg loudnorm, video stream copied)
# Cloud container only: export REMOTION_CHROME=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
```

## Open items
- [ ] Listen through on real speakers and on the venue's system. The mix was checked by meter, not by ear. The voice is an American-accented young female voice. Swap the voice if the team wants a Filipino accent.
- [ ] Team review: icon choices, the generic Manila skyline, and whether "Hospitals" fits the "firsts" story.
