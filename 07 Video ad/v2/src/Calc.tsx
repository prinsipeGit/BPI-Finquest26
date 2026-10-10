import React from 'react';
import {spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, E, Fill, LABEL, MiniRing, Rise, ramp, mix, peso, useLayout, f, TL} from './lib';

/*
 * Onboarding calculator. The real one is still being built; it works out the monthly
 * contribution from the first's amount and how far away it is (minimum 5 years).
 * The ad shows contributions only: amount ÷ months, no assumed return.
 */
const K = TL.calc;
const EX = TL.example;
const MONTHLY = EX.amount / (EX.years * 12);

// key moments, in beats from the start of the scene
export const T = {
	typeFrom: K.name[0] + 0.35,
	typeTo: K.name[0] + 2.4,
	countFrom: K.amount[0] + 0.3,
	countTo: K.amount[0] + 2.2,
	dragFrom: K.when[0] + 0.6,
	dragTo: K.when[0] + 2.0,
	snap: K.when[0] + 2.6,
	press: K.start[0] + 0.9,
	morph: K.next[0],
	rows: [K.next[0] + 0.9, K.next[0] + 1.5, K.next[0] + 2.1],
};

const NEXT = [
	{name: 'First car', amount: 300000, years: 6},
	{name: 'First home down payment', amount: 500000, years: 8},
	{name: 'Retirement trip', amount: 400000, years: 30},
];

const STEPS: {at: number[]; label: string; title: string}[] = [
	{at: K.name, label: 'STEP 01', title: 'Name your first.'},
	{at: K.amount, label: 'STEP 02', title: 'Set how much it costs.'},
	{at: K.when, label: 'STEP 03', title: 'Pick a date at least 5 years away.'},
	{at: K.result, label: 'YOUR PLAN', title: 'See what to set aside each month.'},
	{at: K.start, label: 'START', title: 'Start with as little as ₱100.'},
	{at: K.next, label: 'KEEP GOING', title: 'Then fund your next first.'},
];

const beatOf = (frame: number) => (frame * TL.bpm) / (60 * TL.fps);

const Check: React.FC<{size: number; color: string}> = ({size, color}) => (
	<svg width={size} height={size} viewBox="0 0 24 24" fill="none">
		<path d="M5 12.5 L10 17 L19 7" stroke={color} strokeWidth={3} strokeLinecap="round" strokeLinejoin="round" />
	</svg>
);

/* ---------- the form card ---------- */
const CARD_H = 840;
const ROW_H = 132;

const FieldLabel: React.FC<{u: number; text: string; active: boolean}> = ({u, text, active}) => (
	<div style={{fontFamily: LABEL, fontWeight: 500, fontSize: 20 * u, letterSpacing: '0.12em', color: active ? C.accent : C.muted}}>{text}</div>
);

const Underline: React.FC<{u: number; active: boolean; done: boolean}> = ({u, active, done}) => (
	<div style={{height: 2 * u, background: active ? C.accent : done ? C.ink : C.line, marginTop: 12 * u}} />
);

