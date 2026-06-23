# Identification

Before any causal effect can be *estimated* from data, it must first be **identified** — expressed purely in terms of the observed data distribution under a set of explicit, structural assumptions. Identification is the bridge between a **causal estimand**, defined through potential outcomes (e.g. $\mathbb{E}[Y(1) - Y(0)]$), and a **statistical estimand**, a quantity computable from the observed dataset $D = \{(X_i, T_i, Y_i)\}_{i=1}^{n}$.

This chapter develops the identification toolkit in three steps, using the notation established in {doc}`concepts`: covariates $X$, treatment $T$, outcome $Y$, confounders, and the propensity score $\pi(x) = P(T=1 \mid X=x)$.

## Assumptions for Achieving Identifiability

**{doc}`assumptions`** — The four core assumptions — consistency, SUTVA, positivity, and exchangeability — that allow a causal estimand to be equated with a statistical one. These conditions formalise *when* an observational study can be treated as a conditionally randomized experiment, and how to detect violations of each in practice.

## Achieving Identifiability with Graphical Models

**{doc}`graphical_models`** — Directed acyclic graphs (DAGs) as the language for encoding causal assumptions. Covers the three fundamental path structures (chains, forks, colliders), $d$-separation, and the backdoor and frontdoor criteria for selecting a valid adjustment set relative to the treatment $T$ and outcome $Y$.

## Structural Identification Strategies

**{doc}`methods`** — The main identification strategies that re-express a causal estimand in terms of the observed data distribution: back-door adjustment when all confounders are observed, front-door adjustment through an observed mediator, and instrumental variables when confounding is unmeasured. Each strategy sets up an estimand that the methods in {doc}`inference` then estimate.