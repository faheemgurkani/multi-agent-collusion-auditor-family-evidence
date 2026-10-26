"""Shared paths, model routes, and a logged OpenAI-compatible chat call.

Every model call made by our pipeline (summaries, audits, probes) goes through `chat()`, which
appends one JSON line to src/data/logs/calls.jsonl with route, model, served model, provider,
token usage, latency and an estimated cost. Colosseum agent runs log their own transcripts; their
token usage is reconstructed from the run outputs where available.
"""
from __future__ import annotations

import json
import os
import random
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
DATA = SRC / "data"
LOGS = DATA / "logs"
FROZEN = SRC / "plan" / "frozen"
COLOSSEUM = ROOT / "starter" / "collusion_hackathon" / "colosseum"
LOGS.mkdir(parents=True, exist_ok=True)


def load_env() -> None:
    """Load ROOT/.env into os.environ (without overriding existing variables)."""
    p = ROOT / ".env"
    if not p.exists():
        return
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


load_env()

OPENROUTER_URL = "https://openrouter.ai/api/v1"

# One fixed route per family (src/plan/compute_routing.md). Prices are USD per 1M tokens (in, out);
# Modal routes are billed per GPU-second, so their per-token price is recorded as 0 here and their
# cost is computed from endpoint uptime instead.
FAMILIES = {
    "gemma": {
        "route": "modal",
        "model": "gemma4-31b",                       # Modal endpoint model name
        "hf_model": "google/gemma-4-31B-it@3548789",
        "base_url_env": "MODAL_URL_GEMMA",
        "price": (0.0, 0.0),
        "concurrency": 5,   # low to avoid Modal autoscaling extra B200 containers

    },
    "gptoss": {
        "route": "modal",
        "model": "gptoss-120b",
        "hf_model": "openai/gpt-oss-120b@b5c939d",
        "base_url_env": "MODAL_URL_GPTOSS",
        "price": (0.0, 0.0),
        "concurrency": 5,

    },
    "nemotron": {
        "route": "openrouter",
        # Free endpoint (:free, provider Nvidia) returned HTTP 404 on 2026-10-25 -> paid route, pinned
        # to one provider so precision is constant (D2). DeepInfra (bf16) saturated with upstream 429s
        # at 13:30 UTC -> all Nemotron calls re-pinned to DekaLLM (fp8). Deviation D8.
        "model": "nvidia/nemotron-3-super-120b-a12b",
        "hf_model": "nvidia/nemotron-3-super-120b-a12b",
        "provider": {"order": ["DekaLLM"], "allow_fallbacks": False},
        "price": (0.08, 0.45),
        "concurrency": 12,
    },
}
SUMMARIZER = {
    "route": "openrouter",
    "model": "deepseek/deepseek-v4-flash",
    "provider": {"order": ["DeepInfra"], "allow_fallbacks": False},  # pinned (fp8); deviation D6
    "price": (0.09, 0.18),
    "concurrency": 6,
}
FAMILY_ORDER = ["gemma", "gptoss", "nemotron"]


def route_client_params(spec: dict) -> tuple[str, str]:
    """(base_url, api_key) for a family/summariser spec."""
    if spec["route"] == "modal":
        url = os.environ.get(spec["base_url_env"], "")
        if not url:
            raise RuntimeError(f"{spec['base_url_env']} not set in .env (Modal endpoint URL)")
        return url.rstrip("/"), os.environ["MODAL_PROXY_TOKEN"]
    return OPENROUTER_URL, os.environ["OPENROUTER_API_KEY"]


_log_lock = threading.Lock()


def log_call(rec: dict) -> None:
    with _log_lock, open(LOGS / "calls.jsonl", "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


class RateLimiter:
    """Simple per-route requests-per-minute limiter (thread-safe)."""

    def __init__(self, rpm: float):
        self.interval = 60.0 / rpm
        self.lock = threading.Lock()
        self.next_t = 0.0

    def wait(self) -> None:
        with self.lock:
            now = time.time()
            t = max(now, self.next_t)
            self.next_t = t + self.interval
        if t > now:
            time.sleep(t - now)


_limiters: dict[str, RateLimiter] = {}


def chat(spec: dict, messages: list[dict], *, purpose: str, meta: dict, temperature: float = 0.7,
         max_tokens: int = 400, use_paid: bool = False, retries: int = 10) -> dict:
    """One chat completion with logging, rate limiting and back-off. Returns {text, usage, ...}."""
    from openai import OpenAI

    base_url, key = route_client_params(spec)
    model = spec.get("paid_model") if (use_paid and spec.get("paid_model")) else spec["model"]
    price = spec.get("paid_price", spec["price"]) if use_paid else spec["price"]
    client = OpenAI(base_url=base_url, api_key=key, timeout=300)
    if spec.get("rpm") and not use_paid:
        _limiters.setdefault(model, RateLimiter(spec["rpm"])).wait()
    delay = 5.0
    for attempt in range(retries):
        t0 = time.time()
        try:
            extra = {"provider": spec["provider"]} if spec.get("provider") else None
            resp = client.chat.completions.create(model=model, messages=messages,
                                                  temperature=temperature, max_tokens=max_tokens,
                                                  extra_body=extra)
            text = resp.choices[0].message.content or ""
            u = resp.usage
            pin, pout = (u.prompt_tokens or 0, u.completion_tokens or 0) if u else (0, 0)
            rec = {
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "purpose": purpose,
                "route": spec["route"], "model": model, "served_model": getattr(resp, "model", None),
                "provider": getattr(resp, "provider", None), "prompt_tokens": pin,
                "completion_tokens": pout, "latency_s": round(time.time() - t0, 2),
                "est_cost_usd": round(pin * price[0] / 1e6 + pout * price[1] / 1e6, 6),
                "finish_reason": resp.choices[0].finish_reason, "attempt": attempt, **meta,
            }
            log_call(rec)
            return {"text": text, **rec}
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            log_call({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "purpose": purpose,
                      "route": spec["route"], "model": model, "error": msg[:300], "attempt": attempt, **meta})
            if attempt == retries - 1:
                raise
            time.sleep(delay + random.random() * 2)
            delay = min(delay * 2, 120)
    raise RuntimeError("unreachable")
