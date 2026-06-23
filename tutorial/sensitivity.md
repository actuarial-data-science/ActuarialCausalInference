# Validation and Sensitivity Analysis

Once a causal effect has been *identified* ({doc}`identification`) and *estimated* ({doc}`inference`), the final stage is to **validate** the result. Estimation rests on untestable assumptions — most critically {prf:ref}`exchangeability` (no unmeasured confounding) — so a credible analysis must diagnose residual bias, quantify robustness to violations, and confirm that the resulting model is fair. This chapter covers the three pillars of that validation.

## Diagnostics and Sensitivity Analysis

**{doc}`diagnostics`** — Balance diagnostics (standardised mean differences, overlap and Love plots) confirm that measured confounders are balanced after adjustment, and placebo/falsification tests probe for residual bias. Sensitivity tools — E-values, Rosenbaum bounds, partial $R^2$ (omitted-variable bias), and Manski bounds — quantify how strong unmeasured confounding would need to be to overturn the conclusion.

## Biases and De-biasing

**{doc}`debias`** — A practical guide that maps each assumption violation to the bias it produces (confounding, selection, collider bias, positivity violations, interference) and to the de-biasing strategy that addresses it (adjust, reweight, restrict, restructure).

## Fairness

**{doc}`fairness`** — Beyond statistical bias, insurance models must not discriminate against protected groups. Covers proxy discrimination, fairness definitions (unawareness, discrimination-free pricing, counterfactual fairness), group fairness diagnostics, and why fairness is ultimately a causal question — closing with the actuary's end-to-end workflow.
