import {Easing, continueRender, delayRender, interpolate, spring, staticFile} from 'remotion';

// Palette shared with the Phase 2 fact sheet.
export const C = {
  green: '#0F7A45',
  greenDeep: '#142019',
  greenLight: '#5FC48C',
  mist: '#C9D6CE',
  paper: '#F5F4EE',
  amber: '#C9761F',
  grey: '#6E7872',
  white: '#FFFFFF',
} as const;

// Plus Jakarta Sans (SIL Open Font License), bundled in public/fonts so renders work offline.
const FAMILY = 'Plus Jakarta Sans';
export const fontFamily = `'${FAMILY}', Inter, sans-serif`;

if (typeof document !== 'undefined') {
  const handle = delayRender('Loading Plus Jakarta Sans');
  Promise.all(
    [500, 700, 800].map((w) => {
      const face = new FontFace(FAMILY, `url(${staticFile(`fonts/PlusJakartaSans-${w}.ttf`)})`, {weight: String(w)});
      return face.load().then((loaded) => document.fonts.add(loaded));
    }),
  ).then(() => continueRender(handle));
}

export const W = 1920;
export const H = 1080;
export const SAFE = 96;

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

export const EASE = Easing.bezier(0.65, 0, 0.35, 1); // smooth in-out
export const EASE_OUT = Easing.bezier(0.16, 1, 0.3, 1); // expo-like out
export const EASE_IN = Easing.bezier(0.7, 0, 0.84, 0);

/** 0→1 progress over [start, start + dur]. */
export const prog = (f: number, start: number, dur: number, easing = EASE) =>
  interpolate(f, [start, start + dur], [0, 1], {...clamp, easing});

export const lerp = (a: number, b: number, p: number) => a + (b - a) * p;

export const pop = (f: number, start: number, fps: number) =>
  spring({frame: f - start, fps, config: {damping: 14, stiffness: 180, mass: 0.6}});

export const soft = (f: number, start: number, fps: number) =>
  spring({frame: f - start, fps, config: {damping: 200}, durationInFrames: 24});

/** Piecewise keyframes with per-segment easing. */
export const keys = (f: number, frames: number[], values: number[], easing = EASE) =>
  interpolate(f, frames, values, {...clamp, easing});

export const mixColor = (a: string, b: string, p: number) => {
  const pa = [1, 3, 5].map((i) => parseInt(a.slice(i, i + 2), 16));
  const pb = [1, 3, 5].map((i) => parseInt(b.slice(i, i + 2), 16));
  const c = pa.map((v, i) => Math.round(lerp(v, pb[i], p)));
  return `rgb(${c.join(',')})`;
};
