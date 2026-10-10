import React from 'react';
import {Easing, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/fonts';
import tl from './timeline.json';

/* ---------- fonts (bundled, so renders work offline) ---------- */
// Geist has no ₱ glyph, so Inter (latin-ext) supplies just that character.
for (const w of ['400', '500', '600', '700']) {
	loadFont({family: 'Geist', url: staticFile(`fonts/geist-sans-latin-${w}-normal.woff2`), weight: w});
	loadFont({family: 'PesoFallback', url: staticFile(`fonts/inter-latin-ext-${w}-normal.woff2`), weight: w, unicodeRange: 'U+20B1'});
}
export const SANS = "'Geist', 'PesoFallback', sans-serif";
/** Small uppercase labels: the main font, medium weight, widely tracked. */
export const LABEL = SANS;

/* ---------- timing ---------- */
export const TL = tl;
const FPB = (tl.fps * 60) / tl.bpm;
/** Frame of a beat. Every cut lands on one. */
export const f = (beat: number) => Math.round(beat * FPB);
export const len = ([a, b]: number[]) => f(b) - f(a);

/* ---------- look ---------- */
export const C = {
	paper: '#F4F3EE',
	card: '#FFFFFF',
	ink: '#0E100E',
	ink2: '#3A3F3B',
	muted: '#8B908A',
	line: '#D9D7CF',
	accent: '#0B7A4B',
	accentSoft: '#DDEFE5',
	night: '#0B0D0C',
	rule: '#B9CDE6',
	margin: '#E7A1A1',
	warn: '#D2453B',
	glow: '#34C17F',
};

export const E = {
	out: Easing.bezier(0.16, 1, 0.3, 1),
	inOut: Easing.bezier(0.83, 0, 0.17, 1),
	in: Easing.bezier(0.7, 0, 0.84, 0),
	soft: Easing.bezier(0.33, 1, 0.68, 1),
};

/** 0→1 between frames a and b, clamped. */
export const ramp = (frame: number, a: number, b: number, ease: (t: number) => number = E.out) =>
	interpolate(frame, [a, b], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
export const mix = (a: number, b: number, t: number) => a + (b - a) * t;

export const peso = (n: number) => '₱' + Math.round(n).toLocaleString('en-US');

/* ---------- layout ----------
 * Every first is drawn in one 1000 × 600 "stage" so an end state in one scene can be the
 * start state of the next. 16:9 puts the stage on the right and the caption on the left;
 * 9:16 puts the stage on top and the caption underneath.
 */
export const useLayout = () => {
	const {width, height} = useVideoConfig();
	const vertical = height > width;
	const u = Math.min(width, height) / 1080;
	const stage = vertical
		? {x: 40 * u, y: 470 * u, s: u}
		: {x: width - 1080 * u - 70 * u, y: 190 * u, s: 1.08 * u};
	const caption = vertical
		? {left: 80 * u, top: 1200 * u, width: 920 * u}
		: {left: 120 * u, top: 330 * u, width: 700 * u};
	const toScreen = (vx: number, vy: number) => ({x: stage.x + vx * stage.s, y: stage.y + vy * stage.s});
	return {width, height, vertical, u, stage, caption, toScreen};
};

export const Fill: React.FC<{bg: string; children?: React.ReactNode; style?: React.CSSProperties}> = ({bg, children, style}) => (
	<div style={{position: 'absolute', inset: 0, background: bg, overflow: 'hidden', fontFamily: SANS, fontVariantNumeric: 'tabular-nums', ...style}}>{children}</div>
);

/** The 1000 × 600 drawing area shared by the firsts. */
export const Stage: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => {
	const {stage} = useLayout();
	return (
		<svg
			viewBox="0 0 1000 600"
			width={1000 * stage.s}
			height={600 * stage.s}
			style={{position: 'absolute', left: stage.x, top: stage.y, overflow: 'visible', ...style}}
			fill="none"
			strokeLinecap="round"
			strokeLinejoin="round"
		>
			{children}
		</svg>
	);
};

/** Masked line reveal: text rises into place from behind an edge. */
export const Rise: React.FC<{at: number; children: React.ReactNode; dur?: number; out?: number; style?: React.CSSProperties}> = ({
	at,
	children,
	dur = 12,
	out,
	style,
}) => {
	const frame = useCurrentFrame();
	const p = ramp(frame, at, at + dur);
	const q = out === undefined ? 0 : ramp(frame, out, out + 8, E.in);
	return (
		<span style={{display: 'block', overflow: 'hidden', paddingBottom: '0.08em', marginBottom: '-0.08em', ...style}}>
			<span style={{display: 'block', transform: `translateY(${(1 - p) * 110 - q * 110}%)`}}>{children}</span>
		</span>
	);
};

/** Small habit ring: fills a little more with every first. */
export const MiniRing: React.FC<{progress: number; size: number; color: string; track: string; stroke?: number}> = ({
	progress,
	size,
	color,
	track,
	stroke = 3,
}) => {
	const r = (size - stroke) / 2;
	const c = 2 * Math.PI * r;
	return (
		<svg width={size} height={size} style={{transform: 'rotate(-90deg)', flexShrink: 0}}>
			<circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={track} strokeWidth={stroke} />
			<circle
				cx={size / 2}
				cy={size / 2}
				r={r}
				fill="none"
				stroke={color}
				strokeWidth={stroke}
				strokeLinecap="round"
				strokeDasharray={c}
				strokeDashoffset={c * (1 - Math.max(0, Math.min(1, progress)))}
			/>
		</svg>
	);
};

/** Caption for each first: mono label with the habit ring, then a two-line headline. */
export const Caption: React.FC<{n: number; total: number; lines: string[]; dark?: boolean; at?: number}> = ({n, total, lines, dark, at = 4}) => {
	const frame = useCurrentFrame();
	const {u, caption, vertical} = useLayout();
	const fg = dark ? C.card : C.ink;
	const sub = dark ? 'rgba(255,255,255,0.7)' : C.muted;
	const ring = mix((n - 1) / total, n / total, ramp(frame, at + 4, at + 16));
	return (
		<div style={{position: 'absolute', left: caption.left, top: caption.top, width: caption.width, color: fg}}>
			<div style={{display: 'flex', alignItems: 'center', gap: 14 * u, opacity: ramp(frame, at, at + 8)}}>
				<MiniRing progress={ring} size={30 * u} stroke={4 * u} color={dark ? C.card : C.accent} track={dark ? 'rgba(255,255,255,0.25)' : C.line} />
				<span style={{fontFamily: LABEL, fontWeight: 500, fontSize: 24 * u, letterSpacing: '0.12em', color: sub}}>FIRST {String(n).padStart(2, '0')}</span>
			</div>
			<div style={{fontSize: (vertical ? 100 : 92) * u, fontWeight: 600, letterSpacing: '-0.045em', lineHeight: 1.0, marginTop: 26 * u}}>
				{lines.map((l, k) => (
					<Rise key={k} at={at + 2 + k * 3}>
						{l}
					</Rise>
				))}
			</div>
		</div>
	);
};

/** Point and tangent angle on a quadratic Bézier. */
export const quad = (p0: number[], p1: number[], p2: number[], t: number) => {
	const x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0];
	const y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1];
	const dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0]);
	const dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1]);
	return {x, y, a: (Math.atan2(dy, dx) * 180) / Math.PI};
};
