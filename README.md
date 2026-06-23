# Actuarial Causal Inference Tutorial

<p class="tutorial-subtitle">From Risk Measurement to Intelligent Risk Management</p>

This tutorial demonstrates how we can leverage modern causal machine learning (ML) and data science algorithms to infer causal effects from observational data. While standard ML excels at predicting outcomes, it often remains "causally blind" to the true levers of risk. By moving beyond passive risk measurement toward active and interventional risk management, we explore methods to quantify causal treatment effects in order to achieve intelligent risk mitigation. We apply this theory to actuarial use cases: assessing whether a health-insurance prevention programme is genuinely effective from purely observational data; constructing health-cover premiums that reflect true risk while remaining free of discrimination; routing motor claims to the handler that minimises the combined ratio; and quantifying the mortality reduction attributable to a preventive intervention. Each demonstrates how naïve association misleads, and how causal inference recovers the unbiased effect of interest.

## Introduction and overview
This study has been carried out for the working group "Data Science" of the Swiss Association of Actuaries SAV, see [https://www.actuarialdatascience.org](https://www.actuarialdatascience.org). The historical responsibility of the actuary has always been to ensure financial and societal stability. By building a collective of insureds, insurance ensures that unforeseeable events do not destabilize society. Traditionally, we relied on identifying historical correlations in claims data to categorize and understand risk. With increasing availability of real-time data, advanced ML methods can perform predictive analytics, i.e., forecast disease trajectories or large losses.

Today, in the era of AI, actuarial data science evolves towards prescriptive analytics and intelligent disaster management. Causal inference empowers this transition. It allows us to leverage modern AI algorithms to infer causal effects from observational data. While predictive models identify which factors are associated with loss, true risk management requires understanding the causal effect of an intervention: "If we implement this preventative measure, by how much will we actually reduce the expected loss?".

By identifying true causal drivers rather than mere symptoms, we move from passive risk measurement to active risk mitigation. We can then actively prevent losses before they occur or engage in intelligent disaster management, i.e., trigger interventions that act as true levers for long-term health and financial stability.  Furthermore, by isolating these causal effects, we can eliminate systemic biases and ensure that insurance pricing is not only statistically robust but ethically fair. This is our next step in ensuring a more stable and just society.

## Organisation

### Tutorial
The tutorial guides the reader from foundational concepts, identification and inference of causal effects, to the validation of causal conclusions using sensitivity measures.


**Stage 1 — {doc}`tutorial/concepts`:** Introduces the language of causal inference — treatments, potential outcomes, counterfactuals, confounding — and motivates why association is not causation, especially in actuarial applications.

**Stage 2 — {doc}`tutorial/identification`:** Establishes *when* causal effects can be recovered from observational data. This requires verifying the causal assumptions, using graphical models to select correct adjustment sets, and choosing an identification strategy.
- {doc}`tutorial/assumptions` — Consistency, SUTVA, positivity, exchangeability, and how to detect violations.
- {doc}`tutorial/graphical_models` — DAGs, d-separation, backdoor and frontdoor criteria, causal discovery.
- {doc}`tutorial/methods` — Identification strategies: back-door adjustment, front-door adjustment, and instrumental variables.

**Stage 3 — {doc}`tutorial/inference`:** Covers *how* to estimate causal effects once identification is established. Methods range from classical propensity score approaches to modern machine learning estimators.
- {doc}`tutorial/propensity` — Propensity score matching and inverse probability weighting.
- {doc}`tutorial/regression_methods` — Regression adjustment, doubly robust and orthogonal ML estimators, and quasi-experimental designs.
- {doc}`tutorial/tree_based_methods` — Causal trees and forests for heterogeneous and individualised treatment effect estimation.
- {doc}`tutorial/bayesian` — Bayesian causal inference with BART and Bayesian Causal Forests.

**Stage 4 — {doc}`tutorial/sensitivity`:** Validates causal conclusions by assessing their robustness to untestable assumptions and ensuring the resulting model is fair.
- {doc}`tutorial/diagnostics` — Balance diagnostics, placebo tests, E-values, Rosenbaum bounds, and partial $R^2$ sensitivity analysis.
- {doc}`tutorial/debias` — Catalogue of biases (confounding, selection, collider) and de-biasing strategies.
- {doc}`tutorial/fairness` — Discrimination and fairness in insurance pricing, and why fairness is a causal question.


The actuary's end-to-end workflow connects the identification theory from {doc}`tutorial/identification` with the estimation methods in {doc}`tutorial/inference` and the validation tools in {doc}`tutorial/sensitivity`:

```{figure} tutorial/figs/actuary_workflow.svg
:width: 100%
:name: fig-actuary-workflow
```


### Actuarial Applications

> TODO: visualization, use cases that are embedded in actuarial workflows