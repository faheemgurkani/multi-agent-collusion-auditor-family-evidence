> Source: [Guidelines tab](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25#guidelines) (verbatim conversion), plus the [Apart Sprint Evaluation Rubric (Notion)](https://apartresearch.notion.site/sprint-evaluation-rubric) that the report template links to, plus the judge review form seen on past project pages. Captured 2026-10-24.

## TL;DR: dos and don'ts

**Do**
- Submit a **PDF** made from the [official template](template/) (always the Guidelines-tab one, not an older email version).
- Keep the **main body ≤ 8 pages** (references + appendices don't count; put extra tables/data in appendices). Strong projects: 4–8 pages; a focused 4-pager often beats a noisy 10-pager.
- Abstract of **150–250 words**; title; author names + affiliations.
- Include the required **"Limitations and Dual-Use / Ethical Considerations" appendix**. *The template does not contain this section, so add it yourself.*
- Methods with enough detail to replicate: models, prompts, environments, seeds, metrics.
- Results: quantitative, with **variance, seeds, baselines, and always the positive control**.
- Disclose any **pre-sprint work** explicitly (report + README). Only weekend work is judged.
- Stay on topic (AI collusion). Off-topic projects are disqualified.
- Work through the **pre-submission checklist** (bottom of Guidelines).
- Submit before the deadline. For a PDF fix, **make a new submission with a slightly different title** (the safest route) or email sprints@apartresearch.com before the deadline.

**Don't**
- Don't fabricate results or references (grounds for disqualification).
- Don't hand in an unreadable, one-prompt AI-written report. Judges may **decline to score** a report they can't follow. No AI detectors are used.
- Don't hide prior work (Apart checks online).
- Don't expect re-submitting with the *same* title to replace the PDF (it only updates form details).
- Don't join more than **2 projects per person**.
- Don't let scattered experiments or verbosity crowd out the main result (it costs Execution and Presentation points).

## Reviewer guidance (from the Notion rubric, not shown on the sprint page)

- We score along three different dimensions, from 1 (worst) to 5 (best).
- **Score dimensions independently**: a 5 on Execution isn't always a 5 on Impact or Presentation.
- For Impact & Innovation, focus on **potential impact on AI safety and security**. A quick search may help to assess novelty for areas you're less familiar with.
- **Quality over quantity**: a focused 4-page submission often beats a noisy 10-page one.
  - Verbosity that obscures substance → subtract from **Presentation**
  - Scattered experiments that don't add up → subtract from **Execution**
- **Calibration:**
  - Level 3 = solid hackathon work ← what you'd expect from a competent team in a weekend
  - Level 5 = exceptional ← we expect no more than ~5–10% of projects to reach this quality bar for any given scoring dimension

(The Notion version of Dimension 1 asks "How much would this matter **for AI safety** if it worked?", and its level 5 reads "Tackles a critical **AI safety** problem". The sprint page says "for the field". Otherwise the tables match the ones below.)

## What judges actually fill in (review form on project pages)

For each project, judges submit: a **public critique** (shown on the project page without their name), a **private critique** (Apart, and funders if the judge agrees), a 1–5 score for each of the three dimensions, and an option to **"Decline to score — I can't follow what this report did or found"**. Strong projects' reviews and scores are **shared with funders** (grantmaking.ai), and judges can **endorse** a project for funding. Projects must be public on the website to be judged.

---

# Verbatim Guidelines tab

## Guidelines

## **Judging Criteria**

## Dimension 1: Impact Potential & Innovation

*How much would this matter for the field if it worked? How innovative is it?  
For scores of 4-5: is this actually new to the field, or replicating recent work?*

| Score | Description |
| --- | --- |
| 1 | **Negligible.** No clear problem addressed, or no meaningful novelty. |
| 2 | **Limited.** Addresses a real problem but with a generic or well-trodden approach. Incremental at best. |
| 3 | **Moderate.** Clear problem with a reasonable approach; some novelty in framing or method beyond routine application of existing tools. |
| 4 | **Significant.** Important problem with an original approach, or identifies a neglected problem area. A valuable contribution others could build on. |
| 5 | **Exceptional.** Tackles a critical problem with a genuinely novel approach, or opens a new research direction. Clear theory of change. You'd be excited to share this with researchers in the area. |

## Dimension 2: Execution Quality

*How sound are methodology, implementation, and findings?*

| Score | Description |
| --- | --- |
| 1 | **Seriously flawed.** Methodology broken, results uninterpretable, or implementation doesn't work. |
| 2 | **Weak.** Approach has significant gaps: missing validation, flawed experimental design, or incomplete implementation. |
| 3 | **Competent.** Technically solid given the short duration. Methodology makes sense, results are interpretable, limitations acknowledged, work builds toward clear conclusions. |
| 4 | **Strong.** Thorough methodology with convincing validation. Results clearly support conclusions. Immediately useful for future work. |
| 5 | **Exceptional.** Ambitious scope executed rigorously. Surprising findings, novel methods, or unusually robust validation. |

## Dimension 3: Presentation & Clarity

*How clearly are work, findings, and impact potential communicated?*

| Score | Description |
| --- | --- |
| 1 | **Incomprehensible.** Cannot determine what the project is actually claiming or doing. |
| 2 | **Hard to follow.** Key information buried, missing, or diluted by excessive length. Significant effort to extract main points. |
| 3 | **Clear enough.** Can understand the problem, approach, and results without undue effort. Core content clearly present: problem, method, findings, limitations. |
| 4 | **Well presented.** Easy to follow, well-structured, appropriate level of detail. Target audience would get it quickly. |
| 5 | **Exceptionally clear.** A pleasure to read. Complex ideas made accessible. Could serve as a model for how to present this type of work. |

## Submission Requirements

**Required:**

- Research report (PDF) using the [official template](https://docs.google.com/document/d/1Y5wd3VRbXU5N08BvAGiJUQTaWbMCSPjhzXsR-ozuehg/copy?usp=sharing).
- Maximum 8 pages, not counting references and appendices.
- Project title and abstract, 150 to 250 words.
- Author names and affiliations.
- A "Limitations and Dual-Use / Ethical Considerations" appendix (required, see below).

**Optional:**

- Public GitHub repo.
- A 3 to 5 minute video demo.

## Submission Template => [Link](https://docs.google.com/document/d/1Y5wd3VRbXU5N08BvAGiJUQTaWbMCSPjhzXsR-ozuehg/copy?usp=sharing)

## Recommended Report Structure

Most strong projects are 4 to 8 pages. The cap is 8 pages, not counting references and appendices.

- **Introduction:** the question and why it matters.
- **Related Work:** what you build on (see Resources).
- **Methodology:** enough detail to replicate (models, prompts, environments, seeds, metrics).
- **Results:** quantitative where possible; report variance, seeds and baselines, and always include the positive control.
- **Discussion:** implications, limitations, and future work.
- **Limitations and Dual-Use / Ethical Considerations** (required): state what your result does and does not establish, and note any way your setup or findings could make real-world collusion easier to carry out or harder to detect.
- **References.**

## AI tools and your report

Use AI tools however they help you: to check your reasoning, find gaps in a draft, write and debug code, or help with the writing. Your team is responsible for everything in the report, and made-up results or references can disqualify a project. Judges score each report on the rubric, and a judge can decline to score one too unclear to follow.

## Important Notes

- **Solo or team:** enter solo or as a team. Teams of up to 5 are recommended; larger groups are allowed.
- **Projects:** each person can be on at most two projects.
- **Building on existing work** is allowed and encouraged, but you must clearly identify what is new work done during the sprint. Undisclosed prior work can lead to disqualification. Mark any code you wrote before the sprint as preexisting in the README and the report.
- **Fixing or resubmitting:** if a detail in the form is wrong (a missing team member, a wrong email), submit the form again with the same title and the record updates. The PDF itself is not replaced: to change it, make a new submission with a slightly different title, or email the new PDF to [sprints@apartresearch.com](mailto:sprints@apartresearch.com). Do this before the deadline. Projects go to the judges a few hours after it, and we remove the superseded entry.
- **Where to submit:** through the official submission form on the sprint page.
- **Support:** the Discord help-desk channel (tag @Support), or email [sprints@apartresearch.com](mailto:sprints@apartresearch.com).
- **Pre-submission checklist:** report PDF using the template, 8 pages or fewer before references and appendices, abstract 150 to 250 words, authors and affiliations, Limitations and Dual-Use / Ethical appendix, links work.

## **Frequently Asked Questions**

### Getting started

- **How does the sprint work?** Sign up, join the [Discord server](https://discord.gg/XswWBvugYs), form or join a team (or work solo), pick a track and a research question, build over the weekend, and submit a research report (PDF) by the deadline. Talks and Q&A run throughout.
- **How long is it?** Three days, October 23 to 25, 2026. Submissions are due end of day Sunday October 25, 11:59 PM AoE (Anywhere on Earth). The full schedule with speaker times is on the Schedule tab.
- **Can I participate remotely?** Yes. All talks, collaboration, and submissions happen online through Discord and Zoom. The in-person hubs at Collider in New York City and AI Safety Hong Kong are optional.
- **How do I join the New York City hub?** Sign up on this page and select the New York City location. Hub details (address, hours, local talks) are shared with registered participants before the sprint.
- **How do I join the Hong Kong hub?** Sign up on this page, then register for the venue on the [AI Safety Hong Kong hub page](https://www.aisafetyhk.org/apart-hackathon-hk-hub).
- **How do teams work?** Teams form before or during the sprint. Use the team-forming channels on Discord to find collaborators. Solo is fine. We recommend teams of up to 5, but larger groups are allowed.
- **Do tracks affect scoring?** All projects are scored on the same rubric. Tracks orient your project and point you to relevant resources; you compete across all submissions.
- **What background is required?** None specific. Every research question is tied to existing papers and open-source code, and the Resources tab has a practical start for each one. See "Who should join" on the Overview tab.
- **Do I need a GPU or a compute budget?** No. Every practical start on the Resources tab runs on a normal 16 GB laptop with no GPU, using low-cost API models, with a rough API budget per project.
- **Are the talks recorded?** Yes. Recordings are shared on Discord and on the Schedule tab after each talk.
- **What timezone are deadlines in?** Submissions close Sunday October 25 at 11:59 PM AoE (Anywhere on Earth).
- **Do I need to attend all three days?** No. You can work at your own pace. Talks are optional but recommended. The only hard deadline is the Sunday submission cutoff.
- **Can I participate from any country?** Yes. The sprint is open globally and runs online.

### Submissions

- **What do I submit?** A research report in PDF format using the official template. Think of it as a mini research paper documenting your problem, approach, results, and implications, not a product demo. Include the required Limitations and Dual-Use / Ethical Considerations appendix.
- **Which template should I use?** Always use the one linked on the Guidelines tab. The template in any acceptance email may be older.
- **Will I get a confirmation after submitting?** Yes. You will get a confirmation with your project title shortly after submitting. If you do not, email [sprints@apartresearch.com](mailto:sprints@apartresearch.com).
- **My project doesn't show up on the website after submitting.** Submissions are published manually and can take up to 12 hours to appear. If it is still missing after that, email [sprints@apartresearch.com](mailto:sprints@apartresearch.com).
- **I made a mistake. Can I fix it or update my PDF?** Form details (team members, emails): submit again with the same title and details, and the record updates. The PDF is not replaced: make a new submission with a slightly different title, or email the new PDF to [sprints@apartresearch.com](mailto:sprints@apartresearch.com). Do this before the deadline; projects go to the judges a few hours after it. If unsure, ask in the help-desk channel and tag @Support first.
- **Can I add team members after submitting?** Yes. Update the team list through the submission form. If you need help, ask in the help-desk channel and tag @Support.
- **Can I submit unfinished work?** Yes. Submitting something unfinished is always better than not submitting. Judges evaluate what you accomplished in the timeframe; honest limitations are welcome.
- **Can I use AI tools?** Yes: use AI tools however they help you. Your team is responsible for everything in the report, and made-up results or references can disqualify a project. Judges score each report on the rubric, and a judge can decline to score one too unclear to follow.
- **Can I build on existing research?** Yes, but you must clearly identify what is new work done during the sprint. Undisclosed prior work can lead to disqualification. Mark any code you wrote before the sprint as preexisting in the README and the report.
- **Can I submit multiple projects?** Yes, up to two per person. Each needs its own submission with a unique title. Most participants focus on one.
- **Do you require a particular citation style?** No. Use whichever style you are comfortable with and stay consistent. Judges care about the substance, not the format.

### Judging and results

- **How does judging work?** Your project is assigned to expert judges who review your PDF and score it on the rubric above. Judges typically have about a week after the event to complete reviews.
- **Are individual judge scores shared?** No. The rubric is public, but individual scores stay internal. Constructive feedback is shared with participants without reviewer names.
- **When will results be announced?** Typically 1 to 2 weeks after the judging deadline. Winners are contacted directly, and all participants receive reviewer feedback by email.
- **Top teams are fast-tracked to the Apart Fellowship. Does that mean we are guaranteed a place?** Being a top team fast-tracks your project for the fellowship, which is accelerated consideration, not an automatic place. The fellowship runs its own review, and a strong sprint result is a clear positive signal.

### Support

- Discord help-desk channel, tag @Support.
- Email: [sprints@apartresearch.com](mailto:sprints@apartresearch.com)
