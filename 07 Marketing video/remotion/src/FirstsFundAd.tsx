import React from 'react';
import {AbsoluteFill, random, useCurrentFrame, useVideoConfig} from 'remotion';
import {Icon} from './Icons';
import {KineticText} from './KineticText';
import {Sound} from './Sound';
import {C, EASE_IN, EASE_OUT, H, W, fontFamily, keys, lerp, mixColor, pop, prog} from './theme';
import {T} from './timing';

// ---------------------------------------------------------------- layout
const TRUNK = {x: 260, y: 580};
const SPLIT = 520;
const HOME = {x: 860, y: 380};
const BIZ = {x: 860, y: 780};
const ESS_X = 1460;
const ESS = [
  {name: 'power', label: 'Power', y: 250},
  {name: 'networks', label: 'Networks', y: 440},
  {name: 'ports', label: 'Ports', y: 630},
  {name: 'hospitals', label: 'Hospitals', y: 820},
] as const;
const LINE_Y = 720;
const LINE_X0 = 260;
const LINE_X1 = 1660;
const NODE_X = Array.from({length: 7}, (_, i) => LINE_X0 + (i * (LINE_X1 - LINE_X0)) / 6);
const PILL = {x: 960, y: 470};

// ---------------------------------------------------------------- the amber dot
const DOT_F = [0, T.dotToTrunk, T.trunk, T.converge, T.line - 2, T.pillIn, T.pillIn + 20, T.pillOut, T.pillOut + 20, T.travel, T.travelEnd, T.dotToCenter, T.wipe];
const DOT_X = [960, 960, TRUNK.x, TRUNK.x, LINE_X0, LINE_X0, PILL.x, PILL.x, LINE_X0, LINE_X0, LINE_X1, LINE_X1, 960];
const DOT_Y = [540, 540, TRUNK.y, TRUNK.y, LINE_Y, LINE_Y, PILL.y, PILL.y, LINE_Y, LINE_Y, LINE_Y, LINE_Y, 540];
export const dotX = (f: number) => keys(f, DOT_F, DOT_X);
const dotY = (f: number) => keys(f, DOT_F, DOT_Y);

/** Frame at which the travelling dot reaches node i (used for visuals and sound). */
export const nodeLitFrame = (i: number) => {
  for (let fr = T.travel; fr <= T.travelEnd; fr++) if (dotX(fr) >= NODE_X[i] - 0.5) return fr;
  return T.travelEnd;
};

// ---------------------------------------------------------------- Manila skyline (seeded)
const skyline = (() => {
  let d = 'M96 1000';
  let x = 96;
  let k = 0;
  while (x < 1824) {
    const w = 40 + random(`w${k}`) * 70;
    const h = 18 + random(`h${k}`) * 62 + (k % 7 === 3 ? 30 : 0);
    const top = 1000 - h;
    d += ` L${x.toFixed(0)} ${top.toFixed(0)} L${Math.min(1824, x + w).toFixed(0)} ${top.toFixed(0)} L${Math.min(1824, x + w).toFixed(0)} 1000`;
    if (k % 5 === 1) d += ` M${(x + w / 2).toFixed(0)} ${top.toFixed(0)} L${(x + w / 2).toFixed(0)} ${(top - 18).toFixed(0)} M${Math.min(1824, x + w).toFixed(0)} 1000`;
    x += w + 6 + random(`g${k}`) * 14;
    d += ` L${Math.min(1824, x).toFixed(0)} 1000`;
    k++;
  }
  return d;
})();

const Stroke: React.FC<{d: string; p: number; color?: string; width?: number; offset?: number; opacity?: number}> = ({
  d,
  p,
  color = C.greenDeep,
  width = 3,
  offset,
  opacity = 1,
}) =>
  p <= 0.001 ? null : (
  <path
    d={d}
    pathLength={1}
    strokeDasharray="1 1"
    strokeDashoffset={offset ?? 1 - p}
    fill="none"
    stroke={color}
    strokeWidth={width}
    strokeLinecap="round"
    strokeLinejoin="round"
    opacity={opacity}
  />
  );

