# FINAL SUBMISSION — EDIT LIST
### The Firsts Fund · Los Angeles 76ers · FinQuest 2026
**Source reviewed:** `Submission-LosAngeles76ers_TheFirstsFund_ADMU.pdf` (6 pages, A4)
**Deadline:** 15 August 2026

---

## STATUS SUMMARY

| | |
|---|---|
| Page count | 6 (2 fact sheet + 3 exec + 1 annex) — **compliant** |
| Page size | A4 (595 × 842 pt) — **compliant** |
| Mandatory fact sheet elements | 11 / 11 present — **compliant** |
| Fund comparison (≥3 funds, on fact sheet) | Present — **compliant** |
| Top ten holdings named | Present, remaining six disclosed — **compliant** |
| Feeder fund prohibition | Addressed and turned into an argument — **compliant** |
| Arithmetic | All allocation tables reconcile to 100.00% — **verified** |
| **Blocking issues** | **3 (Edits 1–3 below)** |

---

# PART A — MUST FIX BEFORE SENDING

## EDIT 1 · Team panel placeholders  ⛔ BLOCKING
**Location:** Fact Sheet, page 2, THE TEAM

**Problem.** Four unfilled placeholders are live in the submitted PDF:
- `Prince Angelo C. Rivera — BS Applied Mathematics – Master in Data Science. [credentials to follow]`
- `Luis Tengonciang — [programme, year, credentials to follow]`
- `Karol Josef Fuñe — [programme, year, credentials to follow]`
- `Eric Fabian Thirdy Mendez — [programme, year, credentials to follow]`

Team is a **mandatory** fact sheet element, and the primer asks specifically for *"Education, Work Experience, Certifications."* Empty brackets on a document whose competitive advantage is meticulousness will undo the credibility earned everywhere else.

**Replace with:**

> **Prince Angelo C. Rivera** — BS Applied Mathematics – Master in Data Science, Ateneo de Manila University
> **Luis Tengonciang** — BS Applied Mathematics – Master in Data Science, Ateneo de Manila University
> **Karol Josef Fuñe** — BS Applied Mathematics – Master in Data Science, Ateneo de Manila University
> **Eric Fabian Thirdy Mendez** — BS Applied Mathematics – Master in Data Science, Ateneo de Manila University
>
> *Team Los Angeles 76ers. The Fund's weighting engine, covariance solver, constraint stack and permutation study were built by the team in Python.*

**Also add year level** (e.g. "4th year"). The primer restricts entry to penultimate and graduating students, so stating it doubles as evidence of eligibility.

---

## EDIT 2 · Mislabelled statistic  ⛔ BLOCKING
**Location:** Fact Sheet, page 1, risk statistics table

**Problem.** `Excess return, geometric +1.73%` — 1.73 is the **arithmetic** difference (17.14 − 15.41). The geometric excess is **1.50%**:

```
1.1714 / 1.1541 − 1 = 0.0150 = 1.50%
```

On a sheet that correctly distinguishes downside deviation from volatility and Sortino from Sharpe, this reads as not knowing the difference — which is plainly untrue and therefore a wasted wound.

**Find:** `Excess return, geometric    +1.73%`
**Replace:** `Excess return, geometric    +1.50%`

*(Alternative: keep 1.73 and change the word to "arithmetic". Geometric is the more defensible measure to publish.)*

---

## EDIT 3 · Filename and subject line  ⛔ BLOCKING
**Problem.** Primer specifies `Attachment: [Group Name_Fund Name].pdf` — their example is `FQBuddies_BPIBalancedFund.pdf`. The `[Submission]` prefix and the school belong in the **subject line**, not the filename.

**Current:** `Submission-LosAngeles76ers_TheFirstsFund_ADMU.pdf`

**Change to:**
```
Attachment:  LosAngeles76ers_TheFirstsFund.pdf
To:          finquest@bpi.com.ph
Subject:     [Submission] - LosAngeles76ers_The Firsts Fund_Ateneo de Manila University
```

