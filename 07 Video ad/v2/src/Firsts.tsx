import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, E, Fill, MONO, Stage, Caption, ramp, mix, quad, useLayout, TL} from './lib';

/*
 * Six firsts, each 5+ years away. Each scene has its own motion graphic, and each one
 * starts from the last frame of the one before it, so the transition is part of the story:
 *   01 trip    dot → flight path
 *   02 car     flight path straightens into the road
 *   03 home    car speeds off, the building stacks up from the ground line
 *   04 "I do"  zoom through the lit window into the rings
 *   05 shop    iris out of a ring, the shutter rolls up
 *   06 school  the OPEN sign flips over into a notebook page
 */
export const FIRST_COUNT = 6;
const N = FIRST_COUNT;

/* ---------- shared geometry (stage units, 1000 × 600) ---------- */
export const MNL = [190, 410];
const CTRL = [500, 40];
const TYO = [810, 250];
const GROUND = 440;
const LANE = 485;

const Dot: React.FC<{x: number; y: number; r: number; color?: string; o?: number}> = ({x, y, r, color = C.accent, o = 1}) => (
	<circle cx={x} cy={y} r={Math.max(0, r)} fill={color} opacity={o} />
);

const Label: React.FC<{x: number; y: number; text: string; o: number}> = ({x, y, text, o}) => (
	<text x={x} y={y} textAnchor="middle" fontFamily={MONO} fontSize={22} letterSpacing="0.12em" fill={C.muted} opacity={o}>
		{text}
	</text>
);

const DotGrid: React.FC<{o: number}> = ({o}) => {
	const dots = [];
	for (let x = 20; x <= 980; x += 40) {
		for (let y = 20; y <= 580; y += 40) {
			const d = Math.hypot((x - 500) / 500, (y - 300) / 300);
			const a = Math.max(0, 1 - d) * o;
			if (a > 0.02) dots.push(<circle key={`${x}-${y}`} cx={x} cy={y} r={2.2} fill={C.ink} opacity={a * 0.35} />);
		}
	}
	return <g>{dots}</g>;
};

const Plane: React.FC<{x: number; y: number; a: number; s: number}> = ({x, y, a, s}) => (
	<g transform={`translate(${x} ${y}) rotate(${a}) scale(${s})`}>
		<path d="M26 0 L-10 -6 L-22 -24 L-28 -24 L-20 -5 L-30 -4 L-36 -12 L-40 -12 L-36 0 L-40 12 L-36 12 L-30 4 L-20 5 L-28 24 L-22 24 L-10 6 Z" fill={C.ink} />
	</g>
);

/* ---------- 01 · trip abroad ---------- */
export const Trip: React.FC = () => {
	const frame = useCurrentFrame();
	const t = ramp(frame, 2, 26, E.inOut);
	const p = quad(MNL, CTRL, TYO, t);
	const land = ramp(frame, 24, 32);
	return (
		<Fill bg={C.paper}>
			<Stage>
				<DotGrid o={ramp(frame, 0, 14)} />
				<mask id="arcMask">
					<path d={`M${MNL} Q${CTRL} ${TYO}`} stroke="white" strokeWidth={12} pathLength={1} strokeDasharray="1" strokeDashoffset={1 - t} />
				</mask>
				<path d={`M${MNL} Q${CTRL} ${TYO}`} stroke={C.ink} strokeWidth={4} strokeDasharray="2 14" mask="url(#arcMask)" />
				<Dot x={MNL[0]} y={MNL[1]} r={10} />
				<circle cx={TYO[0]} cy={TYO[1]} r={10 + land * 26} stroke={C.accent} strokeWidth={3} opacity={1 - land} />
				<Dot x={TYO[0]} y={TYO[1]} r={10 * ramp(frame, 22, 28)} />
				<Label x={MNL[0]} y={MNL[1] + 50} text="MNL" o={ramp(frame, 2, 10)} />
				<Label x={TYO[0]} y={TYO[1] + 50} text="TYO" o={ramp(frame, 20, 28)} />
				<Plane x={p.x} y={p.y} a={p.a} s={ramp(frame, 1, 6) * (1 - land)} />
			</Stage>
			<Caption n={1} total={N} lines={['Take Mom & Dad', 'abroad.']} />
		</Fill>
	);
};

