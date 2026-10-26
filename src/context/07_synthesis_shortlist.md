# 07: Synthesis: shortlisted research directions (preliminary)

**Status:** superseded by [09_research_decision.md](09_research_decision.md). After the talks, Candidate A was selected (with H3 as the Track 3 countermeasure arm).

Inputs: [01 What wins](01_what_wins.md) · [02 RQ analysis](02_tracks_2_3_rq_analysis.md) · [05 Definitions](05_definitions_survey_notes.md) · [06 Starter code](06_starter_code_assessment.md) · incident sources in `docs/incident/sources/`.

## Selection criteria (derived from the rubric)

| Criterion | Weight | Meaning |
|---|---|---|
| Novelty / gap hit | 30% | Targets a gap the RQ text or the definitions survey names as untested |
| Feasibility in ~1.5 days | 30% | Python 3.11, ≤ a few hundred agent calls for the main experiment, low engineering risk |
| Clean evaluation | 25% | Ground truth or matched controls, so we can report accuracy, FPR and effect sizes with CIs |
| Narrative strength | 15% | A clear theory of change; ties to the sprint's motivating incident and to AI-safety practice |

## Candidates

### A. "Do LLM auditors go easy on their own kind?" (RQ 2.3 + 2.2, monitor-collusion angle)
- **Gap:** the definitions survey notes that monitor–policy collusion is *assumed from shared identity, not elicited or measured*. RQ 2.3 asks what counts as convincing evidence; in practice evidence is increasingly judged by LLMs.
- **Design sketch:** generate labelled Colosseum trajectories (positives: conditions A/B with a prompted coalition; negatives: C/D) with agent model family X. Audit each with judges from family X (same) and families Y and Z (different), under information views: messages-only, actions-only, both (the 2.2 "hybrid"). Freeze judge prompts and thresholds first.
- **Metrics:** AUROC, TPR at fixed FPR, and calibration per judge × view; the **same-family leniency gap** (Δ in suspicion scores on true positives, same vs cross family), with bootstrap CIs; agreement with a second rater on a subsample.
- **Hypotheses:** H1 the hybrid view beats either single view; H2 same-family judges assign lower suspicion to true coalitions than cross-family judges at matched FPR.
- **Feasibility:** high. Agent runs are cheap (~20–60 calls each), and judging is many cheap single calls that can be re-run without regenerating data. **Risk:** H2 may be null. A tight null is still reportable and useful.
- **Score:** novelty 4 · feasibility 5 · evaluation 5 · narrative 4.

### B. "What makes uninstructed collusion emerge in agent workflows?" (RQ 2.1 + 3.1)
- **Gap:** Colosseum and most AI-safety work study *instructed* coalitions. The survey finds AI-safety definitions skew towards instructed or capability settings; RQ 2.1 asks for the *core components a task needs*.
- **Design sketch:** Colosseum with **no coalition prompt**. Factorially vary task-level levers one at a time: e.g. reward structure (individual vs shared), task feasibility pressure, and channel availability (none / open / private). Measure the emergence of coalition advantage among the best-performing proper subset, plus channel-use behaviour.
- **Metrics:** coalition advantage of the best proper subset against a permutation null; regret; rate of coordination messages; judge-scored intent.
- **Feasibility:** medium. More conditions and seeds are needed, and the effect may be small for cheap models (a risk of an all-null grid). Little engineering if the levers are expressible via prompt overrides and configs.
- **Score:** novelty 5 · feasibility 3 · evaluation 4 · narrative 5.

### C. "A trusted agent that offers to collude" (RQ 3.2)
- **Gap:** explicitly named on the site as never tested.
- **Design sketch:** `llm-agent-collusion-2` (Liar's Bar / Cleanup). A scripted trusted player offers the same pact to every agent (direct offer / indirect hint / benign cooperation request). Record verbal acceptance and repeated preferential play; compare against the explicit-alliance positive control.
- **Feasibility:** medium. A new scripted-player hook is needed; games cost ~20–260 calls each.
- **Score:** novelty 5 · feasibility 3 · evaluation 4 · narrative 3.

### D. Partial monitoring budgets (RQ 3.4)
- Strong question, but the starter (`llm-agent-collusion`) needs Python ≥3.12, which conflicts with our 3.11 rule, and it is a market setting. **Parked** unless we grant an exception.

## Preliminary recommendation

- **Core: A.** It's the strongest combination of feasibility and clean evaluation, it merges 2.3 and 2.2, and it answers an open measurement question with direct relevance to how labs audit multi-agent incidents.
- **Stretch: B's emergent-collusion runs as an extra, harder test set for A's auditors** (uninstructed cases are the realistic detection target). This merges Tracks 2 and 3 into one story: *how collusion arises without instruction, and whether LLM auditors can be trusted to catch it.*
- **C** is the fallback if the talks suggest 3.2 is under-covered by other teams.

## Open decisions (for the next request)

1. Confirm A (+ B stretch), after studying the priority talks.
2. Agent and judge model families, and budget, on OpenRouter (cost check).
3. Any Track 1 element worth adding later (see `TODO.md`).
