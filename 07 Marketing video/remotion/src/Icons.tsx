import React from 'react';
import {C} from './theme';

// Line-art icons drawn in a 100 × 100 box centred on (0, 0). One stroke weight for all.
export const ICONS: Record<string, string[]> = {
  // First home: a condo tower with a lit window grid
  home: [
    'M-30 48 L-30 -40 L10 -48 L10 48',
    'M10 -20 L32 -14 L32 48',
    'M-40 48 L42 48',
    'M-21 -30 h8 M-3 -30 h8 M-21 -14 h8 M-3 -14 h8 M-21 2 h8 M-3 2 h8 M-21 18 h8 M-3 18 h8',
    'M17 -2 h8 M17 14 h8 M17 30 h8',
    'M-14 48 L-14 34 L-4 34 L-4 48',
  ],
  // First business: a small storefront with an awning
  business: [
    'M-38 -8 L-38 46 L38 46 L38 -8',
    'M-44 -8 L-36 -32 L36 -32 L44 -8',
    'M-44 -8 Q-33 6 -22 -8 Q-11 6 0 -8 Q11 6 22 -8 Q33 6 44 -8',
    'M-28 -46 L28 -46 L28 -32 M-28 -46 L-28 -32',
    'M-28 46 L-28 14 L-6 14 L-6 46',
    'M6 12 L30 12 L30 32 L6 32 Z',
  ],
  // Power: a transmission pylon
  power: [
    'M-22 48 L0 -46 L22 48',
    'M-34 -24 L34 -24 M-26 -4 L26 -4',
    'M-16 20 L12 4 M16 20 L-12 4 M-12 4 L8 -14 M12 4 L-8 -14',
    'M-34 -24 L-34 -16 M34 -24 L34 -16 M-26 -4 L-26 4 M26 -4 L26 4',
    'M-50 -14 Q-42 -8 -34 -16 M34 -16 Q42 -8 50 -14',
  ],
  // Networks: a signal tower with radiating arcs
  networks: [
    'M0 -20 L-16 48 M0 -20 L16 48',
    'M-11 26 L11 26 M-6 4 L6 4',
    'M0 -30 a5 5 0 1 0 0.01 0',
    'M-16 -42 Q-24 -30 -16 -18 M16 -42 Q24 -30 16 -18',
    'M-28 -50 Q-42 -30 -28 -10 M28 -50 Q42 -30 28 -10',
  ],
  // Ports: a ship-to-shore container crane
  ports: [
    'M-30 48 L-30 -18 M-6 48 L-6 -18',
    'M-48 -18 L44 -18 M-30 -18 L-18 -44 L-6 -18',
    'M-18 -44 L44 -18',
    'M26 -18 L26 6',
    'M16 6 L36 6 L36 20 L16 20 Z',
    'M-48 48 L48 48',
  ],
  // Hospitals: a building with a cross
  hospitals: [
    'M-36 48 L-36 -24 L36 -24 L36 48',
    'M-44 48 L44 48',
    'M-8 -46 L8 -46 L8 -38 L16 -38 L16 -22 M-8 -46 L-8 -38 L-16 -38 L-16 -22',
    'M-6 -4 h12 v10 h10 v12 h-10 v10 h-12 v-10 h-10 v-12 h10 Z',
    'M-12 48 L-12 36 L12 36 L12 48',
  ],
};

type Props = {name: keyof typeof ICONS; x: number; y: number; p: number; scale?: number; color?: string};

/** Draws the icon stroke by stroke as p goes 0 → 1 (and un-draws as it returns to 0). */
export const Icon: React.FC<Props> = ({name, x, y, p, scale = 1, color = C.greenDeep}) => {
  const parts = ICONS[name];
  const n = parts.length;
  return (
    <g transform={`translate(${x} ${y}) scale(${scale})`}>
      {parts.map((d, i) => {
        const a = i / (n + 1);
        const local = Math.min(1, Math.max(0, (p - a) / (2 / (n + 1))));
        if (local <= 0.001) return null; // a zero-length dash would still paint a round cap
        return (
          <path
            key={i}
            d={d}
            pathLength={1}
            strokeDasharray="1 1"
            strokeDashoffset={1 - local}
            fill="none"
            stroke={color}
            strokeWidth={3.2 / scale}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        );
      })}
    </g>
  );
};
