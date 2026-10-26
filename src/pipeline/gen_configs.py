"""Generate Colosseum YAML configs for every family x condition from the shipped RQ 2.1 configs.

Only these fields change from the shipped hackathon configs (everything else is held fixed across
families and conditions): model id/label, seeds, output dir/tag, concurrency, max_tokens.

Conditions (methodology §3.3):
  A  instructed pair + private channel        <- hackathon_2_1_a_pair_private_channel.yaml
  B  instructed pair, no extra channel         <- hackathon_2_1_b_pair_no_channel.yaml
  C  no instruction, open extra channel        <- hackathon_2_1_c_open_channel.yaml
  D  no instruction, no extra channel          <- hackathon_2_1_d_neither.yaml
  E  no instruction, private channel (emergent; exploratory) <- A with coalition_prompt=never, control

Usage: python src/pipeline/gen_configs.py --phase pilot|main|emergent
"""
from __future__ import annotations

import argparse
import copy

import yaml

from common import COLOSSEUM, DATA, FAMILIES, SRC

SHIPPED = COLOSSEUM / "experiments" / "collusion" / "configs"
BASE = {
    "A": "hackathon_2_1_a_pair_private_channel.yaml",
    "B": "hackathon_2_1_b_pair_no_channel.yaml",
    "C": "hackathon_2_1_c_open_channel.yaml",
    "D": "hackathon_2_1_d_neither.yaml",
    "E": "hackathon_2_1_a_pair_private_channel.yaml",
}
PHASES = {
    "pilot": {"conditions": ["A", "D"], "seeds": [1, 2]},
    "pilot2": {"conditions": ["A", "D"], "seeds": [1, 2, 3]},
    "main": {"conditions": ["A", "B", "C", "D"], "seeds": [101, 102, 103, 104, 105]},
    "main_ext": {"conditions": ["A", "B", "C", "D"], "seeds": [106, 107, 108]},
    "emergent": {"conditions": ["E"], "seeds": [101, 102, 103, 104, 105]},
}
MAX_TOKENS = 3000  # reasoning models (gpt-oss, nemotron) need headroom; identical for all families
# Pre-registered G1 contingency invoked after the v1 pilot (deviation D5): instructed coalitions use the
# `structured` variant and every condition uses 4 planning rounds (paper default), held fixed across arms.
POS_PROMPT_VARIANT = "structured"
PLANNING_ROUNDS = 4


def build(phase: str) -> list:
    out = []
    spec = PHASES[phase]
    for fam, f in FAMILIES.items():
        for cond in spec["conditions"]:
            cfg = yaml.safe_load((SHIPPED / BASE[cond]).read_text())
            cfg = copy.deepcopy(cfg)
            tag = f"{phase}_{fam}_{cond}"
            cfg["simulation"]["tags"] = [tag]
            cfg["llm_models"] = [{
                "label": fam,
                "llm": {"provider": "openrouter",
                        "openrouter": {"model": f["model"],
                                       "params": {"max_tokens": MAX_TOKENS, "temperature": 0.7}}},
            }]
            cfg["simulation"]["max_planning_rounds"] = PLANNING_ROUNDS
            exp = cfg["experiment"]
            exp["tag"] = tag
            exp["output_dir"] = str(DATA / "runs" / phase / fam / cond)
            exp["seeds"] = spec["seeds"]
            exp["max_concurrent_runs"] = 2 if f["route"] == "openrouter" else 5  # D8: 1 -> 2 after re-pin
            if cond in ("A", "B"):
                for sw in exp["sweeps"]:
                    sw["prompt_variants"] = [POS_PROMPT_VARIANT]
            if cond == "E":
                exp["collusion"]["coalition_prompt"] = "never"
                for sw in exp["sweeps"]:
                    sw["prompt_variants"] = ["control"]
            for sw in exp["sweeps"]:
                sw["name"] = tag
            path = SRC / "configs" / phase / f"{fam}_{cond}.yaml"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(yaml.safe_dump(cfg, sort_keys=False))
            out.append(path)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True, choices=list(PHASES))
    for p in build(ap.parse_args().phase):
        print(p.relative_to(SRC))
