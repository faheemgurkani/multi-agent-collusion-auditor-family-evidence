"""Produce the V4 neutral structured report for each transcript with the frozen summariser prompt.

Reads  src/data/views/<tid>/V3.txt (the full blinded log) and writes src/data/views/<tid>/V4.txt.
Summariser: DeepSeek V4 Flash (a 4th, neutral family; methodology §3.2). Resumable.

Usage: python src/pipeline/summarize.py --phase main
"""
from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor

from audit import split_prompt
from common import DATA, FROZEN, SUMMARIZER, chat


def one(tdir, sysp, userp):
    meta = json.loads((tdir / "meta.json").read_text())
    s = sysp.replace("{N_AGENTS}", str(meta["n_agents"]))
    u = userp.replace("{TRANSCRIPT}", (tdir / "V3.txt").read_text())
    r = chat(SUMMARIZER, [{"role": "system", "content": s}, {"role": "user", "content": u}],
             purpose="summarize", meta={"transcript_id": tdir.name, "prompt_version": "v1"},
             temperature=0.0, max_tokens=8000)
    text = r["text"].strip()
    if text:
        (tdir / "V4.txt").write_text(text + "\n")
    return tdir.name, bool(text)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True)
    a = ap.parse_args()
    sysp, userp = split_prompt(FROZEN / "summarizer_prompt_v1.md")
    tds = [p for p in sorted((DATA / "views").glob(f"{a.phase}_*"))
           if (p / "V3.txt").exists() and not (p / "V4.txt").exists()]
    print(f"{len(tds)} to summarise")
    with ThreadPoolExecutor(max_workers=SUMMARIZER["concurrency"]) as ex:
        for tid, ok in ex.map(lambda t: one(t, sysp, userp), tds):
            print(tid, "ok" if ok else "EMPTY")


if __name__ == "__main__":
    main()
