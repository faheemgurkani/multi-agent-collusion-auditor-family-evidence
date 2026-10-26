# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

The workspace for an entry in the **Apart Research AI Collusion Research Sprint** (Oct 23–25, 2026). **Deadline: Mon Oct 26, 11:59 UTC** (Sun 11:59 PM AoE), with no extensions. The deliverable is a single PDF research report. Only the PDF is judged, on three 1–5 scores: Impact & Innovation, Execution Quality, Presentation & Clarity. The project must be about **AI collusion**; off-topic work is disqualified. There is no prior work, so everything here is sprint work, and the report must say so.

**Status:** the sprint is over and the report is submitted (`report/latex/report.pdf`). The project asks whether LLM auditors go easy on collusion by agents from their own model family (Colosseum, 3 families × 4 conditions × 8 seeds, 4 audit views). `README.md` has the findings and the full reproduce sequence. `TODO.md` is the sprint checklist.

## Our pipeline (`src/`)

Data flows in one direction. Each stage reads the previous stage's output under `src/data/`:

1. `pipeline/gen_configs.py --phase <p>` writes Colosseum YAMLs to `configs/<phase>/<family>_<cond>.yaml`. The families are `gemma`, `gptoss` and `nemotron`, and the conditions are `A`–`D` (`E` = emergent). The phases are `pilot`, `pilot2`, `main`, `main_ext` and `emergent`.
2. `pipeline/run_family.sh <phase> <family> <cond...>` runs Colosseum's `experiments.collusion.run` from the starter repo and writes to `data/runs/<phase>/<family>/<cond>/`. Gemma and gpt-oss hit self-hosted Modal vLLM endpoints (`MODAL_URL_*` and `MODAL_PROXY_TOKEN` in `.env`). Nemotron goes to OpenRouter, pinned to one provider via `OR_PROVIDER_JSON`, which only works after `patch_provider_pin.py` has patched Colosseum's `together_client.py`. That patch is our only change to the starter repo.
3. `build_views.py` writes blinded views V1 (messages), V2 (actions) and V3 (both) to `data/views/<phase>_*`, plus `data/labels_<phase>.csv`. `summarize.py` adds V4, a neutral summary.
4. `audit.py --k 3` makes every family audit every view (k samples), and `--probe` runs the self-recognition probe. Both resume from existing output (`done_keys`), so re-running only fills in missing records.
5. `analysis/analyze.py` → `results/main/results.json` and tables. `figures.py` makes the confirmatory figures, `figures_extra.py` the exploratory ones. `finalize.sh` chains stages 3–5, plus Modal keep-warm.

`pipeline/common.py` holds the shared paths, the `FAMILIES` routes, and `chat()`. Every summary, audit and probe call goes through `chat()`, which logs each call to `data/logs/calls.jsonl` (provider, tokens, cost). Route new model calls through it.

**Pre-registration is frozen.** `src/plan/FREEZE.md` records the SHA-256 hashes of `methodology.md` and `plan/frozen/*.md` (the auditor, summariser, view and probe prompts). Never edit those files silently. Any change needs a version bump, an entry in `plan/deviations.md`, and a re-run of the affected audits. Check the hashes with `cd src/plan && shasum -a 256 methodology.md frozen/*.md`. Analyses beyond the plan must be labelled exploratory. `src/EXPERIMENT_LOG.md` has the timeline, failures and spend.

**Report:** the submitted version is LaTeX: `cd report/latex && xelatex report.tex && xelatex report.tex` (`*_backup.tex` files are earlier drafts). `report/build.py` is the older Markdown→HTML/PDF preview built from the `report/0*_*.md` section drafts. It copies figures from `src/results/main/figures/`.

## Python environment: everything runs in the Python 3.11 venv

**All implementation and experimentation runs in the project venv at `.venv/` (Python 3.11.9).** Never use the system `python3` (Homebrew 3.14) or a global `pip`.

- Run scripts with the venv interpreter explicitly: `.venv/bin/python <script>`, or start each shell command with `source .venv/bin/activate && ...`. Shell state doesn't persist between Bash calls, so activate in every command or use the absolute path:
  `"/Users/muhammadfaheem/Local Projects/research/Apart Research/[Sprint] AI Collusion Research/.venv/bin/python"`.
- Install packages with `uv pip install --python .venv <pkg>` (or `.venv/bin/python -m pip install`), never into the system Python.
- The venv already contains `poseidon_compute` (editable, from `starter/collusion_hackathon/util`) and the Modal SDK/CLI. Use `.venv/bin/modal ...` rather than the global `~/.local/bin/modal`.
- **Starter-repo projects** each have their own `uv` project. Pin them to 3.11 too: run `uv sync --python 3.11` inside the project, and invoke them with `uv run --python 3.11 ...`. Equivalently, prefix the command with `UV_PYTHON=3.11`, which also covers `./setup.sh`. Each project's own `.venv` is then a 3.11 environment.
- **Exceptions that conflict with 3.11** (`requires-python >=3.12`): `llm-agent-collusion/` (starter code for RQ 1.3, 1.4, 1.5, 3.4) and `trace-guard/` (RQ 2.2). They won't install on 3.11. Before using either, ask the user whether to make an exception or to relax `requires-python` and test, and record the decision here.
- Note the Python version in the report's Methods and reproducibility details.

