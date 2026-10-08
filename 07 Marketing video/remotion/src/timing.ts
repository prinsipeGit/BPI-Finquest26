// Every frame number in the ad lives here (30 fps, 900 frames = 30.0 s).
// Visual beats are locked to the ElevenLabs voiceover ("Hope - upbeat and clear", take 3).
// Word timestamps: ../audio/vo_words.json. Phrase files: public/audio/vo_*.wav.
export const FPS = 30;
export const DURATION = 900;

/** Voiceover phrases: file, frame it starts, frame it ends. Word frames are noted beside each. */
export const VO = [
  {file: 'vo_A', at: 6, end: 48}, // Your@6 first@15 paycheck@24
  {file: 'vo_B', at: 52, end: 126}, // It's small@62 … but it's a start@101
  {file: 'vo_C', at: 128, end: 269}, // bigger@145 firsts@155 … home@211 … business@246
  {file: 'vo_D', at: 282, end: 366}, // They'll run on the things the world can't do without
  {file: 'vo_E', at: 366, end: 464}, // Power@369 Networks@391 Ports@411 Hospitals@434
  {file: 'vo_F', at: 478, end: 554}, // Firsts@482 Fund@492 invests … them@540
  {file: 'vo_G', at: 562, end: 655}, // Start@567 one hundred@581 pesos@595 Think@613 five years@621
  {file: 'vo_I', at: 718, end: 758}, // Fund@723 your@731 firsts@736
] as const;

export const T = {
  // Scene 1 · Hook: the first paycheck (0–3.6 s)
  cardIn: 0,
  hookLine1: 6, // "Your first paycheck."
  hookLine2: 55, // "Small. But it's a start."
  cardMorph: 84, // notification shrinks into the amber dot
  dotBorn: 104, // just after "start"
  hookOut: 96,

  // Scene 2 · Bigger firsts (3.8–9.1 s)
  dotToTrunk: 114,
  trunk: 134,
  headline1: 140, // "Bigger firsts are coming."
  branches: 160,
  home: 204, // label lands on "home" (211)
  business: 236, // label lands on "business" (246)
  skyline: 168,
  headline1Out: 272,

  // Scene 3 · The essentials (9.5–15.7 s)
  headline2: 286, // "Your firsts run on the world's essentials."
  links: 330,
  essentials: [365, 387, 407, 430] as const, // labels land on Power, Networks, Ports, Hospitals
  sceneOut: 470,

  // Scene 4 · The step (15.9–22.3 s)
  converge: 476,
  line: 506,
  investLine: 480, // "Firsts Fund invests in the companies behind them."
  pillIn: 548, // pill opens 568–582, "one hundred pesos" 581–600
  tap: 592,
  pillOut: 604,
  travel: 626, // dot travels the line, lighting nodes
  travelEnd: 666,
  fiveYears: 614, // "Think five years ahead."
  s4Out: 668,

  // Scene 5 · Resolution (22.4–30 s)
  dotToCenter: 672,
  wipe: 694, // music resolves here (23.13 s)
  wipeEnd: 720,
  brandName: 712, // FIRSTS FUND
  tagline: 721, // FUND / YOUR / FIRSTS land on the spoken words (723, 731, 736)
  rule: 748,
  bpi: 754,
  disclaimer: 716, // on screen 6.1 s
} as const;
