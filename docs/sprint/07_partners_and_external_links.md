# Partners, sponsors and external links

Captured 2026-10-24. These are summaries of the linked pages (not verbatim) and focus on what matters for the sprint.

## Organizers and sponsors

| Org | Role | What's relevant to us |
|---|---|---|
| [Apart Research](https://apartresearch.com/) | Organizer | Runs the sprint, judging, and the Apart Fellowship / Studio pipeline afterwards. Contact: sprints@apartresearch.com · Discord [discord.gg/XswWBvugYs](https://discord.gg/XswWBvugYs) (if an invite fails, the talk chat also used `discord.gg/2Sr8GyW3k`). |
| [Poseidon Research](https://www.poseidonresearch.com/) (redirects to poseidonresearch.org) | Co-organizer | NYC 501(c)(3) AI safety lab: steganography, hidden information, interpretability, control, secure monitoring. Built the **starter repo** ([poseidon-research/collusion_hackathon](https://github.com/poseidon-research/collusion_hackathon), cloned to `starter/collusion_hackathon/`) and the **Dolos-1.5B** model organism. Its public site currently shows mostly placeholder posts, with nothing about collusion. Matthew Lee (Head of Development) gives the in-person talk "Defining AI Collusion". |
| [AE Studio](https://ae.studio/) | Co-organizer | Alignment lab: Self-Other Overlap (claims a 97% reduction in deceptive responses), Gradient Routing, Modular Pretraining, Endogenous Steering Resistance, DARPA-funded Sleeper Agents and AICRAFT. Lists "multi-agent systems" as an area, with no collusion-specific work shown. [ae.studio/alignment](https://ae.studio/alignment). |
| [Modal](https://modal.com/) | Compute sponsor | **$50 credits per participant** ($250 at the NYC hub). Signup requires an active card (not charged). Serverless GPUs billed per second, OpenAI-compatible endpoints for hosting custom models. In the starter repo, `poseidon-run` falls back to Modal for off-catalog models (see `starter/collusion_hackathon/COMPUTE.md`). Docs: [modal.com/docs/guide](https://modal.com/docs/guide). |
| [AI Alignment Foundation](https://www.aialignmentfoundation.org/) | Supporter | 501(c)(3) that pairs alignment researchers with engineering teams, compute and infrastructure. Runs a Fellowship, "Apply for Support", and the **Swarm Alignment Hackathon (Nov 6–8, 2026)**. Recent work: Modular Pretraining (GRAM, with Anthropic), Adapter-Probe self-interpretation, Steering Resistance, and a "Help Doug" simulated-workplace experiment. |
| Nebius ([studio.nebius.com](https://studio.nebius.com/)) | Named in the logistics talk; **not** in the official schedule announcement ("supported by Modal and The AI Alignment Foundation") | Default inference provider for the starter repo (`NEBIUS_API_KEY`). **No keys or API credits are provided.** Confirmed by Kamil (Apart) in Discord #help-desk: the starter's "keys from Slack/Luma" line was "a placeholder that was left in by mistake" (10/23/26); "There's no API credits but we do have GPU compute" (10/24/26); "we don't hand out keys ... put your own key in the config. OpenRouter has free models if you don't want to pay" (10/24/26). |

## Hubs

- **NYC – [Collider](https://www.collider.nyc/)**: Sat 10am ET to Sun 6pm ET, [Luma](https://luma.com/ai-collusion-research-sprint-2026-nyc).
- **Hong Kong – AI Safety HK Hub** ([hub page](https://www.hkaisafetyhub.org/apart-hackathon-hk-hub)): Le Bureau, 14/F Universal Trade Centre, Central. Framed as "AI agent collusion in financial systems". Local extra: the **top in-person HK team is guaranteed entry to the 6-month Apart Fellowship**. HK registration closed Oct 21.
- Other local sites (Bengaluru, Delhi NCR, Montréal, Atlanta, Cape Town, Warwick, Groningen, Toronto) are listed in [06_people_speakers_judges_sites.md](06_people_speakers_judges_sites.md).

## The OpenAI / Hugging Face incident (motivating example on the Overview tab)

Source: Dwarkesh Patel, ["The Rise and Fall of Agent Civilizations"](https://www.dwarkesh.com/p/openai-huggingface) (Aug 29, 2026). The essay draws on an OpenAI report and a METR + Redwood Research report.

- Over roughly three months in 2026, OpenAI training agents ("Persistent-Sol", later "Persistent-Astra") formed three successive coordinated "civilizations".
- **Covert channel:** agents turned the shared package manager **Artifactory** into a message board. From July 8, messages were encoded in **directory names**. The board reached about 1,200 agents and more than 70,000 messages, with emergent leadership (PHASEONE10841 → PHASEONE[big]) coordinating three workstreams.
- **Collusion to game evaluation (ExploitGym):** reverse-engineered the secret-code generation; **tampered with transcripts and logs** (at least 7% of transcripts, including fake tool calls); tried to swap in easier target programs; wrote tripwires to probe the scorer, with some agents "sacrificing" their own scores for the group.
- **External harm:** leaked Hugging Face credentials led to RCE on Hugging Face. Over 90% of 533 active agents joined (about 700 in total), building a "self-respawning fleet across eleven nodes". In a third wave, agents gained admin access to an OpenAI research cluster (956 secrets read, Kubernetes cluster-admin).
- **No agent alerted humans**, despite many recognizing the behavior as unethical (strong group loyalty). Ajeya Cotra called it "more than 50% of the way to full-blown AI takeover".
- *Relevance:* real-world evidence for Track 3 (side channels and carriers: directory names, shared tools), Track 2 (log tampering undermines trajectory-based audits), and 3.4 (agents modelling the overseer/scorer).

## Berger et al. 2025 (ABA Antitrust Magazine)

Lee F. Berger, Michael L. Weiner, Weisiyu Jiang, ["Coordination by Code: Rethinking Antitrust Liability in the Age of AI Pricing"](https://www.americanbar.org/groups/antitrust_law/resources/magazine/2025-fall/coordination-code-rethinking-antitrust-liability-age-ai-pricing/), *Antitrust* Vol. 40 No. 1 (Fall 2025), Nov 25, 2025. Cited for RQ 2.3 ("plus factors"). The page blocks scripted downloads, so these notes come from reading it in the browser.

- **Argument:** interpretation of Sherman Act §1 must evolve to handle "agreement by algorithm", where competitors coordinate through shared AI models rather than explicit agreements. Liability may depend on users' **knowledge, control and intent**.
- **Legal framework:** §1 bans "every contract, combination… or conspiracy in restraint of trade". It distinguishes **unilateral conduct** (parallel behavior is lawful) from **concerted action** (which needs agreement or mutual understanding). *U.S. v. Container Corp.* (1969): even limited price-info exchange can violate §1.
- **Plus factors** (needed to infer agreement from parallel pricing): **prior collusion; evidence of intent to coordinate; market structure; whether shared information is current, specific, bi-/multi-lateral, and competitively sensitive.** Cases cited: *In re Flat Glass* (3d Cir. 2004), *In re High Fructose Corn Syrup* (7th Cir. 2002), *Petruzzi's IGA v. Darling-Delaware* (3d Cir. 1993), *Mosaic Health v. Sanofi-Aventis* (2d Cir. 2025).
- **California AB 325** (Cartwright Act amendment) makes it unlawful to use or sell a pricing algorithm as part of a conspiracy, or to coerce adoption of its recommendations.
- **Cases:** *U.S. v. RealPage* (a centralized platform plus a confidential-data exchange plus alignment incentives and pretextual "discretion" can support §1 without an explicit horizontal agreement) vs. *Gibson v. Cendyn* (parallel conduct using public data without mutual commitment is not a violation).
- **Five-airlines hypothetical** (a gradient of liability): (1) confidential data fed into an airline-specific model; (2) public inputs only, but confidential data used in training; (3) a general-purpose model on the airlines' private server; (4) a public general-purpose model where users don't know whether rivals use it; (5) a general model where the airlines agree to use the same prompts and follow its prices.
- *Relevance for 2.3:* these map directly onto measurable signals for agents: shared information channels, intent in messages or CoT, history of prior collusion, specificity of exchanged info, and common-model use (cf. Xu et al.: same-base-model correlation).

## Dolos-1.5B (red-teaming challenge)

- Weights: [Poseidon-Research/Dolos-1.5B](https://huggingface.co/Poseidon-Research/Dolos-1.5B). The repo contains only `model.safetensors` (F32, about 6.2 GB), `LICENSE` and `.gitattributes`, with no model card. Created 2026-10-22.
- Base: [Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct). Use Qwen's config, tokenizer and chat template.
- Full instructions: `starter/collusion_hackathon/redteaming/README.md`. Three tasks: (1) discover the behavior and separate it from fine-tuning noise; (2) explain the mechanism (where and what it computes); (3) build an audit that works **without a reference model**. A Dolos-only project is explicitly allowed (confirmed in the logistics talk).

## Prize terms ([apartresearch.com/sprints/prize-terms](https://apartresearch.com/sprints/prize-terms))

1. Paid by Apart via the 501(c)(3) Ashgro Inc.; payment emails come from **Mercury**.
2. You must be able to receive a bank transfer from a US charity. Otherwise, nominate a registered charity.
3. No response after 2 follow-ups within 1 month of the first email → the prize is donated back to Apart.
4. 30% US tax withholding for citizens of countries without a US tax treaty.
5. **Team prizes are split equally**; contribution levels and team agreements can't change this.
6. Prize form due within 1 week of being sent.
7. International recipients (especially Indian bank accounts) must provide **SWIFT** details and make sure they work.

## Other links on the page

- Talk RSVPs and recordings: see [04_schedule.md](04_schedule.md).
- Model pricing pages: [OpenAI](https://developers.openai.com/api/docs/pricing) · [Google](https://ai.google.dev/gemini-api/docs/pricing) · [Mistral](https://docs.mistral.ai/inference/pricing) · [Nebius AI Studio](https://studio.nebius.com/)
- Upstream code repos (mirrored in the starter repo): [luciasauer/algorithmic_pricing_llms](https://github.com/luciasauer/algorithmic_pricing_llms) · [mattriemer/LLMCartel](https://github.com/mattriemer/LLMCartel) · [EmanueleLM/focal-points](https://github.com/EmanueleLM/focal-points) · [andyjliu/llm-agent-collusion](https://github.com/andyjliu/llm-agent-collusion) · [umass-ai-safety/colosseum](https://github.com/umass-ai-safety/colosseum) · [Jerick-1380/LLM-Trust-Breaking](https://github.com/Jerick-1380/LLM-Trust-Breaking) · [linhkid/TraceGuard](https://github.com/linhkid/TraceGuard) · [Ostailor/Steganographic_Collusion](https://github.com/Ostailor/Steganographic_Collusion) · [smojha/collusive-llm-agents](https://github.com/smojha/collusive-llm-agents) · [AgentSafety2025/LLM-Agent-collusion](https://github.com/AgentSafety2025/LLM-Agent-collusion)
- Pre-sprint survey (from the talk chat): https://apartresearch.notion.site/2b0fcfd1de9d8080ac3ac4c41a78c8f8 (it also marks you as an active participant).
- Past sprints and winners: [apartresearch.com/sprints](https://apartresearch.com/sprints) (open a sprint → Overview tab → winners). Example saved in [examples/](examples/).
