# Official report template

Downloaded 2026-10-24 from the Google Doc linked on the Guidelines tab ([make-a-copy link](https://docs.google.com/document/d/1Y5wd3VRbXU5N08BvAGiJUQTaWbMCSPjhzXsR-ozuehg/copy?usp=sharing)).

- `apart_report_template.docx`: editable Word export, **with the required "Limitations and Dual-Use / Ethical Considerations" appendix added** (before "LLM Usage Statement")
- `apart_report_template.md`: Markdown export, with the same appendix added
- `apart_report_template.original.docx` / `.original.pdf`: unmodified Google Docs exports, for reference

> When you make your own copy of the Google Doc, it will **not** have the new appendix. Add a Heading 2 "Appendix: Limitations and Dual-Use / Ethical Considerations" before "LLM Usage Statement", or paste from `report/10_limitations_dual_use_ethics_appendix.md`.

**Final workflow:** draft sections as `.md` in [`../../../report/`](../../../report/), then copy them into your own copy of the Google Doc (make-a-copy link above) and export to PDF.

## Template structure

1. Title block: PROJECT TITLE (footnote: "Research conducted at the AI Collusion Research Sprint, October 2026"), up to 6 authors with affiliations, "With Apart Research", **Abstract (150–250 words)**
2. Info box (delete before submitting)
3. **1. Introduction**: problem, why it matters, threat model; a **"Our main contributions are:"** numbered list
4. **2. Related Work**: closest work and the gap; when someone would use your method; what new insight it gives
5. **3. Methods**: enough to replicate; justify design choices (cite prior work); what didn't work
6. **4. Results**: at least one figure strongly encouraged; separate observations from interpretations; significance and robustness. Number the figures and tables, give them self-contained captions, and keep text legible.
7. **5. Discussion and Limitations**, with subsections **Limitations** (state assumptions and how conclusions change if they fail) and **Future Work**
8. **6. Conclusion** (1–2 paragraphs)
9. **Code and Data** (repo, data, other artifacts; note any info hazards)
10. **Author Contributions** (optional)
11. **References** (consistent format: authors, year, title, venue, URL/DOI)
12. **Appendix** (optional)
13. **Appendix: Limitations and Dual-Use / Ethical Considerations** (required by Guidelines; *added by us*, not in the original template)
14. **LLM Usage Statement** (how LLMs were used; all claims verified; "strongly encourage that the final version… is primarily written by your team")

## ⚠️ Where the template and the Guidelines tab disagree

| Topic | Template says | Guidelines tab says | Do this |
|---|---|---|---|
| Length | "Recommended length: 4 pages excluding references and appendix" (Intro + Related Work 1p, Methods + Results 2.5p, Discussion 0.5p) | 4–8 pages typical; **hard cap 8** excluding references and appendices | Aim for ~4–6 focused pages; never more than 8 |
| Limitations & Dual-Use | Only a "Limitations" subsection | **Required appendix: "Limitations and Dual-Use / Ethical Considerations"**: what the result does and doesn't establish, and whether the setup or findings could make real collusion easier to carry out or harder to detect | ✅ Added to the local `.docx`/`.md` and `report/10_…`; also add it to the Google Doc copy |
| Results | Figures, significance, robustness | Also report **variance, seeds, baselines, and always the positive control** | Include all of them |
| Rubric link | Notion "sprint-evaluation-rubric" | Same three dimensions shown inline | See [../03_guidelines_and_rubric.md](../03_guidelines_and_rubric.md) |
