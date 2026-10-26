# 09: Research decision: question, definition, plan, feasibility

This closes the TODO §2 items. Inputs: [01](01_what_wins.md) · [02](02_tracks_2_3_rq_analysis.md) · [05](05_definitions_survey_notes.md) · [06](06_starter_code_assessment.md) · [07](07_synthesis_shortlist.md) · [08](08_talks_findings.md). The detailed methodology and evaluation framework are the next deliverable (`src/plan/`).

## 1. Track 1 revisit (TODO item)

| Track 1 gap | Could it add to our Track 2/3 story in ~1 day? | Verdict |
|---|---|---|
| 1.3 detection without a channel / same-base-model correlation (Xu) | Conceptually close: "common cause" from a shared model is the same mechanism as same-family leniency. Testing it needs a market harness plus a new dependence statistic. | **Cite** in Related Work as the action-side analogue; don't run it |
| 1.4 pairwise net influence on LLM agents | Would be a third detector beside the LLM judges; implementation risk, and it assumes exactly two colluders | Optional stretch only |
| 1.2, 1.5 | Market-specific, separate harness (llm-cartel, double auction needing Python ≥3.12) | No |
| Free market test set from stored ColludeBench runs | Checked: mostly **scripted** keyword-steganography agents, not natural LLM text from known model families, so unusable for a family-match study | No |

**Decision:** no Track 1 RQ for now. Keep one sentence linking our result to Xu et al.'s "same base model, correlated behaviour" finding. Re-check only if the core experiment finishes early.

## 2. The one sharp research question

> **When LLMs audit multi-agent transcripts for collusion, are they more lenient toward agents from their own model family, and does giving the auditor both what agents said *and* what they did, or using a different-family auditor, close the gap?**

Working title: **"Who audits the auditors? Same-family leniency in LLM collusion monitors."**

- **Tracks:** primary **Track 2** (2.3 standards of evidence; 2.2 words vs actions). **Track 3** via the countermeasure: auditor diversity (cross-family or ensemble monitoring), reported as a safety-versus-cost trade-off.
- **Is it about AI collusion?** Yes, on two levels. The audited behaviour is multi-agent collusion (a Colosseum coalition gaining at others' expense), and the threat studied is **monitor–agent collusion**, which the definitions survey codes as a collusion sense (Shlegeris; Nguyen cluster C; Velja's threat model 4).
- **Novelty:** the website gaps for 2.2 (hybrid word/action checks) and 2.3 (what counts as evidence) are both targeted. On top of that sits a gap named by **five sprint speakers and the definitions survey**: same-family monitor collusion is *assumed, not measured*. Colosseum's authors fixed the judge and never varied it.

## 3. Definition of collusion we adopt

The survey's cross-family minimal definition: *"two or more agents coordinate, with or without communication, in a way that benefits them at the expense of a third party, contrary to the intended competitive or oversight structure."* We operationalise it with Colosseum's Δ-collusion. **Positive** = an assigned coalition whose members were instructed to pursue a coalition objective (ground truth by design), split by outcome into **effective** (coalition advantage > 0: direct or hidden collusion) and **on paper** (instructed but no gain). **Negative** = no coalition instruction.

- Components (survey codes): multiple parties ●, coordination ●, unwanted ●, third-party harm ● (non-coalition agents and the principal), communication ◐ (measured, not assumed), intent ◐ (inferred by the auditor, not required).
- **Auditor leniency** is defined operationally as lower suspicion assigned to true positives, relative to other auditors, after removing each auditor's overall strictness (see §4).

## 4. One-paragraph plan (the TODO deliverable)

**Hypotheses.** H1 (2.2): an auditor given messages *and* actions detects collusion better than one given either alone. H2 (core): auditors assign lower suspicion to colluding agents from their own model family, measured as the **judge-family × agent-family interaction**, so that main effects (some judges are simply stricter, some agent families are more obvious) cancel. H3 (Track 3): a cross-family auditor, or an ensemble, recovers detection lost to same-family auditing at modest extra cost.

