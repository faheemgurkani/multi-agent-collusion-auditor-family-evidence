## Code and Data

- **Code repository:** [GitHub URL to be added before submission]. It contains `src/pipeline/` (config generation, run launcher, view builder, summariser, auditor, recognition probe), `src/analysis/` (`analyze.py`, `figures.py`; every number and figure in this report is regenerated from raw logs), and `src/plan/` (the pre-registration, frozen prompts with SHA-256 hashes, and the deviations log).
- **Data:** all 96 main and 10 emergent Colosseum episodes (run configs, tool events, blackboards, metrics), the blinded views V1–V4, all 3,456 audit records with raw outputs, recognition-probe outputs, and the per-call cost log.
- **Pre-existing code:** Colosseum (Nakamura et al., 2026), via the sprint starter repository, is third-party code. We modified one file of its LLM client (to forward an OpenRouter provider-pinning field); the patch script is included. Everything else was written during the sprint.
- **Info hazards:** low. The coalition instructions are Colosseum's published prompt variants, and we introduce no new collusion or evasion technique (see the Dual-Use appendix).

## Author Contributions

M.F.M. designed the study, ran the experiments and analysis, and wrote the report.
