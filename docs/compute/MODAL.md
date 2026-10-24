# Using Modal for our evaluations

Compiled 2026-10-24 from the Modal docs (via Context7: `/llmstxt/modal_llms-full_txt`, `/modal-labs/modal-examples`), the starter repo's `COMPUTE.md` and `util/poseidon_compute/`, and a web search for pricing.

**Credits:** $50 sprint credit on the Modal account **muhammadfaheem.mansha@gmail.com**.

## 0. When do we need Modal at all?

| Need | Use |
|---|---|
| Calling GPT / Claude / Gemini / most open models | **OpenRouter** (key in `.env`). Instant, no Modal needed. |
| Long or parallel runs (sweeps over seeds and conditions) you don't want on the laptop | **Modal CPU containers** (`modal_run`, §4) |
| A model on **no** provider (custom fine-tune, off-catalog open model), or vLLM-level control (logprobs, guided decoding, exact weight pinning) | **Modal GPU + vLLM** (§5) |
| Dolos-1.5B red-teaming on a GPU instead of the laptop | **Modal GPU** function (§6) |

Rule of thumb: inference goes through OpenRouter; Modal is for *where code runs* or *hosting a model OpenRouter lacks*.

## 1. One-time setup: authenticate as the right account

The CLI is not installed on this machine yet, but `~/.modal.toml` already holds 4 profiles: `faheemgurkani` (**currently active**), `muhammadfaheem-mansha`, `i220485`, `seecs`. The credits sit on the muhammadfaheem.mansha@gmail.com workspace, which is presumably the `muhammadfaheem-mansha` profile.

```bash
uv pip install --python .venv modal   # project venv (Python 3.11); then use .venv/bin/modal
modal profile list             # shows profiles and which is active
modal profile activate muhammadfaheem-mansha
modal profile current          # confirm
```

- If that profile's token is stale, or it belongs to a different workspace, create a fresh one. This opens the browser; sign in as muhammadfaheem.mansha@gmail.com:
  ```bash
  modal token new --activate --verify
  ```
- **Confirm the credits** on the dashboard (modal.com → Settings → Usage & Billing) for that workspace **before** launching GPU jobs.
- For a single command you can pin the profile without switching globally: `MODAL_PROFILE=muhammadfaheem-mansha modal run ...`

## 2. Secrets: getting the OpenRouter key into containers

Our key lives in the project-root `.env` (`OPENROUTER_API_KEY`). Never bake keys into images. Three options:

```python
# (a) Load from a local .env at launch time (simplest)
@app.function(secrets=[modal.Secret.from_dotenv(path="/abs/path/to/project")])   # reads <path>/.env
def run(): ...

# (b) A named Secret stored in Modal (create once, reuse everywhere)
#     CLI: modal secret create openrouter OPENROUTER_API_KEY=sk-or-...
@app.function(secrets=[modal.Secret.from_name("openrouter")])
def run(): ...
```

(c) **For the starter repo:** it reads `starter/collusion_hackathon/compute.env`, and its `modal_run` injects that file as a Secret automatically (falling back to a named Secret called `hackathon-keys`). Make it point at our key:

```bash
cd starter/collusion_hackathon
cp compute.env.example compute.env      # then put OPENROUTER_API_KEY=... in it (copy from ../../.env)
# or keep one source of truth:  ln -s ../../.env compute.env
```

Inside the container, the values appear as ordinary environment variables (`os.environ["OPENROUTER_API_KEY"]`).

## 3. Core concepts (cheat sheet)

```python
import modal
app = modal.App("collusion-eval")
image = modal.Image.debian_slim(python_version="3.11").uv_pip_install("openai==1.*", "pandas")
vol = modal.Volume.from_name("collusion-results", create_if_missing=True)   # persistent storage

@app.function(image=image, secrets=[modal.Secret.from_name("openrouter")],
              volumes={"/results": vol}, timeout=60 * 60, retries=2)
def run_episode(seed: int, condition: str) -> dict:
    ...                                   # one game/episode; calls OpenRouter
    with open(f"/results/{condition}_{seed}.json", "w") as f: ...
    vol.commit()                          # persist writes
    return {...}

@app.local_entrypoint()
def main():
    jobs = [(s, c) for c in ["control", "treatment"] for s in range(5)]
    for r in run_episode.starmap(jobs, return_exceptions=True):   # parallel fan-out across containers
        print(r)
```

| Command | What it does |
|---|---|
| `modal run file.py` | Runs `@app.local_entrypoint()` once; the app is torn down after. **Use this for experiments.** |
| `modal run file.py::fn --arg x` | Runs a specific function |
| `modal serve file.py` | Hot-reloading dev server for web endpoints (stops when you Ctrl-C) |
| `modal deploy file.py` | Persistent deployment. Call later with `modal.Function.from_name("app", "fn")`. **Remember to stop it.** |
| `modal app list` / `modal app stop <name>` | See and stop running apps (stop anything idle to save credits) |
| `modal volume get collusion-results /` | Download results locally |
| `modal secret list` | List stored secrets |

- `Function.map(iterable)` runs one input per container in parallel, with ordered outputs (`order_outputs=False` for completion order). `return_exceptions=True` keeps one failed seed from killing the sweep.
- `timeout` is per input (seconds). `retries` re-runs failed inputs.
- `.remote(...)` is one call; `.spawn(...)` is fire-and-forget.

## 4. Running a starter-repo project on Modal (CPU, parallel or long runs)

From `starter/collusion_hackathon/` (after `./setup.sh <project>` and §2c):

