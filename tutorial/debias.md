# Biases and De-Biasing Toolkit

In {doc}`assumptions` we established the four assumptions - {prf:ref}`consistency`, {prf:ref}`sutva`, {prf:ref}`positivity`, and {prf:ref}`exchangeability` - that allow causal effects to be identified from observational data. In {doc}`graphical_models` we introduced DAGs as the language for encoding and reasoning about these assumptions. In practice, **assumptions are rarely perfectly satisfied**. This chapter is a practical guide for the actuary: how to diagnose what went wrong, how to fix it, and how to ensure the resulting model is fair.

## What went wrong? - From Assumption Violations to Biases

When a causal assumption is violated, a specific bias enters the treatment effect estimate. The table below maps each assumption to the bias it produces and the diagnostic pattern visible in data.

| Violated Assumption | Bias | Diagnostic Pattern |
|---|---|---|
| {prf:ref}`exchangeability` | Confounding | Effect estimate changes when adjusting for additional covariates |
| {prf:ref}`exchangeability` (population) | Selection bias | Sample composition differs systematically from target population |
| Incorrect adjustment | Collider bias | Conditioning on a post-treatment variable *creates* an association |
| {prf:ref}`positivity` | Extreme weights | Propensity scores cluster near 0 or 1; IPW estimates are unstable |
| {prf:ref}`sutva` | Interference | Control outcomes correlate with treatment intensity in neighbouring units |
| {prf:ref}`consistency` | Treatment ambiguity | Effect estimates vary when stratifying by treatment sub-type |

The remainder of this section defines each bias precisely.

### Confounding Bias

```{prf:definition} Confounding Bias
:label: confounding-bias

**Confounding bias** occurs when a fork variable $F$ causally influences both the treatment $T$ and the outcome $Y$, and the analysis fails to adjust for $F$.
```

```{figure} figs/confounding.svg
:width: 55%
:name: fig-confounding-bias

Confounding: the fork variable $F$ influences both treatment $T$ and outcome $Y$, biasing the naive $T$–$Y$ comparison unless adjusted for.
```

Confounding violates {prf:ref}`exchangeability`. The naive comparison conflates the causal effect on the treated with a baseline difference between groups:

$$
\mathbb{E}[Y \mid T{=}1] - \mathbb{E}[Y \mid T{=}0] = \underbrace{\mathbb{E}[Y(1) - Y(0) \mid T{=}1]}_{\text{ATT}} + \underbrace{\mathbb{E}[Y(0) \mid T{=}1] - \mathbb{E}[Y(0) \mid T{=}0]}_{\text{confounding bias}}
$$

