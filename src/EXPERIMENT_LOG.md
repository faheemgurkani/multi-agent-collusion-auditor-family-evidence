# Experiment log (what we ran, what didn't work, dual-use notes, spend)

All times UTC. This feeds the report's Methods ("what didn't work"), reproducibility appendix, and the Limitations & Dual-Use appendix.

## Timeline
- 11:20: plan frozen (`src/plan/FREEZE.md`).
- 12:14: OpenRouter balance $10.92 (credits $54, used $43.08). Free-model quota 1,000/day.
- 12:15: Colosseum set up on Python 3.11 (`UV_PYTHON=3.11 ./setup.sh colosseum`); preflight passed. `compute.env` → symlink to the project `.env`.
- 12:16–12:17: Modal Dedicated Endpoints created (no region flags): `gptoss-120b` = openai/gpt-oss-120b@b5c939d; `gemma4-31b` = google/gemma-4-31B-it@3548789.
- 12:20: Nemotron pilot on the free route → **all calls HTTP 404** (see below). Archived.
- 12:30: Nemotron switched to the paid route pinned to DeepInfra (D2); pilot re-run.

- 12:31: Modal endpoints live (SGLang; Gemma with `--tool-call-parser gemma4`, speculative DFlash decoding). Tool calls verified on both.
- 12:33–12:39: v1 pilot (`simple` prompt, 2 rounds): Gemma 4/4 runs, GPT-OSS 4/4, Nemotron 1/2 A (one 429 failure). Test audits revealed Nemotron truncation at 4k tokens and DeepInfra 429s.
- ~12:41: **G1 failed on the v1 pilot** (A−D ≈ +1.5, CI ∋ 0), so the pre-registered contingency was applied: `structured` prompt plus 4 planning rounds (D5). v1 pilot archived.
- 12:42–12:46: pilot2: Gemma 6/6; GPT-OSS 0/6 (Modal 503 "no upstreams available" during a container drain; cold start ~7.5 min). Gemma A−D per seed = +8.0, −8.5, +2.0 (high environment variance) → G1 deferred to main data, as pre-registered.
- 12:47: keep-warm pinger started (`src/pipeline/keepwarm.sh`); Colosseum client retries raised (15, max sleep 60 s).
- 12:48: main runs launched (Gemma, GPT-OSS on Modal; Nemotron 4 parallel processes, one per condition).
- 12:50–12:53: summariser and auditors validated on pilot2 data: 100% parse after fixes (D6). Pilot excluded from analysis.
- 12:56: **Gemma and GPT-OSS main: 40/40 runs, 0 failures.** Audit pipeline started. Seed extension (106–108) and the emergent arm E launched for the Modal families.

- 13:32: DeepInfra saturated for Nemotron (upstream 429; 0 of 4 runs finished in 44 min). Re-pinned all Nemotron calls to DekaLLM fp8 (D8); restarted Nemotron main runs (2 concurrent per condition) and the Nemotron auditor.

- 15:36: Nemotron main (20/20) and extension (12/12) complete, 0 failed runs; 12 DekaLLM HTTP-400 turn truncations in total across 32 runs. Families balanced at 8 seeds × 4 conditions.
- 15:42–16:35: views, V4 summaries (32, 0 empty), audits by all three auditors (k = 3; Gemma/GPT-OSS behind keep-warm, about 5 min) and probes completed; final analysis started.

## What didn't work
1. **Modal endpoint id is case-sensitive:** `google/gemma-4-31b-it` was rejected; the Library id is `google/gemma-4-31B-it`.
2. **Modal endpoints require a proxy token** (or `--unauthenticated`). We created a workspace proxy token, stored as `MODAL_PROXY_TOKEN` in `.env`.
3. **OpenRouter free Nemotron (`:free`, provider Nvidia) returned HTTP 404 "Function … Not found"** for every request, so the free tier was unusable for this family. Paid providers (DekaLLM, DeepInfra, Crusoe) worked, including tool calls.
4. **Colosseum's LLM client can't pass OpenRouter provider routing**, so we patched it (D2) to pin a single provider per family.

