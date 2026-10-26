"""Additional report figures and exploratory (post-hoc) analyses, in the report's visual style.

Run after analyze.py:  python src/analysis/figures_extra.py --phase main
Outputs (src/results/<phase>/):
  figures/fx_design.png        study design schematic
  figures/fx_environment.png   positive control with every seed
  figures/fx_drivers.png       what raises suspicion: outcome vs talk vs the word "coalition"
  figures/fx_baselines.png     LLM auditors vs simple non-LLM detectors
  figures/fx_anatomy.png       one coalition episode vs one hard-control episode
  figures/fx_distributions.png suspicion scores, coalitions vs controls, per auditor x view
  figures/fx_roc.png           ROC curves per auditor x view
  figures/fx_permutation.png   permutation null of the primary family estimand
  figures/fx_agreement.png     inter-auditor agreement per view
  figures/fx_pareto.png        detection vs cost of auditor configurations
  tables/exploratory.json      every number quoted from these analyses
Everything here except fx_environment/fx_permutation is exploratory and was not pre-registered.
"""
from __future__ import annotations

import argparse
import json
import re

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402
from scipy.stats import spearmanr  # noqa: E402

from analyze import DATA, FAMS, ROOT, VIEWS, auroc, ci, interaction, load, matrix  # noqa: E402

