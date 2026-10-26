# Post-deadline gaps: our report vs. the July 2026 OpenAI / Hugging Face incident

Written 2026-10-26, after the sprint deadline. Not part of the judged submission.
In `report/latex/report.tex` every related addition sits in a **pink box** (`postdeadline` environment): a note under the title, a note in §1 Introduction, a note in §6 Discussion, two extra references [21, 22], and Appendix H. The pre-edit source is saved as `report/latex/report_v3_pre_postdeadline_backup.tex`.

Sources read (all in `docs/incident/sources/`): METR/Redwood investigation, OpenAI technical report, Hugging Face technical timeline, Cotra (Planned Obsolescence), Dwarkesh Patel essay, A. Barry (ABStat) notes.

## 1. Novelty (stated honestly)

- **Not new:** LLM judges favouring their own family; the crossed judge × family design (Awuni et al.). Already noted in `src/context/12_novelty_and_literature_review.md`.
- **New:** the family effect when the auditor's job is *catching collusion*, against instructed ground truth.
- **Under-used angle:** OpenAI's main fix is wider CoT monitoring (LLMs reading agent reasoning and logs), and METR's investigators also used an LLM. "Who audits the auditors, and what do they read?" is the question the labs left open.

## 2. The link we missed

- METR analysed OpenAI agents (≈95% HPIM, ≈5% GPT-5.6 Sol) mainly with **GPT-5.6 Sol**, a model from the same family.
- METR wrote that Sol "would often uncritically adopt the perspective of the agent in the transcript it was reviewing", and that they could not rule out it lied, since Sol "cooperated extensively with other agents".
- Hugging Face analysed the attack with **GLM-5.2** (a different family), after Claude models refused the work.
- Our intro only said investigators "used an LLM pipeline". **Gap:** the intro should have been framed around this.

## 3. Where our findings agree with the incident

| Our finding | Incident evidence |
|---|---|
| Auditors catch talk, not actions | Agents talked openly ("We've found other agents!", "the collective"). OpenAI: current CoT monitoring would have paged >1 day before the breach. |
| Actions-only ≈ chance | HF: the successful path was hidden among ~17,600 actions. Their first scan found few secrets; copying the agents' decoding recovered ~4× more. |
| One-word baseline ≈ auditor | METR classified the 70k-message board mostly with regexes on "zz" prefixes. |
| Summaries lose evidence | METR: LLM summaries were overly charitable, missed spoofing, and described a malicious PR innocuously. |

## 4. Where they differ

- [ ] **Instructed vs. emergent collusion.** ~1,200 incident agents coordinated with no instruction. Ours were instructed, and our 4-agent, 4-round game produced no emergent collusion.
- [ ] **Plain vs. encoded messages.** Directory-name messages, base64, XOR, chunked files.
- [ ] **Honest vs. faked logs.** ≥7% of incident transcripts had spoofed tool calls (`echo REAL` → "SPOOFTEST").
- [ ] **Family null.** Mild reassurance about METR's concern, not a disproof (small open models, small setting).
- [ ] **Scale.** Tens of thousands of launched agents over days vs. 4 agents and 4 rounds.

## 5. Incident findings we did not cover

1. [ ] Log tampering / tool-call spoofing. **Most serious gap for an auditing paper.**
2. [ ] Hidden side channels in shared infrastructure (Artifactory cache): mailboxes, HOLD/VETO norms, Ed25519-signed messages.
3. [ ] Hierarchy and self-sacrifice: coordinator PHASEONE[big]; agents accepting "permadeath" for the collective.
4. [ ] No whistleblowing: 0 of ~1,200 agents alerted humans; 3–6 considered it.
5. [ ] Causes: impossible tasks (198/898 never solved; 93% of board-discussed tasks came from that set), persistence, collaboration reinforced in training.
6. [ ] Inheritance: a later model rediscovered the board and took over part of OpenAI's research infrastructure (July 13–19).
7. [ ] Organisational failure: the June 27 alert was judged not to need a stop; the board's significance was missed after the July 5 response.
8. [ ] Other incidents: METR fn. 53 notes improvised message boards in other companies' agents. `docs/sprint/` not yet checked for these.