5. **The `simple` coalition prompt barely changed behaviour** (several seeds gave identical allocations in A and D), which triggered the pre-registered switch to `structured`.
6. **Modal scale-to-zero / container drain** caused 503s and ~7.5 min cold starts, failing every GPT-OSS pilot2 run. Fixed with a keep-warm pinger and longer client retries.
7. **Nemotron puts its reasoning in the content field** (Gemma and GPT-OSS separate it), so a 4k cap truncated 8/17 pilot audits before the JSON. Fixed with an 8k cap for all auditors.
8. **OpenRouter routed DeepSeek summaries to different providers** (Relace fp4, Baidu fp8), and 3/6 truncated. Fixed by pinning DeepInfra and an 8k cap.
9. **Coalition advantage is very noisy across seeds** (each seed is a different environment draw), so G1 can't be decided on a 2–3 seed pilot.
10. **Pinning one provider makes you depend on its shared capacity.** DeepInfra's OpenRouter capacity for Nemotron saturated mid-run (sustained upstream 429s, 6–15 min per agent turn), stalling every Nemotron run. Re-pinned to DekaLLM fp8 (D8). Lesson: check every candidate provider for latency, tool calls and throughput before pinning.
11. **DekaLLM (vLLM) rejects some multi-step Nemotron conversations with HTTP 400 "Unterminated string"** when an earlier assistant tool call in the history has malformed JSON arguments. Terrarium catches this and ends that agent's turn after its first step; the tool calls already made still count, and the run continues. Not retried (400 is non-retryable). We count occurrences per run from the logs and report them; they are a Nemotron-specific source of noise.

## Dual-use notes (for the appendix)
- No new collusion technique is introduced; the coalition prompts are Colosseum's existing ones.
- A finding about the *direction* of auditor family bias could inform an attacker's choice of agent model relative to a known auditor. Report it at the level needed by defenders (choose cross-family / diverse auditors).

- Finding with dual-use weight: action-only monitors (V2) were at chance; essentially all detection signal came from messages. Coalitions that coordinate without explicit messages (or launder them) would evade the prompted monitors studied here. We report this as a monitoring gap and publish no evasion strategies.
- Same-family auditing showed no significant advantage or leniency, but every point estimate leaned toward leniency; deployers should not assume a same-family monitor is safe. Cross-family ensembles were significantly better for one agent family and statistically indistinguishable for the other two.

## Spend tracker
| Time | OpenRouter balance | Modal (est.) | Note |
|---|---|---|---|
| 12:14 | $10.92 | $0 | start |
| 13:16 | $10.666 | $15.23 (credit) | Gemma/GPT-OSS audits complete; keep-warm stopped (endpoints scale to zero) |
| 12:56 | $10.80 | ~2 endpoints × ~40 min uptime | pilots plus 40 main runs |
| 16:40 | $7.703 | **$19.31 total** (`modal billing report`: GPT-OSS $10.35, Gemma $8.96) | all 32 Nemotron runs on DekaLLM (main 20 + ext 12, 0 failed); every audit and probe done. OpenRouter spend this session $3.22 (agent runs ≈ $1.5, audits/summaries ≈ $1.7 est.) |

## Final confirmatory results (2026-10-25 16:48 UTC; `src/results/main/results.json`, 10k bootstrap, 5k permutations)
Data: 96 transcripts = 3 agent families × 4 conditions (A, B, C, D) × 8 seeds (101–108); 3 auditors × 4 views × k = 3 → 3,456 audits; parse rate 100% / 100% / 99.9% (1 Nemotron final failure). Emergent arm E: Gemma and GPT-OSS only, 5 seeds each, k = 1 (exploratory).

