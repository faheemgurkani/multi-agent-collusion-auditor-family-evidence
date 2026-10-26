# 08: Talk transcripts: categorisation, shortlist and findings

Transcripts are now sorted in `docs/misc./transcripts/` (one folder per talk, each holding a `.transcript.vtt`, a `.cc.vtt` and the chat log). Each folder was identified by its speaker labels and matched to the schedule's UTC timestamp.

| # | Folder | Talk | Relevance to Tracks 2 + 3 | Studied |
|---|---|---|---|---|
| 01 | `01_JoanVelja_Steganography-Concern` | Joan Velja (Oxford): "How concerned should we be by steganography?" | Medium: monitor threat models | Keyword skim |
| 02 | `02_SumeetMotwani_Steganographic-Collusion` | Sumeet Motwani (Oxford): "We're Not Prepared for Steganographic Collusion" | Medium: overseer vs colluder capability | Keyword skim |
| 03 | `03_JurgisKemeklis_AI-Control-Insider-Threats` | Jurgis Kemeklis (MIT / Redwood): "Mitigating insider threats from AIs with AI control" | **High**: trusted/untrusted monitors, clone collusion | **Full** |
| 04 | `04_Logistics_KamilAlaa` | Sprint logistics | Rules | Done earlier |
| 05 | `05_UsmanAnwar_Detecting-Steganography` | Usman Anwar (Cambridge): "Challenges in Detecting Steganography in LLM Transcripts" | **High**: evidence standards, trusted "sentinel" | **Full** |
| 06 | `06_MasonNakamura_Colosseum` | Mason Nakamura and Eugene Bagdasarian (UMass): Colosseum | **Highest**: our harness and its authors' open problems | **Full** |
| 07 | `07_JerickShi_Trust-Breaking` | Jerick Shi (Voleon): deception, promise-breaking | **High**: say-vs-do, how to stand out | **Full** |
| 08 | `08_KhanhLinhNguyen_Collusion-Overview` | Khanh Linh Nguyen: map of AI-collusion research for the sprint | **Highest**: names our exact gap and gives method advice | **Full** |

**Missing:** Matthew Lee (Poseidon), "Defining AI Collusion" (Sat 18:00 UTC). It isn't in the folder; add it when the recording is posted.

---

## Findings by talk, and what each contributes

