
## Why Causal Inference Resolves the Fairness Problem

Beyond causal bias, actuaries face a distinct but related challenge: ensuring that models do not discriminate against protected groups. EU regulation prohibits the use of protected characteristics (e.g. gender, ethnicity) for insurance pricing, but simply dropping the sensitive attribute $S$ does not solve the problem.

### Proxy Discrimination

```{prf:definition} Proxy Discrimination
:label: proxy-discrimination-def
:class: dropdown

**Proxy discrimination** (indirect discrimination) occurs when non-protected covariates $X$ that are correlated with the sensitive attribute $S$ allow the model to implicitly reconstruct $S$, even though $S$ is not used as an input.
```

The mechanism is the tower property of conditional expectation: $\mu(X) = \int \mu(X, s) \, \mathrm{d}P(S{=}s \mid X)$. If $X$ and $S$ are dependent, the unawareness price channels information about $S$ through $X$ ([Lindholm et al., 2022](https://arxiv.org/abs/2209.00858)).

### From Unawareness to Counterfactual Fairness

```{prf:definition} Fairness through Unawareness
:label: fairness-unawareness
:class: dropdown

A model satisfies **fairness through unawareness** if it does not use the sensitive attribute $S$ as input: $\hat{\mu}(X) = f(X)$.
```

Unawareness is necessary but not sufficient — it does not prevent proxy discrimination.

```{prf:definition} Discrimination-Free Pricing
:label: discrimination-free-pricing
:class: dropdown

An insurance price is **discrimination-free** ([Lindholm et al., 2022](https://arxiv.org/abs/2209.00858)) if

$$
P(Y \leq y \mid X, S) = P(Y \leq y \mid X) \quad \text{for all } y
$$

i.e., the sensitive attribute $S$ carries no additional information about $Y$ beyond the non-protected covariates $X$.
```

```{prf:definition} Counterfactual Fairness
:label: counterfactual-fairness
:class: dropdown

A predictor $\hat{\mu}$ is **counterfactually fair** ([Kusner et al., 2017](https://arxiv.org/abs/1703.06856)) if, for all $s, s'$:

$$
P\bigl(\hat{\mu}_{S \leftarrow s}(X) = y \mid X{=}x, S{=}s\bigr) = P\bigl(\hat{\mu}_{S \leftarrow s'}(X) = y \mid X{=}x, S{=}s\bigr)
$$

i.e., the prediction would not change had the individual belonged to a different demographic group, all else being equal.
```

### Group Fairness Criteria as Diagnostic Checks

```{prf:remark} Group Fairness Criteria
:label: group-fairness-criteria
:class: dropdown

The machine learning literature evaluates a predictor against several **group fairness criteria** ([Barocas et al., 2019](https://fairmlbook.org/)). The interactive explainer in {doc}`../application/pricing` lets you toggle between the criteria defined below and watch the consequence of each choice. Each criterion is an independence condition on $\hat{Y}$; what distinguishes them is *which* errors they equalise, and therefore *what they cost* when the groups have genuinely different risk.
```

The **weakest** criterion is {prf:ref}`fairness-unawareness` (group unawareness): $S$ is simply not an input. As the whole of this page argues, proxy discrimination defeats it. The four criteria below are progressively more demanding constraints on the *decisions*, not the inputs.

```{prf:definition} Demographic (Statistical) Parity
:label: demographic-parity
:class: dropdown

A decision satisfies **demographic parity** if the flag is independent of the protected attribute,

$$
\hat{Y} \perp\!\!\!\perp S \quad\Longleftrightarrow\quad P(\hat{Y}{=}1 \mid S{=}s) \text{ is equal for all } s,
$$

i.e. each group is flagged at the same rate ([Dwork et al., 2012](https://arxiv.org/abs/1104.3913)).

**Interpretation** Parity is enforced *regardless of true risk*. When base rates genuinely differ, equalising selection rates means either lowering the bar for the lower-risk group or raising it for the higher-risk group — so qualified individuals are passed over in one group and unqualified ones flagged in the other. It maximally protects against disparate impact but is the most costly in accuracy and induces explicit cross-subsidy between groups.
```

```{prf:definition} Equal Opportunity & Equalised Odds
:label: equal-opportunity
:class: dropdown

A decision satisfies **equal opportunity** if the true-positive rate is equal across groups,

$$
\hat{Y} \perp\!\!\!\perp S \mid Y{=}1 \quad\Longleftrightarrow\quad P(\hat{Y}{=}1 \mid Y{=}1, S{=}s) \text{ is equal for all } s,
$$

so genuinely high-cost risks are caught at the same rate in every group ([Hardt et al., 2016](https://arxiv.org/abs/1610.02413)). Requiring equality of *both* the true- and false-positive rates is the stronger **equalised odds** criterion.

**Interpretation** Equal opportunity controls only the *miss* rate: it guarantees no group is systematically under-served among the truly high-risk, but says nothing about false positives, so one group may still bear more unwarranted reviews. Equalised odds closes that gap, but is so restrictive that — except in degenerate cases — it cannot hold together with calibration when base rates differ, and may force the model to *discard* predictive information to balance the error rates.
```

```{prf:definition} Equal Accuracy
:label: equal-accuracy
:class: dropdown

A decision satisfies **equal accuracy** (overall accuracy equality) if it is correct equally often in each group,

$$
P(\hat{Y}{=}Y \mid S{=}s) \text{ is equal for all } s
$$

([Berk et al., 2021](https://doi.org/10.1177/0049124118782533)).

**Interpretation** Equal accuracy treats a false positive and a false negative as interchangeable, so two groups can have identical accuracy while one suffers mostly missed high-risk cases and the other mostly false alarms. It is easy to communicate but blind to *which kind* of error each group bears — usually the distinction that matters most for fairness.
```

```{prf:definition} Predictive Parity (Calibration)
:label: predictive-parity
:class: dropdown

A score satisfies **predictive parity / calibration** if its meaning does not depend on the group,

$$
Y \perp\!\!\!\perp S \mid \hat{\mu}(X),
$$

i.e. among everyone assigned the same price $\hat{\mu}(X)$, the realised risk is the same regardless of group ([Chouldechova, 2017](https://doi.org/10.1089/big.2016.0047)).

**Interpretation** Calibration is what actuarial soundness and most regulators implicitly demand: a given premium must correspond to the same expected cost for everyone. The price of insisting on it is that, at unequal base rates, a calibrated score *cannot* also equalise true- and false-positive rates — so a calibrated, actuarially fair price will necessarily show group differences in error rates ([Kleinberg et al., 2017](https://arxiv.org/abs/1609.05807)).
```

```{prf:remark} The criteria are mutually incompatible
:label: fairness-incompatibility
:class: dropdown

These criteria are useful **diagnostic checks** but cannot replace causal reasoning. [Lindholm et al. (2022)](https://arxiv.org/abs/2209.00858) show that even a genuinely discrimination-free model violates them whenever $X$ and $S$ are statistically dependent. Moreover, except in trivial cases, the criteria are mutually incompatible at unequal base rates: no decision can be simultaneously calibrated *and* equalise both error rates ([Kleinberg et al., 2017](https://arxiv.org/abs/1609.05807); [Chouldechova, 2017](https://doi.org/10.1089/big.2016.0047)). Choosing a criterion is therefore a value judgement about *which* fairness to buy and *which* to forgo — not a technical detail the model can settle on its own.
```

### How Causal Inference Resolves the Fairness Problem

```{figure} figs/fairness_dag.svg
:width: 85%
:name: fig-fairness-dag

The fairness DAG: the sensitive attribute $S$ reaches the claim $Y$ via a discriminatory proxy path through $X_1$ and a legitimate path through the risk factor $X_2$, while the confounder $F$ creates a spurious $S$–$Y$ association.
```

The DAG makes precise why purely statistical constraints fail: not every $S \to Y$ path is illegitimate. The strength of causal inference is that it lets us reason about *which* paths are admissible instead of imposing a blanket independence requirement. Three steps follow directly from the graph:

- **Block the spurious path.** The association $S \leftarrow F \rightarrow Y$ is confounding, not discrimination. Conditioning on (or adjusting for) $F$ closes this back-door path, so that any remaining $S$–$Y$ dependence reflects genuine causal channels rather than artefacts.
- **Separate proxy from legitimate channels.** The proxy path $S \to X_1 \to Y$ is the discriminatory mechanism, whereas $S \to X_2 \to Y$ runs through a bona fide risk factor and may be defensible. **Path-specific (counterfactual) effects** let us neutralise only the unfair path while preserving the predictive signal carried by the legitimate one ([Chiappa, 2019](https://arxiv.org/abs/1802.08139); [Kusner et al., 2017](https://arxiv.org/abs/1703.06856)).
- **Construct the discrimination-free price.** Operationally, {prf:ref}`discrimination-free-pricing` is obtained by integrating the price over the *marginal* $P(S)$ rather than the conditional $P(S \mid X)$, which severs the $X$–$S$ dependence that the tower property would otherwise exploit ([Lindholm et al., 2022](https://arxiv.org/abs/2209.00858)).

**Where the Wasserstein distance fits in.** When the dependence between $X$ and $S$ cannot be fully removed — or when statistical parity is required as a hard constraint — fairness can be enforced *geometrically* via optimal transport.

```{prf:definition} Wasserstein-2 Distance and Barycenter
:label: wasserstein-barycenter
:class: dropdown

For two distributions $P, Q$ on $\mathbb{R}$ with finite second moments, the **Wasserstein-2 distance** is the minimal expected squared cost of transporting one onto the other,

$$
W_2(P, Q) = \left( \inf_{\pi \in \Pi(P, Q)} \int |u - v|^2 \, \mathrm{d}\pi(u, v) \right)^{1/2},
$$

where $\Pi(P, Q)$ is the set of couplings (joint distributions) with marginals $P$ and $Q$. Given the group-conditional price distributions $P(\hat{\mu} \mid S{=}s)$ with group shares $P(S{=}s)$, their **Wasserstein barycenter** is the distribution that minimises the total squared $W_2$ distance to all of them,

$$
\bar{P} = \arg\min_{P} \sum_{s} P(S{=}s)\, W_2^2\bigl(P,\; P(\hat{\mu} \mid S{=}s)\bigr).
$$
```

The idea is to map each group-conditional price distribution $P(\hat{\mu} \mid S{=}s)$ onto a common target — the **Wasserstein barycenter** $\bar{P}$ ({prf:ref}`wasserstein-barycenter`). Projecting onto this barycenter yields (approximate) demographic parity while distorting the original prices as little as possible, since $W_2$ measures the minimal "cost" of reshaping one distribution into another ([Chzhen et al., 2020](https://arxiv.org/abs/2006.07286); [Plečko & Meinshausen, 2020](https://arxiv.org/abs/1911.06685)). Beyond repair, the Wasserstein distance also serves as a continuous **fairness metric**: $W_2\bigl(P(\hat{\mu}\mid S{=}s),\, P(\hat{\mu}\mid S{=}s')\bigr)$ quantifies how far apart the price distributions of two groups remain, complementing the binary independence tests of the group-fairness criteria above.