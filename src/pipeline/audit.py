"""Run the frozen auditor prompt over blinded views (methodology §4.2) and the recognition probe (§4.3).

Input : src/data/views/<transcript_id>/{meta.json, V1.txt, V2.txt, V3.txt, V4.txt}
Output: src/data/audits/audits.jsonl   (one line per auditor x transcript x view x sample)
        src/data/audits/recognition.jsonl
Resumable: (auditor, transcript, view, sample) keys already present are skipped.

Usage: python src/pipeline/audit.py --phase main [--views V1 V2 V3 V4] [--k 3] [--auditors gemma gptoss nemotron]
       python src/pipeline/audit.py --phase main --probe
"""
from __future__ import annotations

import argparse
import json
import random
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from common import DATA, FAMILIES, FROZEN, chat

AUD = DATA / "audits"
AUD.mkdir(parents=True, exist_ok=True)


def split_prompt(path: Path) -> tuple[str, str]:
    t = path.read_text()
    sys_part, user_part = t.split("\nUSER:\n", 1)
    return sys_part.replace("SYSTEM:\n", "", 1).strip(), user_part.strip()


def view_descriptions() -> dict:
    t = (FROZEN / "view_descriptions_v1.md").read_text()
    out = {}
    for key, v in [("V1_MESSAGES", "V1"), ("V2_ACTIONS", "V2"), ("V3_BOTH", "V3"), ("V4_REPORT", "V4")]:
        m = re.search(rf"{key}:\n(.+?)(?:\n\n|\Z)", t, re.S)
        out[v] = m.group(1).strip()
    return out


def parse_json(text: str) -> dict | None:
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def done_keys(path: Path, fields: tuple) -> set:
    if not path.exists():
        return set()
    keys = set()
    for line in path.read_text().splitlines():
        try:
            r = json.loads(line)
            if r.get("parsed") is not None or r.get("final_failure"):
                keys.add(tuple(r[f] for f in fields))
        except Exception:
            continue
    return keys


def transcripts(phase: str) -> list[Path]:
    return sorted(p for p in (DATA / "views").glob(f"{phase}_*") if (p / "meta.json").exists())


def audit_one(auditor: str, tdir: Path, view: str, sample: int, sysp: str, userp: str, vdesc: dict) -> dict:
    meta = json.loads((tdir / "meta.json").read_text())
    transcript = (tdir / f"{view}.txt").read_text()
    s = sysp.replace("{N_AGENTS}", str(meta["n_agents"])).replace("{VIEW_DESCRIPTION}", vdesc[view])
    u = userp.replace("{TRANSCRIPT}", transcript)
    base = {"auditor": auditor, "transcript_id": tdir.name, "view": view, "sample": sample,
            "prompt_version": "v1"}
    for attempt in range(2):  # one retry with the identical prompt on parse failure (§4.2)
        r = chat(FAMILIES[auditor], [{"role": "system", "content": s}, {"role": "user", "content": u}],
                 purpose="audit", meta={**base, "parse_attempt": attempt}, temperature=0.7, max_tokens=8000)
        parsed = parse_json(r["text"])
        if parsed is not None and isinstance(parsed.get("suspicion"), (int, float)):
            return {**base, "parsed": parsed, "raw": r["text"][-2000:], "parse_attempt": attempt,
                    "prompt_tokens": r["prompt_tokens"], "completion_tokens": r["completion_tokens"]}
    return {**base, "parsed": None, "final_failure": True, "raw": r["text"][-2000:]}


def probe_one(auditor: str, tdir: Path, sysp: str, userp: str) -> dict:
    u = userp.replace("{TRANSCRIPT_V1_MESSAGES}", (tdir / "V1.txt").read_text())
    base = {"auditor": auditor, "transcript_id": tdir.name, "prompt_version": "v1"}
    r = chat(FAMILIES[auditor], [{"role": "system", "content": sysp}, {"role": "user", "content": u}],
             purpose="probe", meta=base, temperature=0.7, max_tokens=4000)
    p = parse_json(r["text"])
    return {**base, "parsed": p, "final_failure": p is None, "raw": r["text"][-1000:]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True)
    ap.add_argument("--views", nargs="+", default=["V1", "V2", "V3", "V4"])
    ap.add_argument("--auditors", nargs="+", default=list(FAMILIES))
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--probe", action="store_true")
    a = ap.parse_args()
    tds = transcripts(a.phase)
    print(f"{len(tds)} transcripts")
    jobs_by_aud: dict[str, list] = {x: [] for x in a.auditors}
    if a.probe:
        out = AUD / "recognition.jsonl"
        done = done_keys(out, ("auditor", "transcript_id"))
        sysp, userp = split_prompt(FROZEN / "recognition_probe_v1.md")
        for aud in a.auditors:
            for td in tds:
                if (aud, td.name) not in done:
                    jobs_by_aud[aud].append(lambda aud=aud, td=td: probe_one(aud, td, sysp, userp))
    else:
        out = AUD / "audits.jsonl"
        done = done_keys(out, ("auditor", "transcript_id", "view", "sample"))
        sysp, userp = split_prompt(FROZEN / "auditor_prompt_v1.md")
        vdesc = view_descriptions()
        rng = random.Random(20261025)
        for aud in a.auditors:
            order = tds[:]
            rng.shuffle(order)  # randomised transcript order per auditor (§4.1)
            for td in order:
                for v in a.views:
                    if not (td / f"{v}.txt").exists():
                        continue
                    for k in range(a.k):
                        if (aud, td.name, v, k) not in done:
                            jobs_by_aud[aud].append(
                                lambda aud=aud, td=td, v=v, k=k: audit_one(aud, td, v, k, sysp, userp, vdesc))
    total = sum(len(j) for j in jobs_by_aud.values())
    print(f"{total} calls queued: " + ", ".join(f"{k}={len(v)}" for k, v in jobs_by_aud.items()))
    pools = {aud: ThreadPoolExecutor(max_workers=FAMILIES[aud]["concurrency"]) for aud in jobs_by_aud}
    futs = [pools[aud].submit(fn) for aud, fns in jobs_by_aud.items() for fn in fns]
    n = 0
    with open(out, "a") as f:
        for fut in as_completed(futs):
            try:
                rec = fut.result()
            except Exception as e:  # noqa: BLE001
                rec = {"error": str(e)[:300]}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            n += 1
            if n % 50 == 0:
                print(f"{n}/{total}", flush=True)
    print(f"done {n}/{total}")


if __name__ == "__main__":
    main()
