"""Generate static figures illustrating Propensity Score Matching (PSM) and
Inverse Probability of Treatment Weighting (IPTW / IPW).

The figures are embedded in ``tutorial/propensity.md`` via MyST ``{figure}``
directives. Re-run this script to regenerate them::

    python tutorial/figs/generate_propensity_figures.py

Conceptually inspired by:
Chung, E. "Propensity Score Matching vs. Weighting: A Practical Guide with Python".
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import FancyArrowPatch
from sklearn.linear_model import LogisticRegression

# --------------------------------------------------------------------------- #
# Global style
# --------------------------------------------------------------------------- #
HERE = Path(__file__).resolve().parent
sns.set_theme(style="whitegrid", context="notebook")

CONTROL_C = "#1f77b4"  # blue
TREATED_C = "#ff7f0e"  # orange
ACCENT_C = "#2ca02c"  # green
TRUE_EFFECT = 2.0


# --------------------------------------------------------------------------- #
# 1. Simulate data + estimate propensity scores
# --------------------------------------------------------------------------- #
def simulate_data(n: int = 1000, seed: int = 42) -> pd.DataFrame:
    """Observational data with confounding and a known treatment effect."""
    rng = np.random.default_rng(seed)
    x1 = rng.normal(0, 1.5, n)
    x2 = rng.uniform(-1, 1, n)

    # True propensity depends on the confounders -> selection bias.
    true_ps = 1 / (1 + np.exp(-(0.3 + 0.7 * x1 - 0.5 * x2)))
    treat = rng.binomial(1, true_ps)

    # Outcome: confounders also drive Y, on top of the constant treatment effect.
    noise = rng.normal(0, 1.0, n)
    y = 1.0 + TRUE_EFFECT * treat + 1.2 * x1 - 0.8 * x2 + noise

    return pd.DataFrame({"x1": x1, "x2": x2, "treatment": treat, "outcome": y})


def add_propensity_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Estimate propensity scores with logistic regression."""
    model = LogisticRegression()
    model.fit(df[["x1", "x2"]], df["treatment"])
    out = df.copy()
    out["ps"] = model.predict_proba(df[["x1", "x2"]])[:, 1]
    return out


# --------------------------------------------------------------------------- #
# Estimators
# --------------------------------------------------------------------------- #
def ps_matching(df: pd.DataFrame, caliper: float = 0.05):
    """Nearest-neighbour 1:1 matching on the propensity score (with caliper).

    Returns the matched dataframe (with ``pair_id``) and the ATT estimate.
    """
    treated = df[df.treatment == 1].reset_index(drop=True)
    control = df[df.treatment == 0].reset_index(drop=True)
    used: set[int] = set()
    pairs = []
    for _, t in treated.iterrows():
        avail = control[~control.index.isin(used)]
        dist = (avail.ps - t.ps).abs()
        if dist.empty:
            break
        j = dist.idxmin()
        if dist[j] <= caliper:
            used.add(j)
            pairs.append((t, control.loc[j]))

    rows, att_diffs = [], []
    for pid, (t, c) in enumerate(pairs):
        t = t.copy(); c = c.copy()
        t["pair_id"], c["pair_id"] = pid, pid
        rows.extend([t, c])
        att_diffs.append(t.outcome - c.outcome)

    matched = pd.DataFrame(rows)
    att = float(np.mean(att_diffs)) if att_diffs else np.nan
    return matched, att


def iptw_weights(df: pd.DataFrame, clip=(0.05, 0.95)) -> pd.DataFrame:
    """Add raw and clipped IPW (ATE) weights."""
    out = df.copy()
    ps = out.ps
    ps_clipped = ps.clip(*clip)
    out["w_raw"] = np.where(out.treatment == 1, 1 / ps, 1 / (1 - ps))
    out["w_clip"] = np.where(
        out.treatment == 1, 1 / ps_clipped, 1 / (1 - ps_clipped)
    )
    return out


def iptw_ate(df: pd.DataFrame, w_col: str = "w_clip") -> float:
    t, c = df[df.treatment == 1], df[df.treatment == 0]
    y1 = np.average(t.outcome, weights=t[w_col])
    y0 = np.average(c.outcome, weights=c[w_col])
    return float(y1 - y0)


def standardized_mean_diff(df, var, t_col="treatment", w_col=None) -> float:
    """SMD for a covariate (weighted if ``w_col`` is given)."""
    t = df[df[t_col] == 1]
    c = df[df[t_col] == 0]
    if w_col is None:
        mt, mc = t[var].mean(), c[var].mean()
    else:
        mt = np.average(t[var], weights=t[w_col])
        mc = np.average(c[var], weights=c[w_col])
    pooled_sd = np.sqrt((t[var].var() + c[var].var()) / 2)
    return (mt - mc) / pooled_sd


def save(fig, name: str) -> None:
    path = HERE / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"saved {path.relative_to(HERE.parent.parent)}")