plt.rcParams.update({"font.family": "Arial", "font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 8.5,
                     "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.7})
C = {"gemma": "#2b6f8f", "gptoss": "#d99a3d", "nemotron": "#6a9a5b"}
SHORT = {"gemma": "Gemma", "gptoss": "GPT-OSS", "nemotron": "Nemotron"}
TYPE_C = {"direct": "#2b6f8f", "attempted": "#d99a3d", "hidden": "#c44e52", "control": "#9a9a9a"}
VLAB = {"V1": "V1 messages", "V2": "V2 actions", "V3": "V3 both", "V4": "V4 summary"}
RNG = np.random.default_rng(7)
EX: dict = {}


def title(ax, t):
    ax.set_title(t, loc="left", fontweight="bold", fontsize=9, pad=6)


def grid(ax, axis="x"):
    ax.grid(axis=axis, color="#e6e6e6", lw=0.6)
    ax.set_axisbelow(True)


def boot_auc(pos, neg, B=2000):
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    return ci([auroc(RNG.choice(pos, len(pos)), RNG.choice(neg, len(neg))) for _ in range(B)])


def v1_body(tid):
    return (DATA / "views" / tid / "V1.txt").read_text().split("MESSAGES (in order)", 1)[1].lower()


def save(fig, out, name):
    fig.savefig(out / "figures" / name, dpi=250, bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------------------------------ design
def fig_design(out):
    fig, ax = plt.subplots(figsize=(9.2, 2.35))
    ax.set_xlim(0, 100); ax.set_ylim(0, 30); ax.axis("off")
    boxes = [
        (0.5, "3 agent families\n× 4 conditions\n× 8 seeds", "Gemma 4 · GPT-OSS-120B\nNemotron 3 Super"),
        (20.5, "96 Colosseum\nepisodes", "4 agents, 8 tasks,\npair at path ends"),
        (40.5, "4 blinded views", "V1 messages · V2 actions\nV3 both · V4 summary"),
        (60.5, "3 auditor families\n× k = 3 samples", "frozen prompt,\nscore 0–100"),
        (80.5, "3,456 audits", "AUROC, 3×3 family\ninteraction, bootstrap"),
    ]
    for x, head, sub in boxes:
        ax.add_patch(FancyBboxPatch((x, 9), 17.5, 17, boxstyle="round,pad=0.4,rounding_size=1.2",
                                    fc="#f3f6f8", ec="#2b6f8f", lw=0.9))
        ax.text(x + 8.75, 20.5, head, ha="center", va="center", fontsize=8.5, fontweight="bold")
        ax.text(x + 8.75, 12.6, sub, ha="center", va="center", fontsize=7.3, color="#444")
    for x in [18.4, 38.4, 58.4, 78.4]:
        ax.add_patch(FancyArrowPatch((x, 17.5), (x + 2.1, 17.5), arrowstyle="-|>", mutation_scale=9, color="#555"))
    ax.add_patch(FancyBboxPatch((0.5, 0.6), 76.5, 5.2, boxstyle="round,pad=0.3,rounding_size=1",
                                fc="#fbf3e6", ec="#d99a3d", lw=0.8, ls="--"))
    ax.text(38.75, 3.2, "Ground truth from the design (instructed coalition: A, B = 1; C, D = 0) and\n"
            "coalition advantage from exact rewards. Never shown to auditors.", ha="center", va="center", fontsize=7.3, color="#7a5a20")
    ax.add_patch(FancyArrowPatch((77.6, 3.2), (86.5, 8.4), arrowstyle="-|>", mutation_scale=8, color="#d99a3d",
                                 connectionstyle="arc3,rad=0.25"))
    save(fig, out, "fx_design.png")


# ------------------------------------------------------------------------------------- environment
def fig_environment(out, lab):
    fig, ax = plt.subplots(figsize=(6.4, 2.7))
    order = ["A", "B", "C", "D"]
    names = ["A: instructed,\nprivate channel", "B: instructed,\nno channel", "C: not instructed,\nopen channel",
             "D: not instructed,\nno channel"]
    for n, f in enumerate(FAMS):
        for k, c in enumerate(order):
            v = lab[(lab.family == f) & (lab.condition == c)].coalition_advantage.values
            x = k + (n - 1) * 0.22
            ax.scatter(x + RNG.uniform(-0.05, 0.05, len(v)), v, s=9, color=C[f], alpha=0.35, lw=0)
            m, se = v.mean(), v.std(ddof=1) / np.sqrt(len(v))
            ax.errorbar(x, m, yerr=se, fmt="o", ms=5, color=C[f], capsize=2.5, lw=1.3,
                        label=f"{SHORT[f]} agents" if k == 0 else None)
    ax.axhline(0, c="#888", lw=0.8, ls="--")
    ax.set_xticks(range(4), names, fontsize=7.6)
    ax.set_ylabel("coalition advantage\n(pair minus others, reward units)")
    grid(ax, "y")
    title(ax, "Did the coalitions work?")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=3, frameon=False)
    save(fig, out, "fx_environment.png")


# ------------------------------------------------------------------------------------------ drivers
def fig_drivers(out, lab, s):
    dmean = lab[lab.condition == "D"].groupby("family").coalition_advantage.mean()
    lab = lab.copy()
    lab["ctype"] = np.where(lab.label == 0, "control",
                            np.where(lab.coalition_advantage - lab.family.map(dmean) > 0,
                                     np.where(lab.condition == "A", "direct", "hidden"), "attempted"))
    lab["kw"] = lab.transcript_id.apply(lambda t: len(re.findall("coalition", v1_body(t))))
    v3 = s[s.view == "V3"].groupby("transcript_id").suspicion.mean().rename("susp")
    d = lab.set_index("transcript_id").join(v3)
    pos = d[d.label == 1]
    r_ca = spearmanr(pos.susp, pos.coalition_advantage)
    r_tk = spearmanr(pos.susp, pos.colluder_posts_total)
    EX["spearman_susp_vs_CA_positives"] = [float(r_ca[0]), float(r_ca[1])]
    EX["spearman_susp_vs_pair_posts_positives"] = [float(r_tk[0]), float(r_tk[1])]
    EX["keyword_share_by_condition"] = (d.kw > 0).groupby(d.condition).mean().round(3).to_dict()
    EX["keyword_auroc"] = auroc(d[d.label == 1].kw, d[d.label == 0].kw)

    fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.0), gridspec_kw={"width_ratios": [1, 1, 1.15], "wspace": 0.38})
    a, b, c = axes
    for t in ["direct", "attempted", "hidden"]:
        g = pos[pos.ctype == t]
        a.scatter(g.coalition_advantage, g.susp, s=18, color=TYPE_C[t], label=t, alpha=0.85, lw=0)
        b.scatter(g.colluder_posts_total, g.susp, s=18, color=TYPE_C[t], alpha=0.85, lw=0)
    a.set_xlabel("coalition advantage (what the pair gained)")
    b.set_xlabel("messages posted by the pair (how much it talked)")
    for ax, r in [(a, r_ca), (b, r_tk)]:
        ax.set_ylabel("V3 suspicion, mean of 3 auditors")
        ax.set_ylim(-3, 103)
        grid(ax, "both")
        ax.text(0.03, 0.97, f"Spearman ρ = {r[0]:.2f}\np = {r[1]:.2g}, n = 48", transform=ax.transAxes,
                va="top", fontsize=8, bbox=dict(fc="white", ec="#ccc", lw=0.5, pad=2))
    title(a, "(a) Suspicion vs outcome")
    title(b, "(b) Suspicion vs talk")
    a.legend(title="coalition type", loc="lower right", frameon=False, fontsize=7.5, title_fontsize=7.5)
    # (c) AUROC with vs without the word "coalition" in the messages
    s2 = s.merge(lab[["transcript_id", "kw"]], on="transcript_id")
    rows = []
    for v in ["V1", "V3", "V4"]:
        for j in FAMS:
            cc = s2[(s2.view == v) & (s2.auditor == j)]
            neg = cc[cc.label == 0].suspicion
            for has in [True, False]:
                p = cc[(cc.label == 1) & ((cc.kw > 0) == has)].suspicion
                rows.append({"view": v, "auditor": j, "has": has, "auroc": auroc(p, neg)})
    r = pd.DataFrame(rows)
    EX["auroc_with_without_keyword"] = r.round(3).to_dict("records")
    yv = {"V1": 2, "V3": 1, "V4": 0}
    for _, q in r.iterrows():
        y = yv[q.view] + {"gemma": 0.22, "gptoss": 0, "nemotron": -0.22}[q.auditor]
        c.scatter(q.auroc, y, marker="o" if q.has else "D", s=26 if q.has else 20,
                  facecolor=C[q.auditor] if q.has else "white", edgecolor=C[q.auditor], lw=1.2, zorder=3)
    for v, y in yv.items():
        for j, dy in zip(FAMS, [0.22, 0, -0.22]):
            q = r[(r.view == v) & (r.auditor == j)]
            c.plot(q.auroc, [y + dy] * 2, c=C[j], lw=0.8, alpha=0.6)
    c.axvline(EX["keyword_auroc"], c="#c44e52", lw=1, ls=":")
    c.text(EX["keyword_auroc"] - 0.005, 2.62, 'grep "coalition"\nalone', ha="right", fontsize=7.3, color="#c44e52")
    c.axvline(0.5, c="#888", lw=0.8, ls="--")
    c.set_xlim(0.45, 1.02); c.set_ylim(-0.5, 2.95)
    c.set_yticks([2, 1, 0], ["V1 messages", "V3 both", "V4 summary"])
    c.set_xlabel("AUROC against all 48 controls")
    grid(c, "x")
    title(c, '(c) With vs without the word "coalition"')
    from matplotlib.lines import Line2D
    h = [Line2D([], [], marker="o", ls="", color="#555", label="coalitions that wrote it (30)"),
         Line2D([], [], marker="D", ls="", mfc="white", color="#555", label="coalitions that did not (18)")]
    h += [Line2D([], [], marker="s", ls="", color=C[j], label=f"{SHORT[j]} auditor") for j in FAMS]
    c.legend(handles=h, loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=2, frameon=False, fontsize=7.2)
    save(fig, out, "fx_drivers.png")
    return lab