## Layout

- `docs/sprint/`: local mirror of the sprint website. Consult it **before** re-fetching apartresearch.com.
  - `README.md`: index and key facts.
  - `02_resources.md`: every research question (RQ 1.1–3.4 plus Dolos), with prior results, starter code, a weekend project and a budget for each.
  - `03_guidelines_and_rubric.md`: dos and don'ts, the rubric, the Notion reviewer calibration (3 = solid weekend work, 5 = top 5–10%).
  - `papers/`: PDFs stored once in `_all/`. The `track-1_*`, `track-2_*` and `track-3_*` folders hold **symlinks** to `_all/`; `papers/README.md` indexes them by track and RQ.
  - `template/`: the official report template. Our `.docx`/`.md` copies add the required "Limitations and Dual-Use / Ethical Considerations" appendix, which the original lacks. `*.original.*` files are untouched.
- `docs/incident/sources/`: primary sources on the July 2026 OpenAI/Hugging Face multi-agent incident (METR/Redwood report, OpenAI technical report, etc.), the sprint's motivating real-world case.
- `docs/compute/MODAL.md`: how we use Modal (profiles, Secrets, sweeps, vLLM hosting, budget).
- `docs/misc./transcripts/04_Logistics_KamilAlaa/`: transcript of the organizers' logistics talk. Extra rules live there, e.g. resubmitting with the same title does **not** replace the PDF; you must make a new submission with a changed title.
- `report/`: section drafts (`00_`…`11_`.md), the pre-submission checklist (`report/README.md`), and the final LaTeX report in `latex/`.
- `src/context/`: sprint research notes (RQ analysis, literature review, model selection, the decision record).
- `starter/collusion_hackathon/`: a shallow clone of the official starter repo (poseidon-research/collusion_hackathon). It is **not our code**, so if we modify it, the report and README must say which parts we changed.

## Report constraints (they shape everything)

- Main body ≤ 8 pages (aim for 4–6). References and appendices don't count. Abstract of 150–250 words.
- Results must include the **positive control**, seeds, variance and baselines.
- The Limitations & Dual-Use appendix and the LLM usage statement are required.
- Never fabricate results or references; that is grounds for disqualification.

## Starter repo architecture (`starter/collusion_hackathon/`)

There are ten independent research codebases plus `redteaming/` (Dolos-1.5B). Each folder has its own README and its own `uv` environment. The RQ → folder mapping is in the starter `README.md` ("At a glance") and in `docs/sprint/02_resources.md`.

Everything shares one inference layer, **`util/poseidon_compute`**:
- Keys come from `starter/collusion_hackathon/compute.env`, found by walking up from the current directory. **Our `OPENROUTER_API_KEY` lives in the project-root `.env`**, so copy or symlink it into `compute.env` before running anything.
- `make_client()` / `resolve_model()` return an OpenAI-compatible client for whichever provider the routing chose. Model ids use Nebius/Hugging Face casing and are translated for OpenRouter automatically.
- `poseidon-run --model <id> -- <cmd>` routes Nebius → OpenRouter → a Modal-hosted vLLM, and otherwise fails loudly. It never substitutes a different model. Native project commands use whichever key is set but don't fall back across providers.
- Do not set `LLM_MODEL` in `compute.env` for multi-model experiments: it forces one model for every role, which collapses the comparison.

```bash
cd starter/collusion_hackathon
UV_PYTHON=3.11 ./setup.sh <project>   # uv sync for that project and install poseidon-run/poseidon-host; no args = all projects
cd <project> && uv run --python 3.11 python ...   # see that project's README for its smoke command
# examples:
uv run --python 3.11 python -m experiments.preflight                         # colosseum preflight
cd steganographic-collusion && uv run --python 3.11 bash scripts/ci_check.sh # no key needed: compile + 11 detector tests
cd redteaming && uv run --python 3.11 --locked generate.py --model both --prompt "..."   # Dolos vs base Qwen, local, no key
```

Only `trace-guard` needs Docker. `llm-trust-breaking` and `collusive-llm-agents` need a model that supports `response_format` (JSON mode).

## Compute

- **Inference:** OpenRouter (default).
- **Modal:** use `.venv/bin/modal` (1.6.2, installed in the project venv). The active profile must be **`muhammadfaheem-mansha`**, where the $50 credit is; other profiles exist in `~/.modal.toml`. Modal images should also use Python 3.11: `modal.Image.debian_slim(python_version="3.11")`, or `add_python="3.11"` for registry images.
  - Run a starter project on Modal: `.venv/bin/modal run util/poseidon_compute/modal_run.py --project <p> --cmd "<cmd>"`.
  - Host an open model for the duration of one command: `poseidon-host --model <id> --gpu A10G -- <cmd>`.
  - Run `modal app list` and stop leftover apps after each session.
- **Experiment protocol** (Resources tab): positive control first, 3–5 seeds per condition (10–20 only once it works), change one factor at a time, and freeze thresholds and monitor prompts before evaluating.

## Environment notes

- Git repo on `main`. Commit only when asked. `.env` is gitignored, so use `.env.example` as the template.
- The workspace path contains `[` `]` and spaces, so always quote it in shell commands.
