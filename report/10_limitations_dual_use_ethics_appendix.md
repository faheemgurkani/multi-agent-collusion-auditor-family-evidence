## Appendix: Limitations and Dual-Use / Ethical Considerations

### Limitations

**What the results establish.** In one environment (Colosseum JiraTicket; path topology, 4 agents) with three open-weight families (Gemma 4 31B, GPT-OSS-120B, Nemotron 3 Super) and eight seeds per condition, the results establish the following for a single frozen prompt:
- prompted auditors from these families detect *instructed* coalitions well from messages (AUROC 0.85–0.89);
- they do not detect them from action logs (AUROC 0.48);
- they show no statistically significant same-family effect (pooled interaction −0.029 [−0.063, +0.004], MDE 0.048);
- a neutral summary lowers detection.

**What they do not establish.**
- *Organic collusion.* The coalitions were instructed by Colosseum's coalition prompt, and the environment positive control narrowly failed (A − D = +3.84 [−0.11, +7.83]), so many positives were collusion "on paper". The results do not tell us how auditors fare against coalitions that arise from incentives, or that coordinate strongly through actions alone.
- *Auditor blindness to actions.* The at-chance actions-only result may reflect weak behavioural signal in this environment rather than an auditor limitation.
- *Absence of family bias.* A leniency effect of up to about 0.06 AUROC is inside our CI. Smaller effects, effects at the level of individual models, and effects in frontier closed models remain possible.
- *Generalisation.* The results may not hold for longer horizons, more agents, other topologies, auditors with reasoning traces or tool access, or other prompt wordings.

**Assumptions.**
- Instruction is an adequate stand-in for collusion. If it is not, our positives over-represent "talky" collusion and our detection numbers are optimistic.
- Averaging k = 3 samples gives a stable score per transcript.
- Serving differences (Nemotron in fp8 via OpenRouter; the others on Modal) do not interact with family. A provider check found no added noise.
- Statistical caveats: 16 positives and 16 negatives per auditor × family cell; multiple views are reported, with the pooled diagonal pre-registered as the primary estimand and the rest exploratory.

### Dual-use considerations

**Could this work make real collusion easier to carry out or harder to detect?** The main risk comes from the finding itself. Prompted LLM auditors relied on what agents *say*, and coalitions that left fewer messages, because they had no private channel, were detected least. A capable adversary, or a misaligned system that has learned from such findings, could infer that coordinating implicitly through actions, or keeping coordination talk out of logged channels, evades this class of monitor. We judge the marginal uplift to be low and the defensive value higher:
- The observation is consistent with prior work on the gap between what agents say and what they do (Nakamura et al., 2026) and on information access in monitoring (Arike et al., 2026).
- We publish no evasion technique, optimised prompt, covert channel or steganographic scheme.
- Defenders need to know that language-based auditing has this blind spot, so they can add outcome-based checks: regret, coalition advantage, allocation anomalies.

**Auditor choice.** Our finding of no significant family effect (and a non-significant lean towards leniency) could inform which model an adversary deploys against a known auditor. Because the effect is small and non-significant, we consider this low risk.

**What we withheld or mitigated.**
- The coalition instructions are Colosseum's published prompt variants (`structured`); we wrote no new collusion prompts.
- We release transcripts so that results can be checked, but we do not curate or highlight the "most evasive" transcripts, and we do not release any auditor-evasion analysis beyond the aggregate statistics reported here.
- Discussion of the real-world 2026 multi-agent incident is limited to citing the public investigation as motivation.

### Ethical considerations

- All data is synthetic: LLM agents in a simulated project-planning task. There were no human participants and no personal data.
- The models are open-weight and were used under their respective licences, through Modal and OpenRouter. Prompts sent to third-party providers contain only synthetic content.
- No responsible-disclosure step was needed: we found no vulnerability in a specific deployed product. The general finding (language-based auditors miss implicit coordination) is published here so that deployers of LLM auditors can act on it.
