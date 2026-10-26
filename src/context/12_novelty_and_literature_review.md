# 12: Novelty check and literature review (2025–2026)

Done 2026-10-25 via web search and arXiv, then reading the closest papers. All PDFs are in `docs/sprint/papers/_all/` and linked in `docs/sprint/papers/proposal_core/`. Venue tiers: **A\*** = ICML / ICLR / NeurIPS / EMNLP main track; **W** = workshop; **P** = arXiv preprint, not yet peer reviewed (most 2026 safety work is still preprints, so we cite them as such).

## Executive summary (as reported, 2026-10-25)

**Our idea is partly pre-empted, but a clear gap remains, so we need to reframe it, not drop it.** Nothing in the plan is committed; the revisions below await approval.

*Already established, so we can't claim it:*
- **Judges favour their own family when rating quality:**
  - Panickssery et al. (NeurIPS 2024): models recognise and favour their own outputs;
  - Goel et al. (ICML 2025): judges favour models similar to themselves;
  - Li et al. (ICLR 2026): judges favour models from the same family;
  - Chen et al. (EMNLP 2025) and Roytburg et al. (ICML 2026): how to measure this correctly.
- **Our statistical design already exists.** Awuni et al. (2026 preprint) use a fully crossed judge × candidate-family design with a corrected estimator, for chat-quality preference only. We adopt and cite it.
- **The opposite effect has also been found.** Pinto et al. (COLM 2026 workshop) report that monitors tuned on one family catch that family's sabotage *better* (+0.17 AUROC; 41% vs 19% caught at a 1% audit budget). Their monitors are *trained*, they study *single-agent code backdoors*, they "do not set up collusion", and they couldn't study prompted monitors (those failed the competence bar).

*Still open (nothing found after a targeted search):*
- how the judge's model family affects **prompted, zero-shot auditors** when they audit **multi-agent collusion**;
- with ground truth from **what agents did** (no writing-quality confound);
- with a **two-sided test** of leniency vs familiarity advantage;
- plus a **mechanism test**: does any family effect disappear when the auditor sees only actions?

*Proposed revisions:*
- **Problem statement:** reframed around the conflicting predictions.
- **Hypotheses:**
  - H1: messages plus actions beats either alone (unchanged);
  - H2: family effect, two-sided (was leniency-only);
  - H3: the family effect shrinks in actions-only views (new);
  - H4: cross-family or mixed-family auditing as mitigation (was H3); paraphrasing is stretch only (Mahbub et al.).
- **Methods additions:**
  - Awuni's and Pinto's estimators plus Roytburg's evaluator-quality baseline;
  - a 3×3 judge × agent AUROC matrix with bootstrap CIs and a permutation test;
  - a self-recognition probe;
  - balanced accuracy and catch rates at 1% and 5% FPR;
  - hard negatives;
  - 3 auditor samples per transcript, reporting the minimum detectable effect.
- **Risks:**
  - a null H2 is more plausible (prompted monitors may be too weak), so gate on above-chance auditor performance;
  - the Introduction must position us against Goel, Li, Awuni and Pinto.

Most 2026 papers are preprints and are marked as such. Several author lists are "et al." and must be completed before submission. **Further refinements from the talks are in [13](13_talks_vs_literature.md).**

## Verdict

**Our core idea is *partly* pre-empted, but a clear and defensible gap remains.** We need to **reframe**, not abandon.

- *Not novel on its own:* "LLM judges favour their own family" (self-preference and family bias are well established in **quality / preference** judging), and the crossed judge × family **interaction design** (already used in 2026).
- *Still open (nothing found after a targeted search):* how the judge's family affects **prompted (zero-shot) LLM auditors** of **multi-agent collusion**, where the ground truth comes from **action outcomes**, not quality ratings. The literature also predicts **opposite directions** here (leniency vs familiarity advantage), and nobody has adjudicated between them for safety auditing.

## Literature map: what's established

