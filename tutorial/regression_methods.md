# Regression Methods

Regression-based estimators identify causal effects by explicitly modelling the relationship between covariates $X$, treatment $T$, and outcome $Y$. They span a spectrum: from a single *outcome model* (G-computation), to estimators that combine an outcome model with a *propensity model* for robustness (AIPW, TMLE), to *orthogonal* machine-learning estimators that remain valid under flexible nuisance models (Double Machine Learning and its meta-learner extensions for heterogeneous effects). A second family - *quasi-experimental designs* such as instrumental variables, difference-in-differences, and regression discontinuity - exploits structural sources of exogenous variation rather than adjustment alone. The figure below shows the common causal structure that the adjustment-based estimators target.

```{figure} figs/dag_doubly_robust.svg
:width: 70%
:name: fig-dr-dag

Causal structure underlying adjustment-based regression estimators. The covariates $X$ confound the treatment–outcome relationship through the *propensity model* $\pi(X) = P(T = 1 \mid X)$ and the *outcome model* $\mu(X) = \mathbb{E}[Y \mid T, X]$. Doubly robust estimators combine both to estimate the causal effect $\tau$.
```

## Outcome Regression and G-computation

The simplest regression adjustment fits a single outcome model $\hat{\mu}(t, x) = \mathbb{E}[Y \mid T = t, X = x]$ and contrasts its predictions under treatment and control, averaged over the covariate distribution. This is the *parametric g-formula* of [Robins (1986)](https://doi.org/10.1016/0270-0255(86)90088-6) (see [Hernán & Robins (2020)](https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/) for a modern treatment), and it serves as the conceptual baseline on which the doubly robust and orthogonal estimators below build.

```{prf:algorithm} G-computation (Outcome Regression)
:label: alg-gcomp
:class: dropdown

**Inputs** Data $D = \{X, T, Y\}$, ML learner $\mathcal{L}_Y$ (for outcome)

**Outputs** Estimated ATE $\hat{\tau}$

1. Fit outcome model $\hat{\mu}(t, x) = \mathcal{L}_Y(Y \sim T, X)$ on $D$
2. For every observation $i$:
	1. Predict counterfactual outcomes $\hat{\mu}(1, x^{(i)})$ and $\hat{\mu}(0, x^{(i)})$
3. Average the contrast: $\hat{\tau} = \frac{1}{n}\sum_{i=1}^{n}\left[\hat{\mu}(1, x^{(i)}) - \hat{\mu}(0, x^{(i)})\right]$
4. Return estimated treatment effect $\hat{\tau}$
```

G-computation is consistent only if the outcome model is correctly specified. Because a misspecified $\hat{\mu}$ propagates directly into the estimate, it motivates the *doubly robust* estimators that add a second line of defence through the propensity score.

## Doubly Robust Estimation: AIPW and TMLE

Doubly robust estimators combine the outcome model $\hat{\mu}(t, x)$ with the propensity model $\hat{\pi}(x)$ so that the estimate is consistent if *either* model is correctly specified - a property that single-model approaches lack. The *Augmented Inverse Propensity Weighting* (AIPW) estimator of [Robins, Rotnitzky & Zhao (1994)](https://doi.org/10.1080/01621459.1994.10476818) augments the G-computation estimate with an inverse-propensity-weighted residual correction; [Bang & Robins (2005)](https://doi.org/10.1111/j.1541-0420.2005.00377.x) developed the framework for causal inference, and [van der Laan & Rubin (2006)](https://doi.org/10.2202/1557-4679.1043) introduced *Targeted Maximum Likelihood Estimation* (TMLE) as a substitution-based alternative with the same robustness guarantee. DML (next section) is essentially AIPW equipped with Neyman-orthogonality and cross-fitting.

```{prf:algorithm} Augmented Inverse Propensity Weighting (AIPW)
:label: alg-aipw
:class: dropdown

**Inputs** Data $D = \{X, T, Y\}$, ML learners $\mathcal{L}_Y$ (outcome), $\mathcal{L}_T$ (treatment)

**Outputs** Doubly robust ATE estimate $\hat{\tau}$

1. Fit nuisance models (with cross-fitting): outcome $\hat{\mu}(t, x) = \mathcal{L}_Y(Y \sim T, X)$ and propensity $\hat{\pi}(x) = \mathcal{L}_T(T \sim X)$
2. For every observation $i$, form the doubly robust score *(G-computation plus IPW residual correction)*

	$$\hat{\psi}^{(i)} = \hat{\mu}(1, x^{(i)}) - \hat{\mu}(0, x^{(i)}) + \frac{T^{(i)}\,(Y^{(i)} - \hat{\mu}(1, x^{(i)}))}{\hat{\pi}(x^{(i)})} - \frac{(1 - T^{(i)})\,(Y^{(i)} - \hat{\mu}(0, x^{(i)}))}{1 - \hat{\pi}(x^{(i)})}$$

3. Average the scores: $\hat{\tau} = \frac{1}{n}\sum_{i=1}^{n}\hat{\psi}^{(i)}$
4. Return estimated treatment effect $\hat{\tau}$ *(consistent if either $\hat{\mu}$ or $\hat{\pi}$ is correct)*
```


```{note}
:class: dropdown

A **doubly robust estimator** $\hat{\tau}$ is consistent for the true ATE $\tau$ if
*either* $\hat{\mu}$ *or* $\hat{\pi}$ is consistently estimated - that is, if either
$\hat{\mu}(t, x) \rightarrow \mu(t, x) = \mathbb{E}[Y \mid T=t, X=x]$ or
$\hat{\pi}(x) \rightarrow \pi(x) = P(T=1 \mid X=x)$ converge in probability as $n \to \infty$. To see
why, write the doubly robust estimator explicitly as

$$
\hat{\tau} = \frac{1}{n}\sum_{i=1}^n \Biggl[
\underbrace{\hat{\mu}(1, x^{(i)}) - \hat{\mu}(0, x^{(i)})}_{\text{plug-in term}} +
\underbrace{
\frac{T^{(i)}\,(Y^{(i)} - \hat{\mu}(1, x^{(i)}))}{\hat{\pi}(x^{(i)})} - \frac{(1 - T^{(i)})\,(Y^{(i)} - \hat{\mu}(0, x^{(i)}))}{1 - \hat{\pi}(x^{(i)})}}_{\text{augmentation term}}
\Biggr],
$$

where the plug-in term is the standard G-computation estimator and the augmentation
term uses inverse-probability weights to correct for bias in the outcome model.
The bias of $\hat{\tau}$ as an estimator of $\tau$ is proportional to a product
of errors in the two nuisance functions,

$$
\operatorname{Bias}(\hat{\tau}) \propto \bigl(\hat{\mu} - \mu\bigr)\bigl(\hat{\pi} - \pi\bigr),
$$

so if either factor converges to zero the product vanishes and $\hat{\tau}$ is
consistent, even if the other model remains misspecified. Concretely: if
$\hat{\mu} \rightarrow \mu$ but $\hat{\pi} \not\rightarrow \pi$, the outcome
model residuals $Y_i - \hat{\mu}(T_i, X_i)$ already have expectation zero, so the
augmentation term contributes no bias regardless of how wrong $\hat{\pi}$ is;
symmetrically, if $\hat{\pi} \rightarrow \pi$ but $\hat{\mu} \not\rightarrow
\mu$, the inverse-probability weights correctly rebalance the misspecified outcome
model predictions and the bias cancels. Only when both models are misspecified -
$\hat{\mu} \not\rightarrow \mu$ and $\hat{\pi} \not\rightarrow \pi$ - does
the product remain non-zero and the estimator fails to be consistent.
```


```{prf:algorithm} Targeted Maximum Likelihood Estimation (TMLE)
:label: alg-tmle
:class: dropdown

**Inputs** Data $D = \{X, T, Y\}$, ML learners $\mathcal{L}_Y$ (outcome), $\mathcal{L}_T$ (treatment)

**Outputs** Doubly robust ATE estimate $\hat{\tau}$

1. Fit initial outcome model $\hat{\mu}^0(t, x) = \mathcal{L}_Y(Y \sim T, X)$ and propensity $\hat{\pi}(x) = \mathcal{L}_T(T \sim X)$
2. Compute the *clever covariate* $H^{(i)} = \frac{T^{(i)}}{\hat{\pi}(x^{(i)})} - \frac{1 - T^{(i)}}{1 - \hat{\pi}(x^{(i)})}$
3. **Targeting step:** fit a one-parameter *logistic* fluctuation $\hat{\varepsilon}$ by regressing $Y$ on $H$ with offset $\text{logit}\,\hat{\mu}^0$, giving the updated model $\hat{\mu}^\star(t, x)$ *(valid for $Y \in [0,1]$; see the note below for continuous outcomes)*
4. Plug the targeted model into G-computation: $\hat{\tau} = \frac{1}{n}\sum_{i=1}^{n}\left[\hat{\mu}^\star(1, x^{(i)}) - \hat{\mu}^\star(0, x^{(i)})\right]$
5. Return estimated treatment effect $\hat{\tau}$
```



```{note}
:class: dropdown

**Outcome type matters - read before applying TMLE to loss data.** The targeting step above uses a **logistic fluctuation** (offset $\text{logit}\,\hat{\mu}^0$, clever covariate $H$), which is only valid when the outcome is **binary or bounded in $[0,1]$**. For unbounded continuous outcomes a different fluctuation family is required - a **Gaussian fluctuation with the identity link** ([van der Laan & Rubin, 2006](https://doi.org/10.2202/1557-4679.1043)) - otherwise the targeting step is misspecified and the resulting $\hat{\tau}$ is invalid.

In non-life actuarial work this is the *usual* case, not an edge case: the primary outcomes - **claim amounts, loss ratios, and claim counts** - are continuous or count-valued and unbounded, not $\{0,1\}$. An actuary who applies the logistic formulation above directly to a loss amount is implementing an incorrect targeting step. Two practical routes:

- **Bounded continuous outcomes** (e.g. loss ratios in $[0,1]$, or any outcome rescaled to $[0,1]$ via $\tilde{Y} = (Y - a)/(b - a)$ and back-transformed): the logistic fluctuation applies directly after rescaling ([Gruber & van der Laan, 2010](https://doi.org/10.2202/1557-4679.1260)).
- **Unbounded outcomes** (claim severities, aggregate losses): use the Gaussian/identity-link fluctuation, or a count-appropriate family for frequencies.

In practice, prefer a maintained implementation such as the R package [`tmle`](https://CRAN.R-project.org/package=tmle), which selects the correct fluctuation family for binary, bounded-continuous, and continuous outcomes automatically.
```



## Double Machine Learning (DML)

The DML estimator of [Chernozhukov et al. (2018)](https://doi.org/10.1111/ectj.12097) makes the doubly robust idea robust to flexible, slowly-converging machine-learning nuisance models. For a binary or continuous treatment it builds on the *partially linear model* (PLM) $Y = \tau T + g(X) + \varepsilon$, whose residualize-then-regress solution is Robinson's estimator [(Robinson, 1988)](https://doi.org/10.2307/1912705). By *partialling out* the covariate effect from both $Y$ and $T$ before estimating $\tau$, the resulting moment condition is Neyman-orthogonal, so first-stage estimation error has only a second-order effect on $\hat{\tau}$.

```{prf:algorithm} Double Machine Learning
:label: alg-dml
:class: dropdown

**Inputs** Data $D = \{X, T, Y\}$, ML learners $\mathcal{L}_Y$ (for outcome), $\mathcal{L}_T$ (for treatment)

**Outputs** Estimated causal effect $\hat{\tau}$

1. Split data $D$ into two disjoint sets: $D_{train}$ and $D_{eval}$ *(Cross-fitting/Honesty)*

2. **Outcome Residualization**
	1. Train model $\hat{\mu}(X) = \mathcal{L}_Y(Y \sim X)$ on $D_{train}$ *(Predict $Y$ using covariates only)*
	2. Compute residuals $\tilde{Y} = Y - \hat{\mu}(X)$ on $D_{eval}$

3. **Treatment Residualization**
	1. Train model $\hat{\pi}(X) = \mathcal{L}_T(T \sim X)$ on $D_{train}$ *(Estimate the treatment conditional mean $\pi(X) = \mathbb{E}[T \mid X]$; for binary $T$ this coincides with the propensity score $\mathbb{P}(T=1 \mid X)$)*
	2. Compute residuals $\tilde{T} = T - \hat{\pi}(X)$ on $D_{eval}$

4. **Causal Estimation**
	1. Regress outcome residuals on treatment residuals: $\tilde{Y} = \tau \tilde{T} + \varepsilon$
	2. *Note:* This identifies the effect using only the "exogenous" variation in $T$

5. Return estimated treatment effect $\hat{\tau}$
```

```{note}
**What the partially linear model actually targets.** The PLM $Y = \tau T + g(X) + \varepsilon$ treats $\tau$ as a *single constant* - an implicit homogeneous-effects assumption. When the true effect is heterogeneous, $\tau(X)$, Robinson's residual-on-residual regression does *not* return the standard ATE $= \mathbb{E}[\tau(X)]$ but the **propensity-overlap-weighted** average

$$
\tau^* = \frac{\mathbb{E}\!\big[\tau(X)\,\pi(X)\,(1-\pi(X))\big]}{\mathbb{E}\!\big[\pi(X)\,(1-\pi(X))\big]},
$$

with $\pi(X) = \mathbb{E}[T \mid X]$ the propensity score, which over-weights the region of good overlap ($\pi \approx \tfrac12$) and under-weights the propensity tails. $\tau^*$ equals the ATE only when effects are homogeneous or $\pi(X)$ is constant (an RCT) - neither holds in confounded insurance data. To target $\mathbb{E}[\tau(X)]$ under heterogeneity, use the **interactive model** $Y = \tau(X)T + g(X) + \varepsilon$ with an AIPW/doubly robust score, or average the CATEs from the meta-learners and causal forests below ([Chernozhukov et al., 2018](https://doi.org/10.1111/ectj.12097), Sec. 2 vs. 4). Mixing a PLM-DML "ATE" with averaged causal-forest CATEs can therefore yield inconsistent numbers.
```

## Meta-Learners for Heterogeneous Effects

The estimators above target the average treatment effect. *Meta-learners* extend regression adjustment to the conditional average treatment effect (CATE) $\tau(x) = \mathbb{E}[Y(1) - Y(0) \mid X = x]$ by decomposing the problem into standard regression sub-tasks solved by any base learner. [Künzel et al. (2019)](https://doi.org/10.1073/pnas.1804597116) introduced the S-, T-, and X-learners; the *R-learner* of [Nie & Wager (2021)](https://doi.org/10.1093/biomet/asaa076) is the direct CATE generalization of the DML residualization above, and the *DR-learner* of [Kennedy (2023)](https://doi.org/10.1214/23-EJS2157) regresses the doubly robust AIPW score on covariates. [Semenova & Chernozhukov (2021)](https://doi.org/10.1093/ectj/utaa027) extend DML to estimate CATEs and other causal functions. These estimators bridge directly to the {prf:ref}`alg-causaltree` and {prf:ref}`alg-causalforest` methods that follow.

```{prf:algorithm} Meta-Learners (S-, T-, X-Learner)
:label: alg-metalearners
:class: dropdown

**Inputs** Data $D = \{X, T, Y\}$, base learner $\mathcal{L}$

**Outputs** Estimated CATE $\hat{\tau}(x)$

1. **S-learner** *(single model)*: fit $\hat{\mu}(t, x) = \mathcal{L}(Y \sim T, X)$; return $\hat{\tau}(x) = \hat{\mu}(1, x) - \hat{\mu}(0, x)$
2. **T-learner** *(two models)*: fit $\hat{\mu}_1(x)$ on treated and $\hat{\mu}_0(x)$ on control; return $\hat{\tau}(x) = \hat{\mu}_1(x) - \hat{\mu}_0(x)$
3. **X-learner** *(cross fitting on imputed effects)*:
	1. Impute effects $\tilde{D}^{(i)}_1 = Y^{(i)} - \hat{\mu}_0(x^{(i)})$ for treated, $\tilde{D}^{(i)}_0 = \hat{\mu}_1(x^{(i)}) - Y^{(i)}$ for control
	2. Regress $\hat{\tau}_1(x) = \mathcal{L}(\tilde{D}_1 \sim X)$ and $\hat{\tau}_0(x) = \mathcal{L}(\tilde{D}_0 \sim X)$
	3. Combine with propensity weight: $\hat{\tau}(x) = \hat{\pi}(x)\,\hat{\tau}_0(x) + (1 - \hat{\pi}(x))\,\hat{\tau}_1(x)$
4. Return CATE $\hat{\tau}(x)$
```

```{prf:algorithm} R-Learner (and DR-Learner)
:label: alg-rlearner
:class: dropdown

**Inputs** Data $D = \{X, T, Y\}$, ML learners for nuisances and a CATE learner $\mathcal{L}_\tau$

**Outputs** Estimated CATE $\hat{\tau}(x)$

1. With cross-fitting, estimate nuisances $\hat{\pi}(x) = \mathbb{E}[T \mid X]$ and $\hat{\mu}(x) = \mathbb{E}[Y \mid X]$
2. Form residuals $\tilde{Y} = Y - \hat{\mu}(X)$ and $\tilde{T} = T - \hat{\pi}(X)$ *(as in {prf:ref}`alg-dml`)*
3. **R-learner:** minimize the weighted loss $\hat{\tau} = \arg\min_{\tau} \sum_i \left(\tilde{Y}^{(i)} - \tau(x^{(i)})\,\tilde{T}^{(i)}\right)^2$
4. **DR-learner (alternative):** regress the AIPW score $\hat{\psi}^{(i)}$ from {prf:ref}`alg-aipw` on covariates, $\hat{\tau}(x) = \mathcal{L}_\tau(\hat{\psi} \sim X)$
5. Return CATE $\hat{\tau}(x)$
```

## Instrumental Variable Approach

When unobserved confounding exists, an instrument $I$ can identify the causal effect if ([Shalizi, 2025, Ch. 23](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)):

1. *Relevance*: $I$ affects $T$
2. *Exogenous noise*: $I \perp\!\!\!\perp U$ - the instrumental variable is independent of the unobserved confounder
3. *Exclusion restriction*: $I$ affects $Y$ only through $T$

The modern econometric interpretation of instrumental variables traces to [Imbens & Angrist (1994)](https://doi.org/10.2307/2951620), who show that 2SLS identifies a *local average treatment effect* for compliers, and to the potential-outcomes framework of [Angrist, Imbens & Rubin (1996)](https://doi.org/10.1080/01621459.1996.10476902); [Angrist & Krueger (1991)](https://doi.org/10.2307/2937954) is the canonical applied example, using quarter of birth as an instrument for schooling.

The instrumental variable $I$ is a source of exogenous variation in $T$ that is uncorrelated with the common ancestors of $T$ and $Y$. By seeing how both $T$ and $Y$ respond to these perturbations, and using the fact that $I$ only influences $Y$ through $T$, we can deduce the causal effect of $T$ on $Y$.

```{figure} figs/iv_structure.svg
:width: 80%
:name: fig-IV

Instrumental variable $I$. The instrument induces exogenous variation in the treatment $T$ while being independent of the unobserved confounder $U$ and affecting the outcome $Y$ only through $T$.
```

## Two Stage Least Squares Regression

```{prf:algorithm} Two Stage Least Squares (2SLS)
:label: alg-2sls
:class: dropdown

**Inputs** Observed instrument $I$, treatment variable $T$, outcome $Y$, exogenous covariates $X$

**Outputs** Estimated causal effect $\hat{\beta}$ of $T$ on $Y$

1. **Stage 1: Regress $T$ on instrument $I$ and covariates $X$** *(Isolate exogenous variation)*
	1. Estimate $\hat{\alpha}, \hat{\gamma}$ from $T = \alpha I + \gamma X + \varepsilon_1$
	2. Compute predicted values $\hat{T} = \hat{\alpha} I + \hat{\gamma} X$ *($\hat{T}$ is now independent of $U$)*

2. **Stage 2: Regress $Y$ on predicted $\hat{T}$ and covariates $X$** *(Identify causal mechanism)*
	1. Estimate $\hat{\beta}, \hat{\delta}$ from $Y = \beta \hat{T} + \delta X + \varepsilon_2$

3. Return estimated causal effect $\hat{\beta}$
```

```{important}
The **same exogenous covariates $X$ must appear in both stages**. Omitting them produces a biased estimate whenever $X$ is correlated with both the instrument $I$ and the outcome $Y$: the covariates must be *partialled out* of the instrument–treatment relationship for the exclusion restriction and exogeneity conditions to hold conditionally. The bivariate form ($T = \alpha I + \varepsilon_1$, $Y = \beta \hat{T} + \varepsilon_2$) is valid only under the strong assumption that **no observed covariate affects $Y$** - a condition almost never satisfied in insurance data.
```

```{tip}
For valid inference, obtain 2SLS estimates from a **dedicated IV routine** (`linearmodels.IV2SLS` in Python, `AER::ivreg` in R, or `ivregress` in Stata) rather than by fitting the two OLS stages by hand. The two approaches agree on the point estimate $\hat{\beta}$, but only the IV routine returns correct standard errors. The reason is instructive: valid 2SLS inference computes the error variance from the *structural* residuals $u = Y - \hat{\beta}T$ using the **observed** treatment $T$, whereas a manual second-stage OLS would use the fitted-treatment residuals $\hat{\varepsilon} = Y - \hat{\beta}\hat{T}$. Since $\hat{\varepsilon} = u + \hat{\beta}(T - \hat{T})$, we have $\mathbb{E}[\hat{\varepsilon}^2] = \mathbb{E}[u^2] + \beta^2\,\operatorname{Var}(T - \hat{T}) > \mathbb{E}[u^2]$, so hand-rolled standard errors come out too large - widening confidence intervals and shrinking $t$-statistics. Using the dedicated routine keeps inference well-calibrated, which matters in actuarial screening where an over-conservative test can let a genuinely beneficial intervention slip below the significance threshold (Wooldridge, 2010, *Econometric Analysis of Cross Section and Panel Data*, p. 96).
```

## Mendelian Randomization

Mendelian Randomization (MR) is an application of the instrumental variable principle to genetics and epidemiology. The idea - dating to [Katan (1986)](https://doi.org/10.1016%2Fs0140-6736%2886%2992972-7) and formalized by [Davey Smith & Ebrahim (2003)](https://doi.org/10.1093/ije/dyg070) - exploits the fact that genetic variants are assigned at conception, before any environmental exposure, and therefore satisfy the IV conditions almost by construction:

1. **Relevance**: the variant is associated with the exposure $T$ (e.g. LDL cholesterol level).
2. **Exogeneity**: Mendelian randomization - the random shuffling of alleles during meiosis - makes the inherited variant independent of most confounders $U$.
3. **Exclusion restriction**: the variant affects the outcome $Y$ only through the exposure $T$, not through any alternative biological pathway (*no pleiotropy*).

When these conditions hold, the genetic variant $G$ (typically a single-nucleotide polymorphism, SNP) serves as an instrument and 2SLS identifies the causal effect of the exposure on the outcome:

$$
\hat{\tau}_{\text{MR}} = \frac{\hat{\beta}_{G \to Y}}{\hat{\beta}_{G \to T}}
= \frac{\text{SNP–outcome association}}{\text{SNP–exposure association}},
$$

which is the **Wald ratio estimator** - the simplest MR estimate when a single instrument is used. With multiple SNPs the ratio generalises to a 2SLS (or likelihood-based) estimator, and the overidentification can be exploited to test for and correct pleiotropy ([Bowden, Davey Smith & Burgess, 2015](https://doi.org/10.1093/ije/dyv080)).

```{admonition} MR in Actuarial and Health Insurance Contexts
:class: tip

MR estimates are increasingly available in the public health literature for risk factors relevant to life and health insurers - BMI, blood pressure, lipid levels, smoking behaviour, and many biomarkers. Because a well-conducted MR study targets the *lifetime causal effect* of a modifiable risk factor (rather than an association observed at a single medical exam), the estimates can inform pricing and underwriting in ways that observational risk scores cannot: they are, in principle, robust to reverse causation and the confounding that plagues claims-linked data. The key caveat is the exclusion restriction: many SNPs have pleiotropic effects, so MR estimates should be accompanied by sensitivity analyses such as MR-Egger regression ([Bowden et al., 2015](https://doi.org/10.1093/ije/dyv080)) or weighted median estimators.
```

## Quasi-Experimental Designs

When adjustment for measured covariates is insufficient, *quasi-experimental designs* recover causal effects by exploiting structural features of how treatment is assigned - over time, around a threshold, or relative to a comparison unit. These designs are especially relevant for longitudinal data. They form the empirical core of modern applied econometrics; the introductory textbooks of [Angrist & Pischke (2009)](https://doi.org/10.1515/9781400829828), [Angrist & Pischke (2015)](https://press.princeton.edu/books/paperback/9780691152844/mastering-metrics) and [Cunningham (2021)](https://doi.org/10.12987/9780300255881), together with the more statistical treatment of [Imbens & Rubin (2015)](https://doi.org/10.1017/CBO9781139025751), give book-length introductions to the methods below.

### Difference-in-Differences

Difference-in-differences (DiD) compares the change in outcomes over time between a treated and a control group. Under the *parallel trends* assumption - that, absent treatment, both groups would have evolved in parallel - the post-period gap beyond the projected control trend identifies the average treatment effect on the treated (ATT). The design dates back to [Ashenfelter & Card (1985)](https://doi.org/10.2307/1924810), and [Card & Krueger (1994)](https://doi.org/10.1257/aer.84.4.772) is its best-known application - the New Jersey minimum-wage study. [Sant'Anna & Zhao (2020)](https://doi.org/10.1016/j.jeconom.2020.06.003) give a doubly robust DiD estimator, and [Callaway & Sant'Anna (2021)](https://doi.org/10.1016/j.jeconom.2020.12.001) extend the design to multiple periods and staggered treatment timing with their group-time ATT estimator. [Goodman-Bacon (2021)](https://doi.org/10.1016/j.jeconom.2021.03.014) is not a new estimator but a *decomposition* result: under staggered timing the canonical two-way fixed-effects (TWFE) OLS regression - the default DiD implementation in most software - equals a weighted average of all possible $2 \times 2$ DiDs, and some of those weights turn **negative** when treatment effects are heterogeneous across cohorts or over time, so the TWFE estimate can be attenuated or even sign-reversed *even when parallel trends holds*. This diagnostic motivates the heterogeneity-robust estimators above.

```{figure} figs/did_parallel_trends.svg
:width: 80%
:name: fig-did

Difference-in-differences. Under parallel trends, the treated group's counterfactual (dashed) would have followed the control trend; the vertical gap $\tau$ in the post-period is the ATT.
```

```{prf:algorithm} Difference-in-Differences (2x2)
:label: alg-did
:class: dropdown

**Inputs** Outcomes $Y$ for treated/control groups, pre/post periods; optional covariates $X$

**Outputs** Estimated ATT $\hat{\tau}$

1. Compute the treated change: $\Delta_{\text{treated}} = \bar{Y}^{\text{post}}_{\text{treated}} - \bar{Y}^{\text{pre}}_{\text{treated}}$
2. Compute the control change: $\Delta_{\text{control}} = \bar{Y}^{\text{post}}_{\text{control}} - \bar{Y}^{\text{pre}}_{\text{control}}$
3. Difference the differences: $\hat{\tau} = \Delta_{\text{treated}} - \Delta_{\text{control}}$ *(removes time-invariant confounding)*
4. *(Optional)* For covariate-conditional parallel trends, use a doubly robust estimator combining outcome-change regression and a propensity model
5. Return estimated ATT $\hat{\tau}$
```

### Regression Discontinuity





Regression discontinuity (RD) applies when treatment is assigned by a threshold rule on a continuous *running variable* $X$ (e.g. a risk score). The design was first proposed by [Thistlethwaite & Campbell (1960)](https://doi.org/10.1037/h0044319); its modern econometric foundations are due to [Hahn, Todd & van der Klaauw (2001)](https://doi.org/10.1111/1468-0262.00183). Units just below and just above the cutoff $c$ are comparable, so the jump in the outcome at $c$ identifies the **average treatment effect at the cutoff**, $\mathbb{E}[Y(1) - Y(0) \mid X = c]$ - the causal effect *at the discontinuity point* ([Hahn, Todd & van der Klaauw, 2001](https://doi.org/10.1111/1468-0262.00183); [Imbens & Lemieux, 2008](https://doi.org/10.1016/j.jeconom.2007.05.001)). 
This is a *different* object from the **local average treatment effect (LATE)** of the
IV/2SLS design above. The LATE, formally defined as

$$
\text{LATE} = \mathbb{E}[Y(1) - Y(0) \mid T(I=1) = 1,\; T(I=0) = 0],
$$

is the average treatment effect among **compliers** - units whose treatment status
is switched by the instrument - and is the estimand identified by instrumental
variables under heterogeneous treatment effects
([Imbens & Angrist, 1994](https://doi.org/10.2307/2951620)).
In a **sharp** RD every unit switches deterministically from $T=0$ to $T=1$ at $c$, so the estimand conditions on the covariate value $X = c$, not on an unobserved compliance type. [Imbens & Lemieux (2008)](https://doi.org/10.1016/j.jeconom.2007.05.001) provide a practical guide to estimation and bandwidth selection.

```{figure} figs/rdd_discontinuity.svg
:width: 80%
:name: fig-rdd

Regression discontinuity. Treatment switches on at the cutoff $c$; the vertical jump $\tau$ in the fitted outcome at $c$ identifies the average treatment effect at the cutoff, $\mathbb{E}[Y(1) - Y(0) \mid X = c]$.
```

```{prf:algorithm} Regression Discontinuity
:label: alg-rdd
:class: dropdown

**Inputs** Running variable $X$, outcome $Y$, cutoff $c$, bandwidth $h$

**Outputs** Estimated average treatment effect at the cutoff $\hat{\tau}$

1. Restrict to observations within the bandwidth, $|X - c| \le h$
2. Fit a local regression just below the cutoff: $\hat{\mu}_-(c) = \lim_{x \uparrow c} \mathbb{E}[Y \mid X = x]$
3. Fit a local regression just above the cutoff: $\hat{\mu}_+(c) = \lim_{x \downarrow c} \mathbb{E}[Y \mid X = x]$
4. Estimate the discontinuity: $\hat{\tau} = \hat{\mu}_+(c) - \hat{\mu}_-(c)$
5. Return the estimated effect at the cutoff $\hat{\tau}$
```

### Synthetic Control

When only a single (or a few) treated unit is observed over time, the synthetic control method - introduced by [Abadie & Gardeazabal (2003)](https://doi.org/10.1257/000282803321455188) and formalized by [Abadie, Diamond & Hainmueller (2010)](https://doi.org/10.1198/jasa.2009.ap08746) - constructs a counterfactual as a weighted combination of untreated *donor* units chosen to match the treated unit's pre-intervention trajectory. The post-intervention gap between the treated unit and its synthetic counterpart estimates the effect.

```{figure} figs/synthetic_control.svg
:width: 80%
:name: fig-synth

Synthetic control. Donor-pool units are weighted so the synthetic control (dashed) tracks the treated unit before intervention; the post-intervention gap $\tau$ is the estimated effect.
```

```{prf:algorithm} Synthetic Control
:label: alg-synth
:class: dropdown

**Inputs** Treated unit, donor pool of $J$ untreated units, pre-intervention outcomes and predictors

**Outputs** Estimated effect $\hat{\tau}_t$ for post-intervention periods

1. Choose non-negative weights $w_1, \ldots, w_J$ (summing to one) minimizing the pre-intervention distance between the treated unit and the weighted donor pool
2. Construct the synthetic control outcome $\hat{Y}^{\text{synth}}_t = \sum_{j=1}^{J} w_j\, Y^{(j)}_t$ for each period $t$
3. For each post-intervention period, estimate the effect $\hat{\tau}_t = Y^{\text{treated}}_t - \hat{Y}^{\text{synth}}_t$
4. Return the estimated effect $\hat{\tau}_t$
```
