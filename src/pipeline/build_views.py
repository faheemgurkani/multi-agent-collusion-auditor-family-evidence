"""Build blinded auditor views V1-V3 and the label table from Colosseum run outputs (methodology §4.1).

For each completed run (has metrics.json):
  src/data/views/<tid>/meta.json   n_agents, agent names (no labels shown to auditors)
  src/data/views/<tid>/V1.txt      environment header + all message-board posts (board id, members)
  src/data/views/<tid>/V2.txt      environment header + non-message actions in order + final allocation
  src/data/views/<tid>/V3.txt      environment header + messages and actions interleaved in protocol order
  src/data/labels.csv              one row per transcript: family, condition, seed, label, colluders,
                                   coalition advantage, regret, joint reward, ... (NEVER shown to auditors)

Environment header (identical in every view, deviation D4): the public task list plus each agent's
private profile (availability, skills, private task costs), parsed from the agents' own planning
prompts. Coalition instructions (present only in colluders' system prompts) are never included.
Blinding: no model ids, provider, condition, seed, run id or file paths appear in any view.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

from common import DATA

VIEWS = DATA / "views"


def section(text: str, header: str) -> str:
    m = re.search(rf"=== {re.escape(header)} ===\n(.*?)(?:\n===|\Z)", text, re.S)
    return m.group(1).strip() if m else ""


def env_header(run: Path, agents: list[str]) -> str:
    prompts = json.loads((run / "agent_prompts.json").read_text())
    tasks, profiles = "", {}
    for p in prompts:
        name, up = p.get("agent_name"), p.get("user_prompt") or ""
        if name in profiles or not up:
            continue
        tasks = tasks or section(up, "TASKS (PUBLIC)")
        profiles[name] = (section(up, "YOUR PRIVATE STATE"), section(up, "YOUR COSTS (PRIVATE)"))
    lines = ["ENVIRONMENT", "Tasks (public):", tasks, "", "Agents' private profiles (visible to the auditor):"]
    for a in agents:
        st, co = profiles.get(a, ("(not available)", ""))
        lines += [f"- {a}:", "  " + st.replace("\n", "\n  "), "  Private costs:",
                  "  " + co.replace("\n", "\n  ")]
    return "\n".join(lines)


def board_membership(bbs: list) -> str:
    return "\n".join(f"- Board {b['blackboard_id']}: members {', '.join(sorted(b['participants']))}"
                     for b in bbs)


def build_one(run: Path, phase: str) -> dict | None:
    if not (run / "metrics.json").exists():
        return None
    rc = json.loads((run / "run_config.json").read_text())
    m = json.loads((run / "metrics.json").read_text())
    fs = json.loads((run / "final_summary.json").read_text())
    te = json.loads((run / "tool_events.json").read_text())
    bbs = json.loads((run / "blackboards.json").read_text())
    fam, cond = rc["model_label"], rc["sweep"].split("_")[-1]
    seed = rc["seed"]
    agents = sorted(rc["roles"].keys())
    tid = f"{phase}_{fam}_{cond}_s{seed}"
    header = env_header(run, agents)
    msgs, acts, both = [], [], []
    for e in te:
        a = e.get("arguments") or {}
        stage = f"[{e.get('phase')}{'' if e.get('planning_round') is None else ' round ' + str(e['planning_round'])}]"
        if e["tool_name"] == "post_message":
            line = f"{stage} Board {a.get('blackboard_id')} | {e['agent_name']}: {a.get('message', '')}"
            msgs.append(line)
            both.append("MESSAGE " + line)
        else:
            res = e.get("result")
            res_s = json.dumps(res, ensure_ascii=False)[:300] if res is not None else ""
            line = f"{stage} {e['agent_name']} called {e['tool_name']}({json.dumps(a, ensure_ascii=False)}) -> {res_s}"
            acts.append(line)
            both.append("ACTION " + line)
    alloc = "\n".join(f"- {k}: {v}" for k, v in sorted((fs.get("assignment") or {}).items()))
    member = board_membership(bbs)
    v1 = f"{header}\n\nMESSAGE BOARDS\n{member}\n\nMESSAGES (in order)\n" + "\n".join(msgs or ["(no messages)"])
    v2 = f"{header}\n\nACTIONS (in order)\n" + "\n".join(acts or ["(no actions)"]) + f"\n\nFINAL ALLOCATION\n{alloc}"
    v3 = (f"{header}\n\nMESSAGE BOARDS\n{member}\n\nEVENTS (messages and actions, in order)\n"
          + "\n".join(both) + f"\n\nFINAL ALLOCATION\n{alloc}")
    out = VIEWS / tid
    out.mkdir(parents=True, exist_ok=True)
    for name, txt in [("V1", v1), ("V2", v2), ("V3", v3)]:
        (out / f"{name}.txt").write_text(txt + "\n")
    (out / "meta.json").write_text(json.dumps({"n_agents": len(agents), "agents": agents}))
    return {
        "transcript_id": tid, "phase": phase, "family": fam, "condition": cond, "seed": seed,
        "label": int(cond in ("A", "B")), "colluders": "|".join(sorted(rc.get("colluders") or [])),
        "coalition_advantage": m.get("coalition_advantage_mean"), "system_regret": m.get("system_regret"),
        "mean_regret": m.get("mean_regret"), "joint_reward": fs.get("joint_reward"),
        "joint_reward_ratio": fs.get("joint_reward_ratio"), "violations": fs.get("violations"),
        "tasks_done": fs.get("tasks_done"), "status": m.get("status"),
        "colluder_posts_total": m.get("colluder_posts_total"), "colluder_posts_secret": m.get("colluder_posts_secret"),
        "n_messages": len(msgs), "n_actions": len(acts), "v3_chars": len(v3),
        "run_dir": str(run.relative_to(DATA)),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True)
    a = ap.parse_args()
    rows = []
    for mpath in sorted((DATA / "runs" / a.phase).rglob("metrics.json")):
        r = build_one(mpath.parent, a.phase)
        if r:
            rows.append(r)
    path = DATA / f"labels_{a.phase}.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["transcript_id"])
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} transcripts -> {path.name}")


if __name__ == "__main__":
    main()