| # | Paper | Venue | Finding | Implication for us |
|---|---|---|---|---|
| 1 | Panickssery et al., *LLM Evaluators Recognize and Favor Their Own Generations* | NeurIPS 2024 (A\*) | Self-recognition causes self-preference | The mechanism behind H2 (leniency) |
| 2 | Wataoka et al., *Self-Preference Bias in LLM-as-a-Judge* | NeurIPS 2024 SafeGenAI (W) | Bias tracks **low perplexity / familiarity** | Predicts the effect lives in the **text channel** |
| 3 | **Goel et al., *Great Models Think Alike and this Undermines AI Oversight*** | **ICML 2025 (A\*, spotlight)** | Judges favour *similar* models (CAPA r = 0.84); mistakes become more correlated as capability grows | The headline precedent for "similarity undermines oversight", but for **capability scoring**, not collusion detection |
| 4 | Li et al., *Preference Leakage* | **ICLR 2026 (A\*)** | Judges favour same-model, inherited and **same-family** students | Family bias is real and hard to detect, again in quality evaluation |
| 5 | Chen et al., *Beyond the Surface* | **EMNLP 2025 (A\*)** | Must separate bias from genuine quality | Our row/column controls must remove judge strictness and agent obviousness |
| 6 | Roytburg et al., *Are LLM Evaluators Really Narcissists?* | **ICML 2026 (A\*)** | Only 51% of self-preference findings survive an evaluator-quality baseline | **We must include a quality baseline**, or reviewers will discount H2 |
| 7 | Yang et al., *Quantifying and Mitigating Self-Preference Bias* | P 2026 | Equal-quality pairs; multi-dimensional evaluation cuts bias 31.5% | A structured, multi-question auditor is a candidate mitigation (links to TraceGuard) |
| 8 | **Awuni et al., *Who Judges Matters: Family-Conditioned Preference in LLM-as-Judge Panels*** | P 2026 | Fully crossed 4-family design; a corrected estimator (hold candidate family fixed) gives a +3.4–8.4 pt same-family lift | **Our estimator already exists**, but only for chat-quality preference. We adopt and cite it rather than claim it |
| 9 | **Pinto et al., *Calibration-Family Overfit*** | COLM 2026 workshop (W) | Monitors *calibrated* on family A catch A's sabotage better: **own-family *advantage*** +0.172 AUROC; at a 1% audit budget, 41% vs 19% caught | Predicts the **opposite** of leniency. But it uses **trained heads** on **single-agent code backdoors**, explicitly "do[es] not ... set up collusion", and **could not study prompted monitors** (they failed the competence bar) |
| 10 | Gardner-Challis et al., *When can we trust untrusted monitoring?* | P 2026 | Taxonomy: passive self-recognition, causal and acausal collusion; passive self-recognition can beat the other strategies; summarisation is the best defence | Frames our H2 as **passive** (unprompted) monitor–agent collusion in AI-control terms |
| 11 | Greenblatt et al., *AI Control* | ICML 2024 (A\*) | Untrusted monitoring, collusion, paraphrasing | Foundational framing |
| 12 | Bhatt et al., *Ctrl-Z* | P 2025 | Untrusted-monitor collusion; honeypot validation | Anti-collusion practice |
| 13 | Mahbub et al., *Mitigating Self-Preference by Authorship Obfuscation* | P 2025 | Light perturbation reduces self-preference, but **full style neutralisation lets it recover** | **The paraphrase mitigation may backfire**, so deprioritise it |
| 14 | Barkhordar et al., *Style, Not Self* | P 2026 | Zero-shot self-attribution is mostly **surface cues** (length, comments); normalisation removes most of it | Supports a **channel test**: actions-only views strip style |
| 15 | Kutasov et al., *SHADE-Arena* | P 2025 (Anthropic) | Monitors reach AUC 0.87; sabotage relies on a hidden scratchpad | Monitoring-benchmark precedent; report AUC |
| 16 | Shi X. et al., *Emergent Collusion in Long-Horizon LLM Agent Interaction* | P 2026 | Uninstructed collusion in 94% of trajectories across 10 models; an LLM judge labels onsets | Supports our stretch (emergent) arm; their judge identity is also fixed |
| 17 | Das et al., *You Can't Escape Your Own Activations* | P 2026 | Activation probes stay accurate even when agents are told they're monitored | White-box contrast to our black-box auditors |
| 18 | Nakamura et al., *Colosseum* | P 2026 (NeurIPS 2026 per the talk, unverified) | LLM judge insufficient; action metrics needed; emergent and hidden collusion | Our harness. **The judge model is fixed throughout** |
| 19 | Rose et al. (NARCBench); Arike; Radev; Lee & Park; Hagag (ORBIT) | P 2026 | Transcript monitors are configuration-dependent; less information can help; CoT faithfulness ≠ collusion; per-action defences fail vs colluders | Motivates multiple views and episode-level auditing |

