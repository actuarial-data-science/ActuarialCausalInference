# Causal Inference

With the identification assumptions ({prf:ref}`consistency`, {prf:ref}`sutva`, {prf:ref}`positivity`, {prf:ref}`exchangeability`) established and the correct adjustment set identified via graphical models ({prf:ref}`backdoor-criterion`), we can now turn to **estimation**: computing causal effects from observed data $D = \{(X_i, T_i, Y_i)\}_{i=1}^{n}$.

## From Identification to Estimation

Identification tells us *what* to estimate — it equates a causal estimand with a statistical estimand:

$$
\underbrace{\mathbb{E}[Y(t)]}_{\text{causal}} = \underbrace{\sum_x \mathbb{E}[Y \mid T=t, X=x] \, P(X=x)}_{\text{statistical (adjustment formula)}}
$$

Estimation tells us *how* to compute this quantity from a finite sample. The choice of estimator involves trade-offs between bias, variance, robustness to model misspecification, and the type of treatment effect being targeted.

## Treatment Effects

The three fundamental causal estimands are:

* **Average Treatment Effect (ATE):** The population-level causal effect:
    $$\tau = \mathbb{E}[Y(1) - Y(0)]$$
* **Conditional Average Treatment Effect (CATE):** The effect for a subpopulation with characteristics $X = x$:
    $$\tau(x) = \mathbb{E}[Y(1) - Y(0) \mid X=x]$$
* **Average Treatment Effect on the Treated (ATT):** The effect for those who actually received treatment:
    $$\text{ATT} = \mathbb{E}[Y(1) - Y(0) \mid T=1]$$

Different estimation methods target different estimands. The table below maps methods to their primary targets.

## Estimation Methods Overview

| Method | Primary Estimand | Key Idea | Section |
|--------|-----------------|----------|---------|
| **Propensity Score Matching** | ATT | Pair treated/control units with similar $\pi(x)$ | {doc}`propensity` |
| **Inverse Probability Weighting** | ATE | Re-weight sample to remove confounding | {doc}`propensity` |
| **Double Machine Learning** | ATE | Residualise both $Y$ and $T$ on $X$ to isolate causal variation | {doc}`regression_methods` |
| **Instrumental Variables / 2SLS** | LATE | Use exogenous variation from an instrument | {doc}`regression_methods` |
| **Causal Trees** | CATE | Recursive partitioning to maximise treatment effect heterogeneity | {doc}`tree_based_methods` |
| **Causal Forests** | CATE | Ensemble of causal trees with adaptive neighbourhood weighting | {doc}`tree_based_methods` |
| **Bayesian (BART / BCF)** | CATE | Posterior distributions over treatment effects via sum-of-trees priors | {doc}`bayesian` |

## Chapter Contents

This chapter covers the following estimation approaches:

### Propensity Score Methods

**{doc}`propensity`** — Methods that use the estimated propensity score $\pi(x) = P(T=1 \mid X=x)$ to balance treated and control groups. Covers propensity score matching (targeting ATT) and inverse probability weighting (targeting ATE).

### Regression Methods

**{doc}`regression_methods`** — Regression-based approaches including outcome regression / g-computation, doubly robust estimators (AIPW, TMLE), Double Machine Learning (DML) and meta-learners for heterogeneous effects, plus quasi-experimental designs (IV / 2SLS, difference-in-differences, regression discontinuity, synthetic control).

### Tree-Based Methods

**{doc}`tree_based_methods`** — Causal trees partition the covariate space to discover subpopulations with heterogeneous treatment effects (CATEs) using honest splitting ([Athey & Imbens, 2016](https://doi.org/10.1073/pnas.1510489113)), and causal forests extend them to an ensemble that estimates individualised effects via adaptive nearest-neighbour weighting ([Wager & Athey, 2018](https://doi.org/10.1080/01621459.2017.1319839); [Athey, Tibshirani & Wager, 2019](https://doi.org/10.1214/18-AOS1709)).

### Bayesian Approaches

**{doc}`bayesian`** — Bayesian causal inference treats missing potential outcomes as parameters with prior distributions, yielding full posterior distributions over treatment effects. Covers BART, Bayesian Causal Forests (BCF), and Bayesian propensity scores.
