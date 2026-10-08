"""Original music bed and sound effects for the Firsts Fund 30-second ad.

Everything is synthesised here from sine waves and seeded noise, so the audio is the
team's own work and needs no licence. Run: python3 make_audio.py
Writes WAV files to ../remotion/public/audio/.
"""
import os
import wave

import numpy as np

SR = 48000
DUR = 30.0
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "remotion", "public", "audio")
rng = np.random.default_rng(76)


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def write(name, x):
    """x: (n,) mono or (n, 2) stereo float in -1..1."""
    if x.ndim == 1:
        x = np.stack([x, x], axis=1)
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(os.path.join(OUT, name), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def norm(x, peak_db):
    return x / np.max(np.abs(x)) * 10 ** (peak_db / 20)


def fft_filter(x, lo, hi, soft=0.5):
    """Smooth band-pass in the frequency domain (lo/hi in Hz)."""
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR) + 1e-9
    g = 1 / (1 + (lo / f) ** (4 * soft)) * 1 / (1 + (f / hi) ** (4 * soft))
    return np.fft.irfft(X * g, n)


def reverb(x, seconds=2.4, decay=1.1, seed=0):
    r = np.random.default_rng(seed)
    t = np.arange(int(seconds * SR)) / SR
    ir = r.standard_normal(len(t)) * np.exp(-t / decay * 3)
    ir = fft_filter(ir, 200, 6000)
    ir /= np.sqrt(np.sum(ir ** 2))
    n = len(x) + len(ir)
    size = 1 << (n - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return y


# ---------------------------------------------------------------- music
N = int(DUR * SR)
t = np.arange(N) / SR

# (start s, MIDI notes). Key of D. The last change resolves on the green wipe (~26.2 s).
CHORDS = [
    (0.0, [50, 57, 61, 64, 66]),    # Dmaj9: curious
    (4.0, [47, 54, 57, 61, 62]),    # Bm9
    (7.5, [43, 50, 54, 57, 62]),    # Gmaj7
    (11.0, [42, 50, 54, 57, 62]),   # D/F#
    (13.0, [45, 52, 57, 59, 61]),   # Aadd9
    (14.5, [47, 54, 57, 62, 66]),   # Bm7
    (16.0, [43, 50, 55, 59, 62]),   # G
    (18.0, [40, 47, 55, 59, 62]),   # Em9 (momentum)
    (20.0, [43, 50, 54, 59, 62]),   # Gmaj7
    (22.0, [45, 52, 57, 62, 64]),   # Asus4
    (24.0, [45, 52, 55, 61, 64]),   # A7: tension
    (26.2, [38, 50, 57, 61, 64, 66]),  # Dmaj9: resolution
]
ENDS = [c[0] for c in CHORDS[1:]] + [DUR]


def env_ar(start, end, attack=0.5, release=0.9):
    e = np.clip((t - start) / attack, 0, 1) * np.clip((end + release - t) / release, 0, 1)
    return np.where(t < start, 0, e) ** 1.5


pad = np.zeros((N, 2))
for (start, notes), end in zip(CHORDS, ENDS):
    e = env_ar(start, end, attack=0.6 if start else 1.2)
    for m in notes:
        for side, cents in ((0, -4), (1, 4)):
            f0 = hz(m) * 2 ** (cents / 1200)
            v = sum(np.sin(2 * np.pi * f0 * h * t + h) / h ** 1.6 for h in range(1, 6))
            pad[:, side] += v * e
pad *= 0.6 + 0.4 * np.clip((t - 4) / 20, 0, 1)[:, None]  # pad opens up over time

# Plucked arpeggio: sparse at first, eighths from 4 s (100 bpm => 0.3 s)
pluck = np.zeros((N, 2))


def add_pluck(buf, start, m, amp, pan, tau=0.32):
    i0 = int(start * SR)
    n = int(1.6 * SR)
    if i0 >= N:
        return
    n = min(n, N - i0)
    tt = np.arange(n) / SR
    f0 = hz(m)
    v = (np.sin(2 * np.pi * f0 * tt) + 0.35 * np.sin(4 * np.pi * f0 * tt) + 0.1 * np.sin(6 * np.pi * f0 * tt))
    v *= np.exp(-tt / tau) * np.clip(tt / 0.004, 0, 1) * amp
    buf[i0:i0 + n, 0] += v * (1 - pan)
    buf[i0:i0 + n, 1] += v * pan


pattern = [0, 2, 3, 4, 3, 2, 1, 3]
for (start, notes), end in zip(CHORDS, ENDS):
    upper = [n + 12 for n in notes[1:]]
    step = 0.6 if start < 4 else 0.3
    k = 0
    s = start + (0.15 if start < 4 else 0)
    while s < end - 0.05 and s < 27.5:
        m = upper[pattern[k % len(pattern)] % len(upper)]
        amp = 0.55 if start < 4 else 0.45 + 0.25 * min(1, (s - 4) / 20)
        add_pluck(pluck, s, m, amp, 0.3 if k % 2 else 0.7)
        k += 1
        s += step
# Final shimmer on the resolution
for i, m in enumerate([74, 78, 81, 85, 86]):
    add_pluck(pluck, 26.2 + i * 0.09, m, 0.5, 0.2 + 0.15 * i, tau=0.9)

# Soft pulse bass and shaker from 11 s (momentum), stops for the resolution, returns softly
bass = np.zeros(N)
shaker = np.zeros(N)
beat = 0.6
for (start, notes), end in zip(CHORDS, ENDS):
    if start < 11:
        continue
    s = start
    while s < end - 0.05:
        if s > 28.6:
            break
        i0 = int(s * SR)
        n = min(int(0.55 * SR), N - i0)
        tt = np.arange(n) / SR
        amp = 0.8 if start < 18 else 1.0
        bass[i0:i0 + n] += np.sin(2 * np.pi * hz(notes[0] - 12) * tt) * np.exp(-tt / 0.22) * np.clip(tt / 0.01, 0, 1) * amp
        # off-beat shaker
        j0 = int((s + beat / 2) * SR)
        m = min(int(0.08 * SR), N - j0)
        if m > 0:
            shaker[j0:j0 + m] += rng.standard_normal(m) * np.exp(-np.arange(m) / SR / 0.018) * (0.25 if start < 18 else 0.4)
        s += beat
shaker = fft_filter(shaker, 5000, 14000)

# Rising swell into the wipe (23.8 → 26.2 s)
sw = rng.standard_normal(N)
sw = fft_filter(sw, 1500, 9000) * np.clip((t - 23.8) / 2.4, 0, 1) ** 3 * (t < 26.2)

dry = pad * 0.10 + pluck * 0.16 + np.stack([bass, bass], 1) * 0.30 + np.stack([shaker * 0.8, shaker], 1) * 0.5
dry += np.stack([sw, sw], 1) * 0.10
wet = np.stack([reverb(dry[:, 0], seed=1), reverb(dry[:, 1], seed=2)], 1)
music = dry * 0.75 + wet * 0.55
# Fade in the first 0.3 s, fade out over the last 1.8 s
fade = np.clip(t / 0.3, 0, 1) * np.clip((DUR - t) / 1.8, 0, 1)
music *= fade[:, None]
music = norm(music, -3.0)
os.makedirs(OUT, exist_ok=True)
write("music.wav", music)


# ---------------------------------------------------------------- sound effects
def tone(f, dur, tau, partials=((1, 1.0),), attack=0.003):
    tt = np.arange(int(dur * SR)) / SR
    v = sum(a * np.sin(2 * np.pi * f * r * tt) * np.exp(-tt / (tau / r ** 0.5)) for r, a in partials)
    return v * np.clip(tt / attack, 0, 1)


def pad_to(x, dur):
    out = np.zeros(int(dur * SR))
    out[: len(x)] = x[: len(out)]
    return out


bell = ((1, 1.0), (2.0, 0.35), (2.76, 0.25), (5.4, 0.08))

# Notification: soft two-note ding
d = pad_to(tone(hz(88), 0.9, 0.25, bell), 1.2)
d2 = tone(hz(93), 0.9, 0.3, bell)
i = int(0.12 * SR)
d[i:i + len(d2)] += d2[: len(d) - i]
write("notif.wav", norm(d + 0.3 * reverb(d, 1.2, 0.6, 3), -6))

# Tick: tiny high blip
write("tick.wav", norm(pad_to(tone(2400, 0.06, 0.012), 0.3), -10))

# Whoosh: band-passed noise that brightens as it swells
n = int(0.7 * SR)
tt = np.arange(n) / SR
noise = rng.standard_normal(n)
low, high = fft_filter(noise, 200, 1200), fft_filter(noise, 1200, 6000)
mix = tt / tt[-1]
env = np.sin(np.pi * np.clip(tt / 0.7, 0, 1)) ** 2
write("whoosh.wav", norm((low * (1 - mix) + high * mix) * env, -9))

# Pop: little pitch-drop bubble for nodes appearing
tt = np.arange(int(0.12 * SR)) / SR
f = 950 - 350 * tt / tt[-1]
pop = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.03)
write("pop.wav", norm(pad_to(pop, 0.3), -9))

# Node lights: a rising pentatonic step per node (D major pentatonic)
for k, m in enumerate([74, 76, 78, 81, 83, 86, 88]):
    write(f"node{k}.wav", norm(pad_to(tone(hz(m), 0.5, 0.12, ((1, 1.0), (2, 0.2))), 0.6), -12))

# Tap: click plus a soft low thump
tt = np.arange(int(0.25 * SR)) / SR
tap = np.sin(2 * np.pi * 140 * tt) * np.exp(-tt / 0.04) * 0.9
tap[: int(0.004 * SR)] += rng.standard_normal(int(0.004 * SR)) * 0.5
write("tap.wav", norm(tap, -7))

# Chime for the end card: a gentle D bell with tail
c = pad_to(tone(hz(86), 3.0, 0.9, bell) + 0.6 * tone(hz(81), 3.0, 0.8, bell), 3.5)
write("chime.wav", norm(c + 0.4 * reverb(c, 2.0, 1.0, 4), -8))

print("wrote", sorted(os.listdir(OUT)))
