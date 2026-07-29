# Causal Inference

With the identification assumptions ({prf:ref}`consistency`, {prf:ref}`sutva`, {prf:ref}`positivity`, {prf:ref}`exchangeability`) established and the correct adjustment set identified via graphical models ({prf:ref}`backdoor-criterion`), we can now turn to **estimation**: computing causal effects from observed data $D = \{(X_i, T_i, Y_i)\}_{i=1}^{n}$.

## From Identification to Estimation

Identification tells us *what* to estimate — it equates a causal estimand with a statistical estimand:

$$
\underbrace{\mathbb{E}[Y(t)]}_{\text{causal}} = \underbrace{\sum_x \mathbb{E}[Y \mid T=t, X=x] \, P(X=x)}_{\text{statistical (adjustment formula)}}
$$

Estimation tells us *how* to compute this quantity from a finite sample. The choice of estimator involves trade-offs between bias, variance, robustness to model misspecification, and the type of treatment effect being targeted.

## Treatment Effects

The main causal estimands targeted in this tutorial are:

* **Average Treatment Effect (ATE):** The population-level causal effect:
    $$\tau = \mathbb{E}[Y(1) - Y(0)]$$
* **Conditional Average Treatment Effect (CATE):** The effect for a subpopulation with characteristics $X = x$:
    $$\tau(x) = \mathbb{E}[Y(1) - Y(0) \mid X=x]$$
* **Average Treatment Effect on the Treated (ATT):** The effect for those who actually received treatment:
    $$\text{ATT} = \mathbb{E}[Y(1) - Y(0) \mid T=1]$$
* **Local Average Treatment Effect (LATE):** The effect among the *compliers* — units whose treatment status responds to an instrument $Z$:
    $$\text{LATE} = \mathbb{E}[Y(1) - Y(0) \mid \text{complier}]$$
    Recovered by instrumental-variable methods, it conditions on complier status rather than treatment receipt, so it is a distinct estimand from the ATT ([Imbens & Angrist, 1994](https://doi.org/10.2307/2951620)).

Different estimation methods target different estimands. The table below maps methods to their primary targets.

## Estimation Methods Overview

| Method | Primary Estimand | Key Idea | Chapter |
|--------|-----------------|----------|---------|
| **G-computation** | ATE | Model the outcome $\mathbb{E}[Y \mid T, X]$ and contrast predictions | {doc}`direct_adjustment` |
| **Propensity Score Matching** | ATT | Pair treated/control units with similar $\pi(x)$ | {doc}`direct_adjustment` |
| **Inverse Probability Weighting** | ATE | Re-weight sample to remove confounding | {doc}`direct_adjustment` |
| **AIPW / TMLE / DML** | ATE | Combine outcome and propensity models for robustness | {doc}`direct_adjustment` |
| **Meta-Learners (S/T/X, R/DR)** | CATE | Decompose CATE estimation into regression sub-tasks | {doc}`heterogeneous_effects` |
| **Causal Trees / Forests** | CATE | Partition covariate space to expose effect heterogeneity | {doc}`heterogeneous_effects` |
| **Instrumental Variables / 2SLS** | LATE | Use exogenous variation from an instrument | {doc}`instrumental_variables` |
| **Quasi-Experimental (DiD, RD, SC)** | ATT | Exploit natural experiments and institutional variation | {doc}`quasi_experimental` |
| **Bayesian (BART / BCF)** | CATE | Posterior distributions over treatment effects via sum-of-trees priors | {doc}`bayesian` |

## Chapter Contents

This chapter covers the following estimation approaches, grouped by the strategy they use to recover a causal effect:

### Direct Adjustment

**{doc}`direct_adjustment`** — Estimating $\mathbb{E}[Y(t)]$ by modelling the outcome, the treatment, or both. Covers outcome regression / g-computation, propensity score matching (ATT) and inverse probability weighting (ATE), the doubly robust estimators AIPW and TMLE, and Double Machine Learning (DML).

### Heterogeneous Treatment Effects

**{doc}`heterogeneous_effects`** — Estimating the conditional average treatment effect $\tau(x) = \mathbb{E}[Y(1) - Y(0) \mid X = x]$. Covers the S-, T-, and X-learners, the R- and DR-learners, and causal trees and forests, which partition the covariate space to discover for *whom* a treatment works ([Athey & Imbens, 2016](https://doi.org/10.1073/pnas.1510489113); [Wager & Athey, 2018](https://doi.org/10.1080/01621459.2017.1319839)).

### Instrumental Variables

**{doc}`instrumental_variables`** — Identification and estimation under unmeasured confounding via an instrument. Covers the instrumental-variable estimand, its two-stage least-squares (2SLS) implementation, and Mendelian randomization.

### Quasi-Experimental Designs

**{doc}`quasi_experimental`** — Exploiting natural experiments and institutional variation. Covers difference-in-differences, regression discontinuity, and synthetic control.

### Bayesian Causal Inference

**{doc}`bayesian`** — Bayesian analogues of the methods above. Treats missing potential outcomes as parameters with prior distributions, yielding full posterior distributions over treatment effects; covers the Bayesian potential outcomes model, Bayesian propensity scores, BART, and Bayesian Causal Forests (BCF).
