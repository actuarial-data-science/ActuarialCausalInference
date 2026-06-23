# Assumptions

## From Observational Data to Conditionally Randomized Experiments

Causal inference from observational data relies on the idea that, under the assumptions of the **Rubin Causal Model** ([Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41)), an observational study can be regarded as a *conditionally randomized experiment*. 

Under the assumptions of ignorability (see below), the observed data represent the essential features of a randomized experiment, enabling the identification and consistent estimation of causal effects within the **potential outcomes framework**.

## Potential Outcomes Framework
- [Rubin (1974)](https://doi.org/10.1037/h0037350) extended Neyman's (1923) theory for randomized experiments to observational studies.
- Specifically, when treatment assignment is **strongly ignorable** given a set of observed covariates — that is, when the following two conditions hold ([Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41)):

$$
(Y(1), Y(0)) \perp T \mid X
$$

$$
0 < P(T = 1 \mid X) < 1,
$$

then conditioning on $X$ renders the treatment assignment mechanism analogous to that of a randomized controlled trial. More explanation in the [Assumptions Guide](https://www.uniqcret.com/post/causal-inference-assumptions-guide) and in [Neal (2020)](https://www.bradyneal.com/Introduction_to_Causal_Inference-Aug27_2020-Neal.pdf). See also [Oxford: Causal Assumptions](https://www.stats.ox.ac.uk/~evans/APTS/causassmp.html) for a formal treatment.

### Assumptions

```{prf:assumption} Consistency
:label: consistency

$$
Y(t) = Y \quad \text{when } T = t
$$
```

Links the potential outcomes to the observed outcomes by requiring that the two are equal under the same treatment assignments. This ties the potential outcome $Y(t)$ to the factual outcome $Y$ when the treatment actually received is $T = t$ ([Rubin, 1974](https://doi.org/10.1037/h0037350)).

**Detecting violations:** Consistency is violated when the treatment $T$ is **not well-defined** — i.e., it encompasses multiple distinct versions. If "treated" patients received different dosages, formulations, or timing, then $Y(1)$ is ambiguous. In data, look for heterogeneous treatment protocols, poor adherence, or treatment variation within the $T=1$ group. If the effect estimate changes substantially when stratifying by treatment sub-type, consistency may be compromised.

```{prf:assumption} Stable Unit Treatment Value Assumption (SUTVA)
:label: sutva

$$
Y_i(t_i) \text{ depends only on } t_i \text{ (not on } t_j \text{ for } j \neq i)
$$
```

SUTVA combines consistency and no interference. The **no interference** assumption states that there is no interference between treatment assignment and outcomes across units. Whether one individual receives treatment (or not) has no effect on the potential outcomes of any other individual. This is encapsulated by the usual statistical 'i.i.d.' assumption, but it can easily be violated in a study of the effect of a vaccine or if a treatment is assigned at a group level ([Angrist & Pischke, 2015](https://doi.org/10.2307/j.ctt5vhbqm)).

**Detecting violations:** Interference is suspected when outcomes of untreated units **correlate with the treatment rate in their neighbourhood or group**. In insurance, if offering a discount to some policyholders influences the behaviour of others in the same household or employer group, SUTVA is violated. Diagnostic: compare outcomes of control units across clusters with different treatment intensities — if they differ systematically, interference is present.

```{prf:assumption} Positivity
:label: positivity

$$
0 < P(T = 1 \mid X = x) < 1 \quad \text{with probability } 1
$$

or more strictly (strict positivity):

$$
\varepsilon < P(T = 1 \mid X = x) < 1 - \varepsilon \quad \text{with probability } 1, \text{ for some } \varepsilon > 0
$$
```

This states that, for any possible covariate profile, treatment assignment is not deterministic. For all but a measure zero subset of the population, the probability of receiving treatment **and** of receiving control is non-zero. Violations of positivity lead to extreme propensity score weights and unstable estimates ([Austin, 2011](https://doi.org/10.1080/00273171.2011.568786); [Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41)).

**Detecting violations:** Positivity violations are the most **directly diagnosable** from data. Check the estimated propensity scores $\hat{\pi}(x)$: if they cluster near 0 or 1, some covariate strata have near-deterministic treatment assignment. Diagnostics include: propensity score histograms by treatment group (looking for non-overlap), examining covariate regions with no treated or no control units, and inspecting inverse-probability weights for extreme values. In insurance, positivity fails when certain policyholder profiles are *always* or *never* eligible for a programme. See {ref}`overlap` for how this assumption translates into the *common support* requirement underlying propensity score methods.

```{prf:assumption} Exchangeability (No unobserved confounding)
:label: exchangeability

$$
Y(t) \perp\!\!\!\perp T \mid X \quad \text{for all } t
$$

or equivalently:

$$
(Y(1), Y(0)) \perp\!\!\!\perp T \mid X
$$
```

This implies that conditioning on the observed covariates $X$ is sufficient to remove confounding bias. This is also called *conditional exchangeability*, *conditional ignorability*, or *causal sufficiency* ([Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41); [Wooldridge, 2012](https://doi.org/10.1016/C2011-0-05506-1)). This is the strongest and least verifiable of the four assumptions — see the [Assumptions Guide](https://www.uniqcret.com/post/causal-inference-assumptions-guide) for discussion.

**Detecting violations:** Exchangeability **cannot be directly tested** because it concerns unobserved confounders by definition. However, indirect evidence includes: (1) **sensitivity analysis** — computing E-values or applying the method of [Cinelli & Hazlett (2020)](https://doi.org/10.1111/rssb.12348) to assess how strong an unmeasured confounder would need to be to explain away the effect; (2) **negative control outcomes** — outcomes known to be unaffected by $T$ that should show zero effect if exchangeability holds; (3) **placebo/falsification tests** — applying the estimator to subgroups where no effect is expected. Persistent sensitivity of results to small unmeasured confounders signals concern.

By exchangeability ({prf:ref}`exchangeability`) and consistency ({prf:ref}`consistency`), the estimation of the average (causal) treatment effect can be done based on observed data:

$$
\mathbb{E}[Y(t) \mid T=t] 
\overset{\text{exch.}}{=}\mathbb{E}[Y(t) \mid T=t, X=x]
\overset{\text{cons.}}{=}\mathbb{E}[Y \mid T=t, X=x]
$$
