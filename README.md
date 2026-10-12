# Actuarial Causal Inference Tutorial

<p class="tutorial-subtitle">From Risk Measurement to Risk Management</p>

This tutorial demonstrates how we can leverage modern causal machine learning (ML) and data science algorithms to infer causal effects from observational data. While standard ML performs very well at predicting outcomes, it often remains "causally blind" to the true risk drivers. By moving beyond passive risk measurement toward active and interventional risk management, we explore methods to quantify causal treatment effects in order to achieve effective risk mitigation. We apply this theory to actuarial use cases: assessing whether a health improvement programme is genuinely effective from purely observational data; and routing motor claims to the handler that minimises the combined ratio. Each demonstrates how naïve association misleads, and how causal inference can recover the unbiased effect of interest.

## Introduction and overview
This study has been carried out for the working group "Data Science" of the Swiss Association of Actuaries SAV, see [https://www.actuarialdatascience.org](https://www.actuarialdatascience.org).

The historical responsibility of the actuary has always been to ensure financial and societal stability. By building a collective of insureds, insurance ensures that unforeseeable events do not destabilize society. Traditionally, we rely on identifying historical correlations in claims data to categorize and understand risk. With increasing availability of real-time data, advanced ML methods can perform predictive analytics, e.g., forecast disease trajectories or large losses.

Today, in the era of AI, actuarial data science evolves towards prescriptive analytics and effective disaster management. Causal inference allows us to leverage modern AI algorithms to infer causal effects from observational data. While predictive models identify which factors are associated with loss, active risk management also requires understanding the causal effect of an intervention: "If we implement this preventative measure, by how much will we actually reduce the expected loss?".

By identifying true causal risk drivers rather than mere symptoms, we move from passive risk measurement to active risk mitigation. We can then actively prevent losses before they occur or engage in effective disaster management.

## Organisation

### Tutorial
The tutorial guides the reader from foundational concepts, identification and inference of causal effects, to the validation of causal conclusions using sensitivity measures.


**Stage 1 - {doc}`tutorial/concepts`:** Introduces the language of causal inference - treatments, potential outcomes, counterfactuals, confounding - and motivates why association is not causation, especially in actuarial applications.

**Stage 2 - {doc}`tutorial/identification`:** Establishes *when* causal effects can be recovered from observational data. This requires verifying the causal assumptions, using graphical models to select correct adjustment sets, and choosing an identification strategy.
- {doc}`tutorial/assumptions` - Consistency, SUTVA, positivity, exchangeability, and how to detect violations.
- {doc}`tutorial/graphical_models` - DAGs, d-separation, and the three fundamental path structures (chains, forks, colliders).
- {doc}`tutorial/methods` - Identification strategies: back-door and front-door adjustment (with their graphical criteria), instrumental variables, and causal discovery.

**Stage 3 - {doc}`tutorial/inference`:** Covers *how* to estimate causal effects once identification is established. Methods range from classical propensity score approaches to modern machine learning estimators.
- {doc}`tutorial/direct_adjustment` - G-computation, propensity score matching, inverse probability weighting, and the doubly robust estimators AIPW, TMLE and DML.
- {doc}`tutorial/heterogeneous_effects` - Meta-learners and causal trees and forests for heterogeneous and individualised treatment effect estimation.
- {doc}`tutorial/instrumental_variables` - Instrumental variables, two-stage least squares, and Mendelian randomization for unmeasured confounding.
- {doc}`tutorial/quasi_experimental` - Difference-in-differences, regression discontinuity, and synthetic control.
- {doc}`tutorial/bayesian` - Bayesian causal inference with BART and Bayesian Causal Forests.

**Stage 4 - {doc}`tutorial/sensitivity`:** Validates causal conclusions by assessing their robustness to untestable assumptions and ensuring the resulting model is fair.
- {doc}`tutorial/diagnostics` - Balance diagnostics, placebo tests, E-values, Rosenbaum bounds, and partial $R^2$ sensitivity analysis.
- {doc}`tutorial/debias` - Catalogue of biases (confounding, selection, collider) and de-biasing strategies.
- {doc}`tutorial/fairness` - Discrimination and fairness in insurance pricing, and why fairness is a causal question.


The tutorial connects the identification theory from {doc}`tutorial/identification` with the estimation methods in {doc}`tutorial/inference` and the validation tools in {doc}`tutorial/diagnostics`.


### Actuarial Applications

The actuarial application notebooks ground the tutorial theory in concrete workflows. The diagram below connects the two halves of this book side by side: on the left, the causal-inference-based workflow taught in the tutorial: Concepts, Identification, Inference, Validation, each posing the core question it answers and linking to its chapter. In the middle, the three application notebooks, drawn as bars that span exactly the workflow steps they include; and on the right, the insurance value chain, showing where along the business process, from new product development through underwriting, claims handling and portfolio management to reporting, these causal methods create value. 

```{raw} html
<iframe id="apps-matrix" src="figure/applications_matrix.html?v=20261012c"
        style="width:100%; border:none; height:640px;"
        title="Actuarial applications across the causal-inference workflow"></iframe>
<script>
(function () {
  var iframe = document.getElementById('apps-matrix');

  // Resolve the book's current theme: data-mode is auto|light|dark.
  function currentTheme() {
    var root = document.documentElement;
    var theme = root.getAttribute('data-theme');
    if (theme === 'light' || theme === 'dark') return theme;
    var mode = root.getAttribute('data-mode') || 'auto';
    if (mode === 'light' || mode === 'dark') return mode;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  function sendTheme() {
    if (iframe && iframe.contentWindow) {
      iframe.contentWindow.postMessage({ type: 'set-theme', value: currentTheme() }, '*');
    }
  }

  window.addEventListener('message', function (e) {
    if (!e.data) return;
    if (e.data.type === 'matrix-height') {
      iframe.style.height = (e.data.height + 20) + 'px';
    } else if (e.data.type === 'matrix-ready') {
      sendTheme();
    }
  });

  // Re-send whenever the book theme toggle flips data-mode or data-theme.
  new MutationObserver(sendTheme).observe(document.documentElement, {
    attributes: true, attributeFilter: ['data-mode', 'data-theme']
  });
  // Re-send when the OS theme changes while the book is in "auto" mode.
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', sendTheme);

  iframe.addEventListener('load', sendTheme);
  sendTheme();
})();
</script>
```

## Acknowledgements

We would like to thank Marco Breitig, Michael Mayer, and Jan Tilly for their comprehensive reviews and feedback that led to significant improvements of this tutorial. Furthermore, we would like to thank the [Data Science Working Group](https://www.actuarialdatascience.org) of the SAV for supporting this work.