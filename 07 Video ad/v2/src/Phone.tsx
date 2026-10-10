import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {C, f, Fill, Ring, Coin, peso, useLayout, TL} from './lib';

/*
 * Onboarding calculator, beats 18–44. The real calculator is still being built; it works out
 * the monthly contribution from the first's amount and how far away it is (minimum 5 years).
 * The ad shows contributions only: amount ÷ months, no assumed return.
 */
const P0 = TL.sections.phone[0];
const rel = (r: number[]) => [r[0] - P0, r[1] - P0];
const STEP = {
	s1: rel(TL.phone.step1),
	s2: rel(TL.phone.step2),
	s3: rel(TL.phone.step3),
	res: rel(TL.phone.result),
	start: rel(TL.phone.start),
	next: rel(TL.phone.next),
};
const EX = TL.example;
const MONTHLY = EX.amount / (EX.years * 12);

// key moments, in beats from the start of the phone scene
const T = {
	typeFrom: STEP.s1[0] + 0.4,
	typeTo: STEP.s1[0] + 3.0,
	countFrom: STEP.s2[0] + 0.4,
	countTo: STEP.s2[0] + 2.6,
	dragFrom: STEP.s3[0] + 0.8,
	dragTo: STEP.s3[0] + 2.6,
	snap: STEP.s3[0] + 3.4,
	tapStart: STEP.start[0] + 1.5,
	tapNext: STEP.next[0] + 0.3,
	cards: [STEP.next[0] + 1.0, STEP.next[0] + 1.8, STEP.next[0] + 2.6],
};

const NEXT = [
	{name: 'Unang kotse', amount: 300000, years: 6},
	{name: 'Unang condo (DP)', amount: 500000, years: 8},
	{name: 'Retirement trip', amount: 400000, years: 30},
];

/** Sound cues for the phone scene, in beats from its start (used by the composition). */
export const PHONE_CUES: {beat: number; sfx: string; vol?: number}[] = [
	...Array.from({length: 9}, (_, k) => ({beat: T.typeFrom + (k * (T.typeTo - T.typeFrom)) / 9, sfx: 'type', vol: 0.7})),
	...Array.from({length: 9}, (_, k) => ({beat: T.countFrom + (k * (T.countTo - T.countFrom)) / 9, sfx: 'tick', vol: 0.6})),
	{beat: T.dragFrom, sfx: 'whoosh', vol: 0.3},
	{beat: T.snap, sfx: 'snap'},
	{beat: STEP.res[0], sfx: 'shimmer'},
	{beat: T.tapStart, sfx: 'tap'},
	{beat: T.tapStart + 0.15, sfx: 'coin'},
	{beat: T.tapNext, sfx: 'tap'},
	...T.cards.map((b) => ({beat: b, sfx: 'coin', vol: 0.7})),
];

const CAPTIONS: {at: number[]; n?: string; title: string; sub: string}[] = [
	{at: STEP.s1, n: '1', title: 'Pangalanan ang first mo', sub: 'Name your first'},
	{at: STEP.s2, n: '2', title: 'Magkano?', sub: 'How much it will cost'},
	{at: STEP.s3, n: '3', title: 'Kailan?', sub: '5 years or more from now'},
	{at: STEP.res, title: 'Ito ang monthly mo', sub: 'Your monthly contribution'},
	{at: STEP.start, title: 'Start with as little as ₱100', sub: 'Then keep the habit going'},
	{at: STEP.next, title: 'Tapos, next first naman', sub: 'Same habit, bagong goal'},
];

const useBeat = () => {
	const frame = useCurrentFrame();
	return (frame * TL.bpm) / (60 * TL.fps);
};

const clampI = (b: number, inR: number[], outR: number[], ease = Easing.out(Easing.cubic)) =>
	interpolate(b, inR, outR, {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});

const useSpringAt = (beat: number, damping = 12) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return spring({frame: frame - f(beat), fps, config: {damping, stiffness: 200, mass: 0.6}});
};

/* ---------- phone internals, drawn in a 360 × 760 box and scaled ---------- */
const W = 360;
const H = 760;

