import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, E, Fill, MONO, SANS, Rise, ramp, mix, useLayout, f} from './lib';
import {MNL, NOTEBOOK, Ruled} from './Firsts';

const Accent: React.FC<{children: React.ReactNode; color?: string}> = ({children, color = C.accent}) => <span style={{color}}>{children}</span>;

/* ---------- intro: "You just got your first paycheck. What do you do first?" ---------- */
export const Intro: React.FC = () => {
	const frame = useCurrentFrame();
	const {u, vertical, width, height, toScreen} = useLayout();
	const size = (vertical ? 116 : 136) * u;
	const left = (vertical ? 80 : 120) * u;
	const swap = f(3) - 4; // first line leaves on beat 3
	const end = f(6);
	const chip = ramp(frame, 0, 12) * (1 - ramp(frame, swap, swap + 8, E.in));
	// the dot that becomes Manila on the flight path
	const dotIn = ramp(frame, end - 16, end - 11);
	const travel = ramp(frame, end - 11, end, E.inOut);
	const from = {x: width / 2, y: height / 2};
	const to = toScreen(MNL[0], MNL[1]);
	const dotR = mix(26, 10 * (vertical ? 1 : 1.08), travel) * u;
	return (
		<Fill bg={C.paper}>
			{/* salary notification */}
			<div
				style={{
					position: 'absolute',
					left,
					top: (vertical ? 640 : 250) * u,
					display: 'flex',
					alignItems: 'center',
					gap: 16 * u,
					padding: `${16 * u}px ${26 * u}px`,
					background: C.card,
					borderRadius: 999,
					boxShadow: '0 10px 30px rgba(14,16,14,0.08)',
					opacity: chip,
					transform: `translateY(${(1 - chip) * -30 * u}px)`,
				}}
			>
				<div style={{width: 14 * u, height: 14 * u, borderRadius: 7 * u, background: C.accent}} />
				<span style={{fontFamily: MONO, fontSize: 24 * u, letterSpacing: '0.1em', color: C.ink2}}>SALARY CREDITED</span>
				<span style={{fontFamily: MONO, fontSize: 24 * u, color: C.accent}}>+₱28,000.00</span>
			</div>
			<div
				style={{
					position: 'absolute',
					left,
					top: (vertical ? 760 : 380) * u,
					fontSize: size,
					fontWeight: 600,
					letterSpacing: '-0.05em',
					lineHeight: 1.0,
					color: C.ink,
				}}
			>
				<Rise at={3} out={swap}>
					You just got your
				</Rise>
				<Rise at={6} out={swap + 2}>
					<Accent>first</Accent> paycheck.
				</Rise>
			</div>
			<div
				style={{
					position: 'absolute',
					left,
					top: (vertical ? 760 : 380) * u,
					fontSize: size,
					fontWeight: 600,
					letterSpacing: '-0.05em',
					lineHeight: 1.0,
					color: C.ink,
				}}
			>
				<Rise at={swap + 10} out={end - 16}>
					What do you
				</Rise>
				<Rise at={swap + 13} out={end - 14}>
					do <Accent>first?</Accent>
				</Rise>
			</div>
			<div
				style={{
					position: 'absolute',
					left: mix(from.x, to.x, travel) - dotR,
					top: mix(from.y, to.y, travel) - dotR,
					width: dotR * 2,
					height: dotR * 2,
					borderRadius: dotR,
					background: C.accent,
					transform: `scale(${dotIn})`,
				}}
			/>
		</Fill>
	);
};

