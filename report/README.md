# Report drafts

**Canonical final version: [`latex/report.tex`](latex/report.tex) → `latex/report.pdf`.** It follows the past winner's format (LaTeX, GFS Didot, title and subtitle between rules, hero figure on page 1, findings sections titled as questions, references with URLs, LLM statement after the references, Appendix A = Limitations & Dual-Use). Build: `cd report/latex && xelatex report.tex && xelatex report.tex`. Figures come from `src/analysis/figures.py`. The numbered `.md` files below are the earlier section drafts and are superseded by the LaTeX.

One file per section of the [official template](../docs/sprint/template/README.md). When the drafts are done, paste them into a copy of the Google Doc and export to PDF.

**Pre-submission checklist** (from Guidelines):
- [ ] Report PDF uses the official template
- [ ] Main body ≤ 8 pages (refs + appendices excluded)
- [ ] Abstract 150–250 words
- [ ] Authors + affiliations
- [ ] Limitations and Dual-Use / Ethical appendix (`10_…`)
- [ ] All links work
- [ ] Prior work / preexisting code disclosed (report + README)
- [ ] Positive control, seeds, variance, baselines reported
- [ ] All template guidance text and the info box deleted
- [ ] After submitting: fill in the grant-making form