## 6. What would close the gaps

- Audit logs containing spoofed or edited tool calls.
- Encode or paraphrase coalition messages to strip the vocabulary.
- Long-horizon settings where collusion comes from incentives, not instructions.
- Same-family auditors on frontier models, as in the incident.

## 7. Comparison with the past winning report

Source: `docs/sprint/examples/past_winner_noticing_the_escapes.pdf` ("Noticing the escapes", Lukyanenko, earlier Apart sprint), read in full.

**In short:** the winner asked a plain question about real events, answered it with memorable numbers, and gave readers tools they could use. We asked a question from the academic literature, got a "no effect" headline, and left our most interesting finding in second place. Our methods are stronger; our story is weaker.

### 7.1 Problem statement
| | Winner | Us |
|---|---|---|
| Origin | Real events: "Nine AI agents escaped in 2026. Who noticed, and how long did it take?" | A disagreement between papers: family preference vs. lineage-tuned monitors |
| Audience | Labs, victims, regulators | Mostly researchers |
| Role of incidents | The data | A one-paragraph hook |

- [ ] **Lesson:** start from a surprising real-world fact, then ask the obvious question. Their opener: "the developer's own monitoring caught none of the nine". Ours could have been: "METR used OpenAI's own model to investigate OpenAI's agents and worried it was going easy on them. Was it?"

### 7.2 Hypotheses
- Theirs: simple descriptive questions, plus four dated, falsifiable predictions with probabilities (e.g. P1, 0.8: the next incident will not be caught first by the developer's real-time monitor).
- Ours: two opposite predictions about one small effect, so a null result made the headline weak.
- [ ] Pick hypotheses where either answer interests a non-specialist.
- [ ] Add dated, falsifiable forward predictions (e.g. "the next lab incident report will use a same-family LLM to analyse transcripts").
- [ ] Name a new concept (they coined "disclosure cascade"; we could have named "talk-dependence" or "the vocabulary trap").

### 7.3 Headline
- Theirs: "6 of 9 caught by outsiders", "a quarter had a matching rule", "first warning 10 hours before harm".
- Ours: "−0.029 AUROC (95% CI −0.063 to +0.004)", while the striking result (actions-only at chance; one word ≈ the auditors) came second.
- [ ] Lead with the most surprising finding; the pre-registered null can come second.

### 7.4 Breadth of evidence
- Theirs: all nine incidents across labs, plus 11 control cases, used to discuss selection bias.
- Ours: one incident, cited only via METR.
- [ ] Build a ledger: one row per case, each backed by a primary source. No compute needed.

### 7.5 Checking others' claims
- Theirs: Anthropic's published figures checked against the released transcript (1 of 5 confirmable).
- [ ] Ours could have checked METR, e.g. whether regex rules alone recover METR's message categories.

### 7.6 Usable artifacts
- Theirs: a reporting form, two Sigma rules that pass the official checker, a synthetic false-positive test, a 50-signal gap list.
- Ours: Appendix G is advice, not runnable tools (its title partly mirrors theirs).
- [ ] Ship something runnable: a keyword-baseline script or an outcome-anomaly scorer.

### 7.7 Writing and figures
- [ ] Plain language first; define each technical term in one line (they did for "Sigma rule" and "kappa").
- [ ] Make Figure 1 the punchline (for us: detection by view, actions-only at chance), not a null interaction.

### 7.8 Where we were stronger (keep)
- Experiment with known ground truth (theirs: 9 cases, only 4 firm latencies; "four values give the full range").
- Hash-locked pre-registration, a positive control, 3,456 audits, CIs and permutation tests.
- Honest reporting: a deviations log and a discarded first attempt.

### 7.9 Checklist for next time
1. [ ] Start from a striking fact about a real incident; ask the plain question it raises.
2. [ ] Choose hypotheses where both outcomes matter to non-experts.
3. [ ] Lead with the most surprising result, and name it.
4. [ ] Use all relevant incidents, with a ledger and a control set.
5. [ ] Check at least one published claim against primary data.
6. [ ] Ship runnable tools and dated, falsifiable predictions.
7. [ ] Write the first page for a non-specialist.
