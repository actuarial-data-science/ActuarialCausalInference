# Identification

Before any causal effect can be *estimated* from data, it must first be **identified** — expressed purely in terms of the observed data distribution under a set of explicit, structural assumptions. Identification is the bridge between a **causal estimand**, defined through potential outcomes (e.g. $\mathbb{E}[Y(1) - Y(0)]$), and a **statistical estimand**, a quantity computable from the observed dataset $D = \{(X_i, T_i, Y_i)\}_{i=1}^{n}$.

This chapter develops the identification toolkit in three steps, using the notation established in {doc}`concepts`: covariates $X$, treatment $T$, outcome $Y$, confounders, and the propensity score $\pi(x) = P(T=1 \mid X=x)$.

## Assumptions for Achieving Identifiability

**{doc}`assumptions`** — The four core assumptions — consistency, SUTVA, positivity, and exchangeability — that allow a causal estimand to be equated with a statistical one. These conditions formalise *when* an observational study can be treated as a conditionally randomized experiment, and how to detect violations of each in practice.

## Achieving Identifiability with Graphical Models

**{doc}`graphical_models`** — Directed acyclic graphs (DAGs) as the language for encoding causal assumptions. Covers the three fundamental path structures (chains, forks, colliders), $d$-separation, and the backdoor and frontdoor criteria for selecting a valid adjustment set relative to the treatment $T$ and outcome $Y$.

## Structural Identification Strategies

**{doc}`methods`** — The main identification strategies that re-express a causal estimand in terms of the observed data distribution: back-door adjustment when all confounders are observed, front-door adjustment through an observed mediator, and instrumental variables when confounding is unmeasured. Each strategy sets up an estimand that the methods in {doc}`inference` then estimate.

```{warning}
The back-door criterion is often presented as a **mechanical check** — given an adjustment set, verify that it blocks all back-door paths. In practice, however, the analyst must first **construct the DAG**, and unmeasured confounders — socioeconomic status, risk attitude, prior claims held outside the insurer's database — simply cannot be entered as nodes to adjust for. Satisfying the back-door criterion is therefore an **untestable claim about the completeness of the measured covariate set**, not a property that can be verified from data. Because conditional ignorability cannot be confirmed empirically, **sensitivity analysis is the only way to quantify how far from it the analyst may be**: E-values ([VanderWeele & Ding, 2017](https://doi.org/10.7326/M16-2607)) and the partial-$R^2$ / omitted-variable-bias framework ([Cinelli & Hazlett, 2020](https://doi.org/10.1111/rssb.12348)) express how strong an unmeasured confounder would have to be to overturn the conclusion. These tools are developed in {doc}`sensitivity`.
```