/* ---------- 02 · first car ---------- */
const Car: React.FC<{x: number; tilt: number; spin: number}> = ({x, tilt, spin}) => (
	<g transform={`translate(${x} ${GROUND}) rotate(${tilt} 0 -30)`}>
		<path
			d="M-132 -30 L-132 -54 Q-130 -64 -118 -66 L-72 -68 L-42 -102 Q-36 -108 -26 -108 L46 -108 Q58 -108 66 -100 L98 -68 L122 -64 Q134 -60 134 -48 L134 -30 Z"
			fill={C.accent}
		/>
		<path d="M-34 -98 L-6 -98 L-6 -72 L-58 -72 Z" fill={C.paper} />
		<path d="M4 -98 L42 -98 Q50 -98 56 -92 L76 -72 L4 -72 Z" fill={C.paper} />
		{[-80, 84].map((wx) => (
			<g key={wx} transform={`translate(${wx} -24) rotate(${spin})`}>
				<circle r={24} fill={C.ink} />
				<circle r={9} fill={C.paper} />
				<path d="M0 -9 L0 -20" stroke={C.paper} strokeWidth={4} />
			</g>
		))}
	</g>
);

export const CarScene: React.FC = () => {
	const frame = useCurrentFrame();
	const m = ramp(frame, 0, 9, E.inOut);
	const p0 = [mix(MNL[0], -60, m), mix(MNL[1], LANE, m)];
	const p1 = [mix(CTRL[0], 500, m), mix(CTRL[1], LANE, m)];
	const p2 = [mix(TYO[0], 1060, m), mix(TYO[1], LANE, m)];
	const ground = ramp(frame, 4, 14);
	const drive = ramp(frame, 6, 22);
	const x = mix(-320, 500, drive);
	const v = 1 - drive; // speed, for tilt and speed lines
	const shrink = 1 - ramp(frame, 0, 6);
	return (
		<Fill bg={C.paper}>
			<Stage>
				<DotGrid o={shrink} />
				<path d={`M${p0} Q${p1} ${p2}`} stroke={C.ink} strokeWidth={4} strokeDasharray="2 14" strokeDashoffset={-frame * 9} opacity={mix(1, 0.5, m)} />
				<Dot x={MNL[0]} y={MNL[1]} r={10 * shrink} />
				<Dot x={TYO[0]} y={TYO[1]} r={10 * shrink} />
				<line x1={500 - 560 * ground} y1={GROUND} x2={500 + 560 * ground} y2={GROUND} stroke={C.ink} strokeWidth={4} />
				{[0, 1, 2].map((k) => (
					<line
						key={k}
						x1={x - 160 - k * 10}
						y1={GROUND - 40 - k * 26}
						x2={x - 160 - k * 10 - 260 * v}
						y2={GROUND - 40 - k * 26}
						stroke={C.muted}
						strokeWidth={4}
						opacity={v}
					/>
				))}
				<Car x={x} tilt={-4 * v + 2 * Math.sin(drive * Math.PI) * (1 - v)} spin={drive * 900} />
			</Stage>
			<Caption n={2} total={N} lines={['Buy your', 'first car.']} />
		</Fill>
	);
};

/* ---------- 03 · first home ---------- */
const FLOORS = 6;
const FH = 44;
export const LIT = {x: 558, y: GROUND - FH * 4 + 12 + 10}; // centre of the window that lights up

const Building: React.FC<{frame: number; lit: number}> = ({frame, lit}) => {
	const floor = (i: number) => {
		const p = ramp(frame, 6 + i * 2.4, 14 + i * 2.4);
		const top = GROUND - FH * (i + 1);
		return (
			<g key={i} transform={`translate(0 ${(1 - p) * -90})`} opacity={p}>
				<rect x={400} y={top} width={200} height={FH + 0.5} fill={C.ink} />
				{i === 0 ? (
					<rect x={482} y={top + 10} width={36} height={FH - 10} fill={C.paper} />
				) : (
					[424, 482, 540].map((wx) => (
						<rect
							key={wx}
							x={wx}
							y={top + 12}
							width={36}
							height={20}
							rx={2}
							fill={i === 3 && wx === 540 ? mixColor(lit) : C.paper}
							opacity={i === 3 && wx === 540 ? 1 : 0.9}
						/>
					))
				)}
			</g>
		);
	};
	const back = ramp(frame, 3, 14);
	const side = ramp(frame, 8, 18);
	return (
		<g>
			<rect x={610} y={GROUND - 210 * back} width={120} height={210 * back} fill={C.line} />
			<rect x={300} y={GROUND - 130 * side} width={90} height={130 * side} fill="#E5E3DB" />
			{Array.from({length: FLOORS}, (_, i) => floor(i))}
			<rect x={400} y={GROUND - FH * FLOORS - 10} width={200} height={10} fill={C.ink} opacity={ramp(frame, 20, 24)} />
		</g>
	);
};
const mixColor = (t: number) => (t > 0.5 ? C.accent : C.paper);