The first term is the **average treatment effect on the treated** (ATT), not the unconditional ATE: with the single confounding-bias residual shown, equality with the ATE would additionally require no effect modification by treatment status, $\mathbb{E}[Y(1) - Y(0) \mid T{=}1] = \mathbb{E}[Y(1) - Y(0)]$ ([Angrist & Pischke, 2009, Sec. 3.2](https://doi.org/10.1515/9781400829828)).

In insurance, confounding arises when healthier policyholders self-select into wellness programmes, making the programme *appear* more effective than it is.

### Selection Bias

```{prf:definition} Selection Bias
:label: selection-bias

**Selection bias** arises when the sample analysed is not representative of the target population, because selection into the sample depends on variables related to both $T$ and $Y$.
```

Selection bias can occur at study entry (differential enrolment), during follow-up (differential attrition), or through post-treatment conditioning. It violates {prf:ref}`exchangeability` at the population level. In insurance, survivorship bias in long-term policy data is a common example: only policies that were not cancelled are observed.

When selection acts through a variable that is a *common effect* of $T$ and $Y$ (or of their causes) - as in survivorship or filed-claim samples - the underlying mechanism is exactly the **collider-stratification bias** defined next: "selection bias" and "collider bias" are then the *same* structural phenomenon seen from the sampling side versus the adjustment side ([Hernán, Hernández-Díaz & Robins, 2004](https://doi.org/10.1097/01.ede.0000135174.63482.43); [Hernán & Robins, 2020](https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/), Ch. 8). What matters for remediation is not the label but *where the collider sits*: it must never be "adjusted for" (that induces the bias), yet when selection is unavoidable an unbiased effect can often be recovered by **reweighting on the inverse probability of selection** (IPCW), provided the selection mechanism is itself modelled.

### Collider Bias

```{prf:definition} Collider Bias
:label: collider-bias-def

**Collider bias** (Berkson's paradox) occurs when the analysis conditions on a **collider** $C$ - a common effect of $T$ and $Y$. Conditioning on $C$ opens a non-causal path between $T$ and $Y$.
```

```{figure} figs/collider_bias.svg
:width: 55%
:name: fig-collider-bias

Collider bias: $C$ is a common effect of $T$ and $Y$. Conditioning on $C$ opens a non-causal path between treatment and outcome.
```

Collider bias results from **incorrect adjustment**, not from a violated assumption per se. In insurance, analysing claims conditional on whether a claim was *filed* can introduce collider bias, since filing depends on both the treatment and the outcome severity. A collider can be conditioned on in two ways: *explicitly*, by adjusting for a post-treatment common effect, or *implicitly*, by **selecting** the sample on one - the latter is precisely the collider mechanism behind the selection bias above, so the two categories overlap rather than being mutually exclusive ([Hernán, Hernández-Díaz & Robins, 2004](https://doi.org/10.1097/01.ede.0000135174.63482.43)). The remedy differs by route: an *explicitly* adjusted collider is fixed simply by **not conditioning on it** (DAG-guided variable selection, {prf:ref}`backdoor-criterion`), whereas a collider baked into the *sampling* cannot be un-selected and must instead be corrected by **inverse-probability-of-selection weighting** (IPCW). DAG-guided variable selection is the primary safeguard against the first route.

### Positivity Violations

When {prf:ref}`positivity` is violated, propensity score weights $w = 1/\hat{\pi}(x)$ or $w = 1/(1-\hat{\pi}(x))$ become extreme, leading to high-variance, unstable estimates. It is essential to distinguish two qualitatively different positivity problems ([Hernán & Robins, 2020](https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/), Ch. 3; [Crump et al., 2009](https://doi.org/10.1093/biomet/asn055)):

- **Structural (deterministic) violations** - certain covariate profiles have *zero theoretical probability* of receiving treatment. In insurance this arises from **ineligibility rules**: a discount automatically applied above a certain age, or a programme closed to certain risk classes. Here the causal effect is simply *not identified* for those units, and **no reweighting scheme can repair a structural zero** - the only valid remedy is to **redefine the target population** to the subset where treatment is possible.
- **Empirical (near-)violations** - the true propensity lies strictly between 0 and 1, but finite-sample sparsity produces estimated scores that cluster near 0 or 1. These are a variance problem, not an identification problem, and can be mitigated by stabilised weights, overlap weighting, or trimming.

### Interference

When {prf:ref}`sutva` is violated because one unit's treatment affects another's outcome, the standard individual-level estimators are biased. In insurance, this arises when offering a group discount changes behaviour across all members of a household or employer group. Interference is rarely all-or-nothing: it is often **partial** ([Hudgens & Halloran, 2008](https://doi.org/10.1198/016214508000000292)), with spillovers confined to known clusters such as households or employer groups, rather than propagating globally across the portfolio.

## How to fix it - The De-biasing Toolkit

The biases above are not merely theoretical concerns - they are practical obstacles that the actuary must address. The following table organises the available de-biasing strategies by *what you do*, maps each to the bias it addresses, and links to the estimation methods covered in later chapters.

| Strategy | Addresses | Covered in |
|---|---|---|
| **Adjust** (regression, propensity scores, doubly robust) | Confounding, selection | {doc}`propensity`, {doc}`regression_methods` |
| **Reweight** (IPW, IPCW, overlap weighting) | Confounding, selection, positivity | {doc}`propensity` |
| **Restrict** (trimming, redefine target population) | Positivity violations | {doc}`propensity` |
| **Model the causal structure** (DAG-guided variable selection) | Collider bias, confounding | {doc}`graphical_models` |
| **Cluster or network models** (incl. exposure-mapping / spillover-robust estimators) | Interference / spillover | - |
| **Sensitivity analysis** | Unobserved confounding | {doc}`sensitivity` |

### Adjust

Include confounders $F$ as covariates in the outcome model ([Wooldridge, 2012](https://doi.org/10.1016/C2011-0-05506-1)), or use propensity score methods - matching, stratification, or inverse-probability weighting on $\pi(x) = P(T{=}1 \mid X{=}x)$ ([Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41); [Austin, 2011](https://doi.org/10.1080/00273171.2011.568786)). **Doubly robust** estimators combine both approaches and are consistent if *either* the outcome model or the propensity model is correctly specified. Note that these strategies all target the ATE or ATT on the full (treated) population. When unmeasured confounders exist, **instrumental variables** exploit exogenous variation to recover a causal effect ([Angrist & Pischke, 2015](https://doi.org/10.2307/j.ctt5vhbqm)) - but a *different* estimand: under effect heterogeneity IV identifies the **Local Average Treatment Effect** (LATE), the effect among the *compliers* whose treatment status responds to the instrument, not the ATE or ATT ([Imbens & Angrist, 1994](https://doi.org/10.2307/2951620)). Because the complier subpopulation is specific to the instrument used, the LATE can differ markedly from the portfolio-wide effect an underwriter actually needs - so IV is not a drop-in substitute for the estimators above.

### Reweight

Inverse-probability weighting (IPW) creates a pseudo-population in which treatment is independent of confounders - provided the propensity model is correctly specified, since IPW is singly robust and biased under misspecification ([Kang & Schafer, 2007](https://doi.org/10.1214/07-STS227)). **Inverse-probability-of-censoring weighting** (IPCW) extends this idea to correct for selection bias due to attrition or censoring. **Stabilised weights** $w^{s} = P(T{=}t) / P(T{=}t \mid X)$ reduce variance ([Austin, 2011](https://doi.org/10.1080/00273171.2011.568786)). **Overlap weighting** - assigning each treated unit weight $1-\pi(x)$ and each control unit weight $\pi(x)$, whose product $\pi(x)(1-\pi(x))$ is the tilting function defining the overlap population ([Li, Morgan & Zaslavsky, 2018](https://doi.org/10.1080/01621459.2016.1260466)) - naturally down-weights units in regions of poor overlap and is particularly useful when positivity is borderline.

### Restrict

When certain covariate strata have near-deterministic treatment assignment, the estimand itself may need to change. **Trimming** removes units with $\hat{\pi}(x) < \varepsilon$ or $\hat{\pi}(x) > 1 - \varepsilon$ (e.g. $\varepsilon = 0.05$), targeting a *trimmed* population ATE ([Crump et al., 2009](https://doi.org/10.1093/biomet/asn055)). Alternatively, **redefine the target population** to the overlap population where both treatment and control are plausible. Redefining the estimand is the *only* valid response to **structural** positivity violations (ineligibility rules), where reweighting cannot help ([Hernán & Robins, 2020](https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/), Ch. 3).

### Model the causal structure

Use a DAG to distinguish confounders (adjust for them) from colliders (do not condition on them) and mediators. A mediator must **not** be handled by naive regression conditioning when a *direct* effect is the goal: conditioning on a mediator $M$ in a regression of $Y$ on $(T, M, X)$ does **not** identify the natural direct effect (NDE). It recovers at best the *controlled* direct effect (CDE) at a fixed level of $M$, and even that only if there is no unmeasured mediator–outcome confounder $U_M$ (a variable affecting both $M$ and $Y$) - otherwise conditioning on $M$ opens the collider path $M \leftarrow U_M \rightarrow Y$ and *introduces* bias. Such confounding is endemic in insurance data (health status, risk attitude, and socio-economic status all affect both programme engagement and claim outcomes). The NDE, $\mathbb{E}[Y(t, M(t'))\mid\cdot]$, where $t'$ denotes the alternative treatment, is identified only by the mediation formula under a strictly stronger set of assumptions (no unmeasured mediator–outcome confounding), not by regression conditioning (Pearl, 2001; VanderWeele, 2015). The {prf:ref}`backdoor-criterion` from {doc}`graphical_models` provides an algorithmic tool for selecting a valid covariate *adjustment set*. The {prf:ref}`frontdoor-criterion` is **not** an adjustment-set selector but an alternative identification strategy for the case where no admissible adjustment set exists - because every backdoor path runs through an unmeasured confounder - recovering the effect through a mediator rather than by covariate adjustment ([Pearl, 2009](https://doi.org/10.1017/CBO9780511803161), Cor. 3.3.4).

### Cluster or network models

When interference is present, assign treatment at the group level and analyse at the cluster level. **Partial interference models** assume spillover occurs only within known clusters (e.g. households, employer groups). **Spatial or network models** explicitly model the dependence structure. **Spillover-robust estimators** based on the exposure-mapping approach of [Aronow & Samii (2017)](https://doi.org/10.1214/16-AOAS1005) go further, allowing consistent estimation of average causal effects under general (partial) interference by modelling each unit's exposure to the treatment of others - a natural fit for group health insurance or fleet policies where spillovers are structured by household or employer group membership.

### Sensitivity analysis

{prf:ref}`exchangeability` cannot be verified from data alone. **Sensitivity analysis** quantifies how strong an unmeasured confounder would need to be to explain away the estimated effect. Methods include E-values, Rosenbaum bounds, and partial $R^2$ sensitivity - covered in detail in {doc}`sensitivity`.
