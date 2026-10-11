# Claude Design brief · Firsts Fund pitch deck (Final Showdown, 17 Oct 2026)

Paste the prompt in section 1 into Claude Design. Upload the files in section 2 with it. Sections 3–5 are the spec it should follow.

## 1 · Prompt to paste

> Design a 16:9 pitch deck for a 10-minute live pitch at the BPI Wealth FinQuest 2026 Final Showdown. The product is the **Firsts Fund**, a proposed global equity UITF (a pooled investment fund) for young Filipinos saving for life's firsts five or more years away. The central message is "Fund your firsts."
>
> The attached script (`Pitch script (10 min) - draft v1.md`) is the source of truth: every slide supports one beat of it, and the words on a slide never repeat what the speaker says. Follow the slide list, brand and rules in the attached brief (`Claude Design brief - pitch deck.md`) exactly. Numbers must match the brief character for character. Do not invent statistics, logos or quotes.
>
> Style: clean, modern, warm. Paper background, ink text, one emerald accent, Geist font, lots of space, one idea per slide, big type. It should feel like the 30-second ad (attached frames), not like a bank report. Build the opening as a full-bleed black sequence with phone notifications.
>
> Also produce the annex slides listed in the brief, in a denser but consistent style. Export as PPTX with speaker notes taken from the script.

## 2 · Files to upload

| File (repo path) | Use |
|---|---|
| `Presentation deck/Pitch script (10 min) - draft v1.md` | Script and slide cues |
| `Presentation deck/Claude Design brief - pitch deck.md` | This brief |
| `09 Brand assets/firsts-fund-icon-forest.svg` | Main logo (lime 1, white F on forest) |
| `09 Brand assets/firsts-fund-icon-green.svg` | Alternate logo |
| `04 Fund model/v4 (31 holdings, current)/growth4.png` | Reference for the ₱100 growth chart (have it redrawn in the deck style) |
| `04 Fund model/v4 (31 holdings, current)/hist36.png` | Annex: 36-year history |
| `01 Phase 2 submission/LosAngeles76ers_FirstsFund_FactSheet.pdf` | Annex content and numbers |
| 3–4 screenshots from `07 Video ad/v2/out/FirstsFund_Ad_v2.mp4` | Visual style reference (calculator scene, a first, logo end card) |

## 3 · Brand

| Token | Hex | Use |
|---|---|---|
| paper | `#F4F3EE` | Slide background |
| card | `#FFFFFF` | Cards, phone screens |
| ink | `#0E100E` | Main text |
| ink2 | `#3A3F3B` | Secondary text |
| muted | `#8B908A` | Labels, sources |
| line | `#D9D7CF` | Rules, borders |
| accent (emerald) | `#0B7A4B` | One highlight per slide |
| accentSoft | `#DDEFE5` | Highlight fills |
| forest | `#073B2A` | Logo tile, dark slides |
| lime | `#C5F06A` | The "1" in the logo; use sparingly |
| night | `#0B0D0C` | Opening and close backgrounds |
| warn | `#D2453B` | Only for "Hindsight / not a forecast" labels |

Font: **Geist** (all weights; no monospace). Title 54–72 pt, body ≥ 24 pt, sources 12 pt muted. Peso amounts always written as ₱ with commas (₱120,000).

## 4 · Slide list (main deck, ~16 slides)

