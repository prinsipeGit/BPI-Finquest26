import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, EASE_IN, EASE_OUT, fontFamily, prog} from './theme';

type Props = {
  text: string;
  start: number;
  out?: number; // frame the words start rising out
  x?: number;
  y: number;
  width?: number;
  size: number;
  weight?: 500 | 700 | 800;
  color?: string;
  align?: 'left' | 'center' | 'right';
  stagger?: number;
  tracking?: string;
  lineHeight?: number;
  accent?: {words: string[]; color: string};
  suffix?: React.ReactNode; // rises with the last word
};

/** Words rise into view from behind a mask, then rise out. No fades. */
export const KineticText: React.FC<Props> = ({
  text,
  start,
  out,
  x = 0,
  y,
  width = 1920,
  size,
  weight = 700,
  color = C.greenDeep,
  align = 'center',
  stagger = 3,
  tracking = '-0.02em',
  lineHeight = 1.12,
  accent,
  suffix,
}) => {
  const f = useCurrentFrame();
  const words = text.split(' ');
  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        width,
        textAlign: align,
        fontFamily,
        fontSize: size,
        fontWeight: weight,
        letterSpacing: tracking,
        lineHeight,
        color,
      }}
    >
      {words.map((w, i) => {
        const pin = prog(f, start + i * stagger, 18, EASE_OUT);
        const pout = out === undefined ? 0 : prog(f, out + i * Math.max(1, stagger / 2), 12, EASE_IN);
        const ty = (1 - pin) * 130 - pout * 130; // 130%: clears descenders past the mask
        const isAccent = accent && accent.words.includes(w.replace(/[.,]/g, ''));
        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              overflow: 'hidden',
              verticalAlign: 'top',
              paddingBottom: '0.08em',
              marginBottom: '-0.08em',
            }}
          >
            <span
              style={{
                display: 'inline-block',
                transform: `translateY(${ty}%)`,
                color: isAccent ? accent!.color : undefined,
              }}
            >
              {w.replace(/[.,!?]$/, '')}
              {/[.,!?]$/.test(w) ? <span style={{marginLeft: '-0.07em'}}>{w.slice(-1)}</span> : null}
              {i === words.length - 1 ? suffix : null}
              {i < words.length - 1 ? ' ' : ''}
            </span>
          </span>
        );
      })}
    </div>
  );
};
