# Assumptions

## From Observational Data to Conditionally Randomized Experiments

Causal inference from observational data relies on the idea that, under the assumptions of the **Rubin Causal Model** ([Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41)), an observational study can be regarded as a *conditionally randomized experiment*. 

Under the assumptions of ignorability (see below), the observed data represent the essential features of a randomized experiment, enabling the identification and consistent estimation of causal effects within the **potential outcomes framework**.

## Potential Outcomes Framework
- [Rubin (1974)](https://doi.org/10.1037/h0037350) extended Neyman's (1923) theory for randomized experiments to observational studies.
- Specifically, when treatment assignment is **strongly ignorable** given a set of observed covariates - that is, when the following two conditions hold ([Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41)):

$$
(Y(1), Y(0)) \perp\!\!\!\perp T \mid X
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

The observed outcome $Y$ equals the potential outcome $Y(t)$ whenever the treatment actually received is $T = t$. This assumption is what makes potential outcomes empirically meaningful: without it, $Y(t)$ is a purely abstract quantity with no necessary connection to what is measured in data.

**Detecting violations:** Violations arise when the treatment $T$ is not sufficiently well-defined. If units assigned $T = t$ received meaningfully different variants - different doses, formulations, timing, or delivery mechanisms - then $Y(t)$ is not a single quantity but an average over distinct potential outcomes that should not be conflated. Empirically, this manifests as effect heterogeneity within treatment arms that cannot be explained by measured covariates. Stratifying by treatment sub-type and testing whether effect estimates shift substantially is a practical diagnostic. Interference violations are harder to detect but can sometimes be probed by examining whether outcomes of untreated units vary with the treatment density of their neighbours.

([Rubin, 1980](https://doi.org/10.2307/2287653); [Cole & Frangakis, 2009](https://doi.org/10.1097/EDE.0b013e31818ef366); [VanderWeele, 2009](https://doi.org/10.1097/EDE.0b013e3181bd5638))

```{prf:assumption} Stable Unit Treatment Value Assumption (SUTVA)
:label: sutva

$$
Y_i(t_i) \text{ depends only on } t_i \text{ (not on } t_j \text{ for } j \neq i)
$$
```

In Rubin's original formulation, SUTVA bundled no-interference together with consistency; here we treat them separately to make their distinct diagnostics explicit. The **no interference** assumption states that there is no interference between treatment assignment and outcomes across units. Whether one individual receives treatment (or not) has no effect on the potential outcomes of any other individual. This is a restriction on the **potential-outcomes structure** - $Y_i(t_1,\dots,t_n)$ depends only on unit $i$'s own assignment $t_i$ - and is distinct from the usual statistical 'i.i.d.' assumption, which concerns the joint distribution of the *observed* triplets $(X_i, T_i, Y_i)$. The two operate at different levels and neither implies the other: i.i.d. draws can still exhibit spillovers (e.g. a vaccine study where outcomes depend on neighbours' vaccination), and a stratified sample with no spillovers can violate the identically-distributed component of i.i.d. Consequently, i.i.d. sampling diagnostics cannot certify no interference, which can easily be violated in a study of the effect of a vaccine or if a treatment is assigned at a group level ([Rubin, 1980](https://doi.org/10.2307/2287653); [Hudgens & Halloran, 2008](https://doi.org/10.1198/016214508000000292); [Imbens & Rubin, 2015, §1.6](https://doi.org/10.1017/CBO9781139025751)).

**Detecting violations:** Interference is suspected when outcomes of untreated units **correlate with the treatment rate in their neighbourhood or group**. In insurance, if offering a discount to some policyholders influences the behaviour of others in the same household or employer group, SUTVA is violated. Diagnostic: compare outcomes of control units across clusters with different treatment intensities - if they differ systematically, interference is present.

```{note}
SUTVA is often treated as binary - satisfied or violated - but the literature distinguishes **partial interference** ([Hudgens & Halloran, 2008](https://doi.org/10.1198/016214508000000292)), where spillovers operate only within known clusters, from **global interference**, where they may propagate across the entire population. In group health insurance or fleet policies, interference is typically neither absent nor unbounded but **structured by household or employer group membership**: a wellness incentive or safe-driving programme offered to some members of a group may affect the behaviour and outcomes of others in the same group, but not across groups. When this cluster structure is known, spillover effects can be accommodated rather than assumed away. Beyond the cluster models discussed in {ref}`debias`, **spillover-robust estimators** based on the exposure-mapping approach of [Aronow & Samii (2017)](https://doi.org/10.1214/16-AOAS1005) allow consistent estimation of average causal effects under general (partial) interference by modelling each unit's exposure to the treatment of others.
```

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

**Full (joint) exchangeability** - the *strong ignorability* condition of [Rosenbaum & Rubin (1983)](https://doi.org/10.1093/biomet/70.1.41):

$$
(Y(1), Y(0)) \perp\!\!\!\perp T \mid X
$$
```

Conditioning on the observed covariates $X$ is then sufficient to remove confounding bias. This is also called *conditional exchangeability* or *conditional ignorability* ([Rosenbaum & Rubin, 1983](https://doi.org/10.1093/biomet/70.1.41); [Wooldridge, 2012](https://doi.org/10.1016/C2011-0-05506-1)).

```{note}
:class: dropdown

Three nested versions of exchangeability are commonly written down, in *decreasing* order of strength ([Greenland & Robins, 1986](https://doi.org/10.1093/ije/15.3.413), [2009](https://doi.org/10.1186/1742-5573-6-4)):

1. **Full (joint):** $(Y(1), Y(0)) \perp\!\!\!\perp T \mid X$.
2. **Marginal (per-treatment):** $Y(t) \perp\!\!\!\perp T \mid X$ for all $t$.
3. **Mean exchangeability:** $\mathbb{E}[Y(t) \mid X, T=t] = \mathbb{E}[Y(t) \mid X]$ for all $t$.

Joint independence of the *pair* implies each marginal, but the converse fails in general (two variables can each be independent of $T$ yet not *jointly* independent of it); likewise the marginal form implies mean exchangeability but not conversely. The three levels identify different targets:

- **Mean exchangeability (weakest) is all that the ATE requires**, $\mathbb{E}[Y(1)] - \mathbb{E}[Y(0)]$ - and likewise the CATE $\tau(x)$ - because these depend only on the per-arm outcome *means*.
- **The marginal form** additionally identifies the full marginal outcome *distributions* $P(Y(t) \mid X)$, and hence quantile treatment effects.
- **The full joint form** is needed only for functionals of the *joint* law of $(Y(1), Y(0))$ - the distribution of individual treatment effects, the treated/untreated outcome correlation, or the proportion who benefit.

They should therefore be ranked **full $\succ$ marginal $\succ$ mean**, and only the level actually required for the target estimand need be invoked. The joint form is stated above because it is the classical strong-ignorability condition.
```

In case of violation, exchangeability often produces severe bias, which is a separate dimension from the **probability** that it is violated in a given study; a mild but plausible violation and a severe but implausible one warrant very different responses.

```{note}
:class: dropdown

Rather than treating exchangeability as a binary "true or false" property, it is more useful to adopt a **graduated view of assumption strength**. The empirically productive question is not *"does unobserved confounding exist?"* - it almost always does to some degree - but *"how strong would an unmeasured confounder have to be to overturn our conclusion?"* This reframing makes **sensitivity analysis the natural companion to the exchangeability assumption from the moment it is introduced**: tools such as E-values, Rosenbaum bounds, and Manski-style partial-identification bounds operationalise exactly this graduated view. They are developed in {doc}`sensitivity` and {doc}`diagnostics`.
```

**Detecting violations:** Exchangeability **cannot be directly tested** because it concerns unobserved confounders by definition. However, indirect evidence includes: (1) **sensitivity analysis** - computing E-values or applying the method of [Cinelli & Hazlett (2020)](https://doi.org/10.1111/rssb.12348) to assess how strong an unmeasured confounder would need to be to explain away the effect; (2) **negative control outcomes** - outcomes known to be unaffected by $T$ that should show zero effect if exchangeability holds; (3) **placebo/falsification tests** - applying the estimator to subgroups where no effect is expected. Persistent sensitivity of results to small unmeasured confounders signals concern.

By exchangeability ({prf:ref}`exchangeability`) and consistency ({prf:ref}`consistency`), the estimation of the average (causal) treatment effect can be done based on observed data. At the level of a fixed covariate profile $X=x$,

$$
\mathbb{E}[Y(t) \mid X=x] 
\overset{\text{exch.}}{=}\mathbb{E}[Y(t) \mid X=x, T=t]
\overset{\text{cons.}}{=}\mathbb{E}[Y \mid X=x, T=t],
$$

and marginalising over the covariate distribution (the *g-formula*) yields the average potential outcome:

$$
\mathbb{E}[Y(t)] = \mathbb{E}_X\big[\, \mathbb{E}[Y \mid X, T=t] \,\big].
$$