export const Home: React.FC = () => {
	const frame = useCurrentFrame();
	const go = ramp(frame, 0, 9, E.in);
	const lit = ramp(frame, 24, 26);
	return (
		<Fill bg={C.paper}>
			<Stage>
				<line x1={-60} y1={LANE} x2={1060} y2={LANE} stroke={C.ink} strokeWidth={4} strokeDasharray="2 14" opacity={0.5 * (1 - ramp(frame, 0, 8))} />
				<line x1={-60} y1={GROUND} x2={1060} y2={GROUND} stroke={C.ink} strokeWidth={4} />
				<Building frame={frame} lit={lit} />
				{lit > 0 ? <circle cx={LIT.x} cy={LIT.y} r={20 + 30 * ramp(frame, 25, 34)} fill={C.accent} opacity={0.25 * (1 - ramp(frame, 25, 34))} /> : null}
				<g transform={`translate(0 0) skewX(${-14 * go})`} opacity={1 - ramp(frame, 7, 9)}>
					<Car x={mix(500, 1500, go)} tilt={0} spin={go * 1400} />
				</g>
			</Stage>
			<Caption n={3} total={N} lines={['Get your', 'first home.']} />
		</Fill>
	);
};

/* ---------- 04 · "I do" ---------- */
const RING_L = [452, 300];
const RING_R = [548, 300];
export const IDo: React.FC = () => {
	const frame = useCurrentFrame();
	const zoom = ramp(frame, 0, 10, E.in);
	const s = Math.pow(120, zoom);
	const after = frame >= 10;
	const inL = ramp(frame, 9, 24);
	const inR = ramp(frame, 11, 26);
	const spark = ramp(frame, 22, 32);
	return (
		<Fill bg={after ? C.accent : C.paper}>
			{!after ? (
				<Stage>
					<g transform={`translate(${LIT.x} ${LIT.y}) scale(${s}) translate(${-LIT.x} ${-LIT.y})`}>
						<line x1={-60} y1={GROUND} x2={1060} y2={GROUND} stroke={C.ink} strokeWidth={4} />
						<Building frame={60} lit={1} />
					</g>
				</Stage>
			) : (
				<>
					<Stage>
						<circle cx={mix(-200, RING_L[0], inL)} cy={RING_L[1]} r={84} stroke={C.card} strokeWidth={16} />
						<circle cx={mix(1200, RING_R[0], inR)} cy={RING_R[1]} r={84} stroke={C.card} strokeWidth={16} />
						{Array.from({length: 8}, (_, k) => {
							const a = (k / 8) * Math.PI * 2;
							const r0 = 40 + 50 * spark;
							const r1 = r0 + 26 * (1 - spark);
							return (
								<line
									key={k}
									x1={500 + Math.cos(a) * r0}
									y1={170 + Math.sin(a) * r0}
									x2={500 + Math.cos(a) * r1}
									y2={170 + Math.sin(a) * r1}
									stroke={C.card}
									strokeWidth={5}
									opacity={spark > 0 ? 1 - spark : 0}
								/>
							);
						})}
					</Stage>
					<Caption n={4} total={N} lines={['Say your', 'first “I do.”']} dark at={12} />
				</>
			)}
		</Fill>
	);
};

