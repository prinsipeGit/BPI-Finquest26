import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import {f, len, TL} from './lib';
import {FIRST_SCENES, FIRST_BEATS} from './Firsts';
import {Intro, Fund, Pause, Always, Logo, Legal} from './Story';
import {Calculator, CALC_CUES} from './Calc';

const S = TL.sections;
const firstAt = (k: number) => S.firsts[0] + k * FIRST_BEATS;

// Placeholder sound design; to be redone with better SFX and an ElevenLabs voice-over.
const CUES: {beat: number; sfx: string; vol?: number}[] = [
	{beat: 0.1, sfx: 'ding', vol: 0.7},
	{beat: 3, sfx: 'whoosh', vol: 0.4},
	...FIRST_SCENES.map((_, k) => ({beat: firstAt(k) - 0.2, sfx: 'whoosh', vol: 0.45})),
	...FIRST_SCENES.map((_, k) => ({beat: firstAt(k) + 0.6, sfx: 'pop', vol: 0.5})),
	{beat: S.fund[0] + 1.4, sfx: 'shimmer', vol: 0.7},
	...CALC_CUES.map((c) => ({...c, beat: c.beat + S.calc[0]})),
	{beat: S.always[0] + 0.2, sfx: 'hit', vol: 0.7},
	{beat: S.logo[0], sfx: 'whoosh', vol: 0.6},
	{beat: S.logo[0] + 1, sfx: 'shimmer', vol: 0.6},
];

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
		<Scene range={S.pause}>
			<Pause />
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

		<Audio src={staticFile('audio/music.wav')} volume={0.75} />
		{CUES.map((c, k) => (
			<Sequence key={k} from={Math.max(0, f(c.beat))} layout="none">
				<Audio src={staticFile(`audio/${c.sfx}.wav`)} volume={c.vol ?? 1} />
			</Sequence>
		))}
	</AbsoluteFill>
);
