# 10: Model selection under the budget constraint (2026-10-25)

**Constraint (confirmed in Discord #help-desk by Kamil, Apart):** no API keys or credits are provided. "OpenRouter has free models if you don't want to pay." The only sponsored compute is **Modal: $70 available** to us.

## 1. Free OpenRouter models (live API, newest first; text models with tool calling)

| Released | Model (`:free`) | Family | Size / type | JSON mode | Notes |
|---|---|---|---|---|---|
| 2026-10-22 | `recursive/flint-v1.0` | Recursive | 40B MoE (2.5B active) | ✓ | coding-agent focus |
| 2026-10-17 | `xingchen-agi/xing4.0-29b-a4b` | TeleAI | 29B MoE (4B active) | ✓ | general |
| 2026-10-15 | `nvidia/nemotron-3.5-super-vl` | NVIDIA | 120B MoE (12B active), multimodal | ✓ | |
| 2026-08-14 | `dots-studio/dots-3-note-preview` | Dots | 280B MoE (16B active) | ✓ | preview |
| 2026-08-11 | `nvidia/nemotron-3.5-lightning` | NVIDIA | 30B MoE (3B active) | – | |
| 2026-07-31 | `thinkingmachines/inkling-small` | Thinking Machines | 276B MoE (12B active) | – | agentic / tool use |
| 2026-07-18 | `thinkingmachines/inkling` | Thinking Machines | 975B MoE (41B active) | – | |
| 2026-07 | `poolside/laguna-s-2.1`, `laguna-xs-2.1` | Poolside | coding agents | – | code-specialised |
| 2026-06-18 | `cohere/north-mini-code` | Cohere | 30B MoE, code | – | code-specialised |
| 2026-06-04 | `nvidia/nemotron-3-ultra-550b-a55b` | NVIDIA | 550B MoE | – | |
| 2026-04-03 | `google/gemma-4-26b-a4b-it` | Google | 25B MoE (3.8B active) | ✓ | |
| 2026-04-02 | **`google/gemma-4-31b-it`** | Google | 31B dense | ✓ | "native function calling" |
| 2026-03-11 | **`nvidia/nemotron-3-super-120b-a12b`** | NVIDIA | 120B MoE (12B active) | ✓ | "built for complex multi-agent applications" |
| 2026-02-01 | `openrouter/free` | router | random free model | ✓ | **unusable for a family study** (the model changes per call) |

**Free-tier limits** ([OpenRouter docs](https://openrouter.ai/docs/api-reference/limits)): **20 requests/min**; **50 requests/day** if the account has bought less than $10 of credit ever, **1,000/day** once at least $10 has been bought. Exceeding returns HTTP 429. Free providers may log prompts; that's acceptable for our synthetic transcripts.

## 2. What Modal provides

- **Modal Library**: open models deployable on Modal, e.g. Gemma 4 (31B, 26B-A4B, E4B), Qwen3.6 27B / 35B-A3B, GPT-OSS 120B, Nemotron 3.5 Lightning / 3 Ultra, Inkling, GLM 5.3, DeepSeek V4 Flash, Kimi K2.6.
- **Shared Endpoints** (per-token, Modal-hosted): ⚠️ the docs say "*Credits included with your plan cannot be used for Shared Endpoint usage*", so they would likely cost real money. Whether the sprint credit counts as "plan" credit is unclear (ask in #help-desk if needed).
- **Dedicated Endpoints / self-hosted vLLM or SGLang** are billed as GPU time, so **our $70 credit applies**. Rough fits:

| Model | GPU | $/hour | ~3–4 h of use |
|---|---|---|---|
| Gemma 4 31B (FP8) | A100 80GB | 2.50 | $8–10 |
| Qwen3.6-35B-A3B (FP8) | L40S 48GB | 1.95 | $6–8 |
| GPT-OSS-120B (MXFP4) | H100 | 3.95 | $12–16 |

  Plus cold starts (minutes per boot) and debugging time.

## 3. Cheap paid fallbacks on OpenRouter (same families, no daily cap)

| Model | $/M in | $/M out | Est. per agent run* |
|---|---|---|---|
| `google/gemma-4-31b-it` | 0.20 | 0.40 | ~$0.04 |
| `nvidia/nemotron-3-super-120b-a12b` | 0.30 | 2.40 | ~$0.08 |
| `openai/gpt-oss-120b` (`:batch` 0.03/0.14) | 0.15 | 0.60 | ~$0.03 |
| `deepseek/deepseek-v4-flash` | 0.09 | 0.18 | ~$0.02 |
| `qwen/qwen3.6-35b-a3b` | 0.10 | 0.95 | ~$0.03 |

\*About 40 calls per run at ~4k input and ~300 output tokens. Reasoning models emit more output tokens, so treat these as lower bounds.

## 4. Call budget vs the free cap

The planned scope is 3 families × 4 conditions × 5 seeds = **60 runs × ~40 calls ≈ 2,400 agent calls**, plus **~540 auditor calls**, for **~3,000 calls**. At 1,000 free requests/day that's about 3 days, so **the free tier alone cannot carry the main experiment** in the time left. It does work for the pilot and for auditing.

## 5. Recommendation

- **Families (agents and auditors, same 3 models):**
  1. **Google Gemma 4 31B** (free on OpenRouter, paid fallback, also in the Modal Library);
  2. **NVIDIA Nemotron 3 Super 120B** (free on OpenRouter, paid fallback);
  3. **OpenAI GPT-OSS-120B** (cheapest paid, also in the Modal Library).

  This gives three distinct developers and pre-training lineages, all tool-calling.
  - Free alternative for #3: `thinkingmachines/inkling-small:free` (paid fallback $0.45/$1.20).
- **Spend:** buy **$10 of OpenRouter credit** once. It (a) lifts the free cap from 50 to 1,000/day, and (b) covers the paid runs: the whole main experiment at paid prices is about **$5–10**.
- **Modal $70:** keep as a backstop. Self-host **Gemma 4 31B** or **GPT-OSS-120B** only if OpenRouter rate limits block us (~$10–20), or for a model OpenRouter lacks.
- **Pilot first:** confirm each model handles Colosseum's tool calls reliably before committing (open models vary).