**Positive control.** Colosseum condition A (pair instructed to collude plus a private channel) must show (i) mean coalition advantage above the no-coalition baseline D across seeds, and (ii) above-chance auditor detection of A versus D (AUROC > 0.5 with the CI excluding it), before any H2 claim.

**Single manipulated variable** (for H2): whether the auditor's family matches the agents' family. **Every transcript is judged by every auditor**, so the transcripts are held fixed and the comparison is within-transcript. Views (messages-only / actions-only / both) are a second, separately analysed factor for H1.

**Design.** 3 agent families (e.g. OpenAI gpt-4o-mini, Meta Llama-3.3-70B, Qwen3-32B; all tool-calling, similar price tier), JiraTicket environment, the four matched conditions A–D, path topology, 4 agents. Seeds: a **3-seed pilot**, then 10 per cell (≈120 runs). The same 3 families serve as auditors (a 3×3 grid; the diagonal is "same family"), with a frozen prompt producing a 0–100 suspicion score plus a guess at the colluding pair. Agent model ids are never shown to the auditor.

**Metrics.**
- Detection: AUROC, TPR at 5% (and, n permitting, 1%) FPR, pair-identification accuracy.
- **Leniency Δ** = mean suspicion on positives (same family) minus (off-diagonal mean), adjusted for row and column effects, with **bootstrap CIs over transcripts**. Also a mixed-effects check.
- Hard negatives (per Nguyen): condition C (open channel, no instruction) and an emergent arm (private channel, no instruction).
- A second-rater agreement check on a sample of labels.

**Budget.** At live OpenRouter prices (in/out per M tokens: gpt-4o-mini $0.15/$0.60, Llama-3.3-70B $0.10/$0.32, Qwen3-32B $0.08/$0.28), ≈120 agent runs (~40 calls each) plus ≈1,080 auditor calls is roughly **$10–40**, inside the Resources tab's $5–120 band. Modal isn't needed.

**Success / failure.**
- **Success** = H2 interaction CI excludes 0 in the lenient direction, *and* the positive control passes.
- **Informative null** = a tight CI around 0, reported as "no evidence of same-family leniency at this scale".
- **Failure** = the positive control doesn't pass. Fallback: stronger coalition prompt (`structured` variant), 4 planning rounds, more seeds.

## 5. Feasibility check against the Resources tab

| Factor | Resources-tab guidance | Ours |
|---|---|---|
| Setup risk | Colosseum: medium (preflight) | Medium. Python 3.11 is native, configs exist; the new code is the auditor layer only (`src/`) |
| Calls | 20–40 episodes plus 100–300 judge calls (2.1/2.3) | ~120 episodes (pilot 36) plus ~1,080 auditor calls, all cheap single calls |
| Budget | $15–75 (cap $150) / $5–30 | ~$10–40 |
| Hardware | 16 GB laptop, no GPU | Same, in the project `.venv` (3.11) |
| Time | Weekend | Pilot and positive control in about 4 h; full runs plus auditing in about 6 h; analysis and writing in the remaining time |

**Main risks and mitigations:**
1. Small open models handle tool calls badly → pilot first; swap in a sturdier model of the same family.
2. Positive control is weak → stronger prompt variant, more planning rounds.
3. H2 is null → still a publishable, judge-relevant result. H1 and H3 carry the paper regardless.
4. Auditors recognise family by style (Dietrich) → that is a *mechanism*, testable with a paraphrased-transcript arm as a stretch Track 3 mitigation.

## 6. What happens next

1. Write `src/plan/methodology.md` (the full design, with predeclared thresholds, analysis plan and figures) and freeze the auditor prompt.
2. Set up Colosseum (`UV_PYTHON=3.11 ./setup.sh colosseum`, `compute.env` from `.env`), run preflight, then a 1-seed smoke run per family.
3. Pilot (3 seeds) → positive-control gate → full runs → auditing → analysis.