const Field: React.FC<{label: string; appear: number; active: boolean; children: React.ReactNode}> = ({label, appear, active, children}) => {
	const p = useSpringAt(appear);
	return (
		<div
			style={{
				background: C.white,
				borderRadius: 18,
				padding: '12px 16px',
				marginBottom: 12,
				border: `3px solid ${active ? C.green : '#E3E8E5'}`,
				transform: `translateY(${(1 - p) * 40}px)`,
				opacity: p,
			}}
		>
			<div style={{fontSize: 15, color: '#58635C', fontWeight: 600}}>{label}</div>
			{children}
		</div>
	);
};

const Calculator: React.FC<{b: number}> = ({b}) => {
	const chars = Math.floor(clampI(b, [T.typeFrom, T.typeTo], [0, EX.name.length], Easing.linear));
	const caret = Math.floor(b * 4) % 2 === 0 && b < STEP.s2[0];
	const amount = clampI(b, [T.countFrom, T.countTo], [0, EX.amount]);

	// slider: starts at 10 years, dragged into the locked zone (2 years), snaps back to 5
	const snapP = useSpringAt(T.snap, 8);
	let years = 10;
	if (b >= T.dragFrom) years = clampI(b, [T.dragFrom, T.dragTo], [10, 2], Easing.inOut(Easing.quad));
	if (b >= T.snap) years = 2 + 3 * snapP;
	const warn = b >= T.dragTo - 0.6 && b < T.snap + 0.6;
	const shown = b >= T.snap ? EX.years : Math.round(years);

	const res = useSpringAt(STEP.res[0], 10);
	const btn = useSpringAt(STEP.start[0], 10);
	const pulse = b >= STEP.start[0] && b < T.tapStart ? 1 + 0.04 * Math.sin((b - STEP.start[0]) * Math.PI * 2) : 1;
	const press = b >= T.tapStart && b < T.tapStart + 0.3 ? 0.94 : 1;

	const trackW = W - 44 - 38;
	const maxY = 30;
	const x = (years / maxY) * trackW;
	const lockW = (5 / maxY) * trackW;

	return (
		<div style={{padding: '0 22px'}}>
			<div style={{fontSize: 26, fontWeight: 800, color: C.deep, margin: '6px 0 14px'}}>Bagong first</div>
			<Field label="Name your first" appear={STEP.s1[0]} active={b < STEP.s2[0]}>
				<div style={{fontSize: 26, fontWeight: 700, color: C.ink, minHeight: 36}}>
					{EX.name.slice(0, chars)}
					<span style={{opacity: caret ? 1 : 0, color: C.green}}>|</span>
				</div>
			</Field>
			<Field label="How much?" appear={STEP.s2[0]} active={b >= STEP.s2[0] && b < STEP.s3[0]}>
				<div style={{fontSize: 34, fontWeight: 800, color: C.ink}}>{peso(amount)}</div>
			</Field>
			<Field label="When?" appear={STEP.s3[0]} active={b >= STEP.s3[0] && b < STEP.res[0]}>
				<div style={{fontSize: 28, fontWeight: 800, color: warn ? C.red : C.ink}}>
					{shown} taon <span style={{fontSize: 18, fontWeight: 600, color: '#58635C'}}>· {shown * 12} buwan</span>
				</div>
				<div style={{position: 'relative', height: 34, marginTop: 6}}>
					<div style={{position: 'absolute', top: 13, left: 0, width: trackW, height: 8, borderRadius: 4, background: '#E3E8E5'}} />
					<div
						style={{
							position: 'absolute',
							top: 11,
							left: 0,
							width: lockW,
							height: 12,
							borderRadius: 4,
							background: 'repeating-linear-gradient(45deg, #C9D3CD 0 4px, #E3E8E5 4px 8px)',
						}}
					/>
					<div style={{position: 'absolute', top: 13, left: lockW, width: Math.max(0, x - lockW), height: 8, borderRadius: 4, background: C.green}} />
					<div
						style={{
							position: 'absolute',
							top: 2,
							left: x - 15,
							width: 30,
							height: 30,
							borderRadius: 15,
							background: warn ? C.red : C.green,
							border: '4px solid white',
							boxShadow: '0 2px 6px rgba(0,0,0,0.25)',
						}}
					/>
				</div>
				<div style={{fontSize: 14, fontWeight: 700, height: 20, color: warn ? C.red : '#9AA59F'}}>
					{warn ? 'Firsts Fund is for firsts 5+ years away' : 'Minimum 5 years'}
				</div>
			</Field>
			<div
				style={{
					background: C.green,
					color: C.cream,
					borderRadius: 18,
					padding: '14px 18px',
					marginBottom: 12,
					transform: `scale(${0.7 + 0.3 * res})`,
					opacity: res,
				}}
			>
				<div style={{fontSize: 15, fontWeight: 600, opacity: 0.85}}>Your monthly contribution</div>
				<div style={{fontSize: 44, fontWeight: 800, lineHeight: 1.1}}>
					{peso(MONTHLY)}
					<span style={{fontSize: 22, fontWeight: 700}}> / buwan</span>
				</div>
				<div style={{fontSize: 13, fontWeight: 500, opacity: 0.85}}>
					{peso(EX.amount)} ÷ {EX.years * 12} months · contributions only
				</div>
			</div>
			<div
				style={{
					background: C.amber,
					color: C.ink,
					borderRadius: 999,
					textAlign: 'center',
					padding: '14px 0',
					fontSize: 22,
					fontWeight: 800,
					transform: `scale(${btn * pulse * press})`,
				}}
			>
				Start with ₱100
			</div>
		</div>
	);
};

