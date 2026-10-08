# Instrumental Variables

*Identification and estimation under unmeasured confounding via an instrument.*

The methods in {doc}`direct_adjustment` and {doc}`heterogeneous_effects` assume unconfoundedness - that all common causes of treatment and outcome are measured. When that fails, an **instrument** can still identify a causal effect by exploiting a source of exogenous variation in the treatment. This chapter develops the instrumental-variable estimand, its two-stage least-squares implementation, and the genetic special case of Mendelian randomization.

## Instrumental Variable Approach


```{figure} figs/iv_structure.svg
:width: 80%
:name: fig-IV

Instrumental variable $I$. The instrument induces exogenous variation in the treatment $T$ while being independent of the unobserved confounder $U$ and affecting the outcome $Y$ only through $T$.
```

When unobserved confounding exists (see {numref}`fig-IV`), an instrument $I$ can identify the causal effect if ([Shalizi, 2025, Ch. 20](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)):

1. *Relevance*: $I$ affects $T$
2. *Exogenous noise*: $I \perp\!\!\!\perp U$ - the instrumental variable is independent of the unobserved confounder
3. *Exclusion restriction*: $I$ affects $Y$ only through $T$
4. *Monotonicity*: $T(I{=}1) \ge T(I{=}0)$ for every unit (no *defiers*) - the condition under which the instrument identifies a LATE for compliers rather than requiring a constant treatment effect

