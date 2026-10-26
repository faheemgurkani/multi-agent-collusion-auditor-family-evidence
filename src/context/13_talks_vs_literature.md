# 13: Talks re-read against the literature review: agreements, conflicts, new ideas

Done 2026-10-25. All 7 shortlisted talks were re-read in full (`docs/misc./transcripts/01`–`08`, excluding Logistics) and compared with the 2024–26 literature in [12](12_novelty_and_literature_review.md). Items the talks raised that our research had missed were checked online, and the relevant papers downloaded to `docs/sprint/papers/_all/` (linked in `proposal_core/`). Matthew Lee's talk is still pending (recording posted, transcript not yet downloaded).

## 1. Talk by talk: what each says, and how it squares with the literature

| Talk | Claims relevant to our proposal | Agrees with | Conflicts with / nuance | Idea it gives us |
|---|---|---|---|---|
| **06 Nakamura & Bagdasarian** (Colosseum) | LLM judge alone is insufficient and "can definitely be fooled"; action metrics are needed. Collusion types: direct / attempted ("on paper") / hidden. Emergent collusion at λ=0 when two benign agents get a private channel. Use JiraTicket or meeting scheduling. A mitigation-vs-performance trade-off is an open weekend project | ORBIT (per-action defences fail vs colluders), NARCBench (2/229 episodes verbalised), Lee & Park (CoT faithfulness ≠ collusion) | Their judge model is **fixed**; judge identity is never varied (our gap) | **Break detection down by collusion type** (direct / attempted / hidden). Report the auditors' safety–cost trade-off |
| **08 Nguyen** (overview) | Lists as missing: "What if the LLM doing the monitoring shares a colluder's model?" Suggests testing whether narrow-question monitors stay honest within the same family. Rules: freeze the monitor; report FPR and TPR at 1/5% FPR and AUROC; hard negatives; computed signals; multiple providers. Say-vs-do cuts both ways | Calls for exactly our study | **Partly out of date:** Pinto 2026 (trained monitors) and Gardner-Challis 2026 (elicited self-recognition) now measure related effects. **Prompted, multi-agent auditing is still unmeasured** | A **structured multi-question auditor** as a mitigation (her TraceGuard idea). Yang 2026 independently finds structured multi-dimensional judging cuts self-preference by 31.5% |
| **03 Kemeklis** (AI control) | Clones coordinate acausally via shared priors and Schelling points, so trusted monitors use a **different base model**. "If one copy monitors another, they may collude." Paraphrasing and redaction are the mitigations. Frame results on a safety–usefulness Pareto frontier | Greenblatt 2024; Shlegeris 2024; Gardner-Challis 2026 (passive self-recognition); Järviniemi 2025 (focal points) | On **paraphrasing**, Mahbub 2025 finds full style neutralisation *recovers* self-preference; Gardner-Challis finds **summarisation** the best defence but insufficient alone. Järviniemi: focal-point collusion between copies succeeded only 31/3,903 times (Claude 3.7), so acausal collusion is *possible but rare* | Report H4 as a **Pareto plot** (detection gain vs auditing cost). Prefer **summarisation / structured report** over paraphrase |
| **05 Anwar** (steganography detection) | Each LLM has its own cover distribution. Detection is defined relative to a **trusted sentinel**. Naive LLM suspicion judges are a weak baseline | Wataoka 2024 (bias tracks perplexity and familiarity); Barkhordar 2026 (surface cues drive self-attribution) | The sentinel view implies a same-family judge might *decode* its family better (familiarity advantage, as in Pinto) **or** find its family's text *unremarkable* (leniency). This is exactly our two-sided H2 | The **channel mechanism test (H3)**: the family effect should shrink when style is removed (actions-only view or a neutral summary) |
| **07 Shi** (deception) | Deception needs divergence plus functional intent. Effects are **model × game dependent**; no model dominates. Stand out by changing an unusual variable and tying it to real-world risk, with a one-step mitigation firms could adopt | Awuni 2026 (family effects vary 3.4–8.4 pt by family) | Warns against generalising from one family pairing | Report **per-cell** effects (3×3 matrix), not only a pooled number. Our variable is the **auditor's identity**. End with a deployable rule ("audit with a different family; use a structured report") |
| **01 Velja** (steganography retrospective) | Threat model 4: **agent and monitor collude**. Hidden encodings arise first within one model, then **between copies of the same weights** (shared priors, zero-shot Schelling), then across models. **Failed attempts are the signal**: OpenAI's DNS monitor read failed attempts as "nothing happened". Proposes an untested side-channel vs monitored-channel route experiment. Pareto frontier as evidence that a defence works | Motwani 2024; Järviniemi 2025; Kaur 2026 (same-model teams easier to detect: AUROC 0.993 vs 0.854 mixed) | Same-weights advantage is shown for *colluders*; whether it transfers to a same-weights *auditor* is untested (our H2) | Score **attempted (unsuccessful) collusion as a positive**, and check whether auditors under-flag it. The route experiment goes to future work (RQ 3.1) |
| **02 Motwani** (secret collusion) | Collusion = deviation from the designer's rules (secrecy not required). Same-weights steganography is easier. In their setup the **overseer was the same family** as the communicators, and "**models become much better at colluding than at oversight**" as capability grows (generation–verification gap). Sceptical of paraphrasing; wants a weekend test of it | Goel 2025 (correlated failures grow with capability); Engels 2025 (oversight success falls as the capability gap widens) | They didn't separate *family* from *capability*. In our lineup the families also differ in capability, so this **confound must be controlled** | Add a **capability / competence covariate** (each auditor's overall AUROC and accuracy on negatives) so the family interaction isn't a capability artefact |

## 2. Where the talks and the literature agree, and where they disagree

**Agree:**
- Transcript-only LLM judging is fragile; actions and outcomes matter (Nakamura, Nguyen ↔ ORBIT, NARCBench, Lee & Park, Arike).
- Same-weights agents share priors, which makes coordination and recognition easier (Velja, Motwani, Kemeklis ↔ Panickssery, Järviniemi, Gardner-Challis, Kaur).
- The auditor's trustworthiness is the weak assumption (Nguyen, Kemeklis, Velja ↔ Goel, Li, Awuni).

**Disagree or nuance:**
- *Paraphrasing:* talks recommend it (Kemeklis) or doubt it (Motwani). The literature shows light perturbation helps but full neutralisation backfires (Mahbub), and summarisation is best but insufficient (Gardner-Challis). **Decision: test summarisation / structured report, not paraphrase.**
- *Direction of the same-family effect:* the talks implicitly assume **leniency** (collusion with the auditor). The literature shows both leniency (quality judging) and **advantage** (trained monitors, Pinto). **Decision: two-sided H2.**
- *"Unmeasured":* Nguyen's gap statement predates Pinto and Gardner-Challis. **Our claim is narrowed to prompted auditors × multi-agent collusion × action ground truth.**

## 3. Overlooked items, verified online

| Raised in talk | Verification | Paper (downloaded) | Effect on our plan |
|---|---|---|---|
| Acausal / focal-point collusion between copies (Kemeklis, Velja, Motwani) | Real but rare: 31/3,903 successes for Claude 3.7 in a policy–monitor code task | Järviniemi 2025, *Subversion via Focal Points*, arXiv:2507.03010 (P) | Supports treating same-family leniency as plausible but not assured |
| Oversight degrades with the capability gap (Motwani) | Formal scaling laws; nested-oversight success 9–52% at a 400 Elo gap | Engels et al. 2025, *Scaling Laws For Scalable Oversight*, **NeurIPS 2025**, arXiv:2504.18530 | **Control for capability**; report each auditor's competence |
| Summarisation vs paraphrase as a defence (Kemeklis, Motwani) | Summarisation is the best signal-jamming defence vs passive self-recognition but insufficient alone; it sometimes summarises away the attack | Gardner-Challis 2026 (already local); Mahbub 2025 (already local) | Use a **neutral-family structured summary** as the mitigation view |
| Same-model vs mixed teams (Velja) | Detection AUROC 0.993 for homogeneous vs 0.854 for heterogeneous agent teams (latent-channel monitor) | Kaur et al. 2026, *Beyond the Transcript*, arXiv:2608.19161 (P) | Motivates a **mixed-family coalition** stretch condition |
| Information access for monitors (Nguyen) | "Less is more": a CoT-only monitor often beats CoT plus actions; extract-and-evaluate +16.8 pt | Arike 2026 (already local) | Keep our view comparison **two-sided** too; actions may *hurt* (post-hoc justification) |

## 4. Candidate additions to the proposal, ranked by value per cost

| # | Addition | Source | Cost | Recommendation |
|---|---|---|---|---|
| A | **Structured-report view:** a neutral-family model summarises "claims vs outcomes"; the auditor reads only that. It is both the 4th view for H1 (the Resources-tab 2.2 suggestion) and the style-stripping **mitigation** for H4 | Resources 2.2; Nguyen; Gardner-Challis; Arike (extract-and-evaluate); Yang (structured, −31.5% SPB) | +1 summary call per transcript | **Add (core)** |
| B | **Detection by collusion type:** direct / attempted / hidden (from coalition advantage × instruction), and whether the family effect differs by type | Nakamura; Velja ("failed attempts are the signal") | Analysis only | **Add (core)** |
| C | **Capability / competence covariate** for each auditor (overall AUROC, accuracy on negatives), included in the interaction model | Motwani; Engels 2025; Goel 2025; Roytburg 2026 | Analysis only | **Add (core)** |
| D | **Self-recognition probe:** "which family produced these agents?", correlated with the per-cell effect | Panickssery; Barkhordar; Gardner-Challis | +1 call per transcript per auditor | **Add (cheap)** |
| E | **Pareto reporting** of mitigations (detection gain vs extra calls and cost) | Kemeklis; Velja; Nakamura | Analysis only | **Add** |
| F | **Mixed-family coalition** (the colluding pair from two different families) | Velja; Kaur 2026 | New runs; needs a check that Colosseum supports per-agent models | **Stretch** |
| G | Paraphrase arm | Kemeklis; Motwani | +1 call per transcript | **Drop to future work** (Mahbub backfire; A covers the style-removal question) |
| H | Side-channel vs monitored-channel route choice | Velja | New environment | **Future work** |

## 5. Resulting proposed framing (incremental to 12)

- **H1 (views):** messages / actions / both / **structured report**. Tested two-sided, given Arike's less-is-more result.
- **H2 (family effect, two-sided):** leniency (H2-L) vs familiarity advantage (H2-F), *controlling for auditor competence* (C).
- **H3 (mechanism):** the family effect shrinks in the actions-only and structured-report views (style removed).
- **H4 (mitigation):** cross-family auditing and the structured report reduce the family gap at modest cost, shown on a Pareto plot (E).
- **Exploratory:**
  - E1: family effect by collusion type (B);
  - E2: self-recognition accuracy vs effect size (D);
  - E3 (stretch): mixed-family coalitions (F).

## 6. Sources (talk-derived additions)

- Järviniemi, O. (2025). Subversion via Focal Points: Investigating Collusion in LLM Monitoring. arXiv:2507.03010. https://arxiv.org/pdf/2507.03010
- Engels, J., Baek, D. D., Kantamneni, S., & Tegmark, M. (2025). Scaling Laws For Scalable Oversight. *NeurIPS 2025*. arXiv:2504.18530. https://arxiv.org/pdf/2504.18530
- Kaur, R., Chari, P., & Raskar, R. (2026). Beyond the Transcript: Detecting Covert Coordination in Latent Multi-Agent Communication. arXiv:2608.19161. https://arxiv.org/pdf/2608.19161
- Gardner-Challis et al. (2026), Mahbub et al. (2025), Arike et al. (2026), Yang et al. (2026): see [12](12_novelty_and_literature_review.md).
