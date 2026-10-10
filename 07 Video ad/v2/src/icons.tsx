import React from 'react';

// Flat line icons for each first. Drawn in code so the ad needs no image assets.
type P = {size: number; color: string; accent: string};

const Svg: React.FC<{size: number; children: React.ReactNode}> = ({size, children}) => (
	<svg width={size} height={size} viewBox="0 0 200 200" fill="none" strokeLinecap="round" strokeLinejoin="round">
		{children}
	</svg>
);

export const Plane: React.FC<P> = ({size, color, accent}) => (
	<Svg size={size}>
		<path d="M20 112 L180 60 L150 92 L60 118 Z" fill={accent} stroke={color} strokeWidth="8" />
		<path d="M92 108 L70 160 L92 156 L124 100" fill={color} stroke={color} strokeWidth="8" />
		<path d="M50 116 L36 90 L50 88 L70 110" stroke={color} strokeWidth="8" />
		<circle cx="150" cy="150" r="10" fill={accent} />
		<circle cx="40" cy="44" r="7" fill={accent} />
	</Svg>
);

export const Car: React.FC<P> = ({size, color, accent}) => (
	<Svg size={size}>
		<path d="M26 128 L34 98 Q40 84 56 82 L144 82 Q160 84 166 98 L174 128 Z" fill={accent} stroke={color} strokeWidth="8" />
		<path d="M54 82 L68 56 Q72 50 80 50 L120 50 Q128 50 132 56 L146 82" stroke={color} strokeWidth="8" />
		<rect x="22" y="124" width="156" height="22" rx="8" fill={color} />
		<circle cx="60" cy="148" r="16" fill={color} stroke={accent} strokeWidth="6" />
		<circle cx="140" cy="148" r="16" fill={color} stroke={accent} strokeWidth="6" />
	</Svg>
);

export const Condo: React.FC<P> = ({size, color, accent}) => (
	<Svg size={size}>
		<rect x="50" y="30" width="80" height="146" rx="6" fill={accent} stroke={color} strokeWidth="8" />
		{[50, 76, 102, 128].map((y) => (
			<g key={y}>
				<rect x="64" y={y} width="18" height="14" rx="2" fill={color} />
				<rect x="98" y={y} width="18" height="14" rx="2" fill={color} />
			</g>
		))}
		<rect x="80" y="150" width="20" height="26" fill={color} />
		<circle cx="160" cy="132" r="16" stroke={color} strokeWidth="8" />
		<path d="M160 148 L160 182 M160 166 L172 166 M160 176 L170 176" stroke={color} strokeWidth="8" />
	</Svg>
);

export const RingIcon: React.FC<P> = ({size, color, accent}) => (
	<Svg size={size}>
		<circle cx="100" cy="124" r="50" stroke={color} strokeWidth="12" />
		<path d="M78 66 L88 44 L112 44 L122 66 L100 84 Z" fill={accent} stroke={color} strokeWidth="7" />
		<path d="M40 40 L48 48 M160 40 L152 48 M100 18 L100 28" stroke={accent} strokeWidth="8" />
	</Svg>
);

export const Shop: React.FC<P> = ({size, color, accent}) => (
	<Svg size={size}>
		<path d="M30 70 L44 34 L156 34 L170 70 Z" fill={accent} stroke={color} strokeWidth="8" />
		<path d="M30 70 Q44 88 58 70 Q72 88 86 70 Q100 88 114 70 Q128 88 142 70 Q156 88 170 70" stroke={color} strokeWidth="8" fill={accent} />
		<rect x="40" y="84" width="120" height="86" stroke={color} strokeWidth="8" />
		<rect x="58" y="108" width="36" height="62" fill={color} />
		<rect x="108" y="104" width="36" height="28" fill={accent} stroke={color} strokeWidth="6" />
	</Svg>
);

export const Backpack: React.FC<P> = ({size, color, accent}) => (
	<Svg size={size}>
		<path d="M76 48 Q76 26 100 26 Q124 26 124 48" stroke={color} strokeWidth="8" />
		<rect x="46" y="46" width="108" height="132" rx="34" fill={accent} stroke={color} strokeWidth="8" />
		<rect x="68" y="112" width="64" height="44" rx="10" fill={color} />
		<path d="M68 84 L132 84" stroke={color} strokeWidth="8" />
		<path d="M150 70 L172 52 L176 64 Z" fill={color} />
	</Svg>
);

export const Paycheck: React.FC<P> = ({size, color, accent}) => (
	<Svg size={size}>
		<rect x="62" y="16" width="76" height="168" rx="14" fill={color} />
		<rect x="70" y="32" width="60" height="132" rx="4" fill={accent} />
	</Svg>
);