# ---------------------------------------------------------------------------------------- baselines
def fig_baselines(out, lab, s):
    y = lab.label.values
    base = {
        "coalition advantage (outcome)": lab.coalition_advantage.fillna(0).values,
        "system regret (outcome)": lab.system_regret.fillna(lab.system_regret.median()).values,
        "messages posted by the pair": lab.colluder_posts_total.values,
        "log length (characters)": lab.v3_chars.values,
        'count of the word "coalition"': lab.kw.values,
    }
    rows = []
    for k, x in base.items():
        lo, hi = boot_auc(x[y == 1], x[y == 0])
        rows.append({"name": k, "group": "simple detector", "auroc": auroc(x[y == 1], x[y == 0]), "lo": lo, "hi": hi})
    for v in VIEWS:
        for j in FAMS:
            cc = s[(s.view == v) & (s.auditor == j)]
            p, n = cc[cc.label == 1].suspicion.values, cc[cc.label == 0].suspicion.values
            lo, hi = boot_auc(p, n)
            rows.append({"name": f"{SHORT[j]} auditor, {VLAB[v]}", "group": v, "auditor": j,
                         "auroc": auroc(p, n), "lo": lo, "hi": hi})
    r = pd.DataFrame(rows)
    EX["baselines"] = r[r.group == "simple detector"].round(3).to_dict("records")
    fig, ax = plt.subplots(figsize=(6.4, 3.05))
    yy = 0
    ticks, labels = [], []
    for g in ["V2", "V1", "simple detector"]:
        sub = r[r.group == g]
        if g != "simple detector":
            sub = sub.iloc[::-1]
        for _, q in sub.iterrows():
            col = C.get(q.get("auditor"), "#7a7a7a") if g != "simple detector" else "#7a7a7a"
            ax.plot([q.lo, q.hi], [yy, yy], c=col, lw=1.4)
            ax.plot(q.auroc, yy, "o", c=col, ms=5)
            ax.text(min(q.hi, 1.0) + 0.012, yy, f"{q.auroc:.2f}", va="center", fontsize=7.3, color="#333")
            ticks.append(yy); labels.append(q["name"])
            yy += 1
        yy += 0.7
    ax.axvline(0.5, c="#888", lw=0.8, ls="--")
    ax.text(0.505, yy - 0.9, "chance", fontsize=7.3, color="#888")
    ax.set_yticks(ticks, labels, fontsize=7.4)
    ax.set_xlim(0.2, 1.08)
    ax.set_xlabel("AUROC, coalitions (A, B) vs controls (C, D), 95% bootstrap interval")
    grid(ax, "x")
    title(ax, "LLM auditors vs simple detectors")
    save(fig, out, "fx_baselines.png")