| # | Script section | Slide | Content (exact) |
|---|---|---|---|
| 1 | Opening | **Notification 1** | Black. Centred phone lock-screen notification: "BPI · Your salary has been credited." Label in the corner, small: "Proposed screens, illustrative". |
| 2 | Opening | **Your firsts** | Black. Lines fade in one by one (one build step each): first paycheck · first flight · first car · first place of your own · first time you took Mom and Dad out |
| 3 | Opening | **What firsts run on** | Each first turns into the business behind it: flight → airport · call home → network · car → port · home → power and water · check-up → hospital. Small holding logos under each: OMA · KDDI, Deutsche Telekom · ICTSI · Engie, Sabesp · Bumrungrad, HCA. |
| 4 | Opening | **The line** | "Everybody has a first. Almost nobody has a fund for it." Then the word "first" collapses into the 1F logo → "Firsts Fund · Fund your firsts." |
| 5 | Research | **Access isn't the problem** | Two big numbers: "₱10,000 → ₱1,000: BPI UITF minimum, 2023" · "1 in 4 PSE accounts held by 18–29-year-olds". Sources in small type. |
| 6 | Research | **The shelf** | Four cards, one line each: Pag-IBIG MP2 ("Safe, lends to government") · Money-market fund ("Built for the short term") · PH index fund ("Same economy as your salary · ₱100 → ₱92 in 5 years") · Global fund of funds ("Two layers of fees · can't see what you own"). Fifth card in emerald: Firsts Fund. Kicker: "What's missing isn't access. It's purpose." |
| 7 | Fund | **The fund in one breath** | Five tiles: Global equity UITF, in pesos (proposed) · 31 essential-service businesses, held directly · ₱100 to start · 1.50% a year, one layer · Goals 5+ years away |
| 8 | M·V·P | **The funnel** | 140 → 129 → 49 → 31, building step by step. Labels: Map the milestone (essential-service businesses; 129 earn from it) · Verify the investment (debt stress test, value and quality vs peers; 49 pass) · Position the risk (no company dominates the risk; 31 held) |
| 9 | M·V·P | **Two examples** | Left card: ICTSI · Manila port operator · **In, 4.8%** · "Passed the same tests as everyone." Right card (muted): Manila Water · **Watchlist** · "Only 28% of operating earnings turn into cash." Footer: "No favourites." |
| 10 | Results | **₱100, five years** | Line chart in pesos, Oct 2021 → Oct 2026: today's holdings ₱100 → **₱306** vs benchmark NFRA ₱100 → **₱161**. Side facts: deepest drop on ₱5,000: **₱372** · without chip and grid-equipment makers: **₱237**. Red label: "Hindsight: today's holdings, backtested after all costs. Not actual fund performance, not a forecast." |
| 11 | Operations | **How it runs** | Five icons: holdings reviewed monthly · weights reset quarterly · ~3% cash for withdrawals · max 20% per company (BSP) · max 25% per service type |
| 12 | CX | **Notification 2 + Meet Bea** | Notification: "BPI · ₱100 invested in Firsts Fund. Goal: First trip abroad with Mom and Dad · 2031". Bea card: 23 · junior accountant · ₱28,000 take-home · ₱2,000 a month for her first: Japan with her parents in 5 years. "Illustrative". |
| 13 | CX | **The calculator** | Phone mock-up, BPI App (label "proposed"): First: Japan with Mom and Dad · Cost ₱120,000 · Date Oct 2031 → **₱2,000 a month, contributions only** · Illustrative growth (assumption shown): about ₱1,710 a month · With 4% inflation: ₱146,000 → ₱2,430 a month · Risk shown in pesos before committing |
| 14 | CX | **When life happens** | Three phone screens side by side: Missed month (goal date unchanged; choose: top-up · more each month · later date) · Dashboard (put in · worth now · gain/loss · progress to goal; no streaks) · Yearly goal review + 2-year reminder (optional move to a lower-risk fund, her decision) |
| 15 | CX | **Customer roadmap** (required slide) | One horizontal journey: Discover (talk, campus, workplace, social) → Try the calculator → Sign up in 4 screens → Monthly plan + top-ups → Yearly review → Reach the first → Name the next first (loops back). Caption: "There's always a new first." |
| 16 | Marketing | **How Bea finds us** | "Fund your firsts." + an 8-s ad clip. Channels in priority order: on-site talks and campus caravans · graduating classes and student orgs · new-hire financial-wellness sessions (incl. BPI payroll companies) · short-form social (lean) · "Chat with us". Arrow from every channel to "Try the calculator". |
| 17 | Marketing | **What's next and how we'll know** | Next (proposed): Sukli round-ups in the BPI App · more than one first. Success = still contributing in month 60: target > 50%. |
| 18 | Close | **Notification 3** | Black. "BPI · Goal review: You're on track for your first trip abroad with Mom and Dad." |
| 19 | Close | **End card** | 1F logo. "Everybody has a first. Now, they can have a fund for it." → "Fund your firsts." Team name, Ateneo de Manila University. |

## 5 · Annex slides (Q&A only)

A1 Fact sheet summary · A2 All 31 holdings with weights by type (networks 25.00, healthcare 22.19, power 19.22, ports 10.04, chips 8.13, water 7.68, grid eq. 2.76, airports 1.98, cash 3) · A3 V rules: debt stress shocks per type, watchlist triggers · A4 Calendar-year returns vs NFRA, ACWI, PSEi (from fact sheet) · A5 36-year history (hist36.png, labelled "industry history, context only") · A6 Rolling 5-year saver results · A7 Goal service mechanics · A8 Sukli guardrails · A9 Fees, liquidity, redemptions · A10 Benchmark choice (NFRA) · A11 Data sources.

## 6 · Rules the design must keep

- Every screen of the BPI App is labelled **"proposed"**. Bea and her budget are labelled **"illustrative"**.
- Every performance number carries the hindsight label. Never write "returns" without "backtested" nearby.
- Numbers in pesos first; percentages only as support.
- No "bets", no "guaranteed", no "safe", no raffles or rewards, no streaks.
- Use "proposed Firsts Fund" or "Firsts Fund" consistently; "UITF", never "mutual fund".
- Text on slides is short. The speaker carries the story.
