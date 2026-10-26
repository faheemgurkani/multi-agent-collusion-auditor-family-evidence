# 11: Current shortlist (questions, problem, hypotheses, papers, talks)

Updated 2026-10-25. ⚠️ **Revisions proposed in [12](12_novelty_and_literature_review.md)**: problem statement reframed, H2 made two-sided (leniency vs familiarity), new H3 channel-mechanism hypothesis, mitigation renumbered H4. Further additions proposed in [13](13_talks_vs_literature.md): structured-report view, collusion-type breakdown, capability covariate, Pareto reporting. Pending approval. The single source of truth for the proposal ahead of `src/plan/`. Background: [09](09_research_decision.md) (decision), [10](10_model_selection.md) (models and budget).

## Shortlisted research questions

- **Main (chosen): RQ 2.3 + 2.2, with a Track 3 countermeasure.** Are LLM collusion auditors more lenient toward agents from their own model family? Does seeing both messages and actions help? Does auditing with other families fix it?
- **Stretch: RQ 2.1 + 3.1**, collusion that emerges without instruction. These runs double as a harder test set for the auditors.
- **Fallback: RQ 3.2**, a trusted agent that offers to collude.
- **Parked:** RQ 3.4 (its code needs Python 3.12) and all of Track 1. RQ 1.3 (Xu et al.) is cited as the action-side analogue.

## Problem statement

LLMs are increasingly used to audit multi-agent transcripts, as in the METR/Redwood investigation of the July 2026 incident, which relied heavily on GPT-5.6 Sol analysis agents. AI-control practice assumes that a monitor from the same model family as the agents may collude with them or go easy on them. But nobody has measured this: collusion-detection work treats the auditor as trustworthy.

## Hypotheses

- **H1:** an auditor given both messages and actions detects collusion better than one given either alone.
- **H2 (core):** auditors give lower suspicion scores to colluding agents from their own family, measured as the judge-family × agent-family interaction.
- **H3:** auditing with a different-family model, or a mix of families, recovers the detection that same-family auditing loses, at modest extra cost.

**Model lineup** (budget-aware, see [10](10_model_selection.md)): Google Gemma 4 31B, NVIDIA Nemotron 3 Super 120B (both free on OpenRouter), and OpenAI GPT-OSS-120B (cheap paid, also in the Modal Library). Each serves as both agent and auditor.

## Related papers

Paths are under `docs/sprint/papers/_all/`; all are also linked in `docs/sprint/papers/proposal_core/`.

**Core**
- Nakamura 2026, *Colosseum*: our harness and metrics. `Nakamura_2026_Colosseum_2602.15198.pdf`
- Greenblatt 2023, *AI Control*: trusted and untrusted monitoring. `Greenblatt_2023_AIControl_2312.06942.pdf`
- Shlegeris 2024, *How to prevent collusion when using untrusted models to monitor each other* (Redwood blog): monitor–policy collusion. `Shlegeris_2024_PreventCollusionUntrustedMonitoring.md`
- Nguyen 2026, *TraceGuard*: same-model monitor collusion assumed, not measured. `Nguyen_2026_2604.03968.pdf`

**Say vs do (2.2)**
- Shi 2026, *When Agents Lie*. `Shi_2026_2607.05132.pdf`
- Radev 2026, *The Best-Laid SCHEMEs*. `Radev_2026_2605.29178.pdf`
- Arike 2026, monitors and information access. `Arike_2026_2601.21112.pdf`
- **Lee & Park 2026, *Faithful yet Collusive*:** CoT faithfulness doesn't reveal collusion. `LeePark_2026_FaithfulYetCollusive_2609.18346.pdf` *(new)*
- **Hagag 2026, *ORBIT*:** per-action defences fail against colluding agents. `Hagag_2026_ORBIT_2609.33102.pdf` *(new)*

**Monitor awareness and evasion**
- Kale 2025. `Kale_2025_2508.19461.pdf`
- Najt 2026, *SLEIGHT-Bench*. `Najt_2026_2605.16626.pdf`
- Jiralerspong 2026. `Jiralerspong_2026_2603.16928.pdf`

**Same-model coordination and identity**
- Dietrich 2026, peer identification from style. `Dietrich_2026_2606.09854.pdf`
- Xu 2026, the same base model gives correlated behaviour (link to Track 1's RQ 1.3). `Xu_2026_2607.26385.pdf`
- Aharon 2026, tacit coordination. `Aharon_2026_2601.22184.pdf`
- **Mallen 2024, *Subversion Strategy Eval*:** instances coordinating without communication. `Mallen_2024_SubversionStrategyEval_2412.12480.pdf` *(new, found via the starter reading list)*

**Detection methods and steganography**
- **Rose 2026 (NARCBench):** white-box multi-agent collusion detection; only 2 of 229 emergent episodes verbalised. `Rose_2026_2604.01151.pdf` (NARCBench is this paper's benchmark; already local)
- **Anwar 2026, *A Decision-Theoretic Formalisation of Steganography With Applications to LLM Monitoring*:** the steganographic gap and the trusted sentinel. `Anwar_2026_DecisionTheoreticSteganography_2602.23163.pdf` *(new)*
- **Motwani 2024, *Secret Collusion among AI Agents*:** a same-family overseer; oversight lags collusion as capability grows. `Motwani_2024_SecretCollusion_2402.07510.pdf` *(new)*
- Rippin 2026, tool-enabled steganography. `Rippin_2026_2606.28425.pdf`

**Definitions:** the collusion-definitions survey, `starter/collusion_hackathon/literature/definitions/README.md`.

**Motivation:** the METR/Redwood and OpenAI incident reports, `docs/incident/sources/`.

## Related talks (`docs/misc./transcripts/`)

- **Most important:**
  - Nakamura & Bagdasarian, Colosseum (`06`)
  - Khanh Linh Nguyen, collusion overview (`08`)
- **High:**
  - Kemeklis, AI control (`03`)
  - Anwar, detecting steganography (`05`)
  - Shi, trust-breaking (`07`)
- **Supporting:**
  - Velja (`01`)
  - Motwani (`02`)
- **Pending:** Matthew Lee, "Defining AI Collusion". The recording is now posted in Discord #announcements, but its transcript has not been downloaded yet.
