# Tree-Based Methods

The methods in {doc}`propensity` and {doc}`regression_methods` are built to recover a *single* number — the ATE or ATT averaged over the population. Tree-based methods instead target the **conditional average treatment effect** (CATE) $\tau(x) = \mathbb{E}[Y(1) - Y(0) \mid X = x]$, asking *for whom* the treatment works rather than *whether* it works on average. They share the same identification backbone (unconfoundedness and {ref}`overlap`) but let the data, rather than a fixed functional form, discover which covariates drive effect heterogeneity. The tree ensembles underlying these estimators — CART, bagging, and random forests — are covered in the standard machine-learning textbooks of [Hastie, Tibshirani & Friedman (2009)](https://doi.org/10.1007/978-0-387-84858-7) and, at an introductory level, [James et al. (2021)](https://doi.org/10.1007/978-1-0716-1418-1); [Athey & Imbens (2019)](https://doi.org/10.1146/annurev-economics-080217-053433) survey how these methods are adapted for causal estimation.

Conceptually they sit at the intersection of the two earlier toolkits:

- **From propensity score methods.** {prf:ref}`alg-psm` matches treated and control units on the *scalar* propensity score $\hat{\pi}(x)$, while {prf:ref}`alg-psw` reweights them. A causal forest generalises both ideas: instead of matching on a hand-picked distance, it learns an **adaptive neighbourhood** directly in covariate space — two patients are "close" when the trees repeatedly place them in the same leaf. The resulting forest weights $\alpha^{(j)}(x)$ play the role of data-driven matching weights, and overlap remains the binding requirement (a leaf needs both treated and control members to yield a contrast).
- **From regression methods.** Like the doubly robust and orthogonal estimators ({prf:ref}`alg-aipw`, {prf:ref}`alg-dml`), causal trees and forests *residualise* the outcome and the treatment against out-of-bag nuisance predictions $\hat{Y}^{(-i)}$ and $\hat{\pi}^{(-i)}(x)$. This makes them doubly robust to misspecification and connects them directly to the R-learner of {prf:ref}`alg-rlearner` — a causal forest can be read as a locally-weighted, non-parametric R-learner.

The two algorithms below differ in granularity. A **causal tree** partitions the population into a handful of interpretable subgroups, assigning every member of a leaf the same effect estimate. A **causal forest** averages many such trees to deliver a smooth, individualised estimate $\hat{\tau}(x)$ for each patient.

## Causal Trees

(sec:ct)=
Our first approach to infer heterogeneous treatment effects is based on causal trees. In contrast to modelling the effect of the treatment on the potential outcome effect linearly, we rely on the idea of [Athey & Imbens (2016)](https://doi.org/10.1073/pnas.1510489113). {prf:ref}`alg-causaltree` shows their procedure according to which a causal tree estimates heterogeneous treatment effects from covariates $X$ and an observed outcome $Y$.

```{prf:algorithm} Causal Tree
:label: alg-causaltree
:class: dropdown

**Inputs** Covariates $X \in \mathcal{X}$, treatment $T \in \{0,1\}$, observed outcome $Y \in \mathcal{Y}$

**Outputs** Estimated CATE $\hat{\tau}^{(\ell)}(x)$

1. Subsample data and split into *construction* and *estimation* sets *(Honesty)*
2. While partition of construction data is still possible: *(Stopping criterion applies)*
	1. Create partition into two subpopulations maximizing heterogeneity
3. Map estimation data into determined tree leaves $\mathcal{L}$
4. For every leaf $\ell \in \mathcal{L}$:
	1. Estimate local CATE $\hat{\tau}^{(\ell)}(x)$ using estimation data
5. Return CATE $\hat{\tau}^{(\ell)}(x)$
```

Similar to CART [(Breiman et al., 1984)](https://doi.org/10.1201/9781315139470), a causal tree partitions the sample into subgroups. It creates a partition of the patient population into subpopulations (i.e., leaves $\ell\in\mathcal{L}$) using recursive binary splitting. In contrast to a decision tree, a causal tree estimates the treatment effect $\hat{\tau}$ directly by modelling the contrast in potential outcomes rather than modelling both potential outcomes and then taking their contrast. 

Since a covariate that affects the expected outcome $\mathbb{E}[Y \mid X = x]$ does not necessarily affect the treatment effect and vice versa, the splitting criterion is chosen with respect to covariates that actually cause treatment effect heterogeneity, as explained below.

For each split, the outcome-covariate pair is determined such that it maximizes the weighted difference $n_L\cdot n_R\cdot (\hat{\tau}_L-\hat{\tau}_R)^2$ where $n_L$ denotes the number of observations assigned to the left node and $n_R$ the number of observations that are assigned to right node. The first two factors, $n_L$ and $n_R$ make sure that the two sides are well balanced and the squared difference makes sure that the treatment effects between the two subpopulations are as heterogeneous as possible. A constant, hence homogeneous, treatment effect is assumed across all observations within the respective subpopulation aggregated in a leaf. Within each leaf, units act as if randomised: the CATE is the difference in mean outcomes. We denote $\mathbb{E}[Y^{(-i)} \mid X = x^{(i)}] = \hat{Y}^{(-i)}$:

\begin{align}
     \hat{\tau}_L\leftarrow lm\left((Y^{(i)}-\hat{Y}^{(-i)})\sim(T^{(i)}-\hat{\pi}^{(-i)}(x^{(i)})):x^{(i)}\in L\right) \\
     \hat{\tau}_R\leftarrow  lm\left((Y^{(i)}-\hat{Y}^{(-i)})\sim(T^{(i)}-\hat{\pi}^{(-i)}(x^{(i)})):x^{(i)}\in R\right)
\end{align}

The stopping criterion of further partitioning the population into subgroups is usually pre-specified by hyperparameters such as the minimum number of observations per leaf, a threshold for the weighted difference in the resulting treatment effects or a difference in sizes between the resulting nodes in terms of control and treatment group. If one of these minimum requirements is not met due to an additional split, the partitioning process is stopped and the algorithm intermediately returns the partition of $\mathcal{L}$. Given this partition, the estimation step is executed to get CATEs that basically are differences in outcomes for treatment and control observations. In every leaf $\ell$, there are both treated and untreated patients. Hence, the CATE is estimated as

\begin{equation}
    \hat{\tau}^{(\ell)}(x)=\frac{\sum_{\{i:T^{(i)}=0,\, x^{(i)}\in \ell\}}Y^{(i)}}{\left|\{i:T^{(i)}=0,\, x^{(i)}\in \ell\}\right|}-\frac{\sum_{\{i:T^{(i)}=1,\, x^{(i)}\in \ell\}}Y^{(i)}}{\left|\{i:T^{(i)}=1,\, x^{(i)}\in \ell\}\right|}
\end{equation}

```{figure} figs/causal_tree.svg
:width: 90%
:name: fig-causal-tree

Anatomy of a causal tree. Recursive binary splits on the covariates $X$ carve the population into leaves, with each split chosen to maximise the heterogeneity $n_L \cdot n_R \cdot (\hat{\tau}_L - \hat{\tau}_R)^2$ of the resulting effects — not to predict $Y$. Within a leaf the units behave as if randomised, so the CATE is simply the difference in mean outcomes between its treated and control members (an exact, equal-weight match inside the leaf). The leaves estimate visibly different effects ($\hat{\tau}^{(\ell)} \approx +6, +1, -2$), which is exactly the heterogeneity the splits are designed to expose.
```

The underlying assumptions are that in each leaf, the treatment effect is the same across all observations in the leaf and the leaves are small enough that the $(Y, T)$ pairs of each observation in a leaf behave as if they have come from a RCT: this requires that $T$ is randomly distributed across the observations in the leaf given the covariates and the outcome $Y$ is independent of the assigned treatment $T$.

To ensure unbiased estimates of CATEs, the principle of *honesty* is introduced for causal trees and causal forests [(Athey & Imbens, 2016)](https://doi.org/10.1073/pnas.1510489113). A method is called honest if the entire sample of patients is split into two parts, one for tree construction and one to estimate the treatment effects within the leaves. Hence, model selection is decoupled from model estimation. This addresses the post-selection inference problem and ensures unbiased estimates of CATEs.

The method is regarded doubly robust since we apply inverse propensity score weighting at every step $t$: We combine the outcome model and propensity score model to reduce the sensitivity to misspecifications. Even if only one of the two is well specified, the resulting CATE estimator is more robust. This is necessary in presence of observational data, where the treatment is not assigned randomly.

With a causal tree, we estimate heterogeneous treatment effects, differentiating by subgroups. We additionally introduce causal forests that ensure a stronger degree of personalization in treatment effect estimation using adaptive nearest neighborhood estimation.

## Causal Forests

(sec:cf)=
We additionally introduce causal forests that ensure a stronger degree of personalization in treatment effect estimation using adaptive nearest neighbourhood estimation. Similarly as for random forests [(Breiman, 2001)](https://doi.org/10.1023/A:1010933404324), the CATEs in this specific ensemble method of causal forests are estimated by a combination of the estimations of the weak learners, i.e. causal trees that are estimated $B$ times. In addition, principles such as random split selection and recursive binary splitting are the same here as for random forests [(Athey, Tibshirani & Wager, 2019)](https://doi.org/10.1214/18-AOS1709). However, the CATEs are not calculated as simple averages over $B$ causal trees but by a weighted average over the local patient neighbourhood.

```{prf:algorithm} Causal Forest
:label: alg-causalforest
:class: dropdown

**Inputs** Covariates $X \in \mathcal{X}$, treatment $T \in \{0,1\}$, observed outcome $Y \in \mathcal{Y}$

**Outputs** Estimated CATE $\hat{\tau}(x)$

1. For every tree $b = 1, \ldots, B$:
	1. Split data into *construction* and *estimation* sets *(For honesty)*
	2. While partition of construction data is possible: *(Maximize heterogeneity)*

		1. Create partition into two subpopulations

	3. Determine leaves $\mathcal{L}$ based on estimation data *(Stopping criterion applies)*
	4. For every leaf $\ell \in \mathcal{L}$:

		1. Estimate the CATE $\hat{\tau}^{(\ell,b)}(x)$ on estimation data

	5. Return CATE $\hat{\tau}^{(\ell,b)}(x)$
2. Calculate weights $\alpha^{(i)}(x)$ *(Forest proximity weights)*
3. Calculate final CATE $\hat{\tau}(x)$ *(Weighted average)*
4. Return CATE $\hat{\tau}(x)$
```

Fitting $B$ causal trees, we repeat the separation step into a construction data set and an estimation data set repeatedly for every causal tree. Hence, every single weak learner is fitted on different subsamples of the observational data set. This ensures *honesty* in the ensemble setting as well, when the individual causal trees are composed to a causal forest. Every causal tree again recursively builds a partition into binary splits of the entire patient population based on the construction set. Then, it estimates the CATEs in the leaves $\ell^{(b)}$ based on the estimation set. After $B$ causal trees have been built, the weights required to compose the weighted average of CATEs are calculated for every observation as

\begin{equation}
    \alpha^{(j)}(x)=\frac{1}{B}\sum_{b=1}^{B}\frac{\mathbb{1}\{X^{(j)}\in\ell^{(b)}(x)\}}{\left|\ell^{(b)}(x)\right|}.
\end{equation}

The weights indicate how often another patient $j\not = i$ with covariates $X^{(j)}$ falls in the same leaf as the patient of interest $i$ with covariates $x$ across the trees in the forest. The more often the patients are in the same leaf, the closer they are to each other and the higher is the weight of patient when estimating the treatment effect of the observation with given covariates and outcome.

The causal forest is hence not used to construct the final estimate of CATE as average over all single estimations but rather for adaptive neighbourhood matching of each individual observation. The actual CATE is then calculated locally as a weighted average over its nearest neighbours, i.e. similar patients [(Athey, Tibshirani & Wager, 2019)](https://doi.org/10.1214/18-AOS1709), as

\begin{equation}
    \hat{\tau}(x)=\frac{\sum_{j=1}^n \alpha^{(j)}(x)(Y^{(j)}-\hat{Y}^{(-j)})(T^{(j)}-\hat{\pi}^{(-j)}(x))}{ \sum \alpha^{(j)}(x)(T^{(j)}-\hat{\pi}^{(-j)}(x))^2}.
\end{equation}

```{figure} figs/causal_forest.svg
:width: 95%
:name: fig-causal-forest

How a causal forest builds an adaptive neighbourhood. Across the $B$ honest trees (left), the query patient $x$ repeatedly lands in a leaf alongside different sets of patients. Tallying how often each patient $j$ shares $x$'s leaf yields the forest weight $\alpha^{(j)}(x)$ (right): patient $j_1$, a leaf-mate in every tree, weighs most, whereas $j_4$ — never co-located — contributes nothing. The result is a *learned* local match in covariate space rather than a match on a single propensity score, with out-of-bag residuals making the final weighted estimate doubly robust.
```

To construct the neighbourhood for each single patient $i$, weights are calculated for every other patient $j\not = i$. Note that $\hat{Y}^{(-j)}$ and $\hat{\pi}^{(-j)}(x)$ are calculated out-of-bag, meaning that information about patient $j$ was not used for their estimation. We refer to [Wager & Athey (2018)](https://doi.org/10.1080/01621459.2017.1319839) for more details on the estimation procedure. To assign an observation to a leaf $\ell^{(b)}$ in iteration $b$, the set of covariates can vary across patients to determine the path, as causal forests share the property with random forests to randomly select the set of possible covariates at each split [(Breiman, 2001)](https://doi.org/10.1023/A:1010933404324). Amongst this set, the splitting covariate that maximizes heterogeneity in treatment effects amongst the subgroups, is chosen on a data-driven basis. This allows the path to vary per leaf $\ell$ and per iteration $b$.