const FirstRow: React.FC<{name: string; years: number; monthly: number; appear: number; started?: boolean}> = ({name, years, monthly, appear, started}) => {
	const p = useSpringAt(appear, 11);
	return (
		<div
			style={{
				display: 'flex',
				alignItems: 'center',
				gap: 14,
				background: C.white,
				borderRadius: 18,
				padding: '14px 16px',
				marginBottom: 12,
				transform: `translateX(${(1 - p) * 120}%) scale(${0.9 + 0.1 * p})`,
			}}
		>
			<div style={{position: 'relative', width: 54, height: 54}}>
				<Ring progress={started ? 0.12 : 0.04} size={54} stroke={7} color={C.amber} track="#E3E8E5" />
			</div>
			<div style={{flex: 1}}>
				<div style={{fontSize: 19, fontWeight: 800, color: C.ink, lineHeight: 1.15, whiteSpace: 'nowrap'}}>{name}</div>
				<div style={{fontSize: 14, fontWeight: 600, color: '#58635C'}}>
					{years} taon · {peso(monthly)}/buwan
					{started ? <span style={{color: C.green, fontWeight: 800}}> · Started ✓</span> : null}
				</div>
			</div>
		</div>
	);
};

const MyFirsts: React.FC<{b: number}> = ({b}) => {
	const press = b >= T.tapNext && b < T.tapNext + 0.3 ? 0.94 : 1;
	return (
		<div style={{padding: '0 22px'}}>
			<div style={{fontSize: 26, fontWeight: 800, color: C.deep, margin: '6px 0 14px'}}>My firsts</div>
			<FirstRow name={EX.name} years={EX.years} monthly={MONTHLY} appear={T.tapStart + 0.2} started />
			<div
				style={{
					border: `3px dashed ${C.green}`,
					color: C.green,
					borderRadius: 18,
					textAlign: 'center',
					padding: '12px 0',
					fontSize: 20,
					fontWeight: 800,
					marginBottom: 12,
					transform: `scale(${press})`,
				}}
			>
				+ Add your next first
			</div>
			{NEXT.map((n, k) => (
				<FirstRow key={k} name={n.name} years={n.years} monthly={n.amount / (n.years * 12)} appear={T.cards[k]} />
			))}
		</div>
	);
};

const Finger: React.FC<{b: number; at: number; x: number; y: number}> = ({b, at, x, y}) => {
	const o = clampI(b, [at - 0.6, at - 0.2], [0, 1]) * clampI(b, [at + 0.4, at + 0.8], [1, 0]);
	const s = b < at ? 1 : clampI(b, [at, at + 0.25], [0.7, 1]);
	const ripple = clampI(b, [at, at + 0.6], [0, 1]);
	return (
		<div style={{position: 'absolute', left: x - 30, top: y - 30, width: 60, height: 60, opacity: o, pointerEvents: 'none'}}>
			<div style={{position: 'absolute', inset: 0, borderRadius: 30, background: 'rgba(20,32,26,0.35)', transform: `scale(${s})`}} />
			<div style={{position: 'absolute', inset: 0, borderRadius: 30, border: '3px solid rgba(20,32,26,0.5)', transform: `scale(${1 + ripple * 1.2})`, opacity: 1 - ripple}} />
		</div>
	);
};