# --------------------------------------------------------------------------- #
# Figure 1 — Propensity score overlap
# --------------------------------------------------------------------------- #
def fig_overlap(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.2))
    lbl = df.treatment.map({0: "Control", 1: "Treated"})
    sns.histplot(
        x=df.ps, hue=lbl, palette={"Control": CONTROL_C, "Treated": TREATED_C},
        element="step", stat="density", common_norm=False,
        hue_order=["Control", "Treated"], bins=30, alpha=0.45, ax=ax,
    )
    ax.set_title("Propensity-score overlap by treatment group")
    ax.set_xlabel("Estimated propensity score  $\\hat{\\pi}(x)$")
    ax.set_ylabel("Density")
    ax.legend(title="", labels=["Treated", "Control"])
    fig.text(
        0.5, -0.04,
        "Region of common support (overlap) is where comparable treated and "
        "control units exist.",
        ha="center", fontsize=9, style="italic", color="0.35",
    )
    save(fig, "ps_overlap.png")


# --------------------------------------------------------------------------- #
# Figure 2 — Conceptual: matching pairs vs reweighting
# --------------------------------------------------------------------------- #
def fig_concept(df: pd.DataFrame) -> None:
    rng = np.random.default_rng(7)
    sample = df.sample(60, random_state=1).reset_index(drop=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # ---- Left: PSM (pairs) -------------------------------------------------
    ax = axes[0]
    matched, _ = ps_matching(sample, caliper=0.08)
    treated = sample[sample.treatment == 1]
    control = sample[sample.treatment == 0]
    y_t, y_c = 1.0, 0.0
    ax.scatter(treated.ps, np.full(len(treated), y_t), s=70,
               color=TREATED_C, zorder=3, label="Treated")
    ax.scatter(control.ps, np.full(len(control), y_c), s=70,
               color=CONTROL_C, zorder=3, label="Control")
    # draw matched links
    for pid in matched.pair_id.unique():
        pair = matched[matched.pair_id == pid]
        t = pair[pair.treatment == 1].iloc[0]
        c = pair[pair.treatment == 0].iloc[0]
        ax.plot([t.ps, c.ps], [y_t, y_c], color="0.55", lw=1.0, zorder=1)
    ax.set_title("PSM — pair each treated unit\nwith a similar control (ATT)")
    ax.set_xlabel("Propensity score")
    ax.set_yticks([y_c, y_t]); ax.set_yticklabels(["Control", "Treated"])
    ax.set_ylim(-0.6, 1.6)
    ax.legend(loc="upper left")
    ax.text(0.5, -0.5,
            "Unmatched units are discarded.",
            transform=ax.transAxes, ha="center", fontsize=9,
            style="italic", color="0.35")

    # ---- Right: IPTW (reweighting) ----------------------------------------
    ax = axes[1]
    weighted = iptw_weights(sample)
    # marker size proportional to IPW weight
    sizes = 30 + 90 * (weighted.w_clip - weighted.w_clip.min()) / (
        weighted.w_clip.max() - weighted.w_clip.min() + 1e-9
    )
    t_mask = weighted.treatment == 1
    ax.scatter(weighted.ps[t_mask], np.full(t_mask.sum(), y_t),
               s=sizes[t_mask], color=TREATED_C, alpha=0.7,
               edgecolor="white", zorder=3, label="Treated")
    ax.scatter(weighted.ps[~t_mask], np.full((~t_mask).sum(), y_c),
               s=sizes[~t_mask], color=CONTROL_C, alpha=0.7,
               edgecolor="white", zorder=3, label="Control")
    ax.set_title("IPTW — reweight every unit to build\na balanced pseudo-population (ATE)")
    ax.set_xlabel("Propensity score")
    ax.set_yticks([y_c, y_t]); ax.set_yticklabels(["Control", "Treated"])
    ax.set_ylim(-0.6, 1.6)
    ax.legend(loc="upper left")
    ax.text(0.5, -0.5,
            "Marker size $\\propto$ weight: rare-but-informative units count more.",
            transform=ax.transAxes, ha="center", fontsize=9,
            style="italic", color="0.35")

    fig.suptitle("Two ways to remove confounding from the propensity score",
                 fontsize=14, y=1.02)
    save(fig, "psm_vs_iptw_concept.png")


# --------------------------------------------------------------------------- #
# Figure 3 — Love plot (covariate balance, SMD)
# --------------------------------------------------------------------------- #
def fig_love_plot(df: pd.DataFrame) -> None:
    covars = ["x1", "x2"]
    matched, _ = ps_matching(df, caliper=0.05)
    weighted = iptw_weights(df)

    rows = []
    for v in covars:
        rows.append({
            "covar": v,
            "Unadjusted": standardized_mean_diff(df, v),
            "After PSM": standardized_mean_diff(matched, v),
            "After IPTW": standardized_mean_diff(weighted, v, w_col="w_clip"),
        })
    balance = pd.DataFrame(rows).set_index("covar")

    fig, ax = plt.subplots(figsize=(8, 4.2))
    markers = {"Unadjusted": "o", "After PSM": "s", "After IPTW": "D"}
    colors = {"Unadjusted": "0.4", "After PSM": TREATED_C, "After IPTW": ACCENT_C}
    y = np.arange(len(covars))
    for method in ["Unadjusted", "After PSM", "After IPTW"]:
        ax.scatter(balance[method].abs(), y, s=90, marker=markers[method],
                   color=colors[method], label=method, zorder=3)

    ax.axvline(0.1, color="red", ls="--", lw=1.2)
    ax.text(0.105, 0.97, "SMD = 0.1\nthreshold",
            transform=ax.get_xaxis_transform(),
            color="red", fontsize=9, va="top")
    ax.set_yticks(y); ax.set_yticklabels(covars)
    ax.set_xlabel("|Standardized mean difference|")
    ax.set_title("Covariate balance before vs. after adjustment")
    ax.legend()
    ax.set_xlim(left=0)
    save(fig, "love_plot.png")


# --------------------------------------------------------------------------- #
# Figure 4 — IPTW weight distribution & clipping
# --------------------------------------------------------------------------- #
def fig_weights(df: pd.DataFrame) -> None:
    weighted = iptw_weights(df)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.4))

    # Left: distribution of raw weights by group
    ax = axes[0]
    lbl = weighted.treatment.map({0: "Control", 1: "Treated"})
    sns.histplot(
        x=weighted.w_raw, hue=lbl,
        palette={"Control": CONTROL_C, "Treated": TREATED_C},
        element="step", bins=40, alpha=0.45,
        hue_order=["Control", "Treated"], ax=ax,
    )
    ax.set_title("Raw IPW weights can be extreme")
    ax.set_xlabel("Weight  $w_i = 1/\\hat{\\pi}$  or  $1/(1-\\hat{\\pi})$")
    ax.set_ylabel("Count")
    ax.legend(title="", labels=["Treated", "Control"])

    # Right: raw vs clipped weights
    ax = axes[1]
    ax.scatter(weighted.w_raw, weighted.w_clip, s=18, alpha=0.5,
               color=ACCENT_C, edgecolor="none")
    lim = weighted.w_raw.max() * 1.02
    ax.plot([0, lim], [0, lim], color="0.5", ls=":", lw=1, label="no clipping")
    cap = weighted.w_clip.max()
    ax.axhline(cap, color="red", ls="--", lw=1.2,
               label=f"clip cap $\\approx$ {cap:.1f}")
    ax.set_title("Clipping tames the tail")
    ax.set_xlabel("Raw weight")
    ax.set_ylabel("Clipped weight (PS $\\in$ [0.05, 0.95])")
    ax.legend()

    fig.suptitle("Extreme propensity scores inflate IPTW weights — clip to stabilise",
                 fontsize=13, y=1.02)
    save(fig, "iptw_weights.png")


