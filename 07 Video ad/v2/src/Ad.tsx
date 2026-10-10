import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile} from 'remotion';
import {f, len, TL} from './lib';
import {FIRST_SCENES, FIRST_BEATS} from './Firsts';
import {Intro, Fund, Always, Logo, Legal} from './Story';
import {Calculator, CALC_CUES} from './Calc';
import VO from './vo.json';

const S = TL.sections;
const firstAt = (k: number) => S.firsts[0] + k * FIRST_BEATS;
const fps = TL.fps;
const sec = (s: number) => Math.round(s * fps);

// ElevenLabs sound effects (public/audio/sfx), placed on beats. `max` trims a clip to that many seconds.
const CUES: {beat: number; sfx: string; vol?: number; max?: number}[] = [
	{beat: 0.05, sfx: 'notif', vol: 0.5},
	{beat: firstAt(0) - 0.3, sfx: 'whoosh', vol: 0.5},
	{beat: firstAt(0) + 0.5, sfx: 'plane', vol: 0.35},
	{beat: firstAt(1) + 0.4, sfx: 'car', vol: 0.5},
	{beat: firstAt(2), sfx: 'car', vol: 0.3},
	{beat: firstAt(2) + 0.6, sfx: 'stack', vol: 0.5},
	{beat: firstAt(3) - 0.5, sfx: 'riser', vol: 0.4},
	{beat: firstAt(3) + 2.1, sfx: 'shutter', vol: 0.35, max: 1.3},
	{beat: firstAt(4), sfx: 'page', vol: 0.6},
	{beat: firstAt(4) + 1.2, sfx: 'pencil', vol: 0.4},
	{beat: S.fund[0] - 1.7, sfx: 'riser', vol: 0.3},
	{beat: S.fund[0] + 0.6, sfx: 'boom', vol: 0.6},
	{beat: S.calc[0] - 0.2, sfx: 'whoosh', vol: 0.45},
	...CALC_CUES.map((c) => ({...c, beat: c.beat + S.calc[0]})),
	{beat: S.logo[0], sfx: 'whoosh', vol: 0.45},
	{beat: S.logo[0] + 0.4, sfx: 'boom', vol: 0.7},
	{beat: S.logo[0] + 2.1, sfx: 'success', vol: 0.3},
];

// Music dips under the voice: full level between lines, about a third while someone speaks.
const MUSIC_UP = 0.5;
const MUSIC_DOWN = 0.18;
const speaking = VO.map((v) => [sec(v.at), sec(v.at + v.dur)]);
const musicVolume = (frame: number) => {
	let d = 1; // 1 = no voice nearby, 0 = voice playing
	for (const [a, b] of speaking) {
		if (frame >= a && frame <= b) return MUSIC_DOWN;
		d = Math.min(d, interpolate(frame, [a - 6, a, b, b + 9], [1, 0, 0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
	}
	return MUSIC_DOWN + (MUSIC_UP - MUSIC_DOWN) * d;
};

const Scene: React.FC<{range: number[]; children: React.ReactNode}> = ({range, children}) => (
	<Sequence from={f(range[0])} durationInFrames={len(range)} layout="none">
		<AbsoluteFill>{children}</AbsoluteFill>
	</Sequence>
);

export const FirstsAd: React.FC = () => (
	<AbsoluteFill style={{background: '#000'}}>
		<Scene range={S.intro}>
			<Intro />
		</Scene>
		{FIRST_SCENES.map((Comp, k) => (
			<Scene key={k} range={[firstAt(k), firstAt(k + 1)]}>
				<Comp />
			</Scene>
		))}
		<Scene range={S.fund}>
			<Fund />
		</Scene>
		<Scene range={S.calc}>
			<Calculator />
		</Scene>
		<Scene range={S.always}>
			<Always />
		</Scene>
		<Scene range={S.logo}>
			<Logo />
		</Scene>
		<Scene range={S.legal}>
			<Legal />
		</Scene>

		{/* placeholder music bed (scripts/make_audio.py) until a licensed or ElevenLabs track is in */}
		<Audio src={staticFile('audio/music.wav')} volume={musicVolume} />
		{/* voice-over: ElevenLabs "Justin Case - Warm, Trustworthy, Clear", one line per clip */}
		{VO.map((v, k) => (
			<Sequence key={`vo${k}`} from={sec(v.at)} layout="none">
				<Audio src={staticFile(v.file)} volume={1} />
			</Sequence>
		))}
		{CUES.map((c, k) => (
			<Sequence key={k} from={Math.max(0, f(c.beat))} durationInFrames={c.max ? sec(c.max) : undefined} layout="none">
				<Audio src={staticFile(`audio/sfx/${c.sfx}.wav`)} volume={c.vol ?? 1} />
			</Sequence>
		))}
	</AbsoluteFill>
);
