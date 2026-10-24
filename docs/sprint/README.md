# AI Collusion Research Sprint: local reference

Everything from the [sprint page](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25), captured 2026-10-24, so you don't have to go back to the website.

## Key facts
- **Deadline: Sun Oct 25, 11:59 PM AoE = Mon Oct 26, 11:59 UTC.** No extensions.
- **Deliverable:** one PDF from the official template, **≤ 8 pages** main body, abstract 150–250 words, plus the **required Limitations & Dual-Use/Ethics appendix**. Only the PDF is scored.
- **Judging:** three independent 1–5 scores: **Impact & Innovation · Execution Quality · Presentation & Clarity**. A 3 is "solid weekend work"; only ~5–10% of projects get a 5 on any dimension.
- **Tracks:** (1) Markets & Collusion, RQ 1.1–1.5 · (2) Detection & Audit, RQ 2.1–2.3 + the Dolos-1.5B red-teaming challenge · (3) Carriers & Countermeasures, RQ 3.1–3.4. Tracks are inspiration only and can be combined, but the project **must be about AI collusion**.
- **Compute:** every default route runs on a 16 GB laptop with no GPU, using API models (Nebius/OpenRouter), at roughly $5–120 per project. Modal gives $50 credit each.
- **Prizes:** $1,000 / $500 / $300 / $100 / $100, a fellowship fast-track, and grant-maker exposure (fill in the grant form after submitting).

## Files
| File | Contents |
|---|---|
| [01_overview.md](01_overview.md) | Overview tab: framing, the three questions, tracks and RQs, who should join, partners |
| [02_resources.md](02_resources.md) | Resources tab: full RQs with prior results, plus a practical start for each RQ (starter code, weekend project, budget) |
| [03_guidelines_and_rubric.md](03_guidelines_and_rubric.md) | **Dos and don'ts**, Notion reviewer guidance and calibration, the judge form, then the verbatim Guidelines tab (rubric, submission requirements, recommended structure, FAQ) |
| [04_schedule.md](04_schedule.md) | Talks with recording links, hub times |
| [05_submission_and_signup_forms.md](05_submission_and_signup_forms.md) | Every field on the submission form (title, summary, PDF, publish?, tracks, optional extras, team) |
| [06_people_speakers_judges_sites.md](06_people_speakers_judges_sites.md) | Speakers, all judges and mentors (with expertise; useful for audience calibration), local sites |
| [07_partners_and_external_links.md](07_partners_and_external_links.md) | Sponsors, the OpenAI/HF incident, ABA "plus factors" article, Dolos details, prize terms, all repo links |
| [08_logistics_talk_notes.md](08_logistics_talk_notes.md) | Extra rules and tips from the logistics talk |
| [template/](template/README.md) | Official template (.docx/.pdf/.md) and **where it disagrees with the Guidelines** |
| [papers/](papers/README.md) | 28 PDFs, sorted by track (one folder per track) and indexed by RQ |
| [examples/](examples/) | A past first-place report (AI Incident Response Sprint) to show the bar |
| [`../../starter/collusion_hackathon/`](../../starter/collusion_hackathon/README.md) | Official starter repo (shallow clone): 10 codebases plus Dolos, a ~230-paper reading list, and a collusion-definitions survey |
| [`../../report/`](../../report/README.md) | Our report drafts, one `.md` per template section, plus the pre-submission checklist |

## Takeaways for scoring well (from the rubric, guidelines and talk)
1. **Pick one sharp question and one clean experiment.** Scattered experiments lose Execution points. Focus beats breadth.
2. **Positive control first** (reproduce the known collusion condition), then vary **one factor**. Report seeds, variance and baselines. The Resources tab recommends 3–5 seeds per condition, expanding to 10–20 only once the positive control works.
3. **Novelty matters for 4–5 on Impact.** Each RQ notes what *hasn't* been tested yet (e.g. replacement studies in 1.2, a trusted agent offering collusion in 3.2, mid-run peer swaps in 3.3, partial-monitoring budgets in 3.4). Aim there.
4. **Decide early which definition of collusion you're studying** (`starter/.../literature/definitions/`). It determines what counts as evidence. For 2.3, the antitrust "plus factors" give a ready-made framework.
5. **Clarity:** main body of 4–6 tight pages, a clear contributions list, at least one strong numbered figure, everything else in appendices. Write it ourselves (with AI help) and have someone read it before submitting.
6. **Disclose and be honest:** limitations, dual-use, preexisting work, and an LLM usage statement.
