
## Causal Inference and Fairness

Beyond causal bias, actuaries face a distinct but related challenge: ensuring that models do not discriminate against protected groups. EU regulation prohibits the use of protected characteristics (e.g. gender, ethnicity) for insurance pricing, but simply dropping the sensitive attribute $S$ does not solve the problem.

### Proxy Discrimination

```{prf:definition} Proxy Discrimination
:label: proxy-discrimination-def
:class: dropdown

**Proxy discrimination** (indirect discrimination) occurs when non-protected covariates $X$ that are correlated with the sensitive attribute $S$ allow the model to implicitly reconstruct $S$, even though $S$ is not used as an input.
```

The mechanism is the tower property of conditional expectation: $\mu(X) = \int \mu(X, s) \, \mathrm{d}P(S{=}s \mid X)$. If $X$ and $S$ are dependent, the unawareness price channels information about $S$ through $X$ ([Lindholm et al., 2021](https://www.cambridge.org/core/journals/astin-bulletin-journal-of-the-iaa/article/discriminationfree-insurance-pricing/ED25C4053690E56050F437B8DF2AD117)).

### From Unawareness to the Discrimination-Free Price

```{prf:definition} Fairness through Unawareness
:label: fairness-unawareness
:class: dropdown

A model satisfies **fairness through unawareness** if it does not use the sensitive attribute $S$ as input: $\hat{\mu}(X) = f(X)$.
```

Unawareness is not sufficient - it does not prevent proxy discrimination.

```{prf:definition} Discrimination-Free Pricing
:label: discrimination-free-pricing
:class: dropdown

An insurance price is **discrimination-free** ([Lindholm et al., 2021](https://www.cambridge.org/core/journals/astin-bulletin-journal-of-the-iaa/article/discriminationfree-insurance-pricing/ED25C4053690E56050F437B8DF2AD117)) if

$$
P(Y \leq y \mid X, S) = P(Y \leq y \mid X) \quad \text{for all } y
$$

i.e., the sensitive attribute $S$ carries no additional information about $Y$ beyond the non-protected covariates $X$.
```

```{prf:remark} Limits of counterfactual fairness for immutable attributes
:label: counterfactual-limits
:class: dropdown

The machine learning literature proposes **counterfactual fairness** ([Kusner et al., 2017](https://arxiv.org/abs/1703.06856)): a predictor is fair if its output would be unchanged had the individual's sensitive attribute been different, with every $S$-descendant regenerated accordingly. Formally ([Kusner et al., 2017](https://arxiv.org/abs/1703.06856), Def. 3) this requires the counterfactual prediction $\hat{\mu}_{S \leftarrow s'}(U)$ - a function of the latent background variables $U$ (the abduction–action–prediction recipe), *not* of the factual features $X$: under the intervention $do(S = s')$ any covariate that descends from $S$ is recomputed from the structural equations rather than held at its observed value.

For immutable characteristics such as gender or ethnicity, this counterfactual is philosophically ill-defined. Because $X$ is partly *constituted* by $S$ through the very causal pathways we are trying to reason about, there is no coherent notion of what the individual's covariates would look like had they been born into a different group. Enforcing counterfactual fairness may therefore erase legitimate causal effects and requires strong, untestable assumptions about the structural equations - assumptions that cannot be verified from observational data alone.
```

```{prf:remark} Causal interpretation of the discrimination-free price
:label: causal-dfp-connection
:class: dropdown

[Lindholm et al. (2021)](https://www.cambridge.org/core/journals/astin-bulletin-journal-of-the-iaa/article/discriminationfree-insurance-pricing/ED25C4053690E56050F437B8DF2AD117), Section 3, provide a causal motivation for {prf:ref}`discrimination-free-pricing` that sidesteps the difficulties of counterfactual fairness entirely. The starting point is a **directed acyclic graph (DAG)** in which $S$ may influence $Y$ both directly ($S \to Y$) and indirectly by shaping the non-protected covariates ($S \to X \to Y$).

The causal question posed is:

> *Given that a policyholder has non-protected characteristics $X = x$, what is the expected claim after removing all causal influence - direct and indirect - of $S$ on $Y$?*

Crucially, the intervention used to answer this question is **not** $do(S = s')$ (changing the sensitive attribute), but rather $do(X = x)$ - **fixing the non-protected covariates to their observed value externally**. This cuts the causal edge $S \to X$ in the DAG: in the resulting mutilated graph, $X$ is no longer influenced by $S$, so $S$ and $X$ become statistically independent. The sensitive attribute $S$ remains free to vary according to its population marginal $P(S)$.

Applying the **truncated factorisation formula** to the mutilated graph then yields ([Proposition 15 of Lindholm et al.](https://www.cambridge.org/core/journals/astin-bulletin-journal-of-the-iaa/article/discriminationfree-insurance-pricing/ED25C4053690E56050F437B8DF2AD117)):

$$E\bigl[Y \mid do(X{=}x)\bigr] = \int E[Y \mid X{=}x,\, S{=}s] \, \mathrm{d}P(S{=}s) = \mu^{\mathrm{df}}(x),$$

which is precisely the discrimination-free price. Causally, $\mu^{\mathrm{df}}$ is the expected claim *in the world where observing $X = x$ conveys no information about $S$* - because $X$ was set by external intervention rather than generated by $S$.

This resolves the philosophical objection cleanly: **we never intervene on $S$ at all**. No assumptions about "what $X$ would look like under a different gender" are needed. The intervention is on the quantity we condition on ($X$), not on the protected attribute. Lindholm et al. also note that the Markovian DAG assumptions underlying Proposition 15, while reasonable in many insurance contexts, are *not* a prerequisite: the discrimination-free price formula removes indirect discrimination regardless of whether a full causal model is available.
```

### Group Fairness Criteria as Diagnostic Checks

```{prf:remark} Group Fairness Criteria
:label: group-fairness-criteria
:class: dropdown

The machine learning literature evaluates a predictor against several **group fairness criteria** ([Barocas et al., 2019](https://fairmlbook.org/)). The interactive explainer in {doc}`../application/pricing` lets you toggle between the criteria defined below and watch the consequence of each choice. Most are *classification-parity* conditions that constrain the decision $\hat{Y}$ (its rate or its errors) across groups; calibration is different - it constrains the outcome given the score, $Y \perp\!\!\!\perp S \mid \hat{\mu}(X)$, fixing the statistical meaning of the score rather than the decision rate. What distinguishes the criteria is *which* errors they equalise, and therefore *what they cost* when the groups have genuinely different risk.
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

**Interpretation** Parity is enforced *regardless of true risk*. When base rates genuinely differ, equalising selection rates means either lowering the bar for the lower-risk group or raising it for the higher-risk group - so qualified individuals are passed over in one group and unqualified ones flagged in the other. It maximally protects against disparate impact but is the most costly in accuracy and induces explicit cross-subsidy between groups.
```

```{prf:definition} Equal Opportunity & Equalised Odds
:label: equal-opportunity
:class: dropdown

A decision satisfies **equal opportunity** if the true-positive rate is equal across groups,

$$
\hat{Y} \perp\!\!\!\perp S \mid Y{=}1 \quad\Longleftrightarrow\quad P(\hat{Y}{=}1 \mid Y{=}1, S{=}s) \text{ is equal for all } s,
$$

so genuinely high-cost risks are caught at the same rate in every group ([Hardt et al., 2016](https://arxiv.org/abs/1610.02413)). Requiring equality of *both* the true- and false-positive rates is the stronger **equalised odds** criterion.

**Interpretation** Equal opportunity controls only the *miss* rate: it guarantees no group is systematically under-served among the truly high-risk, but says nothing about false positives, so one group may still bear more unwarranted reviews. Equalised odds closes that gap, but is so restrictive that - except in degenerate cases - it cannot hold together with calibration when base rates differ, and may force the model to *discard* predictive information to balance the error rates.
```

```{prf:definition} Equal Accuracy
:label: equal-accuracy
:class: dropdown

A decision satisfies **equal accuracy** (overall accuracy equality) if it is correct equally often in each group,

$$
P(\hat{Y}{=}Y \mid S{=}s) \text{ is equal for all } s
$$

([Berk et al., 2021](https://doi.org/10.1177/0049124118782533)).

**Interpretation** Equal accuracy treats a false positive and a false negative as interchangeable, so two groups can have identical accuracy while one suffers mostly missed high-risk cases and the other mostly false alarms. It is easy to communicate but blind to *which kind* of error each group bears - usually the distinction that matters most for fairness.
```

```{prf:definition} Predictive Parity (Calibration)
:label: predictive-parity
:class: dropdown

A score satisfies **predictive parity / calibration** if its meaning does not depend on the group,

$$
Y \perp\!\!\!\perp S \mid \hat{\mu}(X),
$$

i.e. among everyone assigned the same price $\hat{\mu}(X)$, the realised risk is the same regardless of group ([Chouldechova, 2017](https://doi.org/10.1089/big.2016.0047)).

**Interpretation** Calibration is what actuarial soundness and most regulators implicitly demand: a given premium must correspond to the same expected cost for everyone. The price of insisting on it is that, at unequal base rates, a calibrated score *cannot* also equalise true- and false-positive rates - so a calibrated, actuarially fair price will necessarily show group differences in error rates ([Kleinberg et al., 2017](https://arxiv.org/abs/1609.05807)).
```

```{prf:remark} The criteria are mutually incompatible
:label: fairness-incompatibility
:class: dropdown

These criteria are useful **diagnostic checks** but cannot replace causal reasoning. [Lindholm et al. (2021)](https://www.cambridge.org/core/journals/astin-bulletin-journal-of-the-iaa/article/discriminationfree-insurance-pricing/ED25C4053690E56050F437B8DF2AD117) show that even a genuinely discrimination-free model violates them whenever $X$ and $S$ are statistically dependent. Moreover, except in trivial cases, the criteria are mutually incompatible at unequal base rates: no decision can be simultaneously calibrated *and* equalise both error rates ([Kleinberg et al., 2017](https://arxiv.org/abs/1609.05807); [Chouldechova, 2017](https://doi.org/10.1089/big.2016.0047)). Choosing a criterion is therefore a value judgement about *which* fairness to buy and *which* to forgo - not a technical detail the model can settle on its own.
```

### Assessing Fairness in a DAG

```{figure} figs/fairness_dag.svg
:width: 85%
:name: fig-fairness-dag

Assessing fairness in a DAG involves a classification of paths: The sensitive attribute $S$ reaches the claim $Y$ via a discriminatory proxy path through $X_1$ and a legitimate path through the risk factor $X_2$, while the confounder $F$ creates a spurious $S$–$Y$ association.
```

The DAG makes precise why purely statistical constraints fail: not every $S \to Y$ path is illegitimate. The strength of causal inference is that it lets us reason about *which* paths are admissible instead of imposing a blanket independence requirement. Three steps follow directly from the graph:

- **Block the spurious path.** The association $S \leftarrow F \rightarrow Y$ is confounding, not discrimination. Conditioning on (or adjusting for) $F$ closes this back-door path, so that any remaining $S$–$Y$ dependence reflects genuine causal channels rather than artefacts.
- **Separate proxy from legitimate channels.** The proxy path $S \to X_1 \to Y$ is the discriminatory mechanism, whereas $S \to X_2 \to Y$ runs through a bona fide risk factor and is actuarially defensible. Lindholm et al. show that intervening $do(X{=}x)$ - fixing the non-protected covariates externally - severs the $S \to X$ edge, making $S$ independent of $X$ in the mutilated graph. The discrimination-free price is then the expected claim in this post-intervention world, averaged over the marginal $P(S)$, which neutralises the proxy channel without any manipulation of $S$ ([Lindholm et al., 2021](https://www.cambridge.org/core/journals/astin-bulletin-journal-of-the-iaa/article/discriminationfree-insurance-pricing/ED25C4053690E56050F437B8DF2AD117), Section 3).
- **Construct the discrimination-free price.** Operationally, {prf:ref}`discrimination-free-pricing` is obtained by integrating the price over the *marginal* $P(S)$ rather than the conditional $P(S \mid X)$, which severs the $X$–$S$ dependence that the tower property would otherwise exploit ([Lindholm et al., 2021](https://www.cambridge.org/core/journals/astin-bulletin-journal-of-the-iaa/article/discriminationfree-insurance-pricing/ED25C4053690E56050F437B8DF2AD117)).


```{note} Actuarial takeaway: fairness is a causal question
:class: dropdown

Fairness in insurance is, at its core, a *causal* question rather than a purely statistical one. Fairness through unawareness is insufficient because correlated covariates let the price reconstruct the sensitive attribute through proxy channels; the group-fairness criteria, though valuable as diagnostic checks, are mutually incompatible at unequal base rates and cannot by themselves tell discrimination apart from legitimate risk differentiation. Causal reasoning dissolves this tension by making the underlying DAG explicit: it closes spurious confounding paths, isolates the discriminatory proxy channel from actuarially defensible risk factors, and yields the discrimination-free price by averaging over the marginal $P(S)$ instead of the conditional $P(S \mid X)$. For the actuary this reframes non-discrimination as a modelling discipline that is fully aligned with the profession's mandate: premiums that reflect genuine, causally justified risk while remaining free of illegitimate discrimination - actuarially sound and ethically defensible at once, and a concrete instance of the shift from passive risk measurement to active, responsible risk management that runs through this tutorial.
```
