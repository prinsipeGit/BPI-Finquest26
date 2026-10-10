import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import {f, len, TL} from './lib';
import {Hook, FirstCard, MONTAGE_CARD_BEATS, HowTo, Silence, Always, Logo, Legal} from './Scenes';
import {PhoneScene, PHONE_CUES} from './Phone';

const S = TL.sections;

// One-shot sound effects, placed on beats.
const CUES: {beat: number; sfx: string; vol?: number}[] = [
	{beat: 0.1, sfx: 'ding'},
	{beat: 1.6, sfx: 'hit', vol: 0.9},
	...Array.from({length: 6}, (_, k) => ({beat: S.montage[0] + k * MONTAGE_CARD_BEATS, sfx: 'coin', vol: 0.8})),
	...Array.from({length: 6}, (_, k) => ({beat: S.montage[0] + k * MONTAGE_CARD_BEATS - 0.25, sfx: 'whoosh', vol: 0.35})),
	{beat: S.howto[0] - 0.3, sfx: 'whoosh', vol: 0.8},
	{beat: S.phone[0] - 0.3, sfx: 'whoosh', vol: 0.6},
	...PHONE_CUES.map((c) => ({...c, beat: c.beat + S.phone[0]})),
	{beat: S.always[0] + 2, sfx: 'hit'},
	{beat: S.logo[0], sfx: 'hit', vol: 0.8},
	{beat: S.logo[0] + 1.5, sfx: 'shimmer', vol: 0.8},
	{beat: S.logo[0] + 2.5, sfx: 'coin', vol: 0.8},
];

const Scene: React.FC<{range: number[]; children: React.ReactNode}> = ({range, children}) => (
	<Sequence from={f(range[0])} durationInFrames={len(range)} layout="none">
		<AbsoluteFill>{children}</AbsoluteFill>
	</Sequence>
);

export const FirstsAd: React.FC = () => (
	<AbsoluteFill style={{background: '#000'}}>
		<Scene range={S.hook}>
			<Hook />
		</Scene>
		{Array.from({length: 6}, (_, k) => {
			const a = S.montage[0] + k * MONTAGE_CARD_BEATS;
			return (
				<Scene key={k} range={[a, a + MONTAGE_CARD_BEATS]}>
					<FirstCard i={k} />
				</Scene>
			);
		})}
		<Scene range={S.howto}>
			<HowTo />
		</Scene>
		<Scene range={S.phone}>
			<PhoneScene />
		</Scene>
		<Scene range={S.silence}>
			<Silence />
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

		<Audio src={staticFile('audio/music.wav')} volume={0.8} />
		{CUES.map((c, k) => (
			<Sequence key={k} from={Math.max(0, f(c.beat))} layout="none">
				<Audio src={staticFile(`audio/${c.sfx}.wav`)} volume={c.vol ?? 1} />
			</Sequence>
		))}
	</AbsoluteFill>
);