---

# PART B — CLOSES THE LAST REAL GAP

## EDIT 4 · How the sixteen were chosen
**Location:** Fact Sheet, page 2, SELECTION PROCESS — after the `Status: the V gate has not yet been run…` note

**Problem.** The process explains **M** (categories) and **P** (weights) in forensic detail, then states the **V** gate — the only step that selects actual names — has not been run, and that *"no holding should be read as having passed it."*

A judge follows that logic straight to: **"Then how did these sixteen get in the door?"** The document never answers. The most literal reading of your own disclosure is that the names were chosen by unstated means and then sized very rigorously.

**Insert:**

> *What did drive selection: the sixteen were identified as listed companies that publicly disclose a capacity commitment with a stated quantity and date, across the five milestone cost drivers, and that a peso fund can access and trade daily. What remains outstanding is formal issuer-by-issuer testing against the solvency and valuation thresholds above.*

⚠️ **Rewrite this to match what you actually did.** Even *"we identified companies we could confirm own long-lived capacity across the five cost drivers, and verified nothing further"* is stronger than silence — silence reads as "we don't know either."

---

## EDIT 5 · Sector concentration
**Location:** Fact Sheet, page 2, beneath CONSTRAINT STACK

**Problem.** The stack caps Owners, Suppliers, Platforms, single issuer, single group and Philippines — but there is **no GICS sector cap**, and Utilities sits at **27.65%**. Expect the question.

**Add:**

> *No GICS sector cap is imposed. Sector weights are an output of the role caps and the risk model; Utilities is the largest at 27.65%. We disclose it rather than constrain it, on the same basis as the factor concentration above.*

---

# PART C — BACK-TEST: FROM CAVEATS TO AN ERROR BAR

## EDIT 6 · Strengthen the look-ahead disclosure
**Location:** Annex A4, limitations table

**Problem.** You write *"Volatility uses the full panel."* But ERC doesn't run on volatility — it runs on the **full covariance matrix, correlations included**, and correlations are where an optimiser gets most of its edge. If weights were solved once on full-sample covariance, "quarterly rebalancing" means rebalancing *toward a hindsight-optimal target*. That is the **largest** bias, not the second.

**Replace the row:**

| | |
|---|---|
| **Look-ahead in the risk model** | Equal risk contribution is solved on the full-period covariance matrix, so both volatilities *and correlations* use data a live manager would not have had at each rebalancing date. This is the largest of the biases and it flatters the result. |

---

## EDIT 7 · Two missing limitations
**Location:** Annex A4, add as new rows

| | |
|---|---|
| **Universe survivorship** | Every candidate still exists, trades and is liquid in 2026. Companies that were plausible capacity owners in 2021 and have since been delisted, acquired or impaired could not have entered the universe. |
| **Benchmark marginally understated** | MSCI ACWI is reconstructed from iShares ACWI NAV, which carries the ETF's expense ratio and tracking error. This runs in our favour and is not corrected. |

---

## EDIT 8 · Size the biases — highest-leverage edit in the document
**Location:** Annex A4, replace the closing sentence

**Why.** Right now you name four biases and give their direction. Naming is good; **sizing** is what separates a student saying *"back-tests are flawed"* from a manager saying *"here is how flawed, and in which direction."* No competing team will do this.

**Replace:** *"The first two push the reported figures in the flattering direction; the fourth pushes against. None is corrected in the numbers presented."*

**With:**

> **Sizing the biases, rather than only naming them.** Omitted Philippine dividends understate the reported return by roughly 70 bps a year. Unmodelled dividend withholding across seven jurisdictions — the portfolio is 65% Owners and therefore dividend-heavy — together with dealing spreads and FX conversion on quarterly rebalancing across five currencies, would remove on the order of 50–130 bps. The look-ahead in the covariance estimate is the largest term and we cannot size it without re-solving on trailing data. **Net, we would expect the true figure to sit below 17.14%, and we would not defend the reported number to the basis point.**

