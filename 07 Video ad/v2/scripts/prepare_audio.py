"""Cut the ElevenLabs voice-over into lines and clean up the ElevenLabs sound effects.

Sources (kept in assets/elevenlabs/):
  vo_justin_case_take3.mp3  one take of the whole script, voice "Justin Case - Warm, Trustworthy, Clear",
                            model eleven_v4, read with pauses between lines
  sfx/*.mp3                 eleven_text_to_sound_v2, one variation per effect

Writes public/audio/vo/NN.wav, public/audio/sfx/*.wav and src/vo.json (where each line starts, in seconds).
Run from the project root: python3 scripts/prepare_audio.py
"""
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "elevenlabs")
OUT = os.path.join(ROOT, "public", "audio")
TAKE = os.path.join(SRC, "vo_justin_case_take3.mp3")

# Each line of the script: text, where it starts in the video (seconds), playback speed.
# Lines 1–3 and 9–13 run slightly faster so the voice fits the cuts.
LINES = [
    ("You just got your first paycheck.", 0.10, 1.12),
    ("So… what do you do first?", 2.18, 1.12),
    ("Take Mom and Dad abroad.", 3.90, 1.08),
    ("Your first car.", 5.15, 1.0),
    ("Your first home.", 6.45, 1.0),
    ("Your first business.", 8.20, 1.0),
    ("Their first day of school.", 9.95, 1.0),
    ("Fund your firsts.", 11.80, 1.0),
    ("Name your first.", 13.65, 1.1),
    ("Set the amount.", 15.10, 1.1),
    ("Pick a date five years or more away.", 16.30, 1.1),
    ("See what to set aside each month…", 18.20, 1.1),
    ("and start with as little as one hundred pesos.", 19.95, 1.1),
    ("Because there will always be a new first.", 22.30, 1.0),
    ("Firsts Fund.", 24.85, 1.0),
    ("Fund your firsts.", 25.85, 1.0),
]

SFX = ["notif", "whoosh", "plane", "car", "stack", "shutter", "page", "pencil", "typing", "click", "success", "boom", "riser"]


def run(args):
    return subprocess.run(args, capture_output=True, text=True, check=True)


def silences(path, noise="-40dB", dur=0.18):
    log = subprocess.run(["ffmpeg", "-v", "info", "-i", path, "-af", f"silencedetect=n={noise}:d={dur}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
    return list(zip(starts, ends))


def duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).stdout)


def cut_vo():
    os.makedirs(os.path.join(OUT, "vo"), exist_ok=True)
    gaps = silences(TAKE)
    total = duration(TAKE)
    bounds, t = [], 0.0
    for s, e in gaps:
        if s > t + 0.3:
            bounds.append((t, s))
        t = e
    if total > t + 0.3:
        bounds.append((t, total))
    if len(bounds) != len(LINES):
        raise SystemExit(f"expected {len(LINES)} lines in the take, found {len(bounds)}: {bounds}")
    placed = []
    for k, ((a, b), (text, at, speed)) in enumerate(zip(bounds, LINES), 1):
        a, b = max(0.0, a - 0.04), min(total, b + 0.08)
        out = os.path.join(OUT, "vo", f"{k:02d}.wav")
        af = f"atempo={speed}," if speed != 1.0 else ""
        af += "afade=t=in:d=0.02,areverse,afade=t=in:d=0.06,areverse,loudnorm=I=-16:TP=-1.5:LRA=7"
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", TAKE, "-af", af, "-ar", "48000", "-ac", "2", out])
        d = duration(out)
        placed.append({"file": f"audio/vo/{k:02d}.wav", "text": text, "at": at, "dur": round(d, 3)})
    for x, y in zip(placed, placed[1:]):
        if x["at"] + x["dur"] > y["at"] + 0.05:
            print(f"warning: '{x['text']}' runs {x['at'] + x['dur'] - y['at']:.2f}s into the next line")
    json.dump(placed, open(os.path.join(ROOT, "src", "vo.json"), "w"), indent=1)
    return placed


def clean_sfx():
    os.makedirs(os.path.join(OUT, "sfx"), exist_ok=True)
    for name in SFX:
        src = os.path.join(SRC, "sfx", f"{name}.mp3")
        out = os.path.join(OUT, "sfx", f"{name}.wav")
        af = ("silenceremove=start_periods=1:start_threshold=-45dB,"
              "areverse,silenceremove=start_periods=1:start_threshold=-55dB,afade=t=in:d=0.06,areverse,"
              "loudnorm=I=-18:TP=-1.5")
        # strip leading and trailing silence, soften the last 60 ms, even out loudness
        run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", af, "-ar", "48000", "-ac", "2", out])


if __name__ == "__main__":
    placed = cut_vo()
    clean_sfx()
    for p in placed:
        print(f"{p['at']:6.2f}s  {p['dur']:.2f}s  {p['text']}")