const Form: React.FC<{b: number; frame: number; u: number; w: number}> = ({b, frame, u, w}) => {
	const {fps} = useVideoConfig();
	const chars = Math.floor(ramp(b, T.typeFrom, T.typeTo, (t) => t) * EX.name.length);
	const caret = b < K.amount[0] && Math.floor(frame / 8) % 2 === 0;
	const amount = ramp(b, T.countFrom, T.countTo, E.soft) * EX.amount;
	const snapP = spring({frame: frame - f(T.snap), fps, config: {damping: 9, stiffness: 220, mass: 0.6}});
	let years = 10;
	if (b >= T.dragFrom) years = mix(10, 2, ramp(b, T.dragFrom, T.dragTo, E.inOut));
	if (b >= T.snap) years = 2 + 3 * snapP;
	const warn = b >= T.dragTo - 0.5 && b < T.snap + 0.4;
	const shownYears = b >= T.snap ? EX.years : Math.max(1, Math.round(years));
	const res = ramp(b, K.result[0], K.result[0] + 0.8);
	const monthly = ramp(b, K.result[0] + 0.1, K.result[0] + 1.0, E.soft) * MONTHLY;
	const btn = ramp(b, K.start[0], K.start[0] + 0.5);
	const press = b >= T.press && b < T.press + 0.35 ? 0.95 : 1;
	const ripple = ramp(b, T.press, T.press + 0.9);
	const active = (r: number[]) => b >= r[0] && b < r[1];
	const done = (r: number[]) => b >= r[1];
	const pad = 52 * u;
	const inner = w - pad * 2;
	const trackW = inner;
	const x = (years / 30) * trackW;
	const lockW = (5 / 30) * trackW;
	return (
		<div style={{position: 'absolute', left: pad, top: 0, width: inner}}>
			{/* header */}
			<div style={{position: 'absolute', top: 44 * u, left: 0, right: 0, display: 'flex', alignItems: 'center', gap: 14 * u}}>
				<MiniRing progress={0.75} size={30 * u} stroke={5 * u} color={C.accent} track={C.line} />
				<div style={{fontSize: 30 * u, fontWeight: 600, letterSpacing: '-0.03em', color: C.ink, flex: 1}}>New first</div>
				<div style={{fontFamily: LABEL, fontWeight: 500, fontSize: 18 * u, letterSpacing: '0.12em', color: C.muted}}>FIRSTS FUND</div>
			</div>
			{/* name */}
			<div style={{position: 'absolute', top: 130 * u, left: 0, right: 0}}>
				<FieldLabel u={u} text="NAME YOUR FIRST" active={active(K.name)} />
				<div style={{fontSize: 42 * u, fontWeight: 500, letterSpacing: '-0.03em', color: C.ink, marginTop: 8 * u, height: 52 * u, whiteSpace: 'nowrap'}}>
					{EX.name.slice(0, chars)}
					<span style={{color: C.accent, opacity: caret ? 1 : 0}}>|</span>
				</div>
				<Underline u={u} active={active(K.name)} done={done(K.name)} />
			</div>
			{/* amount */}
			<div style={{position: 'absolute', top: 262 * u, left: 0, right: 0}}>
				<FieldLabel u={u} text="TARGET AMOUNT" active={active(K.amount)} />
				<div style={{fontSize: 42 * u, fontWeight: 500, letterSpacing: '-0.03em', color: b >= K.amount[0] ? C.ink : C.line, marginTop: 8 * u, height: 52 * u}}>
					{peso(amount)}
				</div>
				<Underline u={u} active={active(K.amount)} done={done(K.amount)} />
			</div>
			{/* when */}
			<div style={{position: 'absolute', top: 394 * u, left: 0, right: 0}}>
				<div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline'}}>
					<FieldLabel u={u} text="WHEN" active={active(K.when)} />
					<div style={{fontFamily: LABEL, fontWeight: 500, fontSize: 18 * u, letterSpacing: '0.08em', color: warn ? C.warn : C.muted}}>
						{warn ? 'FIRSTS START AT 5 YEARS' : 'MINIMUM 5 YEARS'}
					</div>
				</div>
				<div style={{fontSize: 42 * u, fontWeight: 500, letterSpacing: '-0.03em', color: b < K.when[0] ? C.line : warn ? C.warn : C.ink, marginTop: 8 * u, height: 52 * u}}>
					{shownYears} years <span style={{fontSize: 26 * u, color: C.muted}}>· {shownYears * 12} months</span>
				</div>
				<div style={{position: 'relative', height: 40 * u, marginTop: 14 * u, opacity: b >= K.when[0] ? 1 : 0.35}}>
					<div style={{position: 'absolute', top: 17 * u, left: 0, width: trackW, height: 6 * u, borderRadius: 3 * u, background: C.line}} />
					<div
						style={{
							position: 'absolute',
							top: 14 * u,
							left: 0,
							width: lockW,
							height: 12 * u,
							borderRadius: 3 * u,
							background: `repeating-linear-gradient(45deg, ${C.line} 0 ${4 * u}px, ${C.paper} ${4 * u}px ${8 * u}px)`,
						}}
					/>
					<div style={{position: 'absolute', top: 17 * u, left: lockW, width: Math.max(0, x - lockW), height: 6 * u, borderRadius: 3 * u, background: C.accent}} />
					<div
						style={{
							position: 'absolute',
							top: 4 * u,
							left: x - 16 * u,
							width: 32 * u,
							height: 32 * u,
							borderRadius: 16 * u,
							background: C.card,
							border: `${3 * u}px solid ${warn ? C.warn : C.accent}`,
							boxShadow: '0 4px 12px rgba(14,16,14,0.15)',
						}}
					/>
				</div>
			</div>
			{/* result */}
			<div
				style={{
					position: 'absolute',
					top: 556 * u,
					left: 0,
					right: 0,
					height: 158 * u,
					borderRadius: 22 * u,
					background: C.accentSoft,
					padding: `${22 * u}px ${28 * u}px`,
					boxSizing: 'border-box',
					opacity: res,
					transform: `translateY(${(1 - res) * 24 * u}px)`,
				}}
			>
				<FieldLabel u={u} text="MONTHLY CONTRIBUTION" active />
				<div style={{fontSize: 64 * u, fontWeight: 600, letterSpacing: '-0.05em', color: C.accent, lineHeight: 1.1}}>
					{peso(monthly)}
					<span style={{fontSize: 28 * u, fontWeight: 500, color: C.ink2, letterSpacing: '-0.02em'}}> / month</span>
				</div>
				<div style={{fontFamily: LABEL, fontWeight: 500, fontSize: 16 * u, letterSpacing: '0.06em', color: C.ink2, marginTop: 2 * u}}>
					{peso(EX.amount)} ÷ {EX.years * 12} MONTHS · CONTRIBUTIONS ONLY
				</div>
			</div>
			{/* button */}
			<div style={{position: 'absolute', top: 738 * u, left: 0, right: 0, height: 74 * u, opacity: btn, transform: `scale(${press})`}}>
				<div
					style={{
						position: 'absolute',
						inset: 0,
						borderRadius: 999,
						background: C.ink,
						color: C.card,
						fontSize: 28 * u,
						fontWeight: 500,
						display: 'flex',
						alignItems: 'center',
						justifyContent: 'center',
						overflow: 'hidden',
					}}
				>
					Start with ₱100
					<div
						style={{
							position: 'absolute',
							left: '50%',
							top: '50%',
							width: 40 * u,
							height: 40 * u,
							marginLeft: -20 * u,
							marginTop: -20 * u,
							borderRadius: 999,
							background: 'rgba(255,255,255,0.25)',
							transform: `scale(${ripple * 30})`,
							opacity: ripple > 0 ? 1 - ripple : 0,
						}}
					/>
				</div>
			</div>
		</div>
	);
};