/* ---------- 05 · first business ---------- */
export const SIGN = {x: 500, y: 299, w: 140, h: 54};
const Storefront: React.FC<{frame: number; swing: number}> = ({frame, swing}) => {
	const draw = ramp(frame, 8, 22, E.inOut);
	const awn = ramp(frame, 12, 22);
	const shutter = 1 - ramp(frame, 18, 28, E.inOut);
	return (
		<g>
			<line x1={-60} y1={GROUND} x2={1060} y2={GROUND} stroke={C.ink} strokeWidth={4} opacity={ramp(frame, 6, 14)} />
			<path d="M330 440 L330 170 L670 170 L670 440" stroke={C.ink} strokeWidth={5} pathLength={1} strokeDasharray="1" strokeDashoffset={1 - draw} />
			<g transform={`translate(0 ${(1 - awn) * -80})`} opacity={awn}>
				<rect x={306} y={136} width={388} height={62} rx={14} fill={C.accent} />
				{[372, 436, 500, 564, 628].map((x) => (
					<line key={x} x1={x} y1={146} x2={x} y2={188} stroke={C.card} strokeWidth={3} opacity={0.35} />
				))}
			</g>
			<clipPath id="win">
				<rect x={362} y={226} width={276} height={194} />
			</clipPath>
			<g clipPath="url(#win)" opacity={ramp(frame, 12, 16)}>
				<rect x={362} y={226} width={276} height={194} fill={C.accentSoft} />
				<g transform={`rotate(${swing} 500 236)`}>
					<line x1={470} y1={236} x2={462} y2={SIGN.y - SIGN.h / 2} stroke={C.ink} strokeWidth={3} />
					<line x1={530} y1={236} x2={538} y2={SIGN.y - SIGN.h / 2} stroke={C.ink} strokeWidth={3} />
					<rect x={SIGN.x - SIGN.w / 2} y={SIGN.y - SIGN.h / 2} width={SIGN.w} height={SIGN.h} rx={10} fill={C.accent} />
					<text x={SIGN.x} y={SIGN.y + 10} textAnchor="middle" fontFamily={MONO} fontSize={28} fontWeight={500} letterSpacing="0.14em" fill={C.card}>
						OPEN
					</text>
				</g>
				<g transform={`translate(0 ${-194 * (1 - shutter)})`}>
					<rect x={362} y={226} width={276} height={194} fill="#E2E0D8" />
					{Array.from({length: 13}, (_, k) => (
						<line key={k} x1={362} y1={240 + k * 14} x2={638} y2={240 + k * 14} stroke={C.muted} strokeWidth={2} opacity={0.6} />
					))}
					<rect x={362} y={412} width={276} height={8} fill={C.ink} />
				</g>
			</g>
		</g>
	);
};

const pendulum = (frame: number, from: number) => {
	const t = Math.max(0, frame - from) / 30;
	return frame < from ? 0 : 14 * Math.exp(-3 * t) * Math.sin(t * 11);
};

export const Shop: React.FC = () => {
	const frame = useCurrentFrame();
	const iris = ramp(frame, 0, 11, E.in);
	return (
		<Fill bg={frame < 11 ? C.accent : C.paper}>
			<Stage>
				{frame < 11 ? (
					<>
						<circle cx={RING_L[0]} cy={RING_L[1]} r={84} stroke={C.card} strokeWidth={16} />
						<circle cx={RING_R[0]} cy={RING_R[1]} r={84} stroke={C.card} strokeWidth={16} />
						<circle cx={RING_L[0]} cy={RING_L[1]} r={76 + iris * 1900} fill={C.paper} />
					</>
				) : null}
				<clipPath id="iris">
					<circle cx={RING_L[0]} cy={RING_L[1]} r={frame < 11 ? 76 + iris * 1900 : 5000} />
				</clipPath>
				{frame >= 6 ? (
					<g clipPath="url(#iris)">
						<Storefront frame={frame} swing={pendulum(frame, 24)} />
					</g>
				) : null}
			</Stage>
			{frame >= 10 ? <Caption n={5} total={N} lines={['Open your', 'first business.']} at={12} /> : null}
		</Fill>
	);
};

/* ---------- 06 · first day of school ---------- */
export const NOTEBOOK = '#FBFAF6';
export const RULE_GAP = 54;
export const Ruled: React.FC<{u: number; progress?: (k: number) => number; marginO?: number}> = ({u, progress, marginO = 1}) => {
	const {height} = useLayout();
	const n = Math.ceil(height / (RULE_GAP * u)) + 1;
	return (
		<>
			{Array.from({length: n}, (_, k) => (
				<div
					key={k}
					style={{
						position: 'absolute',
						left: 0,
						right: 0,
						top: (k + 1) * RULE_GAP * u,
						height: 2 * u,
						background: C.rule,
						transformOrigin: 'left center',
						transform: `scaleX(${progress ? progress(k) : 1})`,
					}}
				/>
			))}
			<div style={{position: 'absolute', top: 0, bottom: 0, left: 90 * u, width: 2 * u, background: C.margin, opacity: marginO}} />
		</>
	);
};