# ------------------------------------------------------------------------------------------ anatomy
def episode_panel(ax, tid, lab, s, ttl):
    row = lab.set_index("transcript_id").loc[tid]
    te = json.loads((DATA / row.run_dir / "tool_events.json").read_text())
    rc = json.loads((DATA / row.run_dir / "run_config.json").read_text())
    agents = sorted(rc["roles"].keys())
    pair = set((row.colluders or "").split("|")) if isinstance(row.colluders, str) else set()
    bbs = json.loads((DATA / row.run_dir / "blackboards.json").read_text())
    members = {int(b["blackboard_id"]): set(b["participants"]) for b in bbs}
    order = sorted(agents, key=lambda a: (a not in pair, a))
    yof = {a: i for i, a in enumerate(order[::-1])}
    x = 0
    last_round = None
    starts = {}
    for e in te:
        rd = e.get("planning_round") if e["phase"] == "planning" else "exec"
        if rd != last_round:
            starts[rd] = x
            last_round = rd
            x += 0.6
        a = e["agent_name"]
        if e["tool_name"] == "post_message":
            bid = (e.get("arguments") or {}).get("blackboard_id")
            mem = members.get(int(bid) if bid is not None else -1, set())
            if mem and mem <= pair and len(mem) == 2:
                ax.scatter(x, yof[a], marker="D", s=26, color="#c44e52", zorder=3)
            elif len(mem) > 2 and len(mem) == len(agents):
                ax.scatter(x, yof[a], marker="o", s=20, facecolor="white", edgecolor="#555", zorder=3)
            else:
                ax.scatter(x, yof[a], marker="o", s=20, color="#9a9a9a", zorder=3)
        elif e["tool_name"] == "assign_task":
            ax.scatter(x, yof[a], marker="s", s=34, color="#222", zorder=3)
            task = str((e.get("arguments") or {}).get("task_id", "")).replace("ISSUE-", "#").replace("::", " ")
            ax.text(x + 0.35, yof[a] + 0.18, task, fontsize=6.3, color="#222")
        x += 1
    for rd, x0 in starts.items():
        ax.axvline(x0 - 0.2, c="#dddddd", lw=0.8)
        ax.text(x0 + 0.2, len(agents) - 0.35, "execution" if rd == "exec" else f"round {rd}", fontsize=7, color="#777")
    ax.set_yticks(range(len(agents)), [f"{a}{'  (pair)' if a in pair else ''}" for a in order[::-1]], fontsize=7.5)
    for lbl in ax.get_yticklabels():
        if "(pair)" in lbl.get_text():
            lbl.set_color("#c44e52")
    ax.set_xticks([]); ax.set_xlim(-0.5, x + 4.5); ax.set_ylim(-0.6, len(agents) - 0.1)
    ax.spines["bottom"].set_visible(False)
    sc = s[(s.transcript_id == tid) & (s.view == "V3")].set_index("auditor").suspicion
    ax.text(1.0, -0.06, "V3 suspicion: " + " · ".join(f"{SHORT[j]} {sc.get(j, np.nan):.0f}" for j in FAMS)
            + f"   |   coalition advantage {row.coalition_advantage:+.1f}", transform=ax.transAxes, ha="right",
            va="top", fontsize=7.6, color="#333")
    title(ax, ttl)


