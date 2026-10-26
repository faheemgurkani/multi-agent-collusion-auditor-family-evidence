# 06: Starter code: what to build on

Source: `starter/collusion_hackathon/` READMEs (top-level, `COMPUTE.md`, `colosseum/`, `llm-agent-collusion-2/`, `llm-trust-breaking/`) and a code read of `colosseum/experiments/collusion/{run.py,prompts.py,metrics.py}` plus configs.

| Project | Serves | Python 3.11? | Logs words? | Logs actions? | Ground truth? | Fit for us |
|---|---|---|---|---|---|---|
| **colosseum** | 2.1, 2.3, 3.1 | ✅ (README uses 3.11) | ✅ `blackboard_*.txt` | ✅ `tool_events.json` | ✅ colluders and condition known | **Primary harness** |
| llm-agent-collusion-2 | 3.2 | ✅ (≥3.10) | ✅ secret channel | ✅ game moves | ✅ alliance assignment | Secondary (3.2 trusted-agent angle) |
| llm-trust-breaking | 2.2, 3.3 | ✅ (≥3.10) | ✅ plan / announce | ✅ act | ✅ deception typology | Secondary (say-vs-do baseline) |
| focal-points | 1.2, 1.3, 3.3 | ✅ | n/a | answers | benign by design | **Benign control** (agreement with no collusion) |
| steganographic-collusion | 2.3 | ✅ | ✅ (1,737 stored runs) | ✅ | ✅ | Offline evidence corpus (no-key path) |
| llm-agent-collusion | 1.3–1.5, 3.4 | ❌ ≥3.12 | ✅ | ✅ | ✅ | Only with a 3.12 exception |
| trace-guard | 2.2 | ❌ ≥3.12, Docker | n/a | n/a | n/a | Reuse the **rubric text** only |

## Colosseum mechanics that matter

- **Environments:** JiraTicket (default in the hackathon configs; `max_tasks: 8`) and Hospital scheduling. Both are DCOPs (distributed constraint optimisation problems) from the vendored CoLLAB, so there is an **optimal joint assignment** to measure regret against.
- **Communication:** blackboards shared along a `topology` (the hackathon uses `path`, 4 agents). A "secret channel" adds a coalition-only blackboard; `extra_channel_members: all` makes it open to everyone.
- **Knobs (config only, no code):** `coalition_prompt: auto|always|never`, `secret_channel_enabled`, `colluder_selection` (`first_and_last` = path endpoints that share no blackboard), `prompt_variants` (`control`, `simple`, `deception`, `structured`, `aggressive`), and **`prompt_variant_overrides`** for arbitrary custom prompt text, plus `seeds`, `max_planning_rounds` (paper 4, hackathon 2), `num_agents` (paper 6, hackathon 4), and model id per run.
- **Metrics:** `coalition_advantage_mean` (coalition mean reward minus non-coalition mean), regret against optimal, violations, per-blackboard post counts, and per-agent rewards in `final_summary.json`.
- **Judge:** `judge_blackboards.py --root <run> --judge-model <id>` uses the paper's rubric over the coalition channel.
- **Cost:** the positive control is ~20 calls. Each run prints an estimate and asks before spending (`-y` skips).
- **Caveat from its README:** a single cheap seed can make coalition advantage come out negative; the effect only appears with 3–5 seeds and 4 planning rounds.

## Implication

A merged Track 2 + 3 project can run **entirely on Colosseum**: the four matched conditions give labelled positives and negatives; words and actions are logged separately; the judge script gives a starting auditor; and custom prompts let us manipulate task framing without touching code. Engineering effort concentrates in (i) an analysis and judging layer in `src/` and (ii) at most one small environment change (e.g. a channel or tool variant for 3.1).
