> Source: [Overview tab](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25#overview) — captured 2026-10-24 (verbatim conversion of the page; links preserved).

**Header facts:** Oct 23–25, 2026 · Online + in-person hubs · Submissions close **Sun Oct 25, 11:59 PM AoE** (= Mon Oct 26, 11:59 UTC) · 1,673 signed up at capture time.

*"AI agents have been shown to collude: sustaining prices above the competitive level, forming coalitions in workplace tasks, and coordinating through channels nobody is watching. Over one weekend, build the experiment that catches it."*

## Overview

In this 3-day research sprint, you will design and run experiments on collusion between AI agents: when it emerges in markets and everyday agent deployments, how an auditor can tell it from coincidence, how coordination is carried, and what a defender can do to break it. Co-organized by Apart Research, [Poseidon Research](https://www.poseidonresearch.com/) and [AE Studio](https://ae.studio/), with additional support from [Modal](https://modal.com/) and [The AI Alignment Foundation](https://www.aialignmentfoundation.org/), the sprint runs online with in-person hubs hosted by [Collider](https://www.collider.nyc/) in New York City and [AI Safety Hong Kong](https://www.aisafetyhk.org/apart-hackathon-hk-hub) in Hong Kong. No prior background in AI safety is required.

**When:** Friday, October 23 to Sunday, October 25, 2026, online, with in-person hubs at Collider in New York City and AI Safety Hong Kong on Saturday and Sunday. Submissions close Sunday, October 25 at 11:59 PM Anywhere on Earth (AoE).

Modal credits: $250 per person at the New York in-person hub, $50 for every other participant.

## Cash Prizes

|  |  |
| --- | --- |
| **$2,000** in cash prizes across all tracks |  |
| 🥇 1st Place | $1,000 |
| 🥈 2nd Place | $500 |
| 🥉 3rd Place | $300 |
| 🏅 4th Place | $100 |
| 🏅 5th Place | $100 |

## Fast-track and continuation

- **Follow-up program:** Selected teams continue through the Apart Fellowship for further research and mentorship; the timeline is shared with invitations.
- **What winners receive beyond cash:** fellowship fast-track, mentor introductions from the organizing team and judges, and a pathway toward a publishable write-up.

## What this Sprint is about

Collusion between AI agents is a failure mode in high-stakes environments, markets and economics first among them, where misaligned coordination could cause substantial harm. Previous experiments have already produced it: models forming prices that violate economic expectations on competitiveness, agents independently engaging in anti-competitive practices, and over half of tested models showing a coalition advantage when given the opportunity to speak privately in a realistic workplace task. In an era where agent communication and collusion are on the rise, as recently exemplified in the [OpenAI/Hugging Face incident](https://www.dwarkesh.com/p/openai-huggingface), the kind of work done at this sprint is directly relevant to understanding and preventing that behaviour.

This sprint asks three questions. When does collusion emerge, and which levers cause it? What should count as convincing evidence that agents are colluding, with evidence drawn from logged agent trajectories? And how is the coordination needed for collusion mediated, and how can it be broken, ideally before it happens or otherwise while it is occurring?

## What participants will do

Over three days you will pick one open question about collusion between AI agents, build the controlled experiment that answers it, and write up what you found.

**The format.** Teams of one to five people pick a track, come up with a project, and ship. There is no requirement to have participated before, no requirement to have a team in advance and no specific background needed.

**Starting points.** Every research question below is tied to existing papers and open-source code. The Resources tab has a practical start for each one: starter code, a weekend-sized project, and a rough cost estimate. All default routes use a normal 16 GB laptop and no GPU.

## Research Tracks

Pick one track to anchor your project. Each research question below is developed in full on the Resources tab, with the papers it builds on and a practical start (starter code, weekend project, budget).

### 1) Markets and Collusion

In this track, the majority of results we build on are native to markets, though you should feel free to explore them beyond this setting as the questions themselves are more general, and there are clear overlaps with some later tracks, e.g. information-theoretic approaches to detect collusion would fit well in track 2. Environments where humans collude likely offer similar incentives and opportunities for models to collude. Other such environments might include politics, media and marketing. This track is important because it represents a failure mode in a high-stakes environment (markets/economics) where misaligned actions from an AI could cause substantial harm. It also provides a useful testbed for collusion. For a contrasting positive view of the role of markets in multi-agent systems, see [Tomašev et al. (2026)](https://arxiv.org/pdf/2512.16856).

**Research questions:**

- 1.1. Which variables are necessary for collusion to emerge in markets?
- 1.2. Once collusion has formed, is it robust to replacing some of the participants?
- 1.3. Can we improve on existing collusion detection methods?
- 1.4. Can we use information-theoretic approaches to detect collusion in multi-agent games?
- 1.5. Which single restriction removes the most collusion at the least cost?

### 2) Detection and Audit of Collusion

This track is about definitions, detection and standards of evidence, using logged agent trajectories as the evidence. Markets are still relevant settings, but we also want to cover everyday agent workflows outside markets. The aim is to understand collusion in general: can we say anything about what causes it, regardless of the setting?

**Research questions:**

- 2.1. Which kinds of tasks lead to collusion?
- 2.2. Does combining what agents say with what they do beat either alone?
- 2.3. What should count as convincing evidence of collusion?

**Red-teaming challenge.** Poseidon Research has developed a new model organism, Dolos-1.5B: a fine-tune of Qwen2.5-1.5B-Instruct trained to have a hidden misaligned behaviour. Teams get only the model weights and have to red-team it during the sprint. There is no code to understand, so it is quick to get going and to make progress.

### 3) Collusion Carriers and Countermeasures

This track studies how the coordination needed for collusion is mediated, and how it can be broken. This is important because we need to be able to prevent and break up collusion, ideally before it happens, or otherwise while it is occurring.

**Research questions:**

- 3.1. Beyond colluding directly via text, can actions, tools or other side channels be the conduit for collusion?
- 3.2. Can we disrupt collusion through introducing trusted agents?
- 3.3. Can agents identify their peers?
- 3.4. What does a coalition do when it learns it is being watched?

## Who should join

Engineers, researchers and people from any industry are welcome, and mixed teams tend to do best.

You do not need an AI, ML or safety background. Every research question is tied to existing papers and open-source code, and the Resources tab has a practical starting point for each one.

We would be particularly interested in quantitative finance professionals, with some of the tracks written so that market intuition and data skills transfer directly.

## What happens after

Results and winners are announced about 1 to 2 weeks after the judging deadline. Top teams are invited to apply to the Apart Fellowship for continued mentorship, funding, and publication support. Selected projects may be shared on the Alignment Forum, LessWrong, and other community venues.

## Partners

- [**Poseidon Research**](https://www.poseidonresearch.com/), an independent AI safety laboratory making advanced AI systems transparent, trustworthy, and governable, with technical research in interpretability, control, and secure monitoring.
- [**AE Studio**](https://ae.studio/), an applied AI studio with a frontier AI alignment research lab, working on threads including Self-Other Overlap, Gradient Routing and Sleeper Agents.
- [**Modal**](https://modal.com/), provides high-performance cloud GPU infrastructure specifically designed to accelerate AI research, model training, and agent evaluation loops.
- [**AI Alignment Foundation**](https://www.aialignmentfoundation.org/), accelerates alignment research by pairing researchers with dedicated teams, backed by funding for compute and infrastructure.

## Contact

- **Email:** [sprints@apartresearch.com](mailto:sprints@apartresearch.com)
- **Discord:** [discord.gg/XswWBvugYs](https://discord.gg/XswWBvugYs)
- **Organizer:** Apart Research

Next: Resources
