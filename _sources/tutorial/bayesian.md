# Bayesian Causal Inference

This section is part of {doc}`inference`, which covers the estimation of causal effects from observational data. While the preceding sections focus on frequentist methods (propensity scores, regression, causal trees/forests), here we take a **Bayesian** perspective.

Bayesian methods offer a natural framework for causal inference by treating unknown quantities — potential outcomes, treatment effects, and model parameters — as random variables with prior distributions updated by observed data $D$. This section introduces the key ideas, following [Rubin (1978)](https://doi.org/10.1214/aos/1176344064), [Shalizi (2025, Ch. 21)](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf), and the [Causal ML Book](https://www.causalmlbook.com/).

## Why Bayesian Causal Inference?

In the potential outcomes framework, the fundamental problem is that we observe only one of $Y(1)$ or $Y(0)$ for each unit. The Bayesian approach treats the **missing potential outcomes as parameters** to be inferred:

- **Prior beliefs** encode what we know before seeing the data — for example, that treatment effects are likely small, or that confounders have plausible distributions.
- **Posterior inference** yields a full distribution over causal estimands (ATE, CATE), naturally quantifying **uncertainty** in a way that frequentist point estimates and confidence intervals do not.
- **Model comparison** via Bayes factors or posterior predictive checks helps select among competing causal models.

## Bayesian Potential Outcomes Model

```{prf:definition} Bayesian Causal Model
:label: bayesian-causal-model
:class: dropdown

For each unit $i$ with covariates $X_i$ and binary treatment $T_i$, define the potential outcome models:

$$
Y_i(0) \mid X_i, \theta_0 \sim f_0(Y \mid X_i, \theta_0), \qquad Y_i(1) \mid X_i, \theta_1 \sim f_1(Y \mid X_i, \theta_1)
$$

with priors $\theta_0 \sim p(\theta_0)$ and $\theta_1 \sim p(\theta_1)$. The individual treatment effect is $\tau_i = Y_i(1) - Y_i(0)$, and the posterior distribution of the ATE is:

$$
p(\tau \mid D) = \int \left[\mathbb{E}_{\theta_1}[Y(1) \mid X] - \mathbb{E}_{\theta_0}[Y(0) \mid X]\right] \, p(\theta_0, \theta_1 \mid D) \, d\theta_0 \, d\theta_1
$$
```

Under {prf:ref}`exchangeability`, the observed outcome model for unit $i$ is:

$$
Y_i \mid X_i, T_i, \theta \sim \begin{cases} f_0(Y \mid X_i, \theta_0) & \text{if } T_i = 0 \\ f_1(Y \mid X_i, \theta_1) & \text{if } T_i = 1 \end{cases}
$$

The posterior $p(\theta_0, \theta_1 \mid D)$ is computed via Bayes' rule, and the CATE for a new unit with covariates $x$ is:

$$
\tau(x) = \mathbb{E}[Y(1) - Y(0) \mid X = x, D]
$$

## Bayesian Additive Regression Trees (BART)

**BART** ([Chipman, George & McCulloch, 2010](https://doi.org/10.1214/09-AOAS285)) is a sum-of-trees regression model; its use for causal inference was introduced by [Hill (2011)](https://doi.org/10.1198/jcgs.2010.08162), and it is now the most widely used Bayesian method for heterogeneous treatment effect estimation. It models the outcome as a sum of regression trees with Bayesian priors on tree structure and leaf parameters.

```{prf:definition} BART for Causal Inference
:label: bart
:class: dropdown

The outcome model is:

$$
Y_i = f(X_i, T_i) + \varepsilon_i, \qquad f(X_i, T_i) = \sum_{j=1}^{m} h_j(X_i, T_i; \mathcal{T}_j, \mathcal{M}_j)
$$

where each $h_j$ is a regression tree with structure $\mathcal{T}_j$ and leaf parameters $\mathcal{M}_j$, and $\varepsilon_i \sim \mathcal{N}(0, \sigma^2)$.

The CATE is estimated as:

$$
\hat{\tau}(x) = \hat{f}(x, 1) - \hat{f}(x, 0)
$$

where $\hat{f}$ is the posterior mean of the sum-of-trees model.
```

BART's advantages for causal inference include:
- **Flexible nonparametric modelling** of the outcome surface without specifying functional form.
- **Automatic uncertainty quantification** through the posterior distribution — credible intervals for $\tau(x)$ come directly from the MCMC output.
- **Regularisation** via the tree priors, which favours shallow trees and prevents overfitting.

### Bayesian Causal Forests (BCF)

[Hahn, Murray & Carvalho (2020)](https://doi.org/10.1214/19-BA1195) extend BART specifically for causal inference by separating the prognostic and treatment effect components:

$$
Y_i = \mu(X_i) + \tau(X_i) \cdot T_i + \varepsilon_i
$$

where $\mu(X_i)$ captures the baseline outcome (prognostic function) and $\tau(X_i)$ captures the heterogeneous treatment effect. Each is itself a *separate* sum-of-trees ensemble with its own BART prior — the prognostic trees $h_j$ build up $\mu$ and the treatment-effect trees $g_k$ build up $\tau$:

$$
\mu(X_i) = \sum_{j=1}^{m_\mu} h_j(X_i; \mathcal{T}_j^{\mu}, \mathcal{M}_j^{\mu}), \qquad \tau(X_i) = \sum_{k=1}^{m_\tau} g_k(X_i; \mathcal{T}_k^{\tau}, \mathcal{M}_k^{\tau})
$$

These are exactly the trees $h_j$ and $g_k$ labelled in the figure below: the two ensembles never share trees, and only $\tau$ is multiplied by the treatment $T_i$. This separation improves treatment effect estimation by preventing the prognostic signal from contaminating the treatment effect estimate, a phenomenon called **regularisation-induced confounding**.

BCF additionally incorporates the estimated propensity score $\hat{\pi}(X_i)$ as a covariate in the prognostic model to reduce confounding bias.

```{figure} figs/bayesian_bcf.svg
:width: 95%
:name: fig-bayesian-bcf

Bayesian Causal Forest decomposition. The outcome is split into a *prognostic* function $\mu(X)$ — the baseline outcome surface — and a *treatment effect* function $\tau(X)$, each modelled by its own independent BART ensemble (a sum of shallow, shrunk trees). Giving $\tau(X)$ a separate prior and scale stops the strong prognostic signal from being shrunk into the effect estimate, the *regularisation-induced confounding* that [Hahn, Murray & Carvalho (2020)](https://doi.org/10.1214/19-BA1195) flag. The estimated propensity score $\hat{\pi}(X)$ enters the prognostic model as an extra covariate to further reduce confounding bias.
```

## Bayesian Propensity Score Methods

The propensity score $\pi(x) = P(T=1 \mid X=x)$ can also be estimated within a Bayesian framework, yielding a posterior distribution over the propensity scores and propagating this uncertainty into the causal estimate.

```{prf:definition} Bayesian Propensity Score
:label: bayesian-propensity
:class: dropdown

Given a model $T_i \mid X_i, \alpha \sim \text{Bernoulli}(\pi(X_i; \alpha))$ with prior $\alpha \sim p(\alpha)$, the Bayesian propensity score is the posterior predictive:

$$
\hat{\pi}(x \mid D) = \int \pi(x; \alpha) \, p(\alpha \mid D) \, d\alpha
$$

Treatment effect estimates using this posterior propensity score account for **propensity model uncertainty**, unlike plug-in frequentist approaches.
```

## Posterior Inference for Treatment Effects

Bayesian causal inference outputs a **posterior distribution** over the estimand, from which we derive:

| Quantity | Interpretation |
|----------|---------------|
| $\mathbb{E}[\tau \mid D]$ | Posterior mean ATE |
| $\text{Var}[\tau \mid D]$ | Posterior variance (uncertainty) |
| 95% credible interval | $[\tau_{0.025}, \tau_{0.975}]$ from the posterior |
| $P(\tau > 0 \mid D)$ | Posterior probability that treatment is beneficial |

The posterior probability $P(\tau(x) > 0 \mid D)$ is particularly useful for **decision-making**: it directly quantifies the probability that the treatment is beneficial for a given subgroup, which is more interpretable for actuarial applications than a p-value.

```{figure} figs/bayesian_posterior.svg
:width: 80%
:name: fig-bayesian-posterior

From prior to posterior. A weakly informative *prior* $p(\tau)$ encodes the belief that the effect is plausibly small and centred near zero. After conditioning on the data $D$, the *posterior* $p(\tau \mid D)$ is narrower and shifted, summarising everything we know about the effect. Unlike a frequentist point estimate, it yields the posterior mean $\mathbb{E}[\tau \mid D]$, a 95% *credible* interval (a direct probability statement about $\tau$), and the decision-relevant posterior probability $P(\tau > 0 \mid D)$ — the shaded mass to the right of zero.
```

## Comparison with Frequentist Approaches

| Aspect | Frequentist | Bayesian |
|--------|-------------|----------|
| **Uncertainty** | Confidence intervals (coverage guarantee) | Credible intervals (direct probability) |
| **Prior information** | Not formally incorporated | Encoded via priors |
| **Small samples** | Relies on asymptotic approximations | Exact finite-sample posterior |
| **HTE estimation** | Causal forests ([Wager & Athey, 2018](https://doi.org/10.1080/01621459.2017.1319839)) | BART / BCF ([Hill, 2011](https://doi.org/10.1198/jcgs.2010.08162)) |
| **Model uncertainty** | Model selection or averaging | Posterior model probabilities |
| **Computation** | Often closed-form or fast | MCMC (slower but more flexible) |

## Practical Considerations

- **Prior sensitivity:** Check that conclusions are robust to reasonable prior specifications. Use weakly informative priors as defaults.
- **Convergence diagnostics:** Monitor MCMC chains using $\hat{R}$ statistics, effective sample size, and trace plots.
- **Scalability:** BART scales well to moderate-dimensional problems ($p \lesssim 100$). For very high-dimensional $X$, variable selection priors or sparsity-inducing modifications (e.g. DART, [Linero 2018](https://doi.org/10.1080/01621459.2016.1264957)) may be needed.
- **Software:** Popular implementations include `bartCause` (R), `dbarts` (R), and `pymc-bart` (Python).
