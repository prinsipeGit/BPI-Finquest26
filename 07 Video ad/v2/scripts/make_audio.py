"""Placeholder music bed for the Firsts Fund ad (v2). Sound effects and voice now come from ElevenLabs
(see scripts/prepare_audio.py); the old synthesised SFX function is kept below but no longer run.

Everything is synthesised with numpy, so there is nothing to license. The music
follows src/timeline.json beat for beat (124 BPM): sparse hook, building montage,
drop on "Fund your firsts", groove under the calculator, piano, drop, tail.
Swap public/audio/music.wav for a licensed track at the same tempo before release.

Run from the project root: python3 scripts/make_audio.py
"""
import json
import os
import wave

import numpy as np

SR = 44100
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "audio")
TL = json.load(open(os.path.join(ROOT, "src", "timeline.json")))
BEAT = 60.0 / TL["bpm"]
TOTAL = TL["totalBeats"] * BEAT
S = TL["sections"]
rng = np.random.default_rng(76)


def t_of(n):
    return np.arange(int(n * SR)) / SR


def env(n, attack=0.002, decay=0.2):
    t = t_of(n)
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-t / decay)


def band(x, lo=None, hi=None):
    """Brick-wall FFT filter; fine for short one-shots."""
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X = np.fft.rfft(x)
    if lo:
        X[f < lo] = 0
    if hi:
        X[f > hi] = 0
    return np.fft.irfft(X, len(x))


def norm(x, peak=0.9):
    m = np.max(np.abs(x)) or 1
    return x / m * peak


def save(name, x, stereo=None):
    st = stereo if stereo is not None else np.stack([x, x], 1)
    st = (np.clip(st, -1, 1) * 32767).astype(np.int16)
    with wave.open(os.path.join(OUT, name), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(st.tobytes())


# ---------- instruments ----------
def kick(n=0.4, punch=1.0):
    t = t_of(n)
    f = 45 + 110 * np.exp(-t / 0.03)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t / 0.18) * punch + 0.3 * band(rng.standard_normal(len(t)), 2000) * np.exp(-t / 0.004)


def clap(n=0.25):
    t = t_of(n)
    nz = band(rng.standard_normal(len(t)), 900, 6000)
    e = np.exp(-t / 0.06) * (1 + 0.6 * np.exp(-((t - 0.012) % 0.012) / 0.003))
    return norm(nz * e, 0.6)


def hat(n=0.06, open_=False):
    t = t_of(0.25 if open_ else n)
    nz = band(rng.standard_normal(len(t)), 7000)
    return norm(nz * np.exp(-t / (0.08 if open_ else 0.015)), 0.35)


def tone(freq, n, harm=(1, 0.5, 0.25, 0.12), decay=0.3, attack=0.004):
    t = t_of(n)
    x = sum(a * np.sin(2 * np.pi * freq * (k + 1) * t) for k, a in enumerate(harm))
    return x * env(n, attack, decay)


def bassnote(freq, n):
    t = t_of(n)
    saw = sum(np.sin(2 * np.pi * freq * k * t) / k for k in range(1, 8))
    e = np.clip(t / 0.005, 0, 1) * np.clip((n - t) / 0.02, 0, 1)
    return saw * e * 0.5


def stab(freqs, n=0.18):
    t = t_of(n)
    x = sum(np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.004 * t) + 0.25 * np.sin(2 * np.pi * f * 2 * t) for f in freqs)
    return x * env(n, 0.003, 0.09) / len(freqs)


def pad(freqs, n):
    t = t_of(n)
    x = sum(np.sin(2 * np.pi * f * t) + np.sin(2 * np.pi * f * 1.006 * t) + 0.4 * np.sin(2 * np.pi * f * 0.997 * t) for f in freqs)
    e = np.clip(t / 0.6, 0, 1) * np.clip((n - t) / 1.5, 0, 1)
    return x * e / (3 * len(freqs))


def riser(n):
    t = t_of(n)
    nz = rng.standard_normal(len(t))
    chunks = 24
    out = np.zeros_like(nz)
    L = len(nz) // chunks
    for i in range(chunks):
        seg = nz[i * L:(i + 1) * L]
        lo = 300 + 6000 * (i / chunks) ** 2
        out[i * L:(i + 1) * L] = band(seg, lo, lo * 2.5)
    sweep = np.sin(2 * np.pi * np.cumsum(200 + 1200 * (t / n) ** 2) / SR)
    return norm((out * 0.8 + sweep * 0.25) * (t / n) ** 1.6, 0.5)


# chord progression, one chord per bar: A  E  F#m  D
A2, E2, Fs2, D2 = 110.0, 82.41, 92.5, 73.42
CHORDS = [
    (A2, [440.0, 554.37, 659.25]),
    (E2, [415.3, 493.88, 659.25]),
    (Fs2, [440.0, 554.37, 739.99]),
    (D2, [440.0, 587.33, 739.99]),
]


