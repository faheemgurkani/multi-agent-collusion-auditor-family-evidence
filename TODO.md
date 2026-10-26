# Sprint TODO: AI Collusion Research Sprint

**Hard deadline: Sun Oct 25, 11:59 PM AoE = Mon Oct 26, 11:59 UTC.** No extensions. Projects go to the judges a few hours after the deadline.

Source tags: **[G]** Guidelines tab · **[O]** Overview tab · **[R]** Resources tab · **[S]** Schedule tab · **[L]** Logistics talk · **[T]** report template · **[N]** Notion reviewer rubric. Full details are in `[docs/sprint/](docs/sprint/README.md)`.

---

## 0. Admin and setup (do first)

- [x] Fill in the **pre-sprint survey** (marks us as active participants; required separately for every sprint): [https://apartresearch.notion.site/2b0fcfd1de9d8080ac3ac4c41a78c8f8](https://apartresearch.notion.site/2b0fcfd1de9d8080ac3ac4c41a78c8f8) [L]
- [x] Join **Discord** ([discord.gg/XswWBvugYs](https://discord.gg/XswWBvugYs); if it fails, try `discord.gg/2Sr8GyW3k`, an incognito window or your phone) [G][L]
  - [x] Questions go to **#help-desk, tagging @Support**. Don't DM the organizers. [G][L]
  - [x] Optional: post the project or look for teammates in the **projects-and-teams** forum [L]
- [x] Decide the team: solo is fine; 1–3 people tend to do best; up to 5 is recommended. No team registration is needed, since members are just listed on the submission form. [G][L]
- [x] Respect the limit of **at most 2 projects per person**, and focus on **one** project. [G][L]
- [x] Claim **Modal credits: $50 per person**. Signup needs an active card, which isn't charged. [O][L]
  - Account with the credits: muhammadfaheem.mansha@gmail.com. Modal CLI 1.6.2 is installed (`uv tool install modal`, at `~/.local/bin/modal`), and the **active profile is now `muhammadfaheem-mansha`** (workspace `muhammadfaheem-mansha`, environment `main`). See [`docs/compute/MODAL.md`](docs/compute/MODAL.md).
- [x] Get an inference key, `NEBIUS_API_KEY` **or** `OPENROUTER_API_KEY` (OpenRouter also covers GPT, Gemini and Claude). Event keys come via Slack or Luma, per the starter README. [R]
  - `OPENROUTER_API_KEY` is in the project-root `.env`. The starter repo reads `starter/collusion_hackathon/compute.env` instead, so copy or symlink it there before running (see MODAL.md §2).
- [x] Note the starting point: **no prior work** (we began at the sprint). Still say so explicitly in the report and the repo README. [G][L]

## 1. Context to absorb

Findings are in [`src/context/`](src/context/README.md). Scope: **Tracks 2 + 3**.

- [x] Read the full research questions plus each one's practical start: `[docs/sprint/02_resources.md](docs/sprint/02_resources.md)` [R]. See `src/context/02_*`.
- [x] Read the rubric, the reviewer guidance and the dos and don'ts: `[docs/sprint/03_guidelines_and_rubric.md](docs/sprint/03_guidelines_and_rubric.md)` [G][N]. See `src/context/01_*`.
- [x] Skim a **past winning report** to calibrate the bar (~8 pages with a table, plus appendices): `[docs/sprint/examples/](docs/sprint/examples/)` [L]. See `src/context/01_*` §3.
- [x] Shortlist the important talks (`src/context/04_*`).
- [x] Categorise transcripts into per-talk folders; study the shortlisted ones fully (Nakamura, Nguyen, Anwar, Kemeklis, Shi) and skim Velja and Motwani. See `src/context/08_*`. Matthew Lee's "Defining AI Collusion" recording is **not yet available**; add it when posted.
- [ ] Talks [S]:
  - [ ] Watch the recording of Khanh Linh Nguyen's overview of AI collusion research and the most useful topics for the sprint (Sat 8:15am ET)
  - [ ] Attend Matthew Lee's **"Defining AI Collusion"** (Sat 2:00pm ET / 18:00 UTC, streamed on Zoom; [RSVP](https://luma.com/ai-collusion-research-sprint-matthew-lee)), or watch the recording later
  - [x] Optional: earlier talk recordings relevant to the chosen research question (steganography: Velja, Motwani, Anwar; Colosseum: Bagdasarian and Nakamura; trust-breaking: Shi; AI control: Kemeklis). Studied via transcripts; see `src/context/08_*`.
- [x] Skim the **collusion-definitions survey**: `starter/collusion_hackathon/literature/definitions/README.md` [R]. See `src/context/05_*`.

## 2. Choose the project

- [x] Tracks chosen: **2 and 3** (merge or shortlist their RQs). Preliminary shortlist is in `src/context/07_*`.
- [x] **Later:** revisit Track 1. Add a Track 1 RQ only if it is realistically supportable in the time left and adds impact or novelty to the Track 2/3 story. **Done: none added for now** (1.3 is cited as the action-side analogue; reconsider only if the core experiment finishes early). See `src/context/09_*` §1.

- [x] Pick **one sharp research question**. Tracks are inspiration only and can be combined. [O][L] **Chosen: same-family leniency in LLM collusion auditors (Track 2.3 + 2.2, plus a Track 3 countermeasure).** See `src/context/09_*` §2.
- [x] Check it is **about AI collusion** (off-topic projects are disqualified). [L] Yes: it audits multi-agent collusion, and the threat is monitor–agent collusion.
- [x] Aim for novelty, which is needed for a 4 or 5 on Impact. Start from the **gaps the website names** [R][N]. Targets 2.2 and 2.3, plus the same-family-monitor gap named by 5 speakers and the definitions survey:
  - 1.2: no replacement study exists yet in which newcomer models re-engage in collusion
  - 1.3: detection without a communication channel (Schelling salience across providers); anti-examples
  - 1.4: pairwise net influence has never been applied to LLM agents
  - 1.5: comparing several levers on cost versus collusion removed
  - 2.1: tasks outside markets that produce collusion
  - 2.2: hybrid word/action consistency checks across agents
  - 2.3: operationalizing antitrust "plus factors" for agents
  - 3.2: a trusted agent that offers to collude has never been tested
  - 3.3: removing a feature mid-run, or swapping a peer mid-run
  - 3.4: multiple agents under a partial monitoring budget
  - Dolos-1.5B: find the behaviour, explain it, and audit it without a reference model
- [x] **Decide which definition of collusion** we study, since it determines what counts as evidence. [R] The survey's minimal cluster-B definition, operationalised with Colosseum's Δ-collusion. See `src/context/09_*` §3.
- [x] Write a one-paragraph plan covering: hypothesis, positive control, the **single variable** we manipulate, metrics, seeds, budget, and what result would count as success or failure. [R][G] See `src/context/09_*` §4.
- [x] Check feasibility against the Resources tab's setup risk, number of calls and budget ($5–$120 typical; 16 GB laptop, no GPU). [R] About $10–40 at live OpenRouter prices. See `src/context/09_*` §5.
- [x] **Next:** write the full methodology and evaluation framework in `src/plan/` and freeze the auditor prompt before any test data is seen. **Done:** `src/plan/methodology.md` plus `src/plan/frozen/`, frozen 2026-10-25T11:20:43Z (see `src/plan/FREEZE.md`).

## 3. Build and run the experiment

- [x] Clone and set up the starter repo (`starter/collusion_hackathon/`): `cp compute.env.example compute.env`, then `./setup.sh <project>`. Docker is needed only for trace-guard. [R]
- [x] **Run the positive control first**: reproduce the known collusion condition before changing anything. [R][G] G1 run on 24 family-seed pairs: fails narrowly (CI [−0.11, 7.83]); pre-registered consequence applied.
- [x] Start with **3–5 seeds per condition**; expand to 10–20 only after the positive control works. [R]
- [x] Change **one factor at a time**, holding everything else fixed (economics, task, model, seed). [R]
- [x] **Predeclare and freeze** thresholds, the monitor prompt and the decision rules before evaluating (e.g. pick the rule on half the data, test on the other half). [R] See `src/plan/` (gates G1/G2, analysis §6).
- [x] Measure both **collusion outcomes and legitimate performance or false-positive rate**, not just "high prices". [R]
- [x] Log everything needed to replicate: models and versions, providers, prompts, environment configs, seeds, metrics, run counts, cost. [G][T]
- [x] Compute **variance and confidence intervals**, compare against baselines, and run a significance test where it makes sense. [G][T]
- [x] Record what **didn't work**; the Methods section asks for it. [T]
- [x] Keep notes on dual-use risks as they come up (covert channels, monitor-evasion tricks), for the required appendix. [G]
- [x] Track API spend against the budget. See the `src/EXPERIMENT_LOG.md` spend tracker (OpenRouter $7.70 left of $10.92; Modal within the $70 credit).

Results: `src/results/main/` (results.json, tables, figures); summary in `src/EXPERIMENT_LOG.md` → "Final confirmatory results".

## 4. Write the report (the only thing judged)

Drafts are in `[report/](report/README.md)`, one `.md` file per section. The template is in `[docs/sprint/template/](docs/sprint/template/README.md)`.

- [x] **Title** (with the footnote "Research conducted at the AI Collusion Research Sprint, October 2026") [T][G]
- [x] **Author names and affiliations**: Muhammad Faheem, Independent researcher; With Apart Research, Poseidon Research and AE Studio (template line: "With Apart Research") [G][T]
- [x] **Abstract of 150–250 words** covering problem, approach, key results and takeaway. Write it last. [G][T]
- [x] **1. Introduction**: the question, why it matters, the threat model, and an explicit **"Our main contributions are:"** list [G][T]
- [x] **2. Related Work**: what we build on (cite the Resources papers) and the gap [G][T]
- [x] **3. Methods**: enough detail to replicate (models, prompts, environments, seeds, metrics); justify design choices [G][T]
- [x] **4. Results**: quantitative, with variance, seeds and baselines, **always including the positive control**, and **at least one figure**. Number the figures and tables, give them self-contained captions and legible text, and keep observations separate from interpretation. [G][T]
- [x] **5. Discussion and Limitations** (+ Future Work), stating assumptions and how conclusions change if they fail [G][T]
- [x] **6. Conclusion** (1–2 paragraphs) [T]
- [x] **Code and Data** links: github.com/faheemgurkani/multi-agent-collusion-auditor-family-evidence (**push `src/`, `report/` right after the deadline**; they are currently gitignored); note any info hazards [T]
- [x] Author Contributions (optional) [T]
- [x] **References**: consistent style, and **every one verified** (made-up references can disqualify) [G][T]
- [x] Appendix: extra tables, data and prompts (doesn't count toward the page limit) [G][L]
- [x] **Required appendix: Limitations and Dual-Use / Ethical Considerations**, covering what the result does and doesn't establish, and how the work could make real collusion easier to carry out or harder to detect [G][L]
- [x] **LLM Usage Statement** (drafted; revise in your own words, since Guidelines want team-written text): the team writes the text; AI-assisted, with every claim verified [T][G][L]

### Report quality gates

- [x] **Main body ≤ 8 pages**: `report/latex/report.pdf`, main body ends on p. 8, References start p. 9 (aim for 4–6 focused pages; references and appendices excluded) [G][L][N]
- [x] Main claims stated plainly, with no overclaiming; scattered side experiments cut or moved to appendices [N]
- [x] Self-score honestly against all three rubric dimensions (Impact & Innovation, Execution, Presentation; 3 = solid weekend work) [G][N]
- [x] (Claude full read-through done; **you should still read it once**) Someone reads it start to finish: could a judge follow it? A judge can decline to score an unclear report. [G][L]
- [x] **Delete all template guidance text and the info box** (LaTeX version has none) [T]
- [x] Prior work disclosure statement included ("no prior work") [G][L]
- [x] Every link works (21/21 URLs return 200; arXiv titles match) [G]
- [x] ~~Google Doc~~ Replaced by LaTeX that reproduces the template's title block (as the past winner did). Submission file: `report/Penstronus_Who_audits_the_auditors.pdf`

## 5. Optional extras (not scored, but help others and grant makers)

- [ ] Public **GitHub repo**: README with run instructions; mark any pre-existing code; no secrets in `compute.env` [G]
- [ ] **3–5 minute video demo** [G]
- [ ] Slides or a project image for the submission form [form]

## 6. Submit

- [ ] Run the **pre-submission checklist**: template PDF · ≤ 8 pages before references and appendices · abstract 150–250 words · authors and affiliations · Limitations & Dual-Use appendix · links work [G]
- [ ] Fill in the **submission form** ("Submit your project" on the sprint page). Field list: `[docs/sprint/05_submission_and_signup_forms.md](docs/sprint/05_submission_and_signup_forms.md)` [G][L]
  - [ ] Project title · Project summary (short abstract) · PDF report (≤ 25 MB)
  - [ ] "Interested in publishing?" Yes/No
  - [ ] Tracks: tick **every** track the project fits
  - [ ] Optional: presentation recording, code link, slides, image, additional material
  - [ ] Team name, location; for each member: name, email, Discord, Google Scholar
  - [ ] Accept the prize terms
- [ ] Fill in the **grant-making form** that appears after submitting [L]
- [ ] **Submit early**, with buffer before the deadline. To change the PDF, make a **new submission with a slightly different title** (or email [sprints@apartresearch.com](mailto:sprints@apartresearch.com)), before the deadline. Resubmitting with the same title only updates form details. [G][L]
- [ ] Check the **confirmation email**; the project should appear on the site within ~12 hours (email if it doesn't) [G]

## 7. After the sprint

- [ ] Watch for results: 1–2 weeks after judging per the website, 2–4 weeks per the talk. Reviewer feedback arrives by email. [O][G][L]
- [ ] If we win: return the prize form **within 1 week**, answer within 1 month, and make sure bank or SWIFT details work (payment comes from Mercury; prizes are split equally across the team) [prize terms]
- [ ] If invited (~80–100 projects): apply to the Apart Studio / Fellowship (remote and funded) [O][L]
- [ ] Optional: share the write-up on LessWrong or the Alignment Forum [O]
