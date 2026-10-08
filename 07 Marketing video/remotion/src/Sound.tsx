import React from 'react';
import {Audio, Sequence, staticFile} from 'remotion';
import {T, VO} from './timing';

type Cue = {at: number; file: string; volume: number};

const DUCK = 0.3; // music level under the voice (about −10 dB)
const RAMP = 8; // frames

/** Music level: full between phrases, ducked under the voice, with short ramps. */
const musicVolume = (f: number) => {
  let v = 1;
  for (const s of VO) {
    const into = Math.min(1, Math.max(0, (f - (s.at - RAMP)) / RAMP));
    const outOf = Math.min(1, Math.max(0, (s.end + RAMP - f) / RAMP));
    v = Math.min(v, 1 - (1 - DUCK) * Math.min(into, outOf));
  }
  return v;
};

/** Voiceover phrases, music bed and frame-placed sound effects (music/SFX from ../audio/make_audio.py). */
export const Sound: React.FC<{nodeFrames: number[]}> = ({nodeFrames}) => {
  const cues: Cue[] = [
    {at: T.cardIn + 3, file: 'notif', volume: 0.55},
    {at: T.dotBorn - 2, file: 'tick', volume: 0.6},
    {at: T.dotToTrunk - 2, file: 'whoosh', volume: 0.45},
    {at: T.branches + 28, file: 'pop', volume: 0.4},
    {at: T.home - 2, file: 'tick', volume: 0.35},
    {at: T.business - 2, file: 'tick', volume: 0.35},
    {at: T.links, file: 'whoosh', volume: 0.3},
    ...T.essentials.map((at) => ({at, file: 'pop', volume: 0.32})),
    {at: T.converge + 4, file: 'whoosh', volume: 0.45},
    {at: T.pillIn + 20, file: 'pop', volume: 0.5},
    {at: T.tap, file: 'tap', volume: 0.65},
    ...nodeFrames.map((at, i) => ({at, file: `node${i}`, volume: 0.42})),
    {at: T.dotToCenter, file: 'whoosh', volume: 0.5},
    {at: T.wipe + 8, file: 'chime', volume: 0.4},
  ];
  return (
    <>
      <Audio src={staticFile('audio/music.wav')} volume={musicVolume} />
      {VO.map((s) => (
        <Sequence key={s.file} from={s.at} layout="none">
          <Audio src={staticFile(`audio/${s.file}.wav`)} volume={1} />
        </Sequence>
      ))}
      {cues.map((c, i) => (
        <Sequence key={i} from={c.at} layout="none">
          <Audio src={staticFile(`audio/${c.file}.wav`)} volume={Math.min(1, c.volume * 0.9)} />
        </Sequence>
      ))}
    </>
  );
};