def build_music():
    mix = np.zeros(int((TOTAL + 2.5) * SR))

    def put(x, beat, gain=1.0):
        i = int(beat * BEAT * SR)
        j = min(len(mix), i + len(x))
        mix[i:j] += x[: j - i] * gain

    def in_(sec, b):
        lo, hi = S[sec]
        return lo <= b < hi

    for b16 in range(int(TL["totalBeats"] * 4)):
        b = b16 / 4.0
        bar = int(b // 4)
        root, triad = CHORDS[bar % 4]
        on_beat = b16 % 4 == 0
        off = b16 % 4 == 2
        silent = in_("legal", b) or (S["always"][0] <= b < S["always"][0] + 2)
        if silent:
            continue
        drop = in_("fund", b) or in_("always", b) or in_("logo", b)
        groove = in_("calc", b) or drop
        build = in_("firsts", b)
        hook = in_("intro", b)

        if on_beat:
            put(kick(punch=1.15 if drop else 1.0), b, 0.9)
        if (groove or build) and on_beat and int(b) % 2 == 1:
            put(clap(), b, 0.5 if groove else 0.35)
        if (groove or build) and off:
            put(hat(open_=groove), b, 0.6)
        if groove and b16 % 2 == 1:
            put(hat(), b, 0.35)
        if (groove or build) and off:
            put(bassnote(root, BEAT * 0.45), b, 0.45 if build else 0.6)
        if groove and b16 % 8 in (2, 5):
            put(stab(triad), b, 0.35 if not drop else 0.45)
        if hook and on_beat:
            put(stab(triad, 0.12), b, 0.12)

    # risers into the calculator and into the silence
    put(riser(4 * BEAT), S["fund"][0] - 4, 1.0)
    put(riser(4 * BEAT), S["always"][0] - 4, 0.9)
    # piano note after the silence, drop two beats later
    pn = tone(440.0, 2.5, (1, 0.6, 0.3, 0.2, 0.1), decay=0.9) + tone(659.25, 2.5, (1, 0.5, 0.2), decay=0.8) * 0.6
    put(norm(pn, 0.5), S["always"][0])
    # warm pad tail under the logo and the legal card
    put(pad([220.0, 277.18, 329.63, 440.0], (S["legal"][1] - S["logo"][0]) * BEAT + 1.5), S["logo"][0], 0.9)

    mix = mix[: int(TOTAL * SR)]
    # gentle stereo: hats and stabs slightly wide via tiny delay
    d = int(0.008 * SR)
    left = mix
    right = np.concatenate([np.zeros(d), mix[:-d]]) * 0.92 + mix * 0.08
    fade = np.ones(len(mix))
    fl = int(0.8 * SR)
    fade[-fl:] = np.linspace(1, 0, fl)
    st = np.stack([left * fade, right * fade], 1)
    return st / (np.max(np.abs(st)) or 1) * 0.85


def pluck(freq, n=0.5):
    """Soft felt-piano / pluck: a few sine partials with a quick bloom and a gentle decay."""
    t = t_of(n)
    x = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 2 * t) + 0.12 * np.sin(2 * np.pi * freq * 3 * t)
    return x * np.clip(t / 0.006, 0, 1) * np.exp(-t / 0.28)


def shaker(n=0.08):
    t = t_of(n)
    return norm(band(rng.standard_normal(len(t)), 5000, 12000) * np.sin(np.pi * t / n) ** 2, 0.2)