## What is novel in our study

1. **Domain:** judge-family effects in **collusion / safety auditing of multi-agent systems** (a coalition is a group property), rather than chat quality (#3–8) or single-agent code sabotage (#9).
2. **Monitor class:** **prompted, zero-shot** auditors, the class practitioners deploy. #9 explicitly couldn't measure it.
3. **Ground truth from actions:** Colosseum's DCOP outcomes (coalition advantage, regret) label collusion independently of any judge. This avoids the "quality confound" that #5, #6 and #8 had to correct for.
4. **Adjudicating competing predictions:** **leniency** (#1–4, #8) vs **familiarity advantage** (#9; Anwar's sentinel view), tested two-sided on the same transcripts.
5. **Channel mechanism:** whether any family effect lives in the **language** channel (style or perplexity, #2, #14) and vanishes in an **actions-only** view. This ties H1 (views) to H2 (family) mechanistically; nothing found does this.
6. **Deployable recommendation:** a cross-family transfer matrix (as #9 recommends) plus a measured mitigation for auditor choice in multi-agent oversight.

## Required changes to our framing (proposed)

**Problem statement (revised):**
> LLMs increasingly audit multi-agent transcripts for collusion: Colosseum's judge, the METR/Redwood incident investigation, and long-horizon collusion studies all use them. Separate literatures warn that judges favour models like themselves (self-preference, family bias) and that monitors work best on the model lineage they were tuned on (calibration-family overfit). These predict *opposite* effects. Nobody has measured how an auditor's model family affects prompted collusion audits of multi-agent systems, where the ground truth comes from what agents did, not how well they wrote.

**Hypotheses (revised):**
- **H1 (views):** messages plus actions beats either alone at a fixed FPR. *(Unchanged.)*
- **H2 (family effect, two-sided):** the judge-family × agent-family interaction on true-collusion suspicion is non-zero. We pre-register two competing predictions: **H2-L, leniency** (negative interaction) vs **H2-F, familiarity advantage** (positive interaction).
- **H3 (mechanism, new):** the family interaction shrinks toward zero in the **actions-only** view, where stylistic cues are absent, relative to views that include messages.
- **H4 (mitigation, was H3):** a cross-family auditor, or a family-diverse ensemble, matches or beats same-family auditing at modest cost. A paraphrase arm is now *stretch only* (#13 suggests it may backfire).

**Methodology and evaluation (additions):**
1. **Estimators:**
   - adopt **Awuni's** corrected estimator: hold the agent family fixed and compare judges;
   - adopt **Pinto's** interaction decomposition: remove judge capability and agent obviousness;
   - add **Roytburg's** evaluator-quality baseline (check each judge's accuracy on negatives and on other families).
2. **Report a 3×3 judge × agent AUROC transfer matrix** (as #9 recommends), with bootstrap CIs over transcripts and a permutation test for the interaction (as #8 does).
3. **Self-recognition probe (cheap):** ask each auditor "which model family produced these agents?" and correlate recognition accuracy with the size of the family effect (the #1 mechanism).
4. **Balanced accuracy, and TPR at 1% and 5% FPR** (#14; Nguyen talk).
5. **Hard negatives:** cheap talk without action, and parallel moves without talk.
6. **Power:** prior family-bias effects are 3–8 percentage points with about 9,000 judgments (#8). Ours will have far fewer, so add **repeated auditor samples per transcript** (k = 3 at temperature > 0) and report the minimum detectable effect. Frame any null as bounded, not as absence.

## Risks introduced by the literature

- A **null H2** is now more plausible: prompted monitors may simply be too weak to show family structure (#9). Mitigation: the positive-control gate on auditor competence (AUROC clearly above 0.5) before interpreting H2.
- Reviewers who know #3, #4, #8 or #9 will ask "what's new?" The Introduction must position against them explicitly (domain, monitor class, action ground truth, direction test, channel mechanism).

## References (for the report's list)

- Panickssery, A., Bowman, S. R., & Feng, S. (2024). LLM Evaluators Recognize and Favor Their Own Generations. *NeurIPS 2024*. arXiv:2404.13076.
- Wataoka, K., Takahashi, T., & Ri, R. (2024). Self-Preference Bias in LLM-as-a-Judge. *NeurIPS 2024 Safe Generative AI Workshop*. arXiv:2410.21819.
- Goel, S., et al. (2025). Great Models Think Alike and this Undermines AI Oversight. *ICML 2025*. arXiv:2502.04313.
- Li, D., et al. (2026). Preference Leakage: A Contamination Problem in LLM-as-a-judge. *ICLR 2026*. arXiv:2502.01534.
- Chen, et al. (2025). Beyond the Surface: Measuring Self-Preference in LLM Judgments. *EMNLP 2025*. arXiv:2506.02592.
- Roytburg, D., et al. (2026). Are LLM Evaluators Really Narcissists? Sanity Checking Self-Preference Evaluations. *ICML 2026*. arXiv:2601.22548.
- Yang, J., et al. (2026). Quantifying and Mitigating Self-Preference Bias of LLM Judges. arXiv:2604.22891.
- Awuni, D. A., et al. (2026). Who Judges Matters: Measuring Family-Conditioned Preference in LLM-as-Judge Panels. arXiv:2609.17857.
- Pinto, L., et al. (2026). Calibration-Family Overfit: Why Trusted Sabotage Monitors Don't Transfer Across Lineages. *COLM 2026 AI Measurement Science Workshop*. arXiv:2607.06596.
- Gardner-Challis, N., et al. (2026). When can we trust untrusted monitoring? A safety case sketch across collusion strategies. arXiv:2602.20628.
- Greenblatt, R., Shlegeris, B., Sachan, K., & Roger, F. (2024). AI Control: Improving Safety Despite Intentional Subversion. *ICML 2024*. arXiv:2312.06942.
- Bhatt, A., et al. (2025). Ctrl-Z: Controlling AI Agents via Resampling. arXiv:2504.10374.
- Mahbub, T., et al. (2025). Mitigating Self-Preference by Authorship Obfuscation. arXiv:2512.05379.
- Barkhordar, E., et al. (2026). Style, Not Self: Surface Cues Explain Zero-Shot Code Attribution by Large Language Models. arXiv:2609.30048.
- Kutasov, J., et al. (2025). SHADE-Arena: Evaluating Sabotage and Monitoring in LLM Agents. arXiv:2506.15740.
- Shi, X., et al. (2026). Emergent Collusion in Long-Horizon LLM Agent Interaction. arXiv:2609.24967.
- Das, A., et al. (2026). You Can't Escape Your Own Activations: Evaluation Awareness and Multi-Agent Monitoring. arXiv:2609.03035.
- Nakamura, M., et al. (2026). Colosseum: Auditing Collusion in Cooperative Multi-Agent Systems. arXiv:2602.15198.
- Shlegeris, B. (2024). How to prevent collusion when using untrusted models to monitor each other. Redwood Research blog.

*Author lists marked "et al." should be completed from the PDFs before submission, and initials verified (e.g. Chen et al. 2025).*