export const FirstsFundAd: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();

  // Camera drift through scenes 2–3 for depth; returns to 0 before the line forms.
  const drift = keys(f, [T.dotToTrunk, T.sceneOut, T.line], [0, -28, 0]);
  const out = prog(f, T.sceneOut, 24, EASE_IN); // scene 2–3 elements leave

  // ------------------------------------------------ scene 1: notification → dot
  const cardEnter = pop(f, T.cardIn, fps);
  const morph = prog(f, T.cardMorph, 30);
  const cardW = lerp(640, 28, morph);
  const cardH = lerp(132, 28, morph);
  const cardR = lerp(30, 14, morph);
  const cardContent = 1 - prog(f, T.cardMorph - 4, 10);

  // ------------------------------------------------ scene 2–3 drawing progress
  const trunkP = prog(f, T.trunk, 26, EASE_OUT) - out;
  const branchP = prog(f, T.branches, 34) - out;
  const homeP = prog(f, T.home, 40) * (1 - out);
  const bizP = prog(f, T.business, 40) * (1 - out);
  const skyP = prog(f, T.skyline, 100) * (1 - prog(f, T.sceneOut, 30));

  // ------------------------------------------------ scene 4: line, nodes, pill
  const lineIn = prog(f, T.line, 36, EASE_OUT);
  const lineRetract = prog(f, T.s4Out, 24, EASE_IN); // retracts from the left, into the dot
  const retractX = lerp(LINE_X0, LINE_X1, lineRetract);
  const pillOpen = keys(f, [T.pillIn + 20, T.pillIn + 34, T.pillOut, T.pillOut + 10], [0, 1, 1, 0]);
  const pillVisible = f >= T.pillIn + 20 && f <= T.pillOut + 10;
  const press = keys(f, [T.tap, T.tap + 5, T.tap + 16], [1, 0.93, 1]);
  const ripple = prog(f, T.tap, 22, EASE_OUT);

  // ------------------------------------------------ scene 5: wipe
  const wipe = prog(f, T.wipe, T.wipeEnd - T.wipe);
  const dotR = f < T.wipe ? 14 : lerp(14, 1250, wipe);
  const dotColor = mixColor(C.amber, C.green, prog(f, T.wipe, 14));
  const born = pop(f, T.dotBorn - 2, fps);
  const pulse = prog(f, T.dotBorn, 26, EASE_OUT);

  return (
    <AbsoluteFill style={{backgroundColor: C.paper, fontFamily}}>
      <Sound nodeFrames={NODE_X.map((_, i) => nodeLitFrame(i))} />

      {/* World layer: everything that drifts together */}
      <AbsoluteFill style={{transform: `translateX(${drift}px)`}}>
        <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute'}}>
          {/* Manila skyline, slower parallax */}
          <g transform={`translate(${-drift * 0.6} 0)`}>
            <Stroke d={skyline} p={skyP} color={C.mist} width={2.2} />
          </g>

          {/* Trunk and branches */}
          <Stroke d={`M${TRUNK.x} ${TRUNK.y} L${SPLIT} ${TRUNK.y}`} p={trunkP} color={C.green} width={4} />
          <Stroke d={`M${SPLIT} ${TRUNK.y} C640 ${TRUNK.y} 680 ${HOME.y} ${HOME.x - 70} ${HOME.y}`} p={branchP} color={C.green} width={4} />
          <Stroke d={`M${SPLIT} ${TRUNK.y} C640 ${TRUNK.y} 680 ${BIZ.y} ${BIZ.x - 70} ${BIZ.y}`} p={branchP} color={C.green} width={4} />

          {/* Links from each first to every essential */}
          {[HOME, BIZ].flatMap((m, a) =>
            ESS.map((e, b) => {
              const k = a * 4 + b;
              const p = prog(f, T.links + k * 4, 30) - out;
              return (
                <Stroke
                  key={`l${k}`}
                  d={`M${m.x + 66} ${m.y} C1160 ${m.y} 1180 ${e.y} ${ESS_X - 62} ${e.y}`}
                  p={p}
                  color={C.greenLight}
                  width={2}
                  opacity={0.85}
                />
              );
            }),
          )}

          {/* Milestone icons */}
          <Icon name="home" x={HOME.x} y={HOME.y} p={homeP} scale={1.15} />
          <Icon name="business" x={BIZ.x} y={BIZ.y} p={bizP} scale={1.15} />

          {/* Essentials */}
          {ESS.map((e, i) => (
            <Icon key={e.name} name={e.name} x={ESS_X} y={e.y} p={prog(f, T.essentials[i], 36) * (1 - out)} />
          ))}

          {/* Particles: each first and essential becomes a node on one steady line */}
          {f >= T.converge && f < T.wipe && (
            <>
              <Stroke
                d={`M${LINE_X0} ${LINE_Y} L${LINE_X1} ${LINE_Y}`}
                p={lineIn}
                offset={f >= T.s4Out ? -lineRetract : 1 - lineIn}
                color={C.mist}
                width={4}
              />
              {NODE_X.map((nx, i) => {
                if (i === 0 && f < T.line) return null;
                const from = i === 0 ? {x: LINE_X0, y: LINE_Y} : i === 1 ? HOME : i === 2 ? BIZ : {x: ESS_X, y: ESS[i - 3].y};
                const mp = prog(f, T.converge + 6 + i * 3, 34);
                const x = lerp(from.x, nx, mp);
                const y = lerp(from.y, LINE_Y, mp);
                const appear = pop(f, i === 0 ? T.line : T.converge + i * 2, fps);
                const lit = f >= nodeLitFrame(i);
                const litPop = lit ? pop(f, nodeLitFrame(i), fps) : 0;
                const gone = nx < retractX - 2 ? 0 : 1;
                const s = appear * gone * (1 + 0.35 * Math.sin(Math.PI * Math.min(1, litPop)) * (litPop < 1 ? 1 : 0));
                return (
                  <circle
                    key={`n${i}`}
                    cx={x}
                    cy={y}
                    r={11 * s}
                    fill={lit ? C.green : C.paper}
                    stroke={C.green}
                    strokeWidth={3}
                  />
                );
              })}
            </>
          )}
        </svg>

        {/* Labels attached to the world */}
        <KineticText text="First home" start={T.home + 10} out={T.sceneOut} x={HOME.x - 300} y={HOME.y - 124} width={600} size={40} weight={700} color={C.green} />
        <KineticText text="First business" start={T.business + 10} out={T.sceneOut} x={BIZ.x - 300} y={BIZ.y + 72} width={600} size={40} weight={700} color={C.green} />
        {ESS.map((e, i) => (
          <KineticText key={e.label} text={e.label} start={T.essentials[i] + 6} out={T.sceneOut + i * 2} x={ESS_X + 74} y={e.y - 28} width={360} size={46} weight={800} align="left" />
        ))}
      </AbsoluteFill>

      {/* ------------------------------------------------ headlines */}
      <KineticText text="Your first paycheck." start={T.hookLine1} out={T.hookOut} y={292} size={84} weight={800} />
      <KineticText text="Small. But it's a start." start={T.hookLine2} out={T.hookOut + 4} y={680} size={54} weight={500} color={C.green} />
      <KineticText text="Bigger firsts are coming." start={T.headline1} out={T.headline1Out} x={160} y={104} width={1500} size={66} weight={800} align="left" />
      <KineticText
        text="Your firsts run on the world's essentials."
        start={T.headline2}
        out={T.sceneOut}
        x={160}
        y={104}
        width={1500}
        size={62}
        weight={800}
        align="left"
        accent={{words: ['essentials'], color: C.green}}
      />
      <KineticText
        text="Firsts Fund invests in the companies behind them."
        start={T.investLine}
        out={T.s4Out}
        x={410}
        y={210}
        width={1100}
        size={62}
        weight={800}
        stagger={2}
        accent={{words: ['Firsts', 'Fund'], color: C.green}}
      />
      <KineticText text="Today" start={T.line + 10} out={T.s4Out} x={LINE_X0 - 150} y={LINE_Y + 34} width={300} size={32} weight={500} color={C.grey} />
      <KineticText text="5 years" start={T.line + 16} out={T.s4Out + 10} x={LINE_X1 - 150} y={LINE_Y + 34} width={300} size={32} weight={500} color={C.grey} />
      <KineticText text="Think 5 years ahead." start={T.fiveYears} out={T.s4Out + 6} y={836} size={52} weight={700} color={C.green} />

      {/* ------------------------------------------------ scene 1 notification card (becomes the dot) */}
      {f < T.dotBorn && (
        <div
          style={{
            position: 'absolute',
            left: 960 - cardW / 2,
            top: 540 - cardH / 2 + (1 - cardEnter) * 70,
            width: cardW,
            height: cardH,
            borderRadius: cardR,
            transform: `scale(${0.7 + 0.3 * cardEnter})`,
            background: mixColor(C.white, C.amber, prog(f, T.cardMorph + 6, 20)),
            boxShadow: `0 ${24 * (1 - morph)}px ${60 * (1 - morph)}px rgba(20,32,25,${0.16 * (1 - morph)})`,
            overflow: 'hidden',
            display: 'flex',
            alignItems: 'center',
            gap: 26,
            padding: cardContent > 0 ? '0 30px' : 0,
            boxSizing: 'border-box',
          }}
        >
          <div style={{opacity: cardContent, display: 'flex', alignItems: 'center', gap: 26, width: 580, flexShrink: 0}}>
            <div
              style={{
                width: 76,
                height: 76,
                borderRadius: 20,
                background: C.green,
                color: C.white,
                fontSize: 44,
                fontWeight: 800,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexShrink: 0,
              }}
            >
              ₱
            </div>
            <div style={{flex: 1}}>
              <div style={{fontSize: 34, fontWeight: 800, color: C.greenDeep, letterSpacing: '-0.01em'}}>Salary credited</div>
              <div style={{fontSize: 27, fontWeight: 500, color: C.grey, marginTop: 4}}>Your first paycheck is in.</div>
            </div>
            <div style={{fontSize: 24, fontWeight: 500, color: C.grey, alignSelf: 'flex-start', marginTop: 4}}>now</div>
          </div>
        </div>
      )}

      {/* ------------------------------------------------ the amber dot, pill and wipe */}
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute'}}>
        {f >= T.dotBorn && f < T.dotBorn + 30 && (
          <circle cx={960} cy={540} r={14 + 60 * pulse} fill="none" stroke={C.amber} strokeWidth={3} opacity={0.6 * (1 - pulse)} />
        )}
        {f >= T.dotBorn - 2 && !pillVisible && (
          <circle cx={dotX(f) + (f < T.line ? drift : 0)} cy={dotY(f)} r={dotR * (f < T.dotBorn + 8 ? Math.max(0.8, born) : 1)} fill={dotColor} />
        )}
        {pillVisible && (
          <g transform={`translate(${PILL.x} ${PILL.y}) scale(${press})`}>
            <rect
              x={-lerp(14, 230, pillOpen)}
              y={-lerp(14, 50, pillOpen)}
              width={lerp(28, 460, pillOpen)}
              height={lerp(28, 100, pillOpen)}
              rx={lerp(14, 50, pillOpen)}
              fill={C.amber}
            />
            <text
              x={0}
              y={15}
              textAnchor="middle"
              fontFamily={fontFamily}
              fontSize={42}
              fontWeight={800}
              fill={C.white}
              opacity={Math.max(0, (pillOpen - 0.6) / 0.4)}
            >
              Start with ₱100
            </text>
            {f >= T.tap && (
              <circle cx={120} cy={18} r={10 + 90 * ripple} fill={C.white} opacity={0.45 * (1 - ripple)} />
            )}
          </g>
        )}
        {f >= T.wipeEnd && <rect width={W} height={H} fill={C.green} />}
      </svg>

      {/* ------------------------------------------------ end card */}
      {f >= T.wipeEnd - 6 && (
        <AbsoluteFill>
          <KineticText text="FIRSTS FUND" start={T.brandName} y={318} size={46} weight={700} color={C.mist} tracking="0.32em" stagger={4} />
          <KineticText
            text="FUND YOUR FIRSTS"
            start={T.tagline}
            y={392}
            size={146}
            weight={800}
            color={C.white}
            tracking="-0.035em"
            stagger={7}
            lineHeight={1.05}
            suffix={
              <span
                style={{
                  display: 'inline-block',
                  width: '0.2em',
                  height: '0.2em',
                  marginLeft: '0.05em',
                  borderRadius: '50%',
                  background: C.amber,
                  transform: `scale(${pop(f, T.tagline + 22, fps)})`,
                }}
              />
            }
          />
          <div
            style={{
              position: 'absolute',
              left: 960 - 280 * prog(f, T.rule, 26, EASE_OUT),
              top: 610,
              width: 560 * prog(f, T.rule, 26, EASE_OUT),
              height: 2,
              background: C.mist,
            }}
          />
          <KineticText text="BPI Wealth" start={T.bpi} y={640} size={46} weight={700} color={C.white} tracking="0.01em" />
          <KineticText
            text="Proposed fund concept for BPI Wealth FinQuest 2026. ₱100 minimum is proposed. A UITF is not a deposit and is not insured by PDIC. Its value can fall as well as rise, and you may get back less than you invest. For goals at least five years away."
            start={T.disclaimer}
            x={130}
            y={880}
            width={1660}
            size={28}
            weight={500}
            color={C.mist}
            stagger={0}
            tracking="0"
            lineHeight={1.4}
          />
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};
