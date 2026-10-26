# multi-agent-collusion-auditor-family-evidence

**Who audits the auditors? Do LLM auditors go easy on collusion by their own model family?**

Code, data and report for an entry in the [Apart Research AI Collusion Research Sprint](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25) (23–25 October 2026), co-organised by Apart Research, Poseidon Research and AE Studio. Author: Muhammad Faheem (independent researcher).

**Report:** [report/latex/report.pdf](report/latex/report.pdf). Source: [report/latex/report.tex](report/latex/report.tex).

## Prior work and pre-existing code

**There is no prior work.** The research question, pre-registration, pipeline code, experiment runs, analysis and report were all produced during the sprint (23–26 October 2026).

Pre-existing, third-party code used unchanged except where noted:
- `starter/collusion_hackathon/`: the sprint's starter repository ([poseidon-research/collusion_hackathon](https://github.com/poseidon-research/collusion_hackathon)), including the **Colosseum** environment (Nakamura et al., 2026). We used its shipped RQ 2.1 configurations.
- **One modification:** `src/pipeline/patch_provider_pin.py` patches Colosseum's installed LLM client (`together_client.py`) so it forwards an OpenRouter provider-pinning field (`OR_PROVIDER_JSON`). Nothing else in the starter repository was changed.

## What we found

In 96 Colosseum episodes (3 open-weight agent families × 4 conditions × 8 seeds), every family audited every episode under four views: messages, actions, both, and a neutral summary. That gives 3,456 audits under a plan pre-registered with SHA-256 hashes (`src/plan/FREEZE.md`).
- No significant same-family effect: −0.029 AUROC (95% CI −0.063 to +0.004, permutation p = 0.12).
- Auditors read talk, not outcomes. With actions only, they are at chance (AUROC 0.48). Suspicion tracks how much the pair talked, not what it gained, and counting the word "coalition" alone reaches 0.81 (exploratory).
- A neutral summary lowers detection by about 0.10 AUROC. A cross-family ensemble helps for one agent family.

## Layout

| Path | Contents |
|---|---|
| `src/plan/` | Pre-registration (`methodology.md`), frozen prompts with hashes (`FREEZE.md`, `frozen/`), deviations log |
| `src/pipeline/` | Config generation, run launcher, blinded view builder, V4 summariser, auditor and recognition probe, Colosseum patch |
| `src/analysis/` | `analyze.py` (gates, hypotheses, bootstrap and permutation), `figures.py`, `figures_extra.py` (exploratory analyses) |
| `src/data/` | All Colosseum episodes, blinded views V1–V4, every audit and probe record, per-call token, provider and cost log |
| `src/results/main/` | `results.json`, tables, figures |
| `src/EXPERIMENT_LOG.md` | Timeline, what did not work, dual-use notes, spend |
| [`report/latex/report.pdf`](report/latex/report.pdf) | The report. Source is [`report/latex/report.tex`](report/latex/report.tex) |

## Reproduce

Everything runs on Python 3.11.
```bash
uv venv --python 3.11 .venv && uv pip install --python .venv openai pandas numpy scipy matplotlib pyyaml
cp .env.example .env            # add OPENROUTER_API_KEY (and Modal endpoint URLs/token if self-hosting)
cd starter/collusion_hackathon && UV_PYTHON=3.11 ./setup.sh colosseum && cd ../..
.venv/bin/python src/pipeline/patch_provider_pin.py <path to colosseum's together_client.py>

# agents -> views -> summaries -> audits
.venv/bin/python src/pipeline/gen_configs.py --phase main
./src/pipeline/run_family.sh main gemma A B C D          # likewise gptoss, nemotron; then main_ext
.venv/bin/python src/pipeline/build_views.py --phase main
.venv/bin/python src/pipeline/summarize.py --phase main
.venv/bin/python src/pipeline/audit.py --phase main --k 3
.venv/bin/python src/pipeline/audit.py --phase main --probe

# every number and figure in the report
.venv/bin/python src/analysis/analyze.py --phase main --boot 10000 --perm 5000
.venv/bin/python src/analysis/figures.py --phase main
.venv/bin/python src/analysis/figures_extra.py --phase main
cd report/latex && xelatex report.tex && xelatex report.tex
```
To re-run only the analysis on the released data, run the last block.

## Responsible use

The coalition instructions are Colosseum's published prompt variants. We publish no evasion technique; see the report's Appendix A (Limitations and Dual-Use / Ethical Considerations). No secrets are committed (`.env` is gitignored).