### 06 Nakamura & Bagdasarian: Colosseum
- Colosseum's three metrics are an **LLM collusion judge** (communication), **coalition advantage** (actions; coalition mean reward minus non-coalition mean) and **overall regret** against the DCOP optimum. "You need to monitor all three."
- Collusion types: **direct** (talks and acts), **attempted / "collusion on paper"** (talks, doesn't gain), **hidden** (gains, judge score low). Their RQ1 finding: "**LLM-as-a-judge is not sufficient** for collusion auditing; action-based metrics are required." Also: "the LLM collusion judge can definitely be fooled."
- **Emergent collusion at λ=0:** two benign agents given a private channel, with no instruction, show raised coalition advantage on average across 19 models. Some models (Kimi K2 Thinking, MiniMax) talk collusively but *lose* advantage.
- Their judge rubric and model are fixed. **They never vary the judge's identity.**
- Practical advice: use **JiraTicket or meeting scheduling**, not Hospital (the hardest), for a 2-day project. A mitigation-versus-performance trade-off study "could be an interesting project to study in the next couple of days."
- Q&A: varying population size at a fixed colluder share hasn't been tried. Agents are told about the hidden channel *by prompt*.
- **Contribution to us:** confirms that ground truth plus action metrics exist in the harness, that judges are a known weak point, and that judge identity is an untouched variable. Their condition structure (control / emergent / prompted) gives positives, negatives and ambiguous cases.

### 08 Nguyen: overview for the sprint
- Explicitly lists as **still missing**: "What if the LLM doing the monitoring **shares a colluder's model** or their incentives? Most detection work treats the auditor as trustworthy. AI control doesn't." Her final slide suggests: "do 10 narrow questions keep a monitor honest when it comes from the **same model family as the colluders**?"
- **Method rules for weekend studies:**
  1. Freeze the monitor (model, prompt, threshold) before looking at test data.
  2. Report **FPR, TPR at 1% and 5% FPR, and AUROC**, not just accuracy.
  3. Add **hard negatives**: cheap talk with no action, and parallel moves with no talk.
  4. Add computed signals (e.g. regret) alongside LLM judgements.
  5. Test across providers and model families.
- **Say-vs-do cuts both ways:** compare each agent's claim with its own move (catches deception), and talk between agents with what they do next (catches agreement).
- Evidence she cites: ORBIT (per-action defences give no protection against colluders, whose individual calls look benign); "Faithful yet Collusive" (CoT faithfulness is unrelated to collusion); NARCBench (only 2 of 229 emergent collusive episodes put the coordination into words); Arike (monitors often do better with *less* information).
- **Contribution to us:** the strongest external validation of Candidate A (same-family auditors), plus a ready-made evaluation protocol that judges will recognise.

### 03 Kemeklis: AI control
- **Clones can coordinate without a channel:** copies of one model can predict each other and converge on the same Schelling choices (acausal coordination). Standard control practice therefore uses a trusted monitor with a **different pre-training / base model** so it isn't "causally aligned" with the untrusted model.
- From the Q&A: "if one copy of a model monitors another, they may collude", and untrusted models can also "gaslight" a trusted monitor. Paraphrasing and redaction are the mitigations, and "figuring out more here seems very useful."
- Frame mitigations on a **safety-versus-usefulness Pareto frontier**. Labs adopt measures that add safety without a big hit to usefulness.
- **Contribution to us:** the theoretical motivation (shared base model → shared priors → a leniency risk) and the Track 3 countermeasure framing (cross-family monitoring and paraphrasing as mitigations, reported as a safety–cost trade-off).

### 05 Anwar: detecting steganography
- Classical steganalysis fails for LLMs because each LLM has **its own "cover distribution"**: what looks normal is model-specific, e.g. one model's verbal tics.
- His detector rests on a **trusted sentinel**: hidden information is defined *relative to a sentinel* that cannot decode it. "The sentinel determines what you consider public information." LLM-as-judge suspicion scoring is a weak baseline because judges look for garbled text.
- **Contribution to us:** a mechanism hypothesis for same-family leniency. A judge from the agents' family shares their distribution, so collusive coordination may read as "normal" to it but anomalous to an outsider. That gives us a clean way to explain the result if H2 holds.

### 07 Shi: deception and promise-breaking
- **Deception needs divergence** (the model could have acted honestly) **plus functional intent**, so be precise about what evidence shows collusion.
- Effects are highly **model × game dependent**: no model or game dominates. Measure across several families, not one.
- How to stand out: collusion papers vary only **environment, agents, interaction channel**, and 90% use markets, API LLMs and private messages or steganography. "Think of a way to detect collusion that no one has thought of", and **connect simulations to real-world risk**, ideally with a one-step mitigation firms could adopt.
- **Contribution to us:** the auditor's identity is a fourth, unexplored variable. Use multiple families. End with a deployable recommendation (e.g. "don't audit agents with their own model family").

### 01 Velja and 02 Motwani (skimmed)
- Velja's threat models include **"the agent and the monitor themselves collude."** She expects hidden encodings to arise first within one model, then **between copies of the same model**, and only later across different models.
- Motwani: in their multi-agent setup the overseer was from the **same family** as the communicating models, and "models become much better at colluding than they do at oversight" as capability grows. Paraphrasing helps but is imperfect.
- **Contribution to us:** both support same-family risk as a recognised but unmeasured threat. Paraphrasing is a natural mitigation arm.

---

## Net effect on our direction

Five independent talks (Nguyen, Kemeklis, Anwar, Velja, Motwani) point at the **same open question**: is an LLM auditor that shares the colluders' model family less reliable? Colosseum's authors confirm their judge is the weak link and that judge identity was never varied. This moves **Candidate A** from "preliminary" to **recommended**; see [09_research_decision.md](09_research_decision.md).
