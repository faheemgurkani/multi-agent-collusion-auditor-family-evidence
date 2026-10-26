# 01: What wins (rubric, reviewer guidance, dos/don'ts, sample paper)

Sources: [`docs/sprint/03_guidelines_and_rubric.md`](../../docs/sprint/03_guidelines_and_rubric.md), [`docs/sprint/08_logistics_talk_notes.md`](../../docs/sprint/08_logistics_talk_notes.md), the past first-place report [`docs/sprint/examples/past_winner_noticing_the_escapes.pdf`](../../docs/sprint/examples/past_winner_noticing_the_escapes.pdf) (read in full; pages 1 and 3 also viewed as images).

## 1. The scoring model, turned into design constraints

| Dimension | What a 4–5 needs | Design implication for us |
|---|---|---|
| **Impact & Innovation** | "Is this actually new, or replicating recent work?" An original approach or a neglected problem, a clear theory of change, "you'd be excited to share this." | Don't stop at the Resources tab's weekend project. Add a twist that hits a gap the RQ text names explicitly, and ground it in the July incident, which is the strongest available theory of change. |
| **Execution** | Thorough methodology, convincing validation, results that support the conclusions. "Scattered experiments that don't add up" are penalised. | **One** main question, a positive control first, one variable at a time, predeclared thresholds and decision rules, seeds plus variance plus baselines, honest nulls. |
| **Presentation** | Easy to follow, the right level of detail; "verbosity that obscures substance" is penalised. | 4–6 page main body, a contributions list, one hero figure, everything else in appendices. |

Calibration: **3 = solid weekend work**; **5 = at most the top ~5–10% per dimension**. Dimensions are scored independently. A judge can **decline to score** a report they can't follow.

## 2. Hard rules (any one can sink us)

- PDF from the official template; **≤ 8 pages** main body; abstract 150–250 words; authors and affiliations.
- The **Limitations and Dual-Use / Ethical** appendix is required, and especially sensitive for this topic.
- **Must be about AI collusion** (off-topic means disqualification). No fabricated results or references (disqualification).
- Disclose prior work (none here). At most 2 projects per person. Deadline **Mon Oct 26, 11:59 UTC**.

## 3. What the past winner did, and what to copy

*"Noticing the escapes"* (AI Incident Response Sprint, 1st place; one author plus Claude; 23 PDF pages = 8 main + references + 13 appendix pages).

**Structure:** Title, subtitle question, authors "with Claude (Anthropic)", "With Apart Research and CeSIA", Abstract → 1 Intro (with **Figure 1 on page 1**: a timeline that *is* the story) → 2 Related work (**one short page**; each prior work plus what it lacks) → 3 Methods (bold run-in paragraph heads: "The ledger.", "Latencies.", "The coverage audit.", "The control set.") → 4–6 findings sections, each **titled as the finding/question** ("Who noticed first", "Would the alarms have gone off?") → 7 Discussion (artifacts, future work, short Limitations and Dual-use paragraphs) → main ledger Table 2 → References (precise, archived URLs) → LLM Usage Statement → Appendices A–H (A = Limitations & Dual-Use in depth, plus an inter-rater check, data-quality errors, pre-registered predictions, artifacts).

**Patterns worth copying:**
1. **A real-incident hook in the first paragraph**, with concrete numbers. We have the same asset: the OpenAI/HF incident is the sprint's own stated motivation.
2. **Every number reproducible by script** from checked-in data ("A script ... recomputes every number in this paper"). Judges reward this under Execution.
3. **Honest uncertainty everywhere:** precision flags on dates, bootstrap CIs on n=4, "this does not allow us to estimate a failure rate", a second blinded reviewer with Cohen's kappa, and a *flawed first attempt* disclosed and discarded.
4. **A control set to measure selection bias**, which is the analogue of our positive and negative controls.
5. **Artifacts beyond the paper** (a proposed intake form, two detection rules, a 50-item gap list, predictions with resolution dates), which add Impact.
6. **A frank LLM usage statement** (the share of text written by AI; a hostile-critic Claude instance caught a fabricated quote), turning AI use into a credibility signal.
7. **Figures that carry the argument:** timeline, latency (log scale), coverage heat-table, signals over time. Each has a self-contained caption.
8. Dual-use is handled concretely: what is *not* published, and why the rest is safe.

## 4. Checklist this implies for our plan

- [ ] A one-sentence finding that fits in a Figure 1 caption.
- [ ] A ground-truth or control design that lets us report accuracy *and* false-positive rate, or effect sizes with CIs.
- [ ] Predeclared hypotheses and decision rules (pre-registration-lite, with a timestamped file in the repo).
- [ ] A second-rater or agreement check on any LLM-judge labels.
- [ ] A script that regenerates every table and figure from raw logs.
- [ ] An artifact others can reuse (a configurable environment, detector, rubric or dataset).