const Screen: React.FC = () => {
	const b = useBeat();
	const swap = clampI(b, [T.tapStart + 0.15, T.tapStart + 0.55], [0, 1], Easing.inOut(Easing.cubic));
	return (
		<div style={{width: W, height: H, background: '#F4F7F5', borderRadius: 50, overflow: 'hidden', position: 'relative'}}>
			{/* status bar + app header */}
			<div style={{height: 44, display: 'flex', justifyContent: 'space-between', padding: '14px 34px 0', fontSize: 15, fontWeight: 700, color: C.ink}}>
				<span>9:41</span>
				<span>●●● ▮</span>
			</div>
			<div style={{display: 'flex', alignItems: 'center', gap: 10, padding: '10px 22px 6px'}}>
				<Ring progress={0.75} size={34} stroke={6} color={C.amber} track="#D6DED9" />
				<div style={{fontSize: 22, fontWeight: 800, color: C.green}}>Firsts Fund</div>
			</div>
			<div style={{position: 'relative', height: H - 110}}>
				<div style={{position: 'absolute', inset: 0, transform: `translateX(${-swap * 100}%)`}}>
					<Calculator b={b} />
				</div>
				<div style={{position: 'absolute', inset: 0, transform: `translateX(${(1 - swap) * 100}%)`}}>
					<MyFirsts b={b} />
				</div>
			</div>
			<Finger b={b} at={T.tapStart} x={W / 2} y={H - 66} />
			<Finger b={b} at={T.tapNext} x={W / 2} y={300} />
		</div>
	);
};

/* ---------- the scene: phone + step caption ---------- */
export const PhoneScene: React.FC = () => {
	const frame = useCurrentFrame();
	const b = useBeat();
	const {u, vertical} = useLayout();
	const phoneH = (vertical ? 1180 : 960) * u;
	const s = phoneH / (H + 24);
	const enter = clampI(frame, [0, 7], [1, 0]);
	const cap = CAPTIONS.find((c) => b >= c.at[0] && b < c.at[1]) ?? CAPTIONS[CAPTIONS.length - 1];
	const capIn = clampI(b, [cap.at[0], cap.at[0] + 0.4], [0, 1]);

	const caption = (
		<div
			key={cap.title}
			style={{
				width: (vertical ? 960 : 820) * u,
				textAlign: vertical ? 'center' : 'left',
				transform: `translateX(${(1 - capIn) * (vertical ? 0 : 60) * u}px) translateY(${(1 - capIn) * (vertical ? 40 : 0) * u}px)`,
				opacity: capIn,
				filter: `blur(${(1 - capIn) * 10}px)`,
			}}
		>
			{cap.n ? (
				<div
					style={{
						display: 'inline-flex',
						alignItems: 'center',
						justifyContent: 'center',
						width: 96 * u,
						height: 96 * u,
						borderRadius: 48 * u,
						background: C.amber,
						color: C.ink,
						fontSize: 56 * u,
						fontWeight: 800,
						marginBottom: 22 * u,
					}}
				>
					{cap.n}
				</div>
			) : (
				<div style={{marginBottom: 22 * u, display: 'inline-block'}}>
					<Coin size={96 * u} />
				</div>
			)}
			<div style={{fontSize: (vertical ? 92 : 100) * u, fontWeight: 800, color: C.cream, lineHeight: 1.02, letterSpacing: -2 * u}}>{cap.title}</div>
			<div style={{fontSize: 46 * u, fontWeight: 500, color: C.mint, marginTop: 16 * u}}>{cap.sub}</div>
		</div>
	);

	return (
		<Fill bg={C.deep} style={{flexDirection: vertical ? 'column' : 'row', gap: (vertical ? 50 : 110) * u}}>
			{vertical ? caption : null}
			<div
				style={{
					width: (W + 24) * s,
					height: phoneH,
					transform: `translateY(${enter * 110}%)`,
					filter: `blur(${enter * 20}px)`,
					flexShrink: 0,
				}}
			>
				<div style={{transform: `scale(${s})`, transformOrigin: 'top left', width: W + 24, height: H + 24, background: '#0B1410', borderRadius: 62, padding: 12}}>
					<Screen />
				</div>
			</div>
			{vertical ? null : caption}
		</Fill>
	);
};