const Row: React.FC<{u: number; name: string; years: number; monthly: number; started?: boolean}> = ({u, name, years, monthly, started}) => (
	<div style={{display: 'flex', alignItems: 'center', gap: 22 * u, height: ROW_H * u, padding: `0 ${40 * u}px`, boxSizing: 'border-box'}}>
		<MiniRing progress={started ? 0.15 : 0.03} size={54 * u} stroke={6 * u} color={C.accent} track={C.line} />
		<div style={{flex: 1, minWidth: 0}}>
			<div style={{fontSize: 32 * u, fontWeight: 600, letterSpacing: '-0.03em', color: C.ink, whiteSpace: 'nowrap'}}>{name}</div>
			<div style={{fontFamily: LABEL, fontWeight: 500, fontSize: 18 * u, letterSpacing: '0.08em', color: C.muted, marginTop: 4 * u}}>
				{years} YEARS · {peso(monthly)}/MONTH
			</div>
		</div>
		{started ? (
			<div style={{display: 'flex', alignItems: 'center', gap: 6 * u, background: C.accentSoft, color: C.accent, borderRadius: 999, padding: `${8 * u}px ${16 * u}px`, fontSize: 20 * u, fontWeight: 600}}>
				<Check size={20 * u} color={C.accent} />
				Started
			</div>
		) : null}
	</div>
);

