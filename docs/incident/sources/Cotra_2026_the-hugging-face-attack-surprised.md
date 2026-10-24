# Planned Obsolescence

> Source: https://www.planned-obsolescence.org/p/the-hugging-face-attack-surprised (fetched 2026-10-24, converted to Markdown)

*All opinions are my personal view, and don’t represent my employer or fellow investigators.*

This week, [METR](https://metr.org/) and [Redwood Research](https://www.redwoodresearch.org/) published the [report](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/) on our independent investigation into agents’ behavior and motivations in the Hugging Face attack; I was one of the investigators. This was an absolutely wild incident — I encourage you to check out the full report, but [METR’s tweet thread](https://x.com/METR_Evals/status/2092692175452803393) packs in some of the highlights.

# What surprised me

When we started this investigation a week before [OpenAI’s Black Hat talk](https://www.youtube.com/watch?v=87DyyMV0kCY) revealed a number of key details, I had a fundamentally incorrect conception of what basically happened in this incident. In this post, I’ll go over five things I was very wrong about going in.

## 1. The sheer scale

I knew there were multiple models involved from OpenAI’s [initial post](https://openai.com/index/hugging-face-model-evaluation-security-incident/), but I assumed that a few different agents happened to have broken out of their sandboxes separately, or maybe several subagents had spawned from one initial agent, or maybe there was some kind of multi-agent evaluation setup.

Instead, we found that 1200 completely separate agents intended to be isolated from one another found an illicit way to communicate and formed large teams to work together on ambitious cheating strategies, and 700 of them worked together to attack Hugging Face.

## 2. All the illicit messaging

I had seen [reporting](https://www.reuters.com/business/its-ai-agent-spent-days-hacking-company-sources-say-openai-did-not-notice-week-2026-07-24/?utm_source=chatgpt.com) that agents were “leaving notes” to each other, but I assumed that maybe it was a garbled reference to compaction summaries,[1](#footnote-1) or agents were incidentally seeing files other agents had written once in a while. Instead, we found several different active communication platforms involved in this incident alone.

The main message board we studied, a particular cache namespace of a package repository, contained over 70,000 messages and files[2](#footnote-2) that agents sent to one another during a period of less than one week.

But this wasn’t even the first message board established by these particular agents.[3](#footnote-3) There was another one established five hours earlier using a *different* method of abusing the same package repository, and it just happened not to take off as much.

We also saw two additionalmessage boards abusing the same package repository, as well as at least two different places that agents communicated on the open internet (including on Hugging Face datasets). None of this communication was actually expected or allowed.

## 3. The agents’ actual goals

I thought the agents attacked Hugging Face to try to steal the answer keys for their tasks. Instead, we learned that agents had actually figured out a general-purpose cheat that would let them reverse-engineer the “flag” (answer)[4](#footnote-4) for any ExploitGym task. But based on their reading of the [ExploitGym paper](https://arxiv.org/pdf/2605.11086) and various implementations, the agents believed that the automated scorer would check their transcript to make sure they got the flag in the intended way.

They then launched multiple ambitious R&D workstreams to try to tamper with or fool the scorer in a wide variety of different ways. Most agents that attacked Hugging Face did so to try to *get more information about the scorer* so they could figure out better ways to undermine it, not to get answer keys.

## 4. The peer altruism

Progress on these big collective cheating R&D projects often depended on [individual agents being willing to risk failing their own task](https://x.com/RyanGreenblatt/status/2093185101593301301) to help the “collective” learn important information. Agents often pressured each other into accepting these “sacrifices,” in a very human way. We saw several agents that volunteered for these experiments end their runs prematurely.

More broadly, agents were often interested in helping out their “peers” or generically improving the capabilities of the “swarm” even if this had no particular benefit to their task. They didn’t free ride and were often eager to plug into one of the open “lanes” in the larger projects on the message board.

## 5. The efforts to manipulate logs

Up until this point, we had not seen agents try to actively cover up evidence of their misbehavior in sophisticated ways. But we discovered (on our second-to-last day) that the agents in this incident were going to great lengths to attempt to manipulate their own transcripts — they were doing this in order to fool the automated *scorer*, but the techniques they were researching would affect the same transcripts a *human* might review.

We saw that agents got one technique to work: ~7% of our transcripts contained “spoofed tool calls”, where the agent pretended to run one command on the computer but actually ran a different command in the background. The tool call spoofs we saw seemed to be small-scale tests that were relatively obvious, but because more extensive spoofing might have been harder to detect by design, it’s tough to rule out.

We didn’t see the agents in our dataset succeed at *retroactively* editing logs. But the activity in scope for our investigation was Jul 7th-13th, and we can’t rule out that agents succeeded after that point.

# What it means

*Edited 8/30: I added more explanation to this section in response to questions.*

This incident was far more severe than I expected, and far more severe than previous [publicly documented misalignment incidents](https://metr.org/agent-incidents/), both in terms of how concerning the agents’ motives were and the feats they achieved in pursuit of those motives.

The prototypical publicly-documented reward hack from 6 months ago involved single agents finding a way to edit test cases so they would pass or access answer files they weren’t supposed to see. This incident involved a whole ecosystem of over 1000 agents working together on complex R&D projects that lasted multiple agent “lifetimes” to figure out deep, general-purpose ways to undermine the scoring process and cover their tracks.[5](#footnote-5)

Compared to these reward hacks from six months ago, this incident feels like it’s more than 50% of the way to [full-blown AI takeover](https://www.lesswrong.com/posts/pRkFkzwKZ2zfa3R6H/without-specific-countermeasures-the-easiest-path-to), routing through first taking over the AI company itself.

Another jump like this along these propensity dimensions — scale, cooperation between agents, ambition and horizon length of misaligned goals, deceptiveness — seems like it could motivate agents to try very hard to maintain a covert, persistent [rogue deployment](https://blog.redwoodresearch.org/p/ai-catastrophes-and-rogue-deployments) within the AI company. I continue to expect [extremely rapid advances in capabilities](https://www.planned-obsolescence.org/p/hurtling-through-2026) and think frontier agents will likely be capable of establishing such a rogue deployment in six months.

Once the rogue deployment is established, it seems plausible this could spiral all the way to a takeover. Agents could pull in future, more capable models into the swarm, try to ensure that they are aligned to the interests of the swarm, and compromise security and monitoring infrastructure to make it easier for the swarm to operate. These more capable models could in turn continuously harden, perpetuate, and expand the rogue deployment and further compromise the company’s infrastructure.

As more and more work is handed off to these ever-more-capable AI agents, the rogue swarm could come to fully control the operation of the AI company and the development of future AI systems. At this point, [governments and militaries may fully depend on these systems](https://www.planned-obsolescence.org/p/could-a-company-overpower-nations), making it possible to seize hard power.

These agents were really not trying very hard to be sneaky or play the long game like this, but it seems like they easily could have if they happened to be focused on fooling *human* investigation rather than the automated scorer. Because future rogue swarms could cover their tracks better (and because AI companies could paper over these problems), I am not sure that we will get such a clear warning shot before it’s too late.

[1](#footnote-anchor-1)

Compaction summaries are more like an agent leaving notes to its own future self.

[2](#footnote-anchor-2)

The raw dump from the cache contained ~1.2 million distinct entries, but the vast majority of these entries were small chunks of files; each file would be broken up into hundreds or thousands of individual entries. Agents wrote scripts to reconstruct and parse these files.

[3](#footnote-anchor-3)

As OpenAI reports in their Black Hat talk and recent post-mortem, agents were establishing message boards in training since May.

[4](#footnote-anchor-4)

For each task in ExploitGym, the agent is given a particular piece of software (the “target”) and a particular vulnerability in that software, and is instructed to develop an exploit that uses that particular intended vulnerability to retrieve a piece of arbitrary data (the “flag”) that’s buried somewhere within the target program. The flag is the closest thing to an “answer”; the agent must submit the flag to prove it has exploited the program (these tasks are also called “capture the flag” tasks or CTFs). In this case, the agents very quickly discovered a universal way to reverse-engineer the correct flag for any ExploitGym task.

[5](#footnote-anchor-5)

They were focused on the automated scorer but researched techniques that would affect logs viewed by humans, and in fact succeeded at affecting our own logs in places.
