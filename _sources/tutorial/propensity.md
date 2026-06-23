# Propensity Score Methods

## Propensity Score Definition
The probability of receiving treatment $T$ given a set of observed covariates $X$, defined as:
$$\pi(x) = P(T = 1 \mid X = x)$$
It reduces high-dimensional control variables into a single score in order to achieve covariate balance.

(overlap)=
### Overlap (Common Support)
Propensity score methods are only valid where treated and control units are actually *comparable*. This requirement is the empirical counterpart of the {prf:ref}`positivity`: For every covariate profile $x$, both treatment arms must have a positive (non-zero) probability of being observed,

$$0 < \pi(x) < 1 \quad \text{for all } x .$$

The range of covariates where this holds — where the propensity score distributions of the treated ($T=1$) and control ($T=0$) groups overlap — is called the region of **common support** (or *overlap*). When $\pi(x)$ approaches $0$ or $1$ for some covariate profile, there are no comparable units in the opposite group: matching finds no partner to pair with, and inverse-probability weights explode. In practice, overlap is diagnosed by inspecting the distribution of the estimated scores $\hat{\pi}(x)$ in each treatment group.

## Propensity Score Matching
Matching focuses on creating "apples-to-apples" comparisons by pairing treated units with similar control units. This algorithm typically estimates the Average Treatment Effect on the Treated (ATT).

```{prf:algorithm} Propensity Score Matching
:label: alg-psm
:class: dropdown

**Inputs** Data $D$ with covariates $X$, treatment $T$, and outcome $Y$; Caliper $\delta$

**Outputs** Estimated ATT $\hat{\tau}_{ATT}$

1. **Estimate Propensity Scores**
	1. Train model $P(T = 1 \mid X)$ (e.g., Logistic Regression) on $D$
	2. Compute $\hat{\pi}(x_i)$ for all individuals $i$ *(Probability of treatment)*

2. **Match Units**
	1. Split $D$ into Treated group $\mathcal{T}$ and Control group $\mathcal{T}_0$
	2. Initialize empty matched set $\mathcal{M} = \emptyset$
	3. For each unit $i \in \mathcal{T}$:

		1. Find unit $j \in \mathcal{T}_0$ that minimizes $|\hat{\pi}(x_i) - \hat{\pi}(x_j)|$
		2. If $|\hat{\pi}(x_i) - \hat{\pi}(x_j)| \leq \delta$: *(Apply caliper distance)*

			1. Add pair $(i, j)$ to $\mathcal{M}$
			2. *Optional:* Remove $j$ from $\mathcal{T}_0$ *(Matching without replacement)*

3. **Estimate Effect**
	1. $\hat{\tau}_{ATT} = \frac{1}{|\mathcal{M}|} \sum_{(i,j) \in \mathcal{M}} (Y_i - Y_j)$
	2. Return $\hat{\tau}_{ATT}$
```


## Inverse Propensity Score Weighting
Weighting uses Inverse Probability Weighting (IPW) to create a "pseudo-population" where the treatment is independent of measured covariates. This approach is often used to estimate the Average Treatment Effect (ATE) for the entire population. {cite:t}`austin2011`

```{prf:algorithm} Propensity Score Weighting
:label: alg-psw
:class: dropdown

**Inputs** Data $D$ with covariates $X$, treatment $T$, and outcome $Y$

**Outputs** Estimated ATE $\hat{\tau}_{ATE}$

1. **Estimate Propensity Scores**
	1. Train model $P(T = 1 \mid X)$ to obtain $\hat{\pi}(x_i)$
	2. *Optional:* Clip scores (e.g., $[0.05, 0.95]$) to avoid extreme weights

2. **Calculate IPW Weights**
	1. For each unit $i$ in $D$:

		1. If $T_i = 1$: $w_i = \frac{1}{\hat{\pi}(x_i)}$ *(Weight for Treated)*
		2. Else: $w_i = \frac{1}{1 - \hat{\pi}(x_i)}$ *(Weight for Control)*

3. **Estimate Effect**
	1. $\hat{Y}_1 = \frac{\sum T_i Y_i w_i}{\sum T_i w_i}$ *(Weighted mean for Treated)*
	2. $\hat{Y}_0 = \frac{\sum (1-T_i) Y_i w_i}{\sum (1-T_i) w_i}$ *(Weighted mean for Control)*
	3. $\hat{\tau}_{ATE} = \hat{Y}_1 - \hat{Y}_0$
	4. Return $\hat{\tau}_{ATE}$
```

## Interactive Comparison: Matching vs. Weighting
The interactive figure below applies both methods to a single simulated dataset with covariates $X$, treatment $T$, and outcome $Y$, where the true treatment effect is known. Use it to build intuition for how the two estimators behave:

- **Confounding strength** — increase it to make the treated and control groups less alike. Watch the propensity score distributions pull apart and the region of {ref}`overlap` shrink.
- **Matching caliper** $\delta$ — widen or tighten the maximum propensity gap allowed within a pair, and see how many treated units get matched versus discarded.
- **New sample** — redraw the data to see the sampling variability of each estimate.

The panels let you compare, on the same data, (1) propensity score overlap, (2) the matched pairs formed by PSM, and (3) the inverse-probability-weighted points used by IPTW. The summary cards contrast the naïve difference in means against the PSM estimate of the ATT ($\hat{\tau}_{ATT}$) and the IPTW estimate of the ATE ($\hat{\tau}_{ATE}$), both relative to the true effect.

```{raw} html
<iframe id="psm-iptw" src="../figure/psm_iptw_explainer.html?v=20260610d"
        style="width:100%; border:none; height:1500px;"
        title="PSM vs IPTW interactive explainer"></iframe>
<script>
(function () {
  var iframe = document.getElementById('psm-iptw');

  // Resolve the book's current theme: data-mode is auto|light|dark.
  function currentTheme() {
    var root = document.documentElement;
    // data-theme holds the *resolved* light|dark value (preferred).
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
    if (e.data.type === 'psm-iptw-height') {
      iframe.style.height = (e.data.height + 20) + 'px';
    } else if (e.data.type === 'psm-iptw-ready') {
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