def build_music_vo():
    """Warm bed for the voiced cut: felt-piano arpeggios, pad and a soft half-time pulse.
    Leaves the 1–4 kHz range open for the voice; the busy dance beat stays in music.wav for the no-voice cut."""
    mix = np.zeros(int((TOTAL + 2.5) * SR))
    kick_env = np.zeros_like(mix)

    def put(x, beat, gain=1.0, buf=None):
        buf = mix if buf is None else buf
        i = int(beat * BEAT * SR)
        j = min(len(buf), i + len(x))
        buf[i:j] += x[: j - i] * gain

    def in_(sec, b):
        lo, hi = S[sec]
        return lo <= b < hi

    pads = np.zeros_like(mix)
    arp_order = [0, 1, 2, 1]
    for b8 in range(int(TL["totalBeats"] * 2)):
        b = b8 / 2.0
        bar = int(b // 4)
        root, triad = CHORDS[bar % 4]
        if in_("legal", b):
            continue
        quiet = S["always"][0] <= b < S["always"][0] + 2  # piano alone before the payoff
        lift = in_("fund", b) or in_("logo", b) or (in_("always", b) and not quiet)
        if not quiet:
            note = triad[arp_order[b8 % 4]] * (2 if (b8 // 4) % 2 and lift else 1)
            put(pluck(note), b, 0.30 if lift else 0.24)
        if b8 % 2 == 0 and not quiet and not in_("intro", b):
            if int(b) % 2 == 0:
                k = kick(0.35, 0.8)
                put(k, b, 0.55 if lift else 0.4)
                put(np.exp(-t_of(0.35) / 0.12), b, 1.0, kick_env)
        if b8 % 2 == 1 and (in_("calc", b) or lift):
            put(shaker(), b, 0.5)
        if b8 % 8 == 0:
            put(pad(triad + [root * 2], 4 * BEAT + 0.4), b, 0.55 if lift else 0.4, pads)
            if not in_("intro", b) and not quiet:
                put(bassnote(root, 4 * BEAT * 0.95) * 0.6, b, 0.35)
    # soft sidechain: the pad breathes with the kick
    mix += pads * (1 - 0.45 * np.clip(kick_env, 0, 1))
    put(riser(4 * BEAT) * 0.5, S["fund"][0] - 4, 0.6)
    pn = tone(440.0, 2.5, (1, 0.6, 0.3, 0.2, 0.1), decay=0.9) + tone(659.25, 2.5, (1, 0.5, 0.2), decay=0.8) * 0.6
    put(norm(pn, 0.5), S["always"][0])
    put(pad([220.0, 277.18, 329.63, 440.0], (S["legal"][1] - S["logo"][0]) * BEAT + 1.5), S["logo"][0], 0.7)
    mix = mix[: int(TOTAL * SR)]
    d = int(0.011 * SR)
    left = mix
    right = np.concatenate([np.zeros(d), mix[:-d]]) * 0.9 + mix * 0.1
    fade = np.ones(len(mix))
    fl = int(0.8 * SR)
    fade[-fl:] = np.linspace(1, 0, fl)
    st = np.stack([left * fade, right * fade], 1)
    return st / (np.max(np.abs(st)) or 1) * 0.85


# ---------- sound effects ----------
def sfx():
    t = t_of
    fx = {}
    # phone notification: two bright tones
    d = np.concatenate([tone(1318.5, 0.12, (1, 0.2), 0.08), tone(1760.0, 0.35, (1, 0.2), 0.15)])
    fx["ding"] = norm(d, 0.8)
    # coin: metallic partials, two quick hits
    def coinhit(n):
        return sum(a * np.sin(2 * np.pi * f * t(n)) for f, a in [(2093, 1), (2637, 0.7), (3951, 0.5), (5274, 0.3)]) * env(n, 0.001, 0.09)
    c = np.zeros(int(0.45 * SR))
    c[: int(0.3 * SR)] += coinhit(0.3)
    c[int(0.07 * SR): int(0.07 * SR) + int(0.38 * SR)] += coinhit(0.38)[: len(c) - int(0.07 * SR)] * 0.8
    fx["coin"] = norm(c, 0.7)
    # whoosh: band-passed noise swell
    n = 0.45
    tt = t(n)
    w = np.zeros(len(tt))
    nz = rng.standard_normal(len(tt))
    L = len(tt) // 16
    for i in range(16):
        lo = 400 + 2500 * np.sin(np.pi * i / 16)
        w[i * L:(i + 1) * L] = band(nz[i * L:(i + 1) * L], lo, lo * 3)
    fx["whoosh"] = norm(w * np.sin(np.pi * tt / n) ** 2, 0.7)
    # sub hit
    fx["hit"] = norm(kick(0.9, 1.4) + 0.4 * band(rng.standard_normal(int(0.9 * SR)), 60, 400) * np.exp(-t(0.9) / 0.12), 0.95)
    # typing click
    fx["type"] = norm(band(rng.standard_normal(int(0.04 * SR)), 2000, 9000) * np.exp(-t(0.04) / 0.006), 0.35)
    # number tick
    fx["tick"] = norm(tone(2600, 0.05, (1,), 0.01), 0.3)
    # slider snap back
    sn = np.concatenate([tone(900, 0.06, (1, 0.3), 0.02), tone(1350, 0.18, (1, 0.3), 0.06)])
    fx["snap"] = norm(sn + 0.2 * np.pad(band(rng.standard_normal(int(0.03 * SR)), 3000), (0, len(sn) - int(0.03 * SR))), 0.6)
    # shimmer: fast rising arpeggio
    notes = [880, 1108.7, 1318.5, 1760, 2217.5, 2637]
    sh = np.zeros(int(1.0 * SR))
    for k, f in enumerate(notes):
        i = int(k * 0.05 * SR)
        x = tone(f, 0.6, (1, 0.15), 0.25)
        sh[i:i + len(x)] += x[: len(sh) - i]
    fx["shimmer"] = norm(sh, 0.55)
    # button tap
    fx["tap"] = norm(tone(500, 0.08, (1, 0.5), 0.02) + 0.3 * band(rng.standard_normal(int(0.08 * SR)), 1500, 5000) * np.exp(-t(0.08) / 0.005), 0.6)
    # check tick for "next first" cards
    fx["pop"] = norm(tone(660, 0.12, (1, 0.3), 0.04) * np.exp(-t(0.12) / 0.05), 0.5)
    for k, v in fx.items():
        save(f"{k}.wav", v)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    m = build_music()
    save("music.wav", None, stereo=m)
    save("music_vo.wav", None, stereo=build_music_vo())
    print("wrote", sorted(os.listdir(OUT)), f"music {len(m) / SR:.2f}s")
