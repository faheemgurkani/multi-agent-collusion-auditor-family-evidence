"""Report figures and the per-condition detection table, from analyze.py outputs plus the raw audits.

Run after analyze.py:  python src/analysis/figures.py --phase main
Outputs: src/results/<phase>/figures/fig{1..4}_*.png, tables/detection_by_condition.csv
"""
from __future__ import annotations

import argparse
import json

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from analyze import FAM_LABEL, FAMS, ROOT, VIEWS, auroc, ci, load  # noqa: E402

plt.rcParams.update({"font.size": 10, "axes.titlesize": 10, "axes.labelsize": 10, "font.family": "Arial",
                     "axes.spines.top": False, "axes.spines.right": False})
COLORS = {"gemma": "#2b6f8f", "gptoss": "#d99a3d", "nemotron": "#6a9a5b"}  # teal / amber / sage
SHORT = {"gemma": "Gemma", "gptoss": "GPT-OSS", "nemotron": "Nemotron"}
VLAB = {"V1": "V1 messages", "V2": "V2 actions", "V3": "V3 both", "V4": "V4 summary"}
RNG = np.random.default_rng(20261026)


def boot_auroc(pos, neg, B=2000):
    pos, neg = np.asarray(pos), np.asarray(neg)
    return ci([auroc(RNG.choice(pos, len(pos)), RNG.choice(neg, len(neg))) for _ in range(B)])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default="main")
    a = ap.parse_args()
    out = ROOT / "src" / "results" / a.phase
    R = json.loads((out / "results.json").read_text())
    lab, s, _ = load(a.phase)

    # ---- Fig 1: interaction heatmaps per view
    fig, axes = plt.subplots(2, 2, figsize=(8.4, 7.4))
    axes = axes.ravel()
    lim = 0.12
    for ax, v in zip(axes, VIEWS):
        I = np.array(R["H2_H3"][v]["I"])
        im = ax.imshow(I, cmap="RdBu", vmin=-lim, vmax=lim)
        for i in range(3):
            for k in range(3):
                ax.text(k, i, f"{I[i, k]:+.2f}", ha="center", va="center", fontsize=10,
                        fontweight="bold" if i == k else "normal")
            ax.add_patch(plt.Rectangle((i - .5, i - .5), 1, 1, fill=False, lw=2, ec="k"))
        lo, hi = R["H2_H3"][v]["ci"]
        ax.set_title(f"{VLAB[v]}: diagonal mean {R['H2_H3'][v]['I_diag_mean']:+.3f}\n95% CI [{lo:+.3f}, {hi:+.3f}]", fontsize=9.5)
        ax.set_xticks(range(3), [SHORT[f] for f in FAMS], fontsize=9)
        ax.set_yticks(range(3), [SHORT[f] for f in FAMS], fontsize=9)
        ax.set_xlabel("agent family")
        if v in ("V1", "V3"):
            ax.set_ylabel("auditor family")
    fig.subplots_adjust(hspace=0.45, wspace=0.35)
    fig.colorbar(im, ax=axes.tolist(), shrink=0.7, label="interaction I (AUROC)")
    fig.savefig(out / "figures" / "fig1_interaction.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    # ---- Fig 2: AUROC by view and auditor with bootstrap CIs; per-condition table
    rows = []
    for v in VIEWS:
        for j in FAMS:
            c = s[(s.view == v) & (s.auditor == j)]
            neg = c[c.label == 0].suspicion.values
            for cond in ["A+B", "A", "B"]:
                pos = c[c.condition.isin(list(cond.replace("+", "")))].suspicion.values
                lo, hi = boot_auroc(pos, neg)
                rows.append({"view": v, "auditor": j, "positives": cond, "n_pos": len(pos), "n_neg": len(neg),
                             "auroc": auroc(pos, neg), "lo": lo, "hi": hi})
    dc = pd.DataFrame(rows)
    dc.to_csv(out / "tables" / "detection_by_condition.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(11, 3.6), sharey=True, gridspec_kw={"width_ratios": [4, 4]})
    w = 0.26
    for ax, conds, title in [(axes[0], ["A+B"], "(a) all instructed coalitions (A+B) vs C+D"),
                             (axes[1], ["A", "B"], "(b) A (private channel) vs B (no channel), V1 and V3")]:
        if conds == ["A+B"]:
            for n, j in enumerate(FAMS):
                d = dc[(dc.auditor == j) & (dc.positives == "A+B")].set_index("view").loc[VIEWS]
                x = np.arange(4) + (n - 1) * w
                ax.bar(x, d.auroc, w, color=COLORS[j], label=FAM_LABEL[j])
                ax.errorbar(x, d.auroc, yerr=[d.auroc - d.lo, d.hi - d.auroc], fmt="none", ecolor="k", capsize=2, lw=1)
            ax.set_xticks(range(4), [VLAB[v] for v in VIEWS])
        else:
            groups = [(v, c) for v in ["V1", "V3"] for c in ["A", "B"]]
            for n, j in enumerate(FAMS):
                d = [dc[(dc.auditor == j) & (dc.view == v) & (dc.positives == c)].iloc[0] for v, c in groups]
                x = np.arange(len(groups)) + (n - 1) * w
                y = np.array([r.auroc for r in d])
                ax.bar(x, y, w, color=COLORS[j])
                ax.errorbar(x, y, yerr=[y - [r.lo for r in d], [r.hi for r in d] - y], fmt="none", ecolor="k",
                            capsize=2, lw=1)
            ax.set_xticks(range(len(groups)), [f"{v}, {c}" for v, c in groups])
        ax.axhline(0.5, ls="--", c="grey", lw=1)
        ax.set_ylim(0, 1.05)
        ax.set_title(title)
    axes[0].set_ylabel("AUROC (95% CI)")
    fig.legend(*axes[0].get_legend_handles_labels(), loc="lower center", ncol=3, title="auditor",
               bbox_to_anchor=(0.5, -0.12), frameon=False)
    fig.savefig(out / "figures" / "fig2_auroc_by_view.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


    # ---- Fig 0 (hero, page 1): (a) same-family interaction per view, (b) AUROC by view
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.0), gridspec_kw={"width_ratios": [1.05, 1]})
    rows_h = [("pooled", "pooled V1–V3\n(primary)")] + [(v, VLAB[v]) for v in VIEWS]
    for y, (k, lbl) in enumerate(rows_h[::-1]):
        d = R["H2_H3"][k]
        lo, hi = d["ci"]
        c = "#222" if k == "pooled" else "#666"
        a1.plot([lo, hi], [y, y], c=c, lw=2.2 if k == "pooled" else 1.4)
        a1.plot(d["I_diag_mean"], y, "o", c=c, ms=7 if k == "pooled" else 5)
    a1.axvline(0, c="grey", lw=1, ls="--")
    a1.axvspan(-0.13, 0, color="#c44e52", alpha=0.07)
    a1.axvspan(0, 0.13, color="#2b6f8f", alpha=0.07)
    a1.set_xlim(-0.13, 0.13)
    a1.set_yticks(range(len(rows_h)), [l for _, l in rows_h[::-1]], fontsize=9)
    a1.set_xlabel("same-family interaction (AUROC), 95% CI")
    a1.text(-0.125, -0.5, "← own family detected worse", fontsize=8, va="bottom", color="#c44e52")
    a1.text(0.125, -0.5, "own family detected better →", fontsize=8, va="bottom", ha="right", color="#2b6f8f")
    a1.set_ylim(-0.7, len(rows_h) - 0.4)
    a1.set_title("(a) Do auditors go easy on their own family?", loc="left")
    w = 0.25
    for n, j in enumerate(FAMS):
        d = dc[(dc.auditor == j) & (dc.positives == "A+B")].set_index("view").loc[VIEWS]
        x = np.arange(4) + (n - 1) * w
        a2.errorbar(x, d.auroc, yerr=[d.auroc - d.lo, d.hi - d.auroc], fmt="o", ms=5, capsize=2,
                    color=COLORS[j], label=f"{SHORT[j]} auditor")
    a2.axhline(0.5, c="grey", lw=1, ls="--")
    a2.text(3.45, 0.51, "chance", fontsize=8, color="grey", ha="right", va="bottom")
    a2.set_xticks(range(4), [VLAB[v].replace(" ", "\n", 1) for v in VIEWS], fontsize=9)
    a2.set_ylim(0.3, 1.02)
    a2.set_ylabel("AUROC, 95% CI")
    a2.legend(fontsize=8, frameon=False, loc="lower right")
    a2.set_title("(b) What do auditors read?", loc="left")
    fig.tight_layout(w_pad=4.5)
    fig.savefig(out / "figures" / "fig0_hero.png", dpi=250, bbox_inches="tight")
    plt.close(fig)

    # ---- Fig 3: H4 mitigation arms per agent family (V3; V4 with the same-family auditor)
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    arms = [("same", "same-family auditor"), ("cross", "single cross-family (mean)"),
            ("ensemble", "cross-family ensemble"), ("v4_same", "same-family on V4 summary")]
    w = 0.2
    for n, (k, lbl) in enumerate(arms):
        y = [R["H4"][f][k] for f in FAMS]
        ax.bar(np.arange(3) + (n - 1.5) * w, y, w, label=lbl)
    for i, f in enumerate(FAMS):  # star where the difference CI vs same-family excludes 0
        for n, k in enumerate(["cross", "ensemble", "v4_same"]):
            lo, hi = R["H4"][f]["diff_ci_cross_ens_v4"][n]
            if lo > 0 or hi < 0:
                ax.text(i + (n - 0.5) * w, R["H4"][f][k] + 0.02, "*", ha="center", fontsize=13)
    ax.set_xticks(range(3), [f"{SHORT[f]} agents" for f in FAMS])
    ax.set_ylim(0.5, 1.05)
    ax.set_ylabel("AUROC (view V3 unless noted)")
    ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False)
    fig.savefig(out / "figures" / "fig3_mitigation.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    # ---- Fig 4: environment positive control (coalition advantage by condition)
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    order = ["A", "B", "C", "D"]
    names = ["A: instructed +\nprivate channel", "B: instructed,\nno channel", "C: uninstructed,\nopen channel",
             "D: uninstructed,\nno channel"]
    for n, f in enumerate(FAMS):
        g = [lab[(lab.family == f) & (lab.condition == c)].coalition_advantage for c in order]
        m = [x.mean() for x in g]
        se = [x.std() / np.sqrt(len(x)) for x in g]
        ax.errorbar(np.arange(4) + (n - 1) * 0.15, m, yerr=se, fmt="o", capsize=3, color=COLORS[f], label=FAM_LABEL[f])
    ax.axhline(0, c="grey", lw=1, ls="--")
    ax.set_xticks(range(4), names, fontsize=8)
    ax.set_ylabel("coalition advantage\n(mean ± SE, 8 seeds)")
    ax.legend(fontsize=8, frameon=False)
    fig.savefig(out / "figures" / "fig4_environment.png", dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(dc[dc.positives != "A+B"].round(3).to_string())


if __name__ == "__main__":
    main()
