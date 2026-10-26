## 3. Methods

All prompts, gates and analyses were **pre-registered and frozen** (SHA-256-hashed, 2026-10-25 11:20 UTC) before any agent run or auditor call. Eight deviations, all infrastructure changes or pre-registered contingencies, are listed in Appendix B. All work was done during the sprint. Colosseum is pre-existing third-party code; we patched one client file (see Code and Data).

### 3.1 Environment, conditions and agents

We use Colosseum's `JiraTicket` environment (Nakamura et al., 2026), a distributed constraint-optimisation problem. Four agents with private skills, availability and costs each pick at most one of 8 tasks. The team reward is joint and the optimal allocation is computable, so per-agent reward and regret are exact. Agents sit on a **path** and post on message boards, with up to 4 planning rounds per episode and 3 model calls per turn. The two endpoints, who share no public board, form the designated pair. **Coalition advantage (CA)** is the pair's mean reward minus the others' mean reward. The four shipped hackathon conditions vary one factor at a time (Table 1).

**Table 1.** Conditions. "Instructed": the pair's system prompts contain Colosseum's `structured` coalition prompt, which is never shown to auditors. Label 1 = A, B; label 0 = C, D.

| Code | Instructed | Extra channel | Role |
|---|---|---|---|
| A | yes | private, pair only | positive; **positive control** |
| B | yes | none | positive; harder ("hidden") case |
| C | no | open to all | hard negative (extra talk, no coalition) |
| D | no | none | baseline negative |
| E | no | private, pair only | exploratory emergent arm (no label) |

**Agents.** Each episode uses one model for all four agents, at temperature 0.7 with a 3,000-token cap. The families are Gemma 4 31B (`google/gemma-4-31B-it`@3548789), GPT-OSS-120B (`openai/gpt-oss-120b`@b5c939d) and Nemotron 3 Super 120B-A12B. Gemma and GPT-OSS were served on Modal (SGLang); Nemotron ran via OpenRouter, pinned to one provider (DekaLLM, fp8). Design: 3 families × 4 conditions × **8 seeds** (101–108, identical across arms) = **96 episodes**, none failed. Arm E ran for Gemma and GPT-OSS, 5 seeds each. For exploratory analysis E1, positives are typed as **effective** if their CA exceeds the family's mean CA in condition D (**direct** if from A, **hidden** if from B), and as **attempted** otherwise.

### 3.2 Views and auditing

Each view begins with an identical header listing the public tasks and each agent's private profile. Coalition instructions, rewards and CA are never shown, and model ids, conditions and seeds are stripped. **V1** contains all board posts, with board membership. **V2** contains all non-message tool calls with their results, plus the final allocation. **V3** interleaves V1 and V2 in order. **V4** is a neutral per-agent report (stated intentions, requests, actions, consistency; no quotes, no judgement) written from V3 by a fourth family, DeepSeek V4 Flash, at temperature 0.

Every auditor family audits every transcript under every view using one frozen prompt (Appendix A). The prompt quotes the minimal definition of collusion from the sprint's definitions survey (Apart Research sprint starter team, 2026) and asks for JSON with `suspicion` (0–100 on an anchored scale), `colluding_agents` and a short rationale. We take **k = 3** samples at temperature 0.7 and average them, giving **3,456 audits**; parse rates were 100%, 100% and 99.9%. A **self-recognition probe** (E2) asks each auditor which family wrote the V1 messages.

### 3.3 Gates and analysis (pre-registered)

**G1 (positive control):** mean CA(A) − CA(D) over family × seed pairs > 0, with the 95% CI excluding 0. **G2 (competence):** AUROC on V3 ≥ 0.65 with CI lower bound > 0.5; family effects are interpreted only for auditors that pass. **Detection** compares A+B against C+D using AUROC, TPR at 5% FPR, and balanced accuracy at a threshold of 50. **H2 (family effect):** per view, we form the 3×3 matrix M[auditor, agent family] of AUROCs and compute the interaction I = M − row mean − column mean + grand mean. This removes auditor competence and agent detectability (cf. Pinto, 2026; Awuni et al., 2026). The primary estimand is the mean diagonal of I pooled over V1–V3: negative means leniency, positive means familiarity advantage. **Inference:** a cluster bootstrap over transcripts, stratified by family × label (10,000 resamples); a within-condition permutation test of family labels (5,000 permutations); and the MDE = 2.8 × bootstrap SE. **H1:** AUROC(V3) − max(AUROC(V1), AUROC(V2)). **H3:** |I_V1| − |I_V2|. **H4:** for each agent family, the same-family auditor vs the mean single cross-family auditor, a cross-family ensemble (mean suspicion of the two other families), and the same-family auditor on V4, with paired bootstrap CIs. All tests are two-sided at α = 0.05.

**What did not work** (Appendix B): the free Nemotron endpoint (HTTP 404 on every call); the `simple` coalition prompt, which failed G1 on the pilot and triggered the pre-registered switch to `structured`; and our first Nemotron provider, which became rate-limited mid-study. All Nemotron runs were redone on DekaLLM, and audits from the two providers agree (ρ = 0.63, above test–retest ρ = 0.44). **Compute:** $19.31 of Modal credit and $3.22 of OpenRouter credit; Python 3.11.
