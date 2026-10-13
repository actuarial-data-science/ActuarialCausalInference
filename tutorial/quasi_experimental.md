# Quasi-Experimental Designs

*Exploiting natural experiments and institutional variation.*

When adjustment for measured covariates is insufficient, *quasi-experimental designs* recover causal effects by exploiting structural features of how treatment is assigned - over time, around a threshold, or relative to a comparison unit. These designs are especially relevant for longitudinal data. They form the empirical core of modern applied econometrics; the introductory textbooks of [Angrist & Pischke (2009)](https://doi.org/10.1515/9781400829828), [Angrist & Pischke (2015)](https://press.princeton.edu/books/paperback/9780691152844/mastering-metrics) and [Cunningham (2021)](https://doi.org/10.12987/9780300255881), together with the more statistical treatment of [Imbens & Rubin (2015)](https://doi.org/10.1017/CBO9781139025751), give book-length introductions to the methods below.

## Difference-in-Differences

Difference-in-differences (DiD) compares the change in outcomes over time between a treated and a control group. Under the *parallel trends* assumption - that, absent treatment, both groups would have evolved in parallel - the post-period gap beyond the projected control trend identifies the average treatment effect on the treated (ATT). The design dates back to [Ashenfelter & Card (1985)](https://doi.org/10.2307/1924810), and [Card & Krueger (1994)](https://doi.org/10.1257/aer.84.4.772) is its best-known application - the New Jersey minimum-wage study. [Sant'Anna & Zhao (2020)](https://doi.org/10.1016/j.jeconom.2020.06.003) give a doubly robust DiD estimator, and [Callaway & Sant'Anna (2021)](https://doi.org/10.1016/j.jeconom.2020.12.001) extend the design to multiple periods and staggered treatment timing with their group-time ATT estimator. [Goodman-Bacon (2021)](https://doi.org/10.1016/j.jeconom.2021.03.014) is not a new estimator but a *decomposition* result: under staggered timing the canonical two-way fixed-effects (TWFE) OLS regression - the default DiD implementation in most software - equals a weighted average of all possible $2 \times 2$ DiDs, and some of those weights turn **negative** when treatment effects are heterogeneous across cohorts or over time, so the TWFE estimate can be attenuated or even sign-reversed *even when parallel trends holds*. This diagnostic motivates the heterogeneity-robust DiD estimators of [Callaway & Sant'Anna (2021)](https://doi.org/10.1016/j.jeconom.2020.12.001), [Sun & Abraham (2021)](https://doi.org/10.1016/j.jeconom.2020.09.006) and [de Chaisemartin & D'Haultfœuille (2020)](https://doi.org/10.1257/aer.20181169), which replace the problematic TWFE weights with convex, interpretable ones.

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

```{admonition} Actuarial example: a bonus-malus or deductible reform
:class: tip

An insurer that overhauls the bonus-malus scale (or raises the base deductible) for one product line, but not another comparable line, has a natural DiD: the reformed line is the treated group, the untouched line the control, and claim frequency or loss ratio the outcome. The ATT is the change in the treated line's outcome net of the common market trend captured by the control line. The parallel-trends assumption is the crux and is partly checkable - plot several *pre-reform* years and confirm the two lines moved together. Watch for anticipation effects (policyholders front-loading claims before a deductible rise) and for staggered roll-out across regions, which brings the negative-weighting TWFE problem above into play.
```

## Regression Discontinuity

Regression discontinuity (RD) applies when treatment is assigned by a threshold rule on a continuous *running variable* $X$ (e.g. a risk score). The design was first proposed by [Thistlethwaite & Campbell (1960)](https://doi.org/10.1037/h0044319); its modern econometric foundations are due to [Hahn, Todd & van der Klaauw (2001)](https://doi.org/10.1111/1468-0262.00183). Units just below and just above the cutoff $c$ are comparable, so the jump in the outcome at $c$ identifies the **average treatment effect at the cutoff**, $\mathbb{E}[Y(1) - Y(0) \mid X = c]$ - the causal effect *at the discontinuity point* ([Hahn, Todd & van der Klaauw, 2001](https://doi.org/10.1111/1468-0262.00183); [Imbens & Lemieux, 2008](https://doi.org/10.1016/j.jeconom.2007.05.001)). 
This is a *different* object from the **local average treatment effect (LATE)** identified by the IV/2SLS design - the effect among **compliers**, the units whose treatment status is switched by the instrument ([Imbens & Angrist, 1994](https://doi.org/10.2307/2951620)). The LATE estimand is defined in {doc}`inference` and developed in {doc}`instrumental_variables`.
In a **sharp** RD every unit switches deterministically from $T=0$ to $T=1$ at $c$, so the estimand conditions on the covariate value $X = c$, not on an unobserved compliance type. In a **fuzzy** RD, by contrast, the treatment probability jumps by less than one at the cutoff, and the discontinuity then identifies a *LATE at the cutoff* among compliers ([Hahn, Todd & van der Klaauw, 2001](https://doi.org/10.1111/1468-0262.00183)). [Imbens & Lemieux (2008)](https://doi.org/10.1016/j.jeconom.2007.05.001) provide a practical guide to estimation and bandwidth selection.

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

```{admonition} Actuarial example: an eligibility or rating threshold
:class: tip

Many insurance rules are sharp functions of a continuous variable: a telematics discount granted only above a driving-score cutoff, a premium loading that switches on at a policyholder age, a reinsurance treaty attaching above a fixed claim size, or a regulatory surcharge triggered at a sum-insured threshold. Comparing outcomes just either side of the cutoff identifies the effect *at the threshold* - for example, the effect of the telematics discount on retention among drivers at the qualifying score. A **fuzzy** variant arises when the rule only shifts the *probability* of treatment (e.g. an age at which a product becomes available but take-up is voluntary), identifying a LATE at the cutoff. The key validity check is that units cannot precisely **manipulate** the running variable to land on the favourable side - a density test around $c$ guards against it.
```

## Synthetic Control

When only a single (or a few) treated unit is observed over time, the synthetic control method - introduced by [Abadie & Gardeazabal (2003)](https://doi.org/10.1257/000282803321455188) and formalised by [Abadie, Diamond & Hainmueller (2010)](https://doi.org/10.1198/jasa.2009.ap08746) - constructs a counterfactual as a weighted combination of untreated *donor* units chosen to match the treated unit's pre-intervention trajectory. The post-intervention gap between the treated unit and its synthetic counterpart estimates the effect. Inference typically relies on **placebo (permutation) tests**: the intervention is reassigned in turn to each donor unit, and the treated unit's post-intervention gap is judged against the resulting distribution of placebo gaps ([Abadie, Diamond & Hainmueller, 2010](https://doi.org/10.1198/jasa.2009.ap08746)).

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

1. Choose non-negative weights $w_1, \ldots, w_J$ (summing to one) minimising the pre-intervention distance between the treated unit and the weighted donor pool
2. Construct the synthetic control outcome $\hat{Y}^{\text{synth}}_t = \sum_{j=1}^{J} w_j\, Y^{(j)}_t$ for each period $t$
3. For each post-intervention period, estimate the effect $\hat{\tau}_t = Y^{\text{treated}}_t - \hat{Y}^{\text{synth}}_t$
4. Return the estimated effect $\hat{\tau}_t$
```

```{admonition} Actuarial example: a regional regulatory change
:class: tip

Suppose a single region (canton, state, or country) bans a rating factor, caps premium increases, or mandates a new cover, while comparable regions are left unchanged. With one treated region and many untreated ones, synthetic control builds a weighted combination of the other regions that reproduces the treated region's pre-change trajectory of average premium, loss ratio, or market share, and reads the post-change gap as the effect of the reform. Inference uses the placebo-in-space test above: reassign the "reform" to each donor region and check that the true treated region's gap is extreme relative to the placebo distribution. The donor pool should exclude regions subject to their own contemporaneous shocks, which would otherwise contaminate the counterfactual.
```