/* ---------- "Fund your firsts." ---------- */
export const Fund: React.FC = () => {
	const frame = useCurrentFrame();
	const {u, vertical, width, height} = useLayout();
	const exit = f(4) - 10;
	const page = 1 - ramp(frame, 6, 14);
	// six dots, one per first, gather into one ring
	const cx = width / 2;
	const cy = height / 2 - (vertical ? 300 : 230) * u;
	const gather = ramp(frame, 12, 22, E.inOut);
	const ringDraw = ramp(frame, 20, 32);
	const out = ramp(frame, exit, exit + 9, E.in);
	const size = (vertical ? 170 : 190) * u;
	const r = 46 * u;
	const circ = 2 * Math.PI * r;
	return (
		<Fill bg={C.paper}>
			<div style={{position: 'absolute', inset: 0, background: NOTEBOOK, opacity: page > 0 ? 1 : 0}}>
				<Ruled u={u} progress={(k) => 1 - ramp(frame, k * 0.6, 9 + k * 0.6, E.in)} marginO={page} />
			</div>
			<div style={{position: 'absolute', inset: 0, opacity: 1 - out, transform: `translateY(${-out * 60 * u}px)`}}>
				{Array.from({length: 6}, (_, k) => {
					const pop = ramp(frame, 4 + k * 1.2, 10 + k * 1.2);
					const x = mix(cx + (k - 2.5) * 56 * u, cx + Math.cos((k / 6) * Math.PI * 2 - Math.PI / 2) * r, gather);
					const y = mix(cy, cy + Math.sin((k / 6) * Math.PI * 2 - Math.PI / 2) * r, gather);
					const d = 18 * u * pop * (1 - ringDraw);
					return <div key={k} style={{position: 'absolute', left: x - d / 2, top: y - d / 2, width: d, height: d, borderRadius: d, background: C.accent}} />;
				})}
				<svg width={r * 2 + 20 * u} height={r * 2 + 20 * u} style={{position: 'absolute', left: cx - r - 10 * u, top: cy - r - 10 * u, transform: 'rotate(-90deg)'}}>
					<circle cx={r + 10 * u} cy={r + 10 * u} r={r} fill="none" stroke={C.accent} strokeWidth={12 * u} strokeLinecap="round" strokeDasharray={circ} strokeDashoffset={circ * (1 - ringDraw)} opacity={ringDraw > 0 ? 1 : 0} />
				</svg>
				<div
					style={{
						position: 'absolute',
						left: 0,
						right: 0,
						top: height / 2 - (vertical ? 120 : 60) * u,
						textAlign: 'center',
						fontSize: size,
						fontWeight: 600,
						letterSpacing: '-0.055em',
						lineHeight: 1.0,
						color: C.ink,
					}}
				>
					{vertical ? (
						<>
							<Rise at={10}>Fund your</Rise>
							<Rise at={14}>
								<Underlined frame={frame} u={u}>
									firsts.
								</Underlined>
							</Rise>
						</>
					) : (
						<Rise at={10}>
							Fund your{' '}
							<Underlined frame={frame} u={u}>
								firsts.
							</Underlined>
						</Rise>
					)}
				</div>
			</div>
		</Fill>
	);
};

const Underlined: React.FC<{frame: number; u: number; children: React.ReactNode}> = ({frame, u, children}) => (
	<span style={{position: 'relative', color: C.accent, display: 'inline-block'}}>
		{children}
		<span
			style={{
				position: 'absolute',
				left: '2%',
				right: '8%',
				bottom: 4 * u,
				height: 12 * u,
				borderRadius: 6 * u,
				background: C.accent,
				transformOrigin: 'left center',
				transform: `scaleX(${ramp(frame, 22, 34)})`,
			}}
		/>
	</span>
);

/* ---------- one beat of quiet ---------- */
export const Pause: React.FC = () => {
	const frame = useCurrentFrame();
	const {u, width, height} = useLayout();
	const d = 16 * u * (0.6 + 0.4 * Math.sin(ramp(frame, 0, 14) * Math.PI));
	return (
		<Fill bg={C.paper}>
			<div style={{position: 'absolute', left: width / 2 - d / 2, top: height / 2 - d / 2, width: d, height: d, borderRadius: d, background: C.accent}} />
		</Fill>
	);
};

/* ---------- "There will always be a new first." ---------- */
const AlwaysText: React.FC<{frame: number}> = ({frame}) => {
	const {u, vertical, height} = useLayout();
	const tick = ramp(frame, 0, 34, (t) => t * t);
	const n = Math.min(99, 7 + Math.floor(tick * 92));
	const inf = frame >= 36;
	const size = (vertical ? 100 : 150) * u;
	return (
		<div style={{position: 'absolute', left: 0, right: 0, top: height / 2 - (vertical ? 230 : 190) * u, textAlign: 'center', color: C.ink}}>
			<div style={{fontFamily: MONO, fontSize: 30 * u, letterSpacing: '0.14em', color: C.muted, height: 50 * u}}>
				FIRST <span style={{color: C.accent, fontFamily: inf ? SANS : MONO, fontSize: inf ? 40 * u : 30 * u}}>{inf ? '∞' : String(n).padStart(2, '0')}</span>
			</div>
			<div style={{fontSize: size, fontWeight: 600, letterSpacing: '-0.05em', lineHeight: 1.02, marginTop: 30 * u}}>
				<Rise at={4}>There will always be</Rise>
				<Rise at={8}>
					a <Accent>new first.</Accent>
				</Rise>
			</div>
		</div>
	);
};