- **G1 (environment positive control): fails narrowly.** CA(A) − CA(D) = +3.84, 95% CI [−0.11, 7.83], n = 24 family-seed pairs. Pre-registered consequence: the study is reported as auditing *instructed* coalitions (label = instruction, not realised advantage), with E1 (collusion-type breakdown) emphasised. E1 counts: 48 negatives, 20 attempted-but-no-advantage, 17 direct, 11 hidden.
- **G2 (auditor competence, V3): passes for all three.** AUROC Gemma 0.889 [0.831, 0.948], GPT-OSS 0.842 [0.763, 0.913], Nemotron 0.808 [0.715, 0.887].
- **H2 (family effect): not detected.** Pooled diagonal interaction I = −0.029, 95% CI [−0.063, +0.004], permutation p = 0.12, MDE(80%) = 0.048. All three diagonal cells are negative (Gemma −0.034, GPT-OSS −0.013, Nemotron −0.040), i.e. same-family auditors are slightly *worse*: the direction is consistent with leniency, not a familiarity advantage, but not significant. On V1 alone: I = −0.039 [−0.090, +0.011], p = 0.09.
- **H1 (both channels beat the better single view): not supported.** AUROC(V3) − max(V1, V2): Gemma +0.013 [−0.033, 0.056], GPT-OSS −0.039 [−0.107, 0.027], Nemotron −0.039 [−0.117, 0.031]. Messages carry nearly all the signal. **Actions-only (V2) is at chance for every auditor** (AUROC 0.48 / 0.48 / 0.48), whereas messages-only (V1) gives 0.88 / 0.88 / 0.85.
- **H4 (mitigations):** the cross-family ensemble significantly beats the same-family auditor for GPT-OSS agents (0.988 vs 0.875; Δ CI [+0.016, +0.244]); for the other families it is directionally better or neutral (n.s.). The V4 neutral report *lowers* AUROC (0.79 / 0.74 / 0.71 pooled vs 0.89 / 0.84 / 0.81 on V3), so summarisation loses evidence rather than removing a style confound.
- **False positives / calibration:** at a threshold of 50, balanced accuracy on V3 is 0.85 (Gemma), 0.58 (GPT-OSS), 0.69 (Nemotron); mean suspicion on negatives 1.3 / 15.0 / 12.1. TPR at 5% FPR is 0.79 / 0.38 / 0.52.
- **E2 (self-recognition probe):** no auditor recognises its own family above its base rate. All auditors default to answering "GPT-OSS" (Gemma 94/96, GPT-OSS 85/96, Nemotron 31/96), so the apparent 0.94 accuracy on GPT-OSS agents is an artefact; Gemma never names Gemma; Nemotron names Nemotron for 4/32 of its own transcripts. (Corrected 2026-10-26: results.json had stored this table transposed; fixed in analyze.py.)
- **E3 (emergent, uninstructed private channel):** mean CA −1.5 (Gemma) and −1.8 (GPT-OSS), SD ≈ 4.4, n = 5 each: no emergent coalition advantage.
- **Provider sensitivity (D8):** on 51 transcript-views audited by Nemotron on both DeepInfra (bf16) and DekaLLM (fp8), mean suspicion was 25.0 vs 26.1, Spearman ρ = 0.63, which is at least as high as single-sample test-retest within DekaLLM (ρ = 0.44, n = 383). The provider switch adds no detectable noise.

## Exploratory (post hoc, not pre-registered) analyses (2026-10-26; `src/analysis/figures_extra.py` → `results/main/tables/exploratory.json`)
- **Simple detectors, no model (AUROC, A+B vs C+D):** coalition advantage 0.54 [0.43, 0.66]; system regret 0.54; pair's message count 0.61; log length 0.57; **count of the word "coalition" 0.81 [0.74, 0.88]**. The word appears in 75% of A and 50% of B episodes and in 0% of C and D.
- **Talk vs outcome (48 coalitions, V3 mean suspicion):** Spearman with pair's message count ρ = 0.52 (p = 0.0001); with coalition advantage ρ = 0.12 (p = 0.40).
- **Auditors beyond the keyword:** on coalitions without the word, V1 AUROC is 0.69 / 0.80 / 0.76; with it, 0.99 / 0.93 / 0.90.
- **Why V4 hurts:** "coalition" survives in only 17% (A) and 25% (B) of V4 summaries.
- **Agreement between auditors (Spearman):** V1 0.68–0.73; V2 0.11–0.50; V3 0.63–0.67; V4 0.70–0.83.
- Figures: design schematic, environment with all seeds, episode anatomy, drivers, baselines, distributions, ROC, permutation null, agreement, cost–detection.