The modern econometric interpretation of instrumental variables traces to [Imbens & Angrist (1994)](https://doi.org/10.2307/2951620), who show that, under monotonicity, 2SLS identifies a *local average treatment effect* for compliers, and to the potential-outcomes framework of [Angrist, Imbens & Rubin (1996)](https://doi.org/10.1080/01621459.1996.10476902); [Angrist & Krueger (1991)](https://doi.org/10.2307/2937954) is the canonical applied example, using quarter of birth as an instrument for schooling.

The instrumental variable $I$ is a source of exogenous variation in $T$ that is uncorrelated with the common ancestors of $T$ and $Y$. By seeing how both $T$ and $Y$ respond to these perturbations, and using the fact that $I$ only influences $Y$ through $T$, we can deduce the causal effect of $T$ on $Y$.


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
The **same exogenous covariates $X$ must appear in both stages**. Omitting them produces a biased estimate whenever $X$ is correlated with both the instrument $I$ and the outcome $Y$: the covariates must be *partialled out* of the instrument–treatment relationship for the exclusion restriction and exogeneity conditions to hold conditionally. The bivariate form ($T = \alpha I + \varepsilon_1$, $Y = \beta \hat{T} + \varepsilon_2$) is valid whenever the instrument is **unconditionally** exogenous - as with a randomised encouragement or a lottery - in which case covariates only sharpen precision. Covariates become *necessary* when the instrument is exogenous only **conditionally** on $X$, i.e. when $X$ is correlated with both $I$ and $Y$ - the situation described above, which is the norm in insurance data.
```

```{tip}
For valid inference, obtain 2SLS estimates from a **dedicated IV routine** (`linearmodels.IV2SLS` in Python, `AER::ivreg` in R, or `ivregress` in Stata) rather than by fitting the two OLS stages by hand. The two approaches agree on the point estimate $\hat{\beta}$, but only the IV routine returns correct standard errors. The reason is instructive: valid 2SLS inference computes the error variance from the *structural* residuals $u = Y - \hat{\beta}T$ using the **observed** treatment $T$, whereas a manual second-stage OLS would use the fitted-treatment residuals $\hat{\varepsilon} = Y - \hat{\beta}\hat{T}$. Since $\hat{\varepsilon} = u + \hat{\beta}(T - \hat{T})$, its variance $\mathbb{E}[\hat{\varepsilon}^2] = \mathbb{E}[u^2] + \beta^2\,\operatorname{Var}(T - \hat{T}) + 2\beta\,\mathbb{E}[u(T - \hat{T})]$ carries a **cross term that is non-zero precisely because $T$ is endogenous** ($u$ is correlated with the first-stage residual $T - \hat{T}$). Its sign is not determined in general, so the hand-rolled standard errors are not merely conservative - they are simply **wrong**, and can err in either direction. Using the dedicated routine keeps inference well-calibrated, which matters in actuarial screening where a mis-calibrated test can wrongly admit a useless intervention or reject a genuinely beneficial one (Wooldridge, 2010, *Econometric Analysis of Cross Section and Panel Data*, p. 96).
```

```{admonition} Instruments in an insurance setting
:class: tip

Valid instruments are rarer in insurance than genetic variants are in epidemiology, but several recurring designs supply one:

- **Randomised encouragement.** An insurer that nudges a random subset of policyholders toward a wellness programme, telematics device, or preventive screening creates an encouragement $I$ that shifts take-up $T$ without directly affecting the outcome $Y$ (claims) - the actuarial analogue of a randomised-encouragement trial.
- **Assignment quasi-randomness.** Broker, agent, or claims-adjuster assignment that is effectively random conditional on observed routing rules can instrument for a treatment they influence (e.g. settlement speed), provided the adjuster affects the outcome *only* through that channel.
- **Administrative geography.** Distance to the nearest claims office, repair shop, or clinic shifts the cost of using a service without plausibly causing the loss itself.
- **Regulatory cut-over dates.** A rating-factor ban or product-rule change that takes effect on a fixed date instruments for the post-reform treatment, exploiting variation no single policyholder controls.

In every case the exclusion restriction is the binding assumption and deserves explicit, domain-specific defence - the encouragement must not change behaviour except through take-up, the adjuster must not affect claims except through the treatment, and so on.
```

## Weak Instruments and Over-identification

The IV conditions guarantee *consistency*, not *precision*. When the instrument is only weakly relevant - the first stage $T = \alpha I + \gamma X + \varepsilon_1$ has a small $\hat{\alpha}$ relative to its standard error - two problems arise even in large samples: the 2SLS estimator becomes badly biased toward the (confounded) OLS estimate, and its sampling distribution is non-normal, so conventional confidence intervals under-cover ([Staiger & Stock, 1997](https://doi.org/10.2307/2171753); [Bound, Jaeger & Baker, 1995](https://doi.org/10.1080/01621459.1995.10476536)).

The standard diagnostic is the **first-stage $F$-statistic** on the excluded instrument(s). A common rule of thumb treats $F < 10$ as a weak-instrument warning, while [Stock & Yogo (2005)](https://doi.org/10.1017/CBO9780511614491.006) provide formal critical values that bound the worst-case 2SLS bias or test-size distortion; recent work argues the threshold should often be considerably higher. In an insurance encouragement design this matters directly: if only a small fraction of nudged policyholders actually take up the programme, the instrument is weak and the LATE estimate - however unbiased in principle - may be too noisy to act on.

With **more instruments than endogenous treatments** (over-identification), the surplus moment conditions can be tested: under the null that *all* instruments satisfy the exclusion restriction, the Sargan ([Sargan, 1958](https://doi.org/10.2307/1907619)) or Hansen $J$ statistic should be small. A rejection signals that at least one instrument violates exogeneity (e.g. a pleiotropic SNP, or an "instrument" that has its own path to the outcome), though the test cannot say which. Over-identification also improves efficiency - the multiple-SNP MR estimators below are the canonical example.

## Mendelian Randomization

Mendelian Randomization (MR) is an application of the instrumental variable principle to genetics and epidemiology. The idea - dating to [Katan (1986)](https://doi.org/10.1016%2Fs0140-6736%2886%2992972-7) and formalised by [Davey Smith & Ebrahim (2003)](https://doi.org/10.1093/ije/dyg070) - exploits the fact that genetic variants are assigned at conception, before any environmental exposure, and therefore satisfy the IV conditions almost by construction:

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

MR estimates are increasingly available in the public health literature for risk factors relevant to life and health insurers - BMI, blood pressure, lipid levels, smoking behaviour, and many biomarkers. Because a well-conducted MR study targets the *lifetime causal effect* of a modifiable risk factor (rather than an association observed at a single medical exam), the estimates can inform pricing and underwriting in ways that observational risk scores cannot: they are, in principle, robust to reverse causation and the confounding that plagues claims-linked data. The key caveat is the exclusion restriction: many SNPs have pleiotropic effects, so MR estimates should be accompanied by sensitivity analyses such as MR-Egger regression ([Bowden et al., 2015](https://doi.org/10.1093/ije/dyv080)) or weighted median estimators ([Bowden et al., 2016](https://doi.org/10.1002/gepi.21965)).
```