export const Calculator: React.FC = () => {
	const frame = useCurrentFrame();
	const b = beatOf(frame);
	const {u, vertical, width, height} = useLayout();
	const cardW = (vertical ? 940 : 860) * u;
	const cardX = vertical ? (width - cardW) / 2 : width - cardW - 120 * u;
	const cardTop = vertical ? 640 * u : (height - CARD_H * u) / 2;
	const enter = ramp(frame, 0, 14);
	const morph = ramp(b, T.morph, T.morph + 0.7, E.inOut);
	const cardH = mix(CARD_H, ROW_H, morph) * u;
	const listTop = vertical ? 700 * u : cardTop + 120 * u;
	const top = mix(cardTop, listTop, morph);
	const step = STEPS.find((s) => b >= s.at[0] && b < s.at[1]) ?? STEPS[STEPS.length - 1];
	const stepFrame = f(step.at[0]);
	return (
		<Fill bg={C.paper}>
			{/* step caption */}
			<div
				key={step.label}
				style={{
					position: 'absolute',
					left: vertical ? 80 * u : 120 * u,
					top: vertical ? 250 * u : 400 * u,
					width: vertical ? 920 * u : 700 * u,
					color: C.ink,
				}}
			>
				<div style={{fontFamily: LABEL, fontWeight: 500, fontSize: 24 * u, letterSpacing: '0.12em', color: C.accent, opacity: ramp(frame, stepFrame, stepFrame + 6)}}>{step.label}</div>
				<div style={{fontSize: (vertical ? 84 : 80) * u, fontWeight: 600, letterSpacing: '-0.045em', lineHeight: 1.02, marginTop: 18 * u}}>
					<Rise at={stepFrame + 1}>{step.title}</Rise>
				</div>
			</div>
			{/* card that turns into the first row of the list */}
			<div
				style={{
					position: 'absolute',
					left: cardX,
					top: top + (1 - enter) * 160 * u,
					width: cardW,
					height: cardH,
					background: C.card,
					borderRadius: 32 * u,
					boxShadow: '0 30px 80px rgba(14,16,14,0.10), 0 2px 6px rgba(14,16,14,0.04)',
					overflow: 'hidden',
					opacity: enter,
				}}
			>
				<div style={{opacity: 1 - ramp(b, T.morph, T.morph + 0.3)}}>
					<Form b={b} frame={frame} u={u} w={cardW} />
				</div>
				<div style={{position: 'absolute', inset: 0, opacity: ramp(b, T.morph + 0.4, T.morph + 0.8)}}>
					<Row u={u} name={EX.name} years={EX.years} monthly={MONTHLY} started />
				</div>
			</div>
			{NEXT.map((n, k) => {
				const p = ramp(b, T.rows[k], T.rows[k] + 0.6);
				return (
					<div
						key={k}
						style={{
							position: 'absolute',
							left: cardX,
							top: listTop + (k + 1) * (ROW_H + 18) * u,
							width: cardW,
							height: ROW_H * u,
							background: C.card,
							borderRadius: 32 * u,
							boxShadow: '0 20px 50px rgba(14,16,14,0.08)',
							opacity: p,
							transform: `translateY(${(1 - p) * 60 * u}px)`,
						}}
					>
						<Row u={u} name={n.name} years={n.years} monthly={n.amount / (n.years * 12)} />
					</div>
				);
			})}
		</Fill>
	);
};

/** Sound cues, in beats from the start of the scene. */
export const CALC_CUES: {beat: number; sfx: string; vol?: number}[] = [
	...Array.from({length: 10}, (_, k) => ({beat: T.typeFrom + (k * (T.typeTo - T.typeFrom)) / 10, sfx: 'type', vol: 0.6})),
	...Array.from({length: 8}, (_, k) => ({beat: T.countFrom + (k * (T.countTo - T.countFrom)) / 8, sfx: 'tick', vol: 0.5})),
	{beat: T.snap, sfx: 'snap'},
	{beat: K.result[0], sfx: 'shimmer', vol: 0.8},
	{beat: T.press, sfx: 'tap'},
	...T.rows.map((r) => ({beat: r, sfx: 'pop', vol: 0.8})),
];