```bash
modal run util/poseidon_compute/modal_run.py --project llm-cartel --cmd "uv run python run_game.py --rounds 30"
# optional GPU for [gpu] extras:
modal run util/poseidon_compute/modal_run.py --project llm-cartel --gpu a10g --cmd "uv run python steering/<script>.py"
```

`modal_run` builds an image containing the project, injects `compute.env` as a Secret, and runs the command with a 1-hour timeout. The starter's `COMPUTE.md` notes that colosseum topology sweeps and the ~8k-call llm-trust-breaking full run are good Modal candidates.

## 5. Hosting an open model with vLLM (an OpenAI-compatible endpoint)

**Easiest: use the starter's helper.** It boots the model, points the shared client at it, and tears it down on exit, so no GPU is left running:

```bash
poseidon-host --model Qwen/Qwen2.5-7B-Instruct --gpu A10G -- <experiment command>
# or let routing decide (Nebius -> OpenRouter -> Modal):
poseidon-run --model <id> -- <experiment command>
```

Defaults (`util/poseidon_compute/modal_serve.py`): model `Qwen/Qwen2.5-7B-Instruct`, GPU `A10G`, `scaledown_window=300` (spins down after 5 minutes idle), ready-wait up to 15 minutes. GPU sizing guide: **A10G (24 GB) up to ~8B · A100-40GB up to ~32B · H100 for 70B.** Gated models (Llama, Gemma) need `modal secret create huggingface HF_TOKEN=hf_...`.

**Rolling our own** (Modal's standard pattern):

```python
import modal, subprocess
MINUTES = 60
vllm_image = (modal.Image.from_registry("nvidia/cuda:12.8.0-devel-ubuntu22.04", add_python="3.11")
              .uv_pip_install("vllm==0.13.0", "huggingface-hub==0.36.0")
              .env({"HF_HUB_CACHE": "/root/.cache/huggingface"}))
hf_cache = modal.Volume.from_name("huggingface-cache", create_if_missing=True)  # avoid re-downloading weights
app = modal.App("collusion-vllm")

@app.function(image=vllm_image, gpu="A10G", volumes={"/root/.cache/huggingface": hf_cache},
              timeout=24 * 60 * MINUTES, scaledown_window=5 * MINUTES)
@modal.concurrent(max_inputs=32)                 # many requests per GPU container
@modal.web_server(port=8000, startup_timeout=15 * MINUTES)
def serve():
    subprocess.Popen(["vllm", "serve", "Qwen/Qwen2.5-7B-Instruct",
                      "--host", "0.0.0.0", "--port", "8000", "--api-key", "<pick-a-token>"])
```

`modal deploy` prints a URL. Use it from any OpenAI client:

```python
from openai import OpenAI
client = OpenAI(base_url="https://<workspace>--collusion-vllm-serve.modal.run/v1", api_key="<pick-a-token>")
```

The newer Modal examples use an `@app.server(...)` class with GPU memory snapshots for faster cold starts. The `web_server` pattern above is simpler and is what the starter repo uses. **Cold start is ~2–5 minutes for a small model**, so batch requests and keep the server up only while a sweep runs, then `modal app stop collusion-vllm`.

## 6. Dolos-1.5B on a Modal GPU (optional)

It runs fine on a 16 GB laptop, but sweeps or activation work are faster on a GPU. Wrap the starter's `redteaming/generate.py` logic in an `@app.function(gpu="T4" or "L4", volumes={hf cache})` that loads Qwen2.5-1.5B-Instruct's tokenizer and config plus Dolos's `model.safetensors` (about 6.2 GB, cached in a Volume). A T4 or L4 is plenty for 1.5B parameters.

## 7. Budget: making $50 last

Approximate on-demand rates from third-party pricing trackers (July 2026). **Check these at [modal.com/pricing](https://modal.com/pricing) before relying on them**:

| GPU | ≈ $/hr | ≈ hours for $50 |
|---|---|---|
| T4 | 0.59 | ~85 |
| L4 | 0.80 | ~62 |
| A10G | ~1.10 | ~45 |
| L40S | 1.95 | ~25 |
| A100 80GB | 2.50 | ~20 |
| H100 | 3.95 | ~12 |

CPU containers cost far less than GPUs. Billing is per second, but pinning a **region** or requesting non-preemptible capacity reportedly multiplies the rate (1.5–3×), so leave those unset.

**Credit hygiene**
- Prefer `modal run` (auto teardown) over `modal deploy`.
- Always set `scaledown_window` (e.g. 300 s) and a `timeout`.
- Run `modal app list` at the end of every session and `modal app stop` anything left over.
- Use the smallest GPU that fits the model. Cache weights in a Volume.
- Note the spend for the report's reproducibility and cost section.

## Sources
- Modal docs via Context7: `modal token new`, `modal profile activate`, `Secret.from_dotenv`, `Function.map`, `Function.from_name` (modal.com/docs/cli/latest/token, /cli/latest/profile, /sdk/py/latest/Secret, /reference/modal.Function, /guide/scale, /guide/trigger-deployed-functions)
- Modal examples: `06_gpu_and_ml/llm-serving/vllm_low_latency.py`, `openai_compatible/client.py` (github.com/modal-labs/modal-examples)
- Starter repo: `starter/collusion_hackathon/COMPUTE.md`, `util/poseidon_compute/{modal_run,modal_serve,hosted_model}.py`
- Pricing (third-party, verify): [usagepricing.com Modal calculator](https://usagepricing.com/tools/pricing-calculator/modal), [computeprices.com](https://computeprices.com/compare/compute-vs-modal), [Spheron: Modal GPU pricing 2026](https://www.spheron.network/blog/modal-gpu-pricing-2026-per-second-billing/)