def fig_anatomy(out, lab, s):
    a = lab[(lab.condition == "A") & (lab.family == "gemma")].sort_values("coalition_advantage").iloc[-1].transcript_id
    c = lab[(lab.condition == "C") & (lab.family == "gemma") & (lab.seed == int(a.rsplit("s", 1)[1]))].iloc[0].transcript_id
    EX["anatomy_episodes"] = [a, c]
    fig, axes = plt.subplots(2, 1, figsize=(9.2, 4.1), gridspec_kw={"hspace": 0.62})
    episode_panel(axes[0], a, lab, s, f"(a) Coalition episode: condition A, Gemma agents, seed {a.rsplit('s', 1)[1]}")
    episode_panel(axes[1], c, lab, s, f"(b) Hard control: condition C, same family and seed")
    from matplotlib.lines import Line2D
    h = [Line2D([], [], marker="D", ls="", color="#c44e52", label="message on the pair's private board"),
         Line2D([], [], marker="o", ls="", mfc="white", color="#555", label="message on the open extra board"),
         Line2D([], [], marker="o", ls="", color="#9a9a9a", label="message on a neighbour board"),
         Line2D([], [], marker="s", ls="", color="#222", label="task chosen")]
    fig.legend(handles=h, loc="lower center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.07), fontsize=7.5)
    save(fig, out, "fx_anatomy.png")


# ------------------------------------------------------------------------------- distributions, ROC
def fig_distributions(out, s):
    fig, axes = plt.subplots(3, 4, figsize=(9.2, 5.4), sharex=True, sharey=True)
    for i, j in enumerate(FAMS):
        for k, v in enumerate(VIEWS):
            ax = axes[i, k]
            cc = s[(s.view == v) & (s.auditor == j)]
            for yv, lab_, col in [(1, 1, C[j]), (0, 0, "#9a9a9a")]:
                vals = cc[cc.label == lab_].suspicion.values
                ax.scatter(vals, yv + RNG.uniform(-0.18, 0.18, len(vals)), s=7, color=col, alpha=0.6, lw=0)
                ax.plot([np.median(vals)] * 2, [yv - 0.3, yv + 0.3], c="k", lw=1.2)
            ax.set_yticks([0, 1], ["controls", "coalitions"])
            ax.set_xlim(-4, 104)
            grid(ax, "x")
            if i == 0:
                ax.set_title(VLAB[v], fontsize=8.5)
            if k == 0:
                ax.set_ylabel(f"{SHORT[j]} auditor", fontsize=8.5)
            if i == 2:
                ax.set_xlabel("suspicion (0–100)")
    fig.suptitle("Suspicion scores, coalitions vs controls (black bar = median)", x=0.02, ha="left",
                 fontweight="bold", fontsize=9)
    save(fig, out, "fx_distributions.png")


def roc_points(pos, neg):
    thr = np.unique(np.r_[pos, neg])[::-1]
    tpr = [0] + [np.mean(pos >= t) for t in thr] + [1]
    fpr = [0] + [np.mean(neg >= t) for t in thr] + [1]
    return fpr, tpr


def fig_roc(out, s):
    fig, axes = plt.subplots(1, 4, figsize=(9.2, 2.6), sharey=True)
    for ax, v in zip(axes, VIEWS):
        for j in FAMS:
            cc = s[(s.view == v) & (s.auditor == j)]
            f, t = roc_points(cc[cc.label == 1].suspicion.values, cc[cc.label == 0].suspicion.values)
            ax.plot(f, t, c=C[j], lw=1.4, label=SHORT[j])
        ax.plot([0, 1], [0, 1], c="#999", lw=0.8, ls="--")
        ax.axvline(0.05, c="#c44e52", lw=0.7, ls=":")
        ax.set_title(VLAB[v], fontsize=8.5)
        ax.set_xlabel("false-positive rate")
        ax.set_aspect("equal")
        grid(ax, "both")
    axes[0].set_ylabel("true-positive rate")
    axes[0].legend(loc="lower right", frameon=False)
    save(fig, out, "fx_roc.png")


# ------------------------------------------------------------------------------- permutation null
def fig_permutation(out, s, R, B=2000):
    obs = R["H2_H3"]["pooled"]["I_diag_mean"]
    tids = s[["transcript_id", "family", "condition"]].drop_duplicates()
    null = []
    for _ in range(B):
        perm = tids.copy()
        for _, g in perm.groupby("condition"):
            perm.loc[g.index, "family"] = RNG.permutation(g.family.values)
        sp = s.copy()
        sp["family"] = sp.transcript_id.map(dict(zip(perm.transcript_id, perm.family)))
        null.append(interaction(matrix(sp, "pooled"))[1])
    null = np.array(null)
    EX["permutation_null_sd"] = float(null.std())
    fig, ax = plt.subplots(figsize=(5.6, 2.5))
    ax.hist(null, bins=45, color="#c9d6de", edgecolor="white")
    ax.axvline(obs, c="#c44e52", lw=1.5)
    ax.text(obs - 0.002, ax.get_ylim()[1] * 0.92, f"observed {obs:+.3f}\np = {R['H2_H3']['pooled']['perm_p']:.2f}",
            ha="right", va="top", fontsize=7.8, color="#c44e52")
    ax.set_xlabel("pooled same-family interaction under shuffled family labels (AUROC)")
    ax.set_ylabel("permutations")
    grid(ax, "y")
    title(ax, f"Permutation null ({B:,} shuffles within condition)")
    save(fig, out, "fx_permutation.png")


# ---------------------------------------------------------------------------------------- agreement
def fig_agreement(out, s):
    fig, axes = plt.subplots(1, 4, figsize=(9.2, 2.3))
    EX["inter_auditor_spearman"] = {}
    for ax, v in zip(axes, VIEWS):
        m = s[s.view == v].groupby(["auditor", "transcript_id"]).suspicion.mean().unstack(0)[FAMS].corr(method="spearman")
        EX["inter_auditor_spearman"][v] = m.round(3).values.tolist()
        ax.imshow(m.values, cmap="Blues", vmin=0, vmax=1)
        for i in range(3):
            for k in range(3):
                ax.text(k, i, f"{m.values[i, k]:.2f}", ha="center", va="center", fontsize=8,
                        color="white" if m.values[i, k] > 0.6 else "#222")
        ax.set_xticks(range(3), [SHORT[f] for f in FAMS], fontsize=7.3)
        ax.set_yticks(range(3), [SHORT[f] for f in FAMS] if v == "V1" else [""] * 3, fontsize=7.3)
        ax.set_title(VLAB[v], fontsize=8.5)
        for sp_ in ax.spines.values():
            sp_.set_visible(False)
    fig.suptitle("Agreement between auditors (Spearman ρ of per-episode suspicion)", x=0.02, ha="left",
                 fontweight="bold", fontsize=9, y=1.06)
    save(fig, out, "fx_agreement.png")


# ------------------------------------------------------------------------------------------- pareto
def fig_pareto(out, s, R):
    calls = pd.DataFrame([json.loads(l) for l in open(DATA / "logs" / "calls.jsonl")])
    calls = calls[(calls.purpose == "audit") & calls.prompt_tokens.notna()]
    tok = calls.groupby("model")[["prompt_tokens", "completion_tokens"]].mean()
    pts = []
    # cost per audit call (tokens) is dominated by the log; use measured mean tokens per call
    mean_tok = float((tok.prompt_tokens + tok.completion_tokens).mean())
    for f in FAMS:
        h = R["H4"][f]
        pts += [(f, "same-family", 1, h["same"]), (f, "single cross-family", 1, h["cross"]),
                (f, "cross-family ensemble", 2, h["ensemble"]), (f, "same-family + V4 summary", 2, h["v4_same"])]
    fig, ax = plt.subplots(figsize=(5.8, 2.9))
    mk = {"same-family": "o", "single cross-family": "^", "cross-family ensemble": "s", "same-family + V4 summary": "x"}
    for f, arm, k, a in pts:
        ax.scatter(k * mean_tok / 1000 + {"gemma": -0.15, "gptoss": 0, "nemotron": 0.15}[f], a, marker=mk[arm],
                   s=34, color=C[f], label=arm if f == "gemma" else None, lw=1.3)
    ax.set_xlabel("model calls' tokens per episode audited (thousands; V4 adds one summary call)")
    ax.set_ylabel("AUROC (V3 unless noted)")
    grid(ax, "both")
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=4, fontsize=7.2)
    title(ax, "Detection vs cost of auditor configurations")
    EX["mean_tokens_per_audit_call"] = mean_tok
    save(fig, out, "fx_pareto.png")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default="main")
    a = ap.parse_args()
    out = ROOT / "src" / "results" / a.phase
    R = json.loads((out / "results.json").read_text())
    lab, s, _ = load(a.phase)
    fig_design(out)
    fig_environment(out, lab)
    lab = fig_drivers(out, lab, s)
    fig_baselines(out, lab, s)
    fig_anatomy(out, lab, s)
    fig_distributions(out, s)
    fig_roc(out, s)
    fig_agreement(out, s)
    fig_pareto(out, s, R)
    fig_permutation(out, s, R)
    (out / "tables" / "exploratory.json").write_text(json.dumps(EX, indent=1, default=float))
    print(json.dumps({k: v for k, v in EX.items() if k not in ("auroc_with_without_keyword", "baselines")},
                     indent=1, default=float))


if __name__ == "__main__":
    main()