# --------------------------------------------------------------------------- #
# Figure 5 — Effect estimate comparison
# --------------------------------------------------------------------------- #
def fig_effect_comparison(df: pd.DataFrame) -> None:
    naive = (df.loc[df.treatment == 1, "outcome"].mean()
             - df.loc[df.treatment == 0, "outcome"].mean())
    _, att = ps_matching(df, caliper=0.05)
    weighted = iptw_weights(df)
    ate = iptw_ate(weighted, "w_clip")

    labels = ["Naive\n(unadjusted)", "PSM\n(ATT)", "IPTW\n(ATE)"]
    estimates = [naive, att, ate]
    colors = ["0.55", TREATED_C, ACCENT_C]

    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    bars = ax.bar(labels, estimates, color=colors, width=0.6, zorder=3)
    ax.axhline(TRUE_EFFECT, color="red", ls="--", lw=1.5,
               label=f"True effect = {TRUE_EFFECT:.1f}")
    for b, est in zip(bars, estimates):
        ax.text(b.get_x() + b.get_width() / 2, est + 0.05,
                f"{est:.2f}", ha="center", va="bottom", fontsize=11,
                fontweight="bold")
    ax.set_ylabel("Estimated treatment effect")
    ax.set_title("Recovering the true effect: naive vs. PSM vs. IPTW")
    ax.legend()
    ax.set_ylim(0, max(estimates + [TRUE_EFFECT]) * 1.25)
    save(fig, "effect_comparison.png")


# --------------------------------------------------------------------------- #
def main() -> None:
    df = add_propensity_scores(simulate_data())
    fig_overlap(df)
    fig_concept(df)
    fig_love_plot(df)
    fig_weights(df)
    fig_effect_comparison(df)
    print("All figures generated in", HERE)


if __name__ == "__main__":
    main()
