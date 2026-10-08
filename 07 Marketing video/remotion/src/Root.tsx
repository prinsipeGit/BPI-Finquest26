import React from 'react';
import {Composition} from 'remotion';
import {FirstsFundAd} from './FirstsFundAd';
import {DURATION, FPS} from './timing';

export const RemotionRoot: React.FC = () => (
  <Composition id="FirstsFund" component={FirstsFundAd} durationInFrames={DURATION} fps={FPS} width={1920} height={1080} />
);
