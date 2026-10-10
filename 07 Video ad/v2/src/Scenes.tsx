import React from 'react';
import {interpolate, useCurrentFrame, Easing} from 'remotion';
import {C, f, Fill, fontFamily, Ring, Coin, usePop, useShake, useLayout, WhipIn, TL} from './lib';
import {Plane, Car, Condo, RingIcon, Shop, Backpack} from './icons';

const S = TL.sections;

/* ---------------- 0–4: hook ---------------- */
export const Hook: React.FC = () => {
	const frame = useCurrentFrame();
	const {u, vertical} = useLayout();
	const drop = usePop(2, 14, 200);
	const slam = usePop(f(1.6), 9, 260);
	const sub = usePop(f(2.6), 12, 220);
	const shake = useShake(f(1.6), 18);
	return (
		<Fill bg={C.ink} style={{flexDirection: 'column', transform: shake}}>
			{/* notification */}
			<div
				style={{
					position: 'absolute',
					top: (vertical ? 260 : 70) * u,
					transform: `translateY(${(1 - drop) * -220 * u}px)`,
					width: 760 * u,
					padding: `${22 * u}px ${30 * u}px`,
					borderRadius: 30 * u,
					background: 'rgba(255,255,255,0.12)',
					backdropFilter: 'blur(10px)',
					display: 'flex',
					alignItems: 'center',
					gap: 22 * u,
					color: C.white,
				}}
			>
				<div style={{width: 64 * u, height: 64 * u, borderRadius: 16 * u, background: C.green, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
					<Coin size={44 * u} />
				</div>
				<div style={{flex: 1}}>
					<div style={{fontSize: 22 * u, opacity: 0.7, fontWeight: 500}}>Payroll · now</div>
					<div style={{fontSize: 32 * u, fontWeight: 700}}>Pumasok na ang unang sahod mo!</div>
				</div>
			</div>
			<div style={{textAlign: 'center', color: C.cream, marginTop: (vertical ? 120 : 110) * u}}>
				<div style={{fontSize: 128 * u, fontWeight: 800, lineHeight: 1, transform: `scale(${0.4 + 0.6 * slam})`, opacity: slam > 0.02 ? 1 : 0, letterSpacing: -2 * u}}>
					First paycheck?
				</div>
				<div style={{fontSize: 64 * u, fontWeight: 700, marginTop: 28 * u, color: C.amber, transform: `translateY(${(1 - sub) * 60 * u}px)`, opacity: sub}}>
					Fund your next firsts.
				</div>
			</div>
		</Fill>
	);
};

/* ---------------- 4–16: montage of firsts (each 5+ years away) ---------------- */
const FIRSTS = [
	{Icon: Plane, line: 'Unang biyahe abroad', sub: 'kasama sina Ma & Pa', bg: C.green, fg: C.cream, accent: C.amber},
	{Icon: Car, line: 'Unang kotse', sub: 'na ikaw ang nagbayad', bg: C.amber, fg: C.ink, accent: C.cream},
	{Icon: Condo, line: 'Unang condo', sub: 'sariling susi', bg: C.cream, fg: C.deep, accent: C.mint},
	{Icon: RingIcon, line: 'Unang “I do”', sub: 'the big day', bg: C.deep, fg: C.cream, accent: C.amber},
	{Icon: Shop, line: 'Unang negosyo', sub: 'your own name on the door', bg: C.green, fg: C.cream, accent: C.mint},
	{Icon: Backpack, line: 'First school year', sub: 'ng anak mo', bg: C.amber, fg: C.ink, accent: C.cream},
];
export const MONTAGE_CARD_BEATS = (S.montage[1] - S.montage[0]) / FIRSTS.length;

export const FirstCard: React.FC<{i: number}> = ({i}) => {
	const frame = useCurrentFrame();
	const {u, vertical} = useLayout();
	const it = FIRSTS[i];
	const icon = usePop(0, 10, 220);
	const text = usePop(3, 11, 240);
	const coinY = interpolate(frame, [0, 7], [-300, 0], {extrapolateRight: 'clamp', easing: Easing.in(Easing.quad)});
	const fill = interpolate(frame, [6, 12], [i / FIRSTS.length, (i + 1) / FIRSTS.length], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const zoom = interpolate(frame, [0, f(MONTAGE_CARD_BEATS)], [1, 1.06]);
	const ringTrack = it.bg === C.cream || it.bg === C.amber ? 'rgba(0,0,0,0.12)' : 'rgba(255,255,255,0.18)';
	const ringColor = it.bg === C.amber ? C.deep : C.amber;
	return (
		<Fill bg={it.bg}>
			<div
				style={{
					display: 'flex',
					flexDirection: vertical ? 'column' : 'row',
					alignItems: 'center',
					gap: 60 * u,
					transform: `scale(${zoom})`,
					color: it.fg,
				}}
			>
				<div style={{transform: `scale(${icon}) rotate(${(1 - icon) * -25}deg)`}}>
					<it.Icon size={(vertical ? 420 : 380) * u} color={it.fg} accent={it.accent} />
				</div>
				<div style={{textAlign: vertical ? 'center' : 'left', transform: `translateX(${(1 - text) * 80 * u}px)`, opacity: text}}>
					<div style={{fontSize: 110 * u, fontWeight: 800, lineHeight: 1.02, letterSpacing: -2 * u, maxWidth: (vertical ? 900 : 900) * u}}>{it.line}</div>
					<div style={{fontSize: 54 * u, fontWeight: 500, marginTop: 16 * u, opacity: 0.85}}>{it.sub}</div>
				</div>
			</div>
			{/* counter */}
			<div style={{position: 'absolute', top: 50 * u, right: 60 * u, fontSize: 64 * u, fontWeight: 800, color: it.fg, opacity: 0.9}}>
				First #{i + 1}
			</div>
			{/* habit motif: coin drops into a ring that fills a little at every first */}
			<div style={{position: 'absolute', bottom: 50 * u, right: 60 * u, width: 150 * u, height: 150 * u}}>
				<Ring progress={fill} size={150 * u} stroke={14 * u} color={ringColor} track={ringTrack} />
				<div style={{position: 'absolute', left: 35 * u, top: 35 * u, transform: `translateY(${coinY * u}px)`}}>
					<Coin size={80 * u} />
				</div>
			</div>
		</Fill>
	);
};

/* ---------------- 16–18: "Paano magsimula?" ---------------- */
export const HowTo: React.FC = () => {
	const {u} = useLayout();
	return (
		<Fill bg={C.cream}>
			<WhipIn from="left">
				<div style={{fontSize: 150 * u, fontWeight: 800, color: C.deep, letterSpacing: -3 * u, textAlign: 'center', lineHeight: 1}}>
					Paano <span style={{color: C.green}}>magsimula?</span>
				</div>
			</WhipIn>
		</Fill>
	);
};

/* ---------------- 44–46: silence ---------------- */
export const Silence: React.FC = () => <Fill bg="#000" />;

/* ---------------- 46–50: there's always a new first ---------------- */
export const Always: React.FC = () => {
	const frame = useCurrentFrame();
	const {u} = useLayout();
	const flip = interpolate(frame, [f(0.3), f(0.9)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
	const words = "There's always a new first.".split(' ');
	const dropAt = f(2); // the beat drops two beats after the piano note
	const flash = interpolate(frame, [dropAt, dropAt + 8], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const bg = frame >= dropAt ? C.green : '#000';
	const shake = useShake(dropAt, 16);
	return (
		<Fill bg={bg} style={{flexDirection: 'column', transform: shake}}>
			<div style={{position: 'absolute', inset: 0, background: C.cream, opacity: frame >= dropAt ? flash * 0.8 : 0}} />
			<div style={{height: 200 * u, overflow: 'hidden', position: 'relative', width: 600 * u, textAlign: 'center'}}>
				<div style={{transform: `translateY(${-flip * 200 * u}px)`}}>
					<div style={{height: 200 * u, fontSize: 170 * u, fontWeight: 800, color: C.grey, lineHeight: `${200 * u}px`}}>#7</div>
					<div style={{height: 200 * u, fontSize: 330 * u, fontWeight: 700, color: C.amber, lineHeight: `${200 * u}px`}}>∞</div>
				</div>
			</div>
			<div style={{fontSize: 104 * u, fontWeight: 800, color: C.cream, marginTop: 30 * u, textAlign: 'center', letterSpacing: -2 * u, padding: `0 ${60 * u}px`}}>
				{words.map((w, k) => {
					const at = f(0.8 + k * 0.25);
					const o = interpolate(frame, [at, at + 4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
					return (
						<span key={k} style={{display: 'inline-block', opacity: o, transform: `translateY(${(1 - o) * 30 * u}px)`, marginRight: 24 * u}}>
							{w}
						</span>
					);
				})}
			</div>
		</Fill>
	);
};

/* ---------------- 50–56: logo ---------------- */
export const Logo: React.FC = () => {
	const frame = useCurrentFrame();
	const {u} = useLayout();
	const ring = interpolate(frame, [0, f(1.5)], [0.05, 1], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
	const word = usePop(f(0.5), 12, 200);
	const tag = usePop(f(1.5), 12, 200);
	const cta = usePop(f(2.5), 14, 200);
	const orbit = [0, 1, 2, 3, 4, 5];
	return (
		<Fill bg={C.green} style={{flexDirection: 'column'}}>
			<div style={{position: 'relative', width: 260 * u, height: 260 * u}}>
				{/* the six firsts converge into one ring */}
				{orbit.map((k) => {
					const a = (k / orbit.length) * Math.PI * 2;
					const d = interpolate(frame, [0, f(1)], [520, 0], {extrapolateRight: 'clamp', easing: Easing.in(Easing.cubic)});
					const o = interpolate(frame, [f(0.8), f(1)], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
					return (
						<div key={k} style={{position: 'absolute', left: (90 + Math.cos(a) * d) * u, top: (90 + Math.sin(a) * d) * u, opacity: o}}>
							<Coin size={80 * u} />
						</div>
					);
				})}
				<div style={{position: 'absolute', inset: 0}}>
					<Ring progress={ring} size={260 * u} stroke={26 * u} color={C.amber} track="rgba(255,255,255,0.15)" />
				</div>
			</div>
			<div style={{fontSize: 140 * u, fontWeight: 800, color: C.cream, marginTop: 40 * u, letterSpacing: -3 * u, transform: `scale(${0.6 + 0.4 * word})`, opacity: word}}>
				Firsts Fund
			</div>
			<div style={{fontSize: 70 * u, fontWeight: 700, color: C.amber, marginTop: 6 * u, transform: `translateY(${(1 - tag) * 40 * u}px)`, opacity: tag}}>
				Fund your firsts.
			</div>
			<div
				style={{
					fontSize: 38 * u,
					fontWeight: 600,
					color: C.deep,
					background: C.cream,
					borderRadius: 999,
					padding: `${14 * u}px ${36 * u}px`,
					marginTop: 40 * u,
					transform: `scale(${cta})`,
				}}
			>
				Start with as little as ₱100
			</div>
		</Fill>
	);
};

/* ---------------- 56–62: legal ---------------- */
export const Legal: React.FC = () => {
	const {u, vertical} = useLayout();
	const o = usePop(0, 20, 120);
	return (
		<Fill bg={C.cream} style={{flexDirection: 'column', padding: `0 ${(vertical ? 70 : 220) * u}px`}}>
			<div style={{display: 'flex', alignItems: 'center', gap: 24 * u, opacity: o}}>
				<Ring progress={1} size={90 * u} stroke={12 * u} color={C.amber} track="rgba(0,0,0,0.1)" />
				<div>
					<div style={{fontSize: 64 * u, fontWeight: 800, color: C.deep, lineHeight: 1}}>Firsts Fund</div>
					<div style={{fontSize: 34 * u, fontWeight: 700, color: C.green}}>Fund your firsts.</div>
				</div>
			</div>
			<div style={{fontSize: 27 * u, lineHeight: 1.45, color: C.ink, marginTop: 44 * u, textAlign: 'center', opacity: o, fontFamily, fontWeight: 500}}>
				Firsts Fund is a proposed unit investment trust fund (UITF) concept for BPI Wealth FinQuest 2026. The ₱100 minimum, the calculator and the features shown are
				proposed. UITFs are not deposits and are not insured by the PDIC. Returns are not guaranteed, and the value of your investment can go down as well as up. The
				calculator example shows contributions only (₱150,000 ÷ 60 months) and assumes no investment return. For goals at least five years away.
			</div>
		</Fill>
	);
};