export const Always: React.FC = () => {
	const frame = useCurrentFrame();
	return (
		<Fill bg={C.paper}>
			<AlwaysText frame={frame} />
		</Fill>
	);
};

/* ---------- logo ---------- */
const Mark: React.FC<{size: number; draw: number}> = ({size, draw}) => {
	const st = size * 0.14;
	const r = (size - st) / 2;
	const c = 2 * Math.PI * r;
	return (
		<svg width={size} height={size} style={{transform: 'rotate(-90deg)'}}>
			<circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(255,255,255,0.12)" strokeWidth={st} />
			<circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={C.glow} strokeWidth={st} strokeLinecap="round" strokeDasharray={c} strokeDashoffset={c * (1 - draw)} />
		</svg>
	);
};

export const Logo: React.FC = () => {
	const frame = useCurrentFrame();
	const {u, vertical} = useLayout();
	const panel = ramp(frame, 0, 11, E.inOut);
	const draw = ramp(frame, 8, 30, E.inOut);
	const cta = ramp(frame, 30, 42);
	return (
		<Fill bg={C.paper}>
			<AlwaysText frame={60} />
			<div
				style={{
					position: 'absolute',
					inset: 0,
					background: C.night,
					transform: `translateY(${(1 - panel) * 100}%)`,
					display: 'flex',
					flexDirection: 'column',
					alignItems: 'center',
					justifyContent: 'center',
					color: C.card,
				}}
			>
				<Mark size={150 * u} draw={draw} />
				<div style={{fontSize: (vertical ? 140 : 150) * u, fontWeight: 600, letterSpacing: '-0.05em', marginTop: 46 * u, lineHeight: 1}}>
					<Rise at={12}>Firsts Fund</Rise>
				</div>
				<div style={{fontSize: 60 * u, fontWeight: 500, letterSpacing: '-0.03em', marginTop: 18 * u, color: 'rgba(255,255,255,0.72)'}}>
					<Rise at={18}>
						Fund your <Accent color={C.glow}>firsts.</Accent>
					</Rise>
				</div>
				<div
					style={{
						marginTop: 56 * u,
						padding: `${18 * u}px ${36 * u}px`,
						borderRadius: 999,
						border: `${2 * u}px solid rgba(255,255,255,0.25)`,
						fontSize: 32 * u,
						fontWeight: 500,
						opacity: cta,
						transform: `translateY(${(1 - cta) * 20 * u}px)`,
					}}
				>
					Start with as little as ₱100
				</div>
			</div>
		</Fill>
	);
};

/* ---------- legal ---------- */
export const Legal: React.FC = () => {
	const frame = useCurrentFrame();
	const {u, vertical} = useLayout();
	const o = ramp(frame, 0, 10);
	return (
		<Fill bg={C.night} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: `0 ${(vertical ? 80 : 260) * u}px`}}>
			<div style={{display: 'flex', alignItems: 'center', gap: 22 * u, color: C.card}}>
				<Mark size={70 * u} draw={1} />
				<div>
					<div style={{fontSize: 52 * u, fontWeight: 600, letterSpacing: '-0.04em', lineHeight: 1}}>Firsts Fund</div>
					<div style={{fontSize: 28 * u, fontWeight: 500, color: 'rgba(255,255,255,0.7)', marginTop: 6 * u}}>
						Fund your <Accent color={C.glow}>firsts.</Accent>
					</div>
				</div>
			</div>
			<div style={{fontSize: 25 * u, lineHeight: 1.55, color: 'rgba(255,255,255,0.62)', marginTop: 50 * u, textAlign: 'center', opacity: o, letterSpacing: '-0.005em'}}>
				Firsts Fund is a proposed unit investment trust fund (UITF) concept for BPI Wealth FinQuest 2026. The ₱100 minimum, the calculator and the features shown are
				proposed. UITFs are not deposits and are not insured by the PDIC. Returns are not guaranteed, and the value of your investment can go down as well as up. The
				calculator example shows contributions only (₱150,000 ÷ 60 months) and assumes no investment return. For goals at least five years away.
			</div>
		</Fill>
	);
};
