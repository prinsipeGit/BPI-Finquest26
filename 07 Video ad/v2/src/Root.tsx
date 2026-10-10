import React from 'react';
import {Composition} from 'remotion';
import {FirstsAd} from './Ad';
import {f, TL} from './lib';

// Two frames shorter than 62 beats so the AAC padding keeps the file at 30.0 s or less.
const DURATION = f(TL.totalBeats) - 2;

export const RemotionRoot: React.FC = () => (
	<>
		<Composition id="FirstsAdV2" component={FirstsAd} durationInFrames={DURATION} fps={TL.fps} width={1920} height={1080} />
		<Composition id="FirstsAdV2Vertical" component={FirstsAd} durationInFrames={DURATION} fps={TL.fps} width={1080} height={1920} />
	</>
);
