// Every frame number in the ad lives here (30 fps, 900 frames = 30.0 s).
// Once a voiceover is added, re-derive these from its word timestamps.
export const FPS = 30;
export const DURATION = 900;

export const T = {
  // Scene 1 · Hook: the first paycheck (0–4 s)
  cardIn: 0,
  hookLine1: 12, // "Your first paycheck."
  hookLine2: 42, // "Small. But it's a start."
  cardMorph: 76, // notification shrinks into the amber dot
  dotBorn: 106,
  hookOut: 88,

  // Scene 2 · Bigger firsts (4–11 s)
  dotToTrunk: 116,
  trunk: 138,
  headline1: 144, // "Bigger firsts are coming."
  branches: 164,
  home: 202,
  business: 226,
  skyline: 176,
  headline1Out: 326,

  // Scene 3 · The essentials (11–18 s)
  headline2: 344, // "Your firsts run on the world's essentials."
  links: 360,
  essentials: [372, 390, 408, 426] as const, // power, networks, ports, hospitals
  sceneOut: 536,

  // Scene 4 · The step (18–25 s)
  converge: 548,
  line: 580,
  investLine: 596, // "Firsts Fund invests in the companies behind them."
  pillIn: 626,
  tap: 672,
  pillOut: 690,
  travel: 712, // dot travels the line, lighting nodes
  travelEnd: 758,
  fiveYears: 716, // "Think 5 years ahead."
  s4Out: 758,

  // Scene 5 · Resolution (25–30 s)
  dotToCenter: 762,
  wipe: 786,
  wipeEnd: 812,
  brandName: 808, // FIRSTS FUND
  tagline: 816, // FUND YOUR FIRSTS.
  rule: 838,
  bpi: 844,
  disclaimer: 808, // on screen ≥ 3 s
} as const;
