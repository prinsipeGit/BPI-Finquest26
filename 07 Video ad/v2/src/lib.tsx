import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {staticFile} from 'remotion';
import {loadFont} from '@remotion/fonts';
import tl from './timeline.json';

// Poppins (OFL) is bundled in public/fonts so renders work offline. latin-ext carries the ₱ sign.
export const fontFamily = 'Poppins';
const RANGES = {
	latin: 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD',
	'latin-ext': 'U+0100-02AF,U+0304,U+0308,U+0329,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF',
};
for (const w of ['500', '600', '700', '800']) {
	for (const [sub, unicodeRange] of Object.entries(RANGES)) {
		loadFont({family: fontFamily, url: staticFile(`fonts/poppins-${sub}-${w}-normal.woff2`), weight: w, unicodeRange});
	}
}

export const TL = tl;
export const FPS = tl.fps;
const FRAMES_PER_BEAT = (tl.fps * 60) / tl.bpm;

/** Frame number of a beat (beats can be fractional). Every cut lands on one. */
export const f = (beat: number) => Math.round(beat * FRAMES_PER_BEAT);
/** Length in frames of a [from, to] beat range. */
export const len = ([a, b]: number[]) => f(b) - f(a);

export const C = {
	green: '#0F7A45',
	deep: '#0A3B26',
	ink: '#14201A',
	cream: '#FFF4E0',
	amber: '#F2A93B',
	amberDeep: '#C9761F',
	mint: '#BFE8CF',
	white: '#FFFFFF',
	grey: '#9AA59F',
	red: '#E2574C',
};

export const peso = (n: number) => '₱' + Math.round(n).toLocaleString('en-US');

export const useLayout = () => {
	const {width, height} = useVideoConfig();
	const vertical = height > width;
	// type scale follows the short side so 16:9 and 9:16 read the same
	const u = Math.min(width, height) / 1080;
	return {width, height, vertical, u};
};

/** Spring that starts at `delay` frames into the current sequence. */
export const usePop = (delay = 0, damping = 12, stiffness = 180) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return spring({frame: frame - delay, fps, config: {damping, stiffness, mass: 0.6}});
};

/** Whip-in: slides in from the side with motion blur over a few frames. */
export const WhipIn: React.FC<{children: React.ReactNode; from?: 'left' | 'right' | 'up'; delay?: number; dur?: number; style?: React.CSSProperties}> = ({
	children,
	from = 'right',
	delay = 0,
	dur = 6,
	style,
}) => {
	const frame = useCurrentFrame();
	const p = interpolate(frame - delay, [0, dur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
	const dist = (1 - p) * 120;
	const tx = from === 'left' ? -dist : from === 'right' ? dist : 0;
	const ty = from === 'up' ? dist : 0;
	return (
		<div style={{transform: `translate(${tx}%, ${ty}%)`, filter: `blur(${(1 - p) * 24}px)`, opacity: p > 0 ? 1 : 0, ...style}}>{children}</div>
	);
};

/** Short camera shake on a hit, starting at `at` frames. */
export const useShake = (at: number, strength = 14, dur = 6) => {
	const frame = useCurrentFrame();
	const k = frame - at;
	if (k < 0 || k > dur) return 'translate(0,0)';
	const d = (1 - k / dur) * strength;
	return `translate(${Math.sin(k * 9.1) * d}px, ${Math.cos(k * 7.3) * d}px)`;
};

export const Fill: React.FC<{bg: string; children?: React.ReactNode; style?: React.CSSProperties}> = ({bg, children, style}) => (
	<div
		style={{
			position: 'absolute',
			inset: 0,
			background: bg,
			display: 'flex',
			alignItems: 'center',
			justifyContent: 'center',
			fontFamily,
			overflow: 'hidden',
			...style,
		}}
	>
		{children}
	</div>
);

/** The recurring habit motif: a ring that fills a little at every first. */
export const Ring: React.FC<{progress: number; size: number; color?: string; track?: string; stroke?: number}> = ({
	progress,
	size,
	color = C.amber,
	track = 'rgba(255,255,255,0.18)',
	stroke = 10,
}) => {
	const r = (size - stroke) / 2;
	const c = 2 * Math.PI * r;
	return (
		<svg width={size} height={size} style={{transform: 'rotate(-90deg)'}}>
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
				strokeDashoffset={c * (1 - Math.min(1, Math.max(0, progress)))}
			/>
		</svg>
	);
};

export const Coin: React.FC<{size: number}> = ({size}) => (
	<svg width={size} height={size} viewBox="0 0 100 100">
		<circle cx="50" cy="50" r="46" fill={C.amber} stroke={C.amberDeep} strokeWidth="6" />
		<circle cx="50" cy="50" r="34" fill="none" stroke={C.amberDeep} strokeWidth="3" opacity="0.6" />
		<text x="50" y="64" textAnchor="middle" fontSize="40" fontWeight="800" fill={C.amberDeep} fontFamily={fontFamily}>
			₱
		</text>
	</svg>
);