const Doodle: React.FC<{frame: number}> = ({frame}) => {
	const pen = {stroke: C.ink2, strokeWidth: 6, fill: 'none'} as const;
	const d = (a: number, b: number) => ({pathLength: 1, strokeDasharray: '1', strokeDashoffset: 1 - ramp(frame, a, b, E.soft)});
	return (
		<g>
			<g transform="translate(330 250)">
				<path d="M0 70 L24 0 L48 70 M10 44 L38 44" {...pen} {...d(13, 19)} />
				<path d="M74 0 L74 70 M74 0 Q114 0 114 17 Q114 34 74 34 Q118 34 118 52 Q118 70 74 70" {...pen} {...d(17, 23)} />
				<path d="M196 10 Q184 0 172 0 Q148 0 148 35 Q148 70 172 70 Q184 70 196 60" {...pen} {...d(21, 27)} />
			</g>
			<path
				d="M640 190 L656 228 L698 230 L666 256 L678 296 L640 274 L602 296 L614 256 L582 230 L624 228 Z"
				stroke={C.accent}
				strokeWidth={6}
				fill="none"
				pathLength={1}
				strokeDasharray="1"
				strokeDashoffset={1 - ramp(frame, 22, 32, E.soft)}
			/>
			<path d="M330 360 Q420 348 560 362" {...pen} strokeWidth={5} {...d(26, 32)} />
		</g>
	);
};

export const School: React.FC = () => {
	const frame = useCurrentFrame();
	const {u, width, height, toScreen, stage} = useLayout();
	const flip = ramp(frame, 0, 13, E.inOut);
	const c = toScreen(SIGN.x, SIGN.y);
	const w0 = SIGN.w * stage.s;
	const h0 = SIGN.h * stage.s;
	const w = mix(w0, width, flip);
	const h = mix(h0, height, flip);
	const cx = mix(c.x, width / 2, flip);
	const cy = mix(c.y, height / 2, flip);
	const settled = frame >= 13;
	return (
		<Fill bg={settled ? NOTEBOOK : C.paper}>
			{!settled ? (
				<>
					<Stage style={{opacity: 1 - ramp(frame, 0, 7)}}>
						<Storefront frame={60} swing={0} />
					</Stage>
					<div style={{position: 'absolute', left: cx - w / 2, top: cy - h / 2, width: w, height: h, perspective: 2000 * u}}>
						<div style={{position: 'absolute', inset: 0, transformStyle: 'preserve-3d', transform: `rotateY(${flip * 180}deg)`}}>
							<div
								style={{
									position: 'absolute',
									inset: 0,
									background: C.accent,
									borderRadius: mix(10 * stage.s, 0, flip),
									backfaceVisibility: 'hidden',
									display: 'flex',
									alignItems: 'center',
									justifyContent: 'center',
									color: C.card,
									fontFamily: MONO,
									fontSize: 28 * stage.s,
									letterSpacing: '0.14em',
								}}
							>
								OPEN
							</div>
							<div style={{position: 'absolute', inset: 0, background: NOTEBOOK, backfaceVisibility: 'hidden', transform: 'rotateY(180deg)', overflow: 'hidden'}}>
								<Ruled u={u} />
							</div>
						</div>
					</div>
				</>
			) : (
				<>
					<Ruled u={u} />
					<Stage>
						<Doodle frame={frame} />
						<text x={330} y={420} fontFamily={MONO} fontSize={22} letterSpacing="0.12em" fill={C.muted} opacity={ramp(frame, 26, 32)}>
							DAY 1
						</text>
					</Stage>
					<Caption n={6} total={N} lines={['Their first', 'day of school.']} at={13} />
				</>
			)}
		</Fill>
	);
};

export const FIRST_SCENES = [Trip, CarScene, Home, IDo, Shop, School];
export const FIRST_BEATS = TL.firstBeats;