*Adjust the bps figures to your own estimates — the point is publishing a range at all.*

---

# PART D — OPTIONAL, HIGH VALUE IF TIME PERMITS

## EDIT 9 · Re-solve on trailing covariance
Re-run the ERC solve on a **rolling 24-month trailing covariance**, rebalanced quarterly, with no forward-looking data.

- If the portfolio holds up → that becomes your headline number and **the look-ahead objection dies outright**. You lead with it instead of caveating it.
- If it degrades materially → far better you learn that tonight than in the room in October.

This is the single most valuable remaining piece of analytical work.

---

# WHAT NOT TO CHANGE

These are the strongest elements in the submission. Leave them alone.

- **The sequence-of-returns argument.** −0.85 for a contributor, +0.85 for a withdrawer, validated independently on 220 months of MSCI ACWI. Your central claim doesn't depend on the back-test at all — say so if pressed.
- **Sukli.** Spend-only, ₱500 balance floor, user-set cap, one-tap revocation, escrow in a money market fund rather than a zero-interest float, daily net settlement. The operational detail is what separates a product from a pitch.
- **The 13th month anchor.** Legally mandated, universally timed, unbudgeted money. *"December acquisition, January habit."*
- **The unit-economics section.** ₱100 at 1.50% earns ₱1.50 a year, stated in a headed section rather than hoped past.
- **Benchmarking against BPI's own funds** — respectfully, letting their published KIIDS do the talking. The fund-of-funds trailing its own benchmark by 4.19 points with IR −1.05 is the strongest argument in the submission.
- **"Where MP2 wins, we say so."** Conceding a comparator is what makes the rest credible.
- **The redemption screen**, loss counted in months rather than percent.
- **The metrics table with a "we would call it a failure" column.**

---

# VERIFIED — NO ACTION NEEDED

All arithmetic independently checked:

| Check | Result |
|---|---|
| Top ten weight | 68.79% ✓ |
| Remaining six | 21.23% ✓ |
| Equities + reserve | 90.02 + 9.98 = 100.00 ✓ |
| Geographic panel | sums to 100.00 ✓ (SG 29.74, IN 11.36, PH 30.01 all tie to constituents) |
| GICS sector panel | sums to 100.00 ✓ (Utilities 27.65, Health Care 15.80 tie to constituents) |
| Sharpe, fund | (17.14 − 5.25) / 11.77 = 1.010 ✓ |
| Sharpe, index | (15.41 − 5.25) / 18.19 = 0.559 ✓ |
| Beta from correlation | 0.58 × 11.77 / 18.19 = 0.375 ✓ |
| Peso translations | 17.23% × ₱5,000 = ₱862 ✓ |
| Fund-of-funds gap | 11.34 − 7.15 = 4.19 pts ✓ |
| Money market comparator | ₱1,000/mo @ 4.5% × 60 = ₱67,146 vs ₱67,238 ✓ |
| `50.1%` duplication from prior draft | Resolved ✓ |

---

# CHECKLIST

- [ ] **1.** Team credentials — remove all four placeholders
- [ ] **2.** `+1.73%` → `+1.50%` (geometric excess)
- [ ] **3.** Rename file; set subject line
- [ ] **4.** Add "what did drive selection" sentence
- [ ] **5.** Add sector-cap disclosure note
- [ ] **6.** Strengthen look-ahead wording in A4
- [ ] **7.** Add survivorship + benchmark rows to A4
- [ ] **8.** Add the sized error bar to A4
- [ ] **9.** *(optional)* Re-solve on trailing covariance
- [ ] Re-export, confirm **6 pages**, A4, Arial embedded
- [ ] Send to finquest@bpi.com.ph

---

*Edits 1–3 are blocking. Everything else strengthens an already strong submission.*
