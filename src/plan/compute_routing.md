# Compute routing and parallelisation plan (supersedes methodology §8 "Plan")

Written 2026-10-25, after the freeze. **Infrastructure only:** prompts, models, views, k, gates and analysis are unchanged. Logged in [deviations.md](deviations.md) as D1.

## 1. Routing: one fixed route per family

The same route serves every agent and auditor call within a family. Mixing providers within a family could change the weights' precision and confound the family effect.

| Family | Model | Route | Why | Billing |
|---|---|---|---|---|
| Google | Gemma 4 31B IT (`google/gemma-4-31b-it`) | **Modal Dedicated Endpoint** (in the Modal Library) | No daily cap, high concurrency | Modal GPU time, **our $70 credit** |
| OpenAI open-weight | GPT-OSS-120B (`openai/gpt-oss-120b`) | **Modal Dedicated Endpoint** (in the Modal Library) | Avoids the paid OpenRouter balance | Modal GPU time, credit |
| NVIDIA | Nemotron 3 Super 120B A12B | **OpenRouter free tier** (`:free`, provider Nvidia); paid fallback on the same provider | Not in the Modal Library (only Nemotron 3.5 Super VL NVFP4, which is a different model) | Free: 1,000 req/day, 20 req/min. Paid fallback about $3.50 worst case |
| Neutral summariser | DeepSeek V4 Flash (`deepseek/deepseek-v4-flash`) | OpenRouter paid | 60 calls only | about $0.05 |

**Notes:**
- Modal endpoints bill only while containers run (they scale to zero). Library models are deployed with `modal endpoint create --model <hf-id>`; Modal picks the serving recipe and GPU.
- **Never** pass `--compute-region` / `--colocate-compute`: they trigger a 1.15–1.75× region multiplier.
- Credit caveat: Modal's docs say plan credits can't pay for *Shared* Endpoints. **Dedicated** Endpoints bill as normal compute, so the credit applies. Confirm on the dashboard after the first hour.

## 2. Calls per family (main study plus pilot)

| Stage | Per family | Total |
|---|---|---|
| Pilot agents (4 runs × ~30 calls) | ~120 | ~360 |
| Main agents (20 runs × ~30 calls) | ~600 | ~1,800 |
| Auditing (60 transcripts × 4 views × k=3) | 720 | 2,160 |
| Recognition probe (60) | 60 | 180 |
| **Per family** | **~1,500** | **~4,500** (+60 summaries) |

**Nemotron on the free tier:** about 1,500 calls fit inside two daily quotas (Sun until 23:59 UTC, then Mon until the deadline): 2 × 1,000. At 20 req/min that's at least 75 minutes of wall time.

## 3. Cost estimate

| Item | Basis | Est. |
|---|---|---|
| Gemma 4 31B on Modal | ~1 H100-class GPU (about $3.95/h) × ~3–4 h endpoint uptime across pilot, main runs and auditing, plus cold starts | $12–18 |
| GPT-OSS-120B on Modal | ~1 H100 (MXFP4) × ~3–4 h | $12–18 |
| Nemotron | free tier; worst case all paid (~7.5M in, 0.5M out at $0.30/$2.40) | $0–3.5 |
| DeepSeek summaries | 60 × ~6k tokens | ~$0.05 |
| **Total** | | **Modal ~$25–36 of $70; OpenRouter ≤ ~$3.5 of the $3.92 balance** |

**Guardrails:**
- Set a Modal spend limit (dashboard) of about $50.
- Stop endpoints between phases (`modal endpoint stop <id>`).
- Run `modal endpoint list` at the end of every session.

## 4. Parallelisation

1. **Three family pipelines run concurrently** as separate processes, each with its own route, so they share no rate limit. Each process sets its own `LLM_BASE_URL` / `LLM_API_KEY` (Modal proxy token `wk-<id>.ws-<secret>`), or the per-model `base_url` in the Colosseum YAML (supported by `colosseum/experiments/common/providers.py`).
2. **Agent runs:** Colosseum `experiment.max_concurrent_runs` set to 6 for the Modal families and 2 for Nemotron (to respect 20 req/min). Seeds and conditions are queued per family.
3. **Streaming hand-off:** as each run finishes, build its views and queue the V4 summary, then its audits. Auditing of family X's transcripts by all three auditors starts while other runs continue. The pilot is processed separately and excluded.
4. **Auditor concurrency:** async workers with per-route limits: Modal endpoints 16–32 in flight; Nemotron a token bucket at 18 req/min with 429 back-off (`Retry-After`); DeepSeek 8 in flight.
5. **Ordering:** pilot (all families in parallel) → G1/G2 check → main runs (parallel) → auditing (parallel, streaming) → analysis. Nemotron's free quota is spent on its agent runs first (the scarcest resource), then its audits; the paid fallback is used only if the quota runs out before the deadline.

## 5. Pilot checks specific to this routing

- **Tool calling works** on each Modal endpoint (Colosseum requires it). If a Library recipe lacks a tool-call parser for a model, fall back to OpenRouter for **all** of that family's calls and log a deviation.
- **Served model id matches** the planned model on every route; log the provider and quantisation per call.
- **Measured throughput and cost per hour** on Modal, used to re-estimate before the main runs.

## 6. Fallbacks (in order)

1. If Nemotron's free quota is exhausted → paid Nemotron (same provider).
2. If the OpenRouter balance is exhausted → top up about $5 (preferred). Alternatively, host the summariser on Modal using a Library model from a **fourth** family (e.g. Qwen3.6 35B A3B FP8). GPT-OSS can't be the summariser because it's one of the audited families.
3. If time or budget is short: the scope cuts in methodology §8 (k 3→2, drop one view, seeds 5→4).
