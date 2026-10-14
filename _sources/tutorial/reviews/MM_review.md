# Review: Actuarial Causal Inference Tutorial

 

Line numbers (`L12`) refer to the file at the commit above. Each item carries one tag:

 

| Tag | Meaning |

|---|---|

| **[Build]** | Broken cross-reference, missing label/file, or something that will produce a Sphinx warning / dead link. Mechanical, please fix. |

| **[Major]** | Statement that is wrong or misleading as written, or a structural inconsistency that will confuse readers. |

| **[Minor]** | Imprecise, incomplete, or missing citation; worth fixing but not wrong per se. |

| **[Nit]** | Typo, wording, style, duplication. |

| **[Verify]** | I could not confirm the claim/reference from the text alone; please check against the source. |

 

---

 

## 0. Overall assessment

 

This is a well-structured and unusually careful tutorial. Things that stand out positively and should be kept as they are:

 

- The four-stage organisation (concepts → identification → estimation → validation) is clear, and the hub pages (`identification.md`, `inference.md`, `sensitivity.md`) make navigation easy.

- The ATT-vs-ATE decomposition of the naive contrast (`concepts.md` L60–66, `debias.md` L33–41) is more precise than in most introductory texts.

- The three worked d-separation examples (`graphical_models.md` L186–282) are excellent teaching material, in particular Example 2 (mediator with unmeasured confounding) and the explicit "identifying independence" paragraphs.

- The sensitivity chapter is strong: fixed-denominator SMD (`diagnostics.md` L72–88), the amplification factor in the partial-$R^2$ bound with numeric under-statement figures, the two robustness values, and the Manski/MTR/MTS discussion are all correct and well motivated. The telematics pre-treatment placebo example (L149) is exactly the kind of actuarial grounding the rest of the tutorial would benefit from.

- The TMLE outcome-type warning, the PLM-DML "what does $\tau^*$ actually target" note, and the Neyman-orthogonality proof are valuable additions rarely found in tutorials.

- The interactive explainers are a real asset.

 

The main weaknesses, in order of importance:

 

1. A handful of **broken MyST references / a missing page** that will surface as build warnings or dead links (Section 1, C10).

2. Several **mathematically over-stated or incorrect sentences**, mostly in `heterogeneous_effects.md`, `instrumental_variables.md`, `bayesian.md` and `fairness.md` (flagged **[Major]** below).

3. **Inconsistent chapter descriptions and notation** across hub pages and chapters (C1–C3).

4. **Bibliography drift**: ~20 in-text citations have no entry in `papers/references.md`, several Shalizi chapter numbers are wrong, and a few DOIs look suspicious (C4, C8).

5. The chapter titled "Inference" contains **no frequentist uncertainty quantification** for any of the ATE/CATE estimators (C11).

 

---

 

## 0b. Reader's checklist — items to confirm during the manual read-through

 

These are the findings where a second pair of eyes matters most: either the claim in the text is substantively wrong/over-stated (**[Major]**), or I could not confirm a reference from the text alone (**[Verify]**). Tick them off while reading; the full reasoning is in the per-file sections below.

 

### Substantive claims to re-read critically ([Major])

 

- [ ] `graphical_models.md` **L128** — faithfulness counter-example: a bare chain $X\to M\to Y$ has one path; cancellation needs a direct edge $X\to Y$ as well. Confirm the sentence is wrong as written.

- [ ] `methods.md` **L14** — table says front-door *estimation* is in `direct_adjustment`; confirm no front-door estimator exists there.

- [ ] `inference.md` **L50** — RD listed as targeting the ATT; compare with `quasi_experimental.md` L37/L47 (effect at cutoff).

- [ ] `direct_adjustment.md` **L253** vs **L429–457** — "DML is essentially AIPW …" but the DML algorithm shown is the PLM/Robinson form; check the two passages are reconciled.

- [ ] `direct_adjustment.md` **L441–452** — is this cross-fitting (swap + average) or single sample-splitting? Is "Honesty" the right term here?

- [ ] `direct_adjustment.md` **L417–424** — TMLE note: is the logistic fluctuation really "invalid" for unbounded $Y$, or is rescale-to-$[0,1]$ the recommended default (Gruber & van der Laan 2010)?

- [ ] `heterogeneous_effects.md` **L45–71** — which causal tree is being defined: Athey–Imbens (difference-in-means splits, no nuisances) or GRF-style (residualised)? Read L53, L57–71, L84, L88–90 together.

- [ ] `heterogeneous_effects.md` **L120** — "$\hat\tau-\tau=O_p(\|\Delta_m\|\,\|\Delta_\pi\|)$": is this the total error or only the nuisance-induced bias?

- [ ] `heterogeneous_effects.md` **L123** — "the CATE estimator stays $\sqrt n$-consistent": does this hold for a nonparametric $\tau(x)$ from a forest?

- [ ] `heterogeneous_effects.md` **L141–151** — forest algorithm computes per-leaf CATEs (Steps 1.4–1.5) that the final estimator (L166–168) never uses; is subsampling missing?

- [ ] `instrumental_variables.md` **L19–23** — LATE claimed for compliers without stating **monotonicity** anywhere in the chapter.

- [ ] `instrumental_variables.md` **L49** — "bivariate 2SLS valid only if no observed covariate affects $Y$": is that the right condition, or is it "instrument only conditionally exogenous"?

- [ ] `instrumental_variables.md` **L53** — SE argument: $\hat\varepsilon=u+\hat\beta(T-\hat T)$; is the cross-term $2\beta\,\mathbb{E}[u(T-\hat T)]$ zero under endogeneity? Does "too large" follow?

- [ ] `quasi_experimental.md` **L9** — Goodman-Bacon "motivates the heterogeneity-robust estimators in `heterogeneous_effects`": are meta-learners/forests the intended target, or Callaway & Sant'Anna / Sun & Abraham?

- [ ] `bayesian.md` **L13** — can Bayes factors select among competing *causal* models (Markov-equivalent DAGs, exchangeability)?

- [ ] `bayesian.md` **L52–66** — Bayesian propensity score: is the feedback / "PS not in the likelihood" issue (Robins & Ritov 1997; Zigler et al. 2013) acknowledged?

- [ ] `bayesian.md` **L107–121** — regularisation-induced confounding: is it addressed by the separate $\tau$ ensemble (as the text says) or by including $\hat\pi(x)$ in $\mu$ (as Hahn, Murray & Carvalho 2020 say)?

- [ ] `fairness.md` **L48–50** — is $P(Y\le y\mid X,S)=P(Y\le y\mid X)$ the Lindholm et al. *definition* of the discrimination-free price, or is the definition $\mu^*(x)=\int\mu(x,s)\,\mathrm dP(s)$ (as derived at L78–80)?

- [ ] `direct_adjustment.md` **L358** — does the orthogonality proof actually need exchangeability at this step, or is $\mathbb{E}[TY\mid X]=\pi(X)\mu(1,X)$ definitional?

- [ ] `assumptions.md` **L114–124** — does the identification derivation need positivity to be well defined?

- [ ] Whole "Inference" chapter — is any frequentist standard error / confidence interval given for G-computation, PSM, IPW, AIPW, TMLE, DML, meta-learners, causal forests? (C11)

 

### References and section numbers to verify against the source ([Verify])

 

- [ ] Shalizi (2025) chapter/section numbers everywhere (C4): `graphical_models.md` L3, L20, L47, L117, L153, L183; `methods.md` L27, L83, L152, L163, L170, L203; `instrumental_variables.md` L17 ("Ch. 23"); `bayesian.md` L5 ("Ch. 21"). Current TOC: 18 Graphical Models · 19 Graphical Causal Models · 20 Identifying Causal Effects · 21 Estimating Causal Effects · 22 Discovering Causal Structure · 23 Time Series.

- [ ] `concepts.md` L32 — Richardson & Robins (2014), DOI 10.1214/14-STS485: is this the intended SCM/PO-equivalence reference?

- [ ] `concepts.md` L56, L60 and elsewhere — Wooldridge (2012), DOI 10.1016/C2011-0-05506-1 (Elsevier DOI for a Cengage textbook?).

- [ ] `direct_adjustment.md` L465 — Chernozhukov et al. (2018) "Sec. 2 vs. 4": PLR is Sec. 4 and IRM Sec. 5 in the *Econometrics Journal* version?

- [ ] `diagnostics.md` L279 — Cinelli & Hazlett (2020) "Sec. 4.3" for robustness values (4.2?).

- [ ] `debias.md` L112 — Pearl (2009) "Cor. 3.3.4": front-door adjustment is Theorem 3.3.4?

- [ ] `fairness.md` L70, L78 — Lindholm et al. "Section 3" / "Proposition 15": numbering in the published ASTIN Bulletin 52(1) version vs arXiv?

- [ ] `fairness.md` L31, L48, L70, L162 — year 2021 vs published 2022 (DOI 10.1017/asb.2021.23); `references.md` lists a *different* Lindholm et al. 2022.

- [ ] `instrumental_variables.md` L53 — Wooldridge (2010) "p. 96" for the manual-2SLS SE remark.

- [ ] `_toc.yml` L10 — does `maxdepth: 1` hide the nested `sections:` in the sidebar?

 

### Notebooks — items to confirm (see Section 20)

 

- [ ] `observational_data.ipynb` cell 6 — the sub-type bonus (+1.5 for half the treated) is added to the *main* outcome `Y`, so the true pooled ATE is 5.75, not the `ATE = 5.0` quoted throughout (cells 4, 11, 23). Is the "bias from $U$" therefore overstated?

- [ ] `observational_data.ipynb` cells 17, 19, 21 — positivity plots use the *true* propensity, and the adjustment set switches between `{X1,X2}` and `{X1..X5}`; is the residual imbalance in cell 21 due to extreme weights (as claimed) or to omitting X3–X5 from the propensity model?

- [ ] `utils.py` `calculate_smd_weighted` — weighted variances in the denominator, contradicting `diagnostics.md` L72–88 (fixed unweighted denominator).

- [ ] `utils.py` `rosenbaum_sensitivity` — sign test, whereas the notebook text (cell 27 comment) and tutorial speak of the signed-rank statistic.

- [ ] `claims_triage.ipynb` cells 11–12 — `LinearDML(X=None)` is the PLM; under the deliberately heterogeneous effect it targets the overlap-weighted $\tau^*$ (see `direct_adjustment.md` L459–466), yet is labelled "debiased ATE" and compared to the true ATE and to the causal-forest mean CATE.

- [ ] `claims_triage.ipynb` cells 14, 19 — estimated CATEs are graded against `tau_true`, which contains the idiosyncratic lognormal factor (an ITE), not the CATE $\mathbb{E}[\tau\mid x]$.

- [ ] `claims_triage.ipynb` cell 27 — "none of our observed features explains anywhere near 12% …" is asserted, not computed; severity likely exceeds it for cost.

- [ ] `health_interventions.ipynb` — is this notebook meant to be published? Exclusion restriction violated by construction (cell 5: `itt` directly multiplies mortality by 0.75) yet `itt` is used as an instrument (cell 21); sign conventions flip between "naive" and estimator outputs (cells 17–23); no ground truth for `df_synthetic`; every output printed twice; no narrative.

 

### Quick visual checks when browsing the built book

 

- [ ] `assumptions.md` L52 — does the `{ref}`debias`` link render, or show as unresolved?

- [ ] `direct_adjustment.md` L90 — does `{cite:t}`austin2011`` render as literal text?

- [ ] `fairness.md` L93 — does the link to `application/pricing` 404? Is the fairness price explainer shown anywhere?

- [ ] `fairness.md` — does the page have a title in the sidebar (no H1 in source)?

- [ ] `diagnostics.md` L281 — does "top of this section" jump to the interactive map?

- [ ] Sidebar — are `application/case_study`, `motivation`, `confounding`, `sensitivity_analysis`, `susceptible_subpopulation` reachable / intended?

 

---

 

## 1. Cross-cutting issues

 

**C1 — `{doc}`sensitivity`` is cited as the place where sensitivity tools "are developed", but that page is a 15-line hub.** The tools live in `diagnostics.md`. Affected: `README.md` L42; `concepts.md` L121 (cites both); `identification.md` L20; `assumptions.md` L110; `methods.md` L219; `debias.md` L96, L120. Point to `diagnostics` (or make `sensitivity.md` carry real content, see `sensitivity.md` below). **[Minor]**

 

**C2 — Chapter descriptions do not match chapter contents.**

- `README.md` L26 says `graphical_models` covers "backdoor and frontdoor criteria, causal discovery"; `identification.md` L13 says the same. In fact the Backdoor Criterion, Frontdoor Criterion and Causal Discovery (SGS/PC) all live in `methods.md` (L29–211). `graphical_models.md` only *references* `backdoor-criterion` forward (L207, L273).

- `methods.md` L27 ("The following criteria provide graphical answers …") is a dangling sentence that clearly used to introduce the criteria inside the graphical-models chapter.

- Suggest either moving the two criteria (and possibly Causal Discovery) back into `graphical_models.md` — they are graphical results, not "strategies" — leaving `methods.md` with the three strategies + estimands, or fixing all descriptions. **[Major]**

 

**C3 — Notation is not consistent, and the notation table is incomplete.**

- Instrument: $Z$ in `inference.md` L31–33 and `methods.md` L215; $I$ in `graphical_models.md` L247ff, `instrumental_variables.md` throughout, `quasi_experimental.md` L40. $Z$ also denotes the adjustment set in the Backdoor Criterion (`methods.md` L33–43) and confounders $Z_1,Z_2,Z_3$ in Example 3. Pick $I$ for the instrument (it is what the figure uses) and add it to the notation table in `concepts.md` L127–139.

- Collider: $C$ in the table (L134) but $K$ in Example 3 (`graphical_models.md` L249).

- Outcome model: $\mu(X)=\mathbb{E}[Y\mid T,X]$ in the figure caption `direct_adjustment.md` L11, $\mu(t,x)=\mathbb{E}[Y\mid T=t,X=x]$ in G-computation/AIPW (L16, L253ff), but $\hat\mu(X)=\mathcal{L}_Y(Y\sim X)=\mathbb{E}[Y\mid X]$ in the DML algorithm (L441ff) and R-learner (`heterogeneous_effects.md` L35). `heterogeneous_effects.md` L105 then introduces $m(x)$ for $\mathbb{E}[Y\mid X]$. Use $\mu(t,x)$ for the outcome model and $m(x)$ for the marginal regression everywhere, and add both to the table.

- $D$ appears twice in the notation table (L125 definition and row L138). **[Minor]**

 

**C4 — Shalizi (2025) chapter numbers.** I checked the current ADAfaEPoV table of contents (text dated 8 Feb 2025): Ch. 18 Graphical Models, 19 Graphical Causal Models, 20 Identifying Causal Effects, 21 Estimating Causal Effects, 22 Discovering Causal Structure, 23 Time Series. Hence:

- `methods.md` L27 and L83 cite "Section 21.1–21.2" / "Section 21.1" for the back-/front-door criteria → these are in **Ch. 20**.

- `instrumental_variables.md` L17 cites "Ch. 23" for IV → Ch. 23 is Time Series; IV is in **Ch. 20**.

- `bayesian.md` L5 cites "Shalizi (2025, Ch. 21)" for Bayesian causal inference → Ch. 21 is frequentist estimation; Shalizi has no Bayesian causal chapter. Remove or replace (e.g. Rubin 1978; Imbens & Rubin 2015 Ch. 8; Li, Ding & Mealli 2023, *JRSS-A*, "Bayesian causal inference: a critical review").

- Because the draft is revised continuously, state the version date in `references.md` ("draft of 8 February 2025") and re-check all §-numbers (`graphical_models.md` L3, L20, L47, L117, L153, L183; `methods.md` L152, L163, L170, L203). **[Verify]**

 

**C5 — US/UK spelling is mixed** ("randomized"/"randomised", "destabilize"/"minimises", "personalization"/"modelling", "categorize"). British spelling dominates; make it uniform. **[Nit]**

 

**C6 — "patients" in an actuarial tutorial.** `heterogeneous_effects.md` uses "patient(s)" 17 times (L45, L73, L86, L101, L157, L163, L165, L175, L178) and `concepts.md` L129 says "patient/policyholder". Replace with "unit"/"policyholder". **[Nit]**

 

**C7 — Verbatim or near-verbatim duplication.** Propensity-score definition (`concepts.md` L44–49 and `direct_adjustment.md` L35–43); the "conditionally randomized experiment" paragraph (`concepts.md` L87 ≡ `assumptions.md` L5–7); LATE definition (`inference.md` L31–35 and `quasi_experimental.md` L37–47); the causal-forest introduction (`heterogeneous_effects.md` L125 ≡ L130); IPW singly-robust statement (`direct_adjustment.md` L90 and `debias.md` L104). Keep one instance and cross-reference. **[Nit]**

 

**C8 — Bibliography drift.** The following in-text citations have **no entry** in `papers/references.md`: Austin 2009; Bowden, Davey Smith & Burgess 2015; Cole & Frangakis 2009; Davey Smith & Ebrahim 2003; Greenland & Robins 1986 and 2009; Hernán, Hernández-Díaz & Robins 2004; Kang & Schafer 2007; Katan 1986; Lindholm et al. 2021 (ASTIN); Lipsitch, Tchetgen & Cohen 2010; Lunceford & Davidian 2004; Neal 2020 (in "Useful Links" only); Richardson & Robins 2014; Rosenbaum 2002; Rubin 1980; Schmidt 2018; VanderWeele 2009; Wooldridge 2012; Wooldridge 2010; Pearl 2001; VanderWeele 2015; Spirtes, Glymour & Scheines 1993; Li, Morgan & Zaslavsky 2018. Conversely Athey & Wager (2019) is listed but never cited. Several citations are plain text without a link (Pearl 2001, VanderWeele 2015 in `debias.md` L112; SGS 1993 in `methods.md` L167; Wooldridge 2010 in `instrumental_variables.md` L53). **[Minor]**

 

**C9 — Blog-grade sources in an SAV publication.** `uniqcret.com/post/causal-inference-assumptions-guide` (`concepts.md` L105, `assumptions.md` L21, `references.md` Useful Links) and `biostatistics.ca` (`concepts.md` L60) are personal blogs. Replace with Hernán & Robins (2020, Chs. 2–3) or Imbens & Rubin (2015, Ch. 12), or at least move them to "Useful Links". **[Minor]**

 

**C10 — Build / link breakages (all verified by grep against the source tree).**

| Location | Problem | Fix |

|---|---|---|

| `assumptions.md` L52 | `{ref}`debias`` — there is no label `(debias)=` anywhere | use `{doc}`debias`` |

| `direct_adjustment.md` L90 | `{cite:t}`austin2011`` — no `.bib` file and no `sphinxcontrib.bibtex` in `_config.yml`; renders as an unresolved role | replace with the inline-link style used everywhere else |

| `fairness.md` L93 | `{doc}`../application/pricing`` — `application/pricing.ipynb` does not exist | create it or remove the sentence; note `figure/fairness_price_explainer.html` exists but is embedded nowhere — presumably meant for this page |

| `diagnostics.md` L281 | `[top of this section](#interactive-how-much-confounding-would-it-take)` — the heading at L15 is "Partial $R^2$: how much confounding would it take?", so the generated anchor will not match | add an explicit label `(interactive-sensitivity)=` above L15 and use `{ref}` |

| `fairness.md` L2 | page has no `#` H1 title; starts at `##` | add `# Fairness and Discrimination-Free Pricing` (or similar) |

| `heterogeneous_effects.md` L52, L129 | `(sec:ct)=` / `(sec:cf)=` placed *after* the headings — they label the following paragraph, not the section — and are never referenced | move above the `##` line or delete |

| `_toc.yml` L36, L39 | commented-out `application/case_study.ipynb` and `application/traffic_study.ipynb` (the latter does not exist); five notebooks in `application/` (`case_study`, `confounding`, `motivation`, `sensitivity_analysis`, `susceptible_subpopulation`) are not in the TOC and will trigger "document isn't included in any toctree" warnings | include or move out of the source tree / add to `exclude_patterns` |

| `tutorial/figs/` | unused assets: `actuary_workflow.svg`, `fairness_dag.svg`, `rosenbaum_bounds.svg`, `effect_comparison.png`, `iptw_weights.png`, `love_plot.png`, `ps_overlap.png`, `psm_vs_iptw_concept.png`, `generate_propensity_figures.py` | delete or use (see `sensitivity.md` below re `actuary_workflow.svg`) |

 

**C11 — No uncertainty quantification for the frequentist estimators.** The chapter is called "Causal Inference" but G-computation, PSM, IPW, AIPW, TMLE, DML, meta-learners and causal forests are all presented as point-estimate algorithms. A short subsection (or a note per algorithm) on standard errors would close an important gap for actuaries who must report confidence intervals: influence-function SE for AIPW/DML ($\widehat{\mathrm{se}} = \mathrm{sd}(\hat\psi_i)/\sqrt n$, which the Neyman-orthogonality section already sets up), the bootstrap and its failure for nearest-neighbour matching (Abadie & Imbens 2008, *Econometrica*), and the GRF variance estimate for causal forests. **[Major]**

 

---

 

## 2. `README.md`

 

- **L10** [Nit] "destabilize", "categorize" (US) vs "minimises", "realised" elsewhere (C5).

- **L24–27** [Major] Chapter descriptions mismatch; see C2.

- **L42** [Minor] "The actuary's end-to-end workflow …" — there is no such workflow section or figure anywhere in the tutorial (`fairness.md` ends with a normative takeaway; `actuary_workflow.svg` is unused). Either add it (natural home: `sensitivity.md`) or drop the sentence. Same issue in `sensitivity.md` L15.

- **L5** [Nit] Two applications are named (health programme, claims routing), but the TOC ships three notebooks (`observational_data`, `claims_triage`, `health_interventions`). Mention all three or explain the matrix.

- **L45–91** [Nit] Fine. The `postMessage(..., '*')` wildcard origin is acceptable for a static site but could be tightened to `location.origin`.

 

## 3. `tutorial/concepts.md`

 

- **L20** [Nit] The Neyman (1923) DOI points to the 1990 *Statistical Science* translation; write "Neyman (1923; transl. 1990)" as in `references.md`.

- **L32** [Verify] "Richardson & Robins, 2014, DOI 10.1214/14-STS485" — please confirm this DOI is the intended reference for SCM/potential-outcome equivalence (their SWIG paper is a 2013 UW CSSS working paper).

- **L56, L60** [Verify] "Wooldridge, 2012, DOI 10.1016/C2011-0-05506-1" — this is an Elsevier book DOI; Wooldridge's *Introductory Econometrics* is published by Cengage. Check the DOI resolves to the intended book.

- **L60** [Minor] Blog link (C9).

- **L87** [Nit] The term "Rubin Causal Model" was coined by Holland (1986), not Rosenbaum & Rubin (1983). Cite Holland, P. W. (1986), "Statistics and Causal Inference", *JASA* 81(396), 945–960, DOI 10.1080/01621459.1986.10478354 — currently absent from the bibliography.

- **L87** [Nit] Paragraph duplicated verbatim in `assumptions.md` L5–7 (C7).

- **L90** [Minor] "This fundamental identification problem was formalised by Rubin (1974)" — the phrase *Fundamental Problem of Causal Inference* and its formalisation are due to Holland (1986). Cite Holland here.

- **L105** [Minor] Blog link (C9). Also the sentence is very long; split after "at the conditional level".

- **L107** [Nit] A paragraph of heterogeneous-treatment-effect references (incl. "Schmidt (2018)", arXiv 1810.13237, not in bibliography) sits under "Identifiability" with no connection to the text. Move to `heterogeneous_effects.md` or delete.

- **L121** [Minor] Points to `diagnostics` **and** `sensitivity` — see C1.

- **L129** [Nit] "patient/policyholder" (C6).

- **L127–139** [Minor] Notation table gaps (C3): no instrument, no $\mu(t,x)$ / $m(x)$, no $\tau$, no ATE/ATT/CATE/LATE abbreviations; $D$ defined twice.

- General [Nit] The section also defines the propensity score (L44–49) which is redefined in `direct_adjustment.md` L35–43 (C7).

 

## 4. `tutorial/identification.md`

 

- **L13, L17** [Major] Descriptions of `graphical_models` and `methods` do not match content (C2).

- **L13–20** [Nit] This file uses em-dashes "—" while every other file uses spaced hyphens " - ". Harmonise.

- **L20** [Minor] Warning box ends "developed in `sensitivity`" → `diagnostics` (C1). Otherwise an excellent paragraph.

 

## 5. `tutorial/assumptions.md`

 

- **L5–7** [Nit] Duplicate of `concepts.md` L87 (C7).

- **L10–21** [Nit] The "Potential Outcomes Framework" is a single sentence broken into two bullets and a continuation paragraph ("- Rubin (1974) extended …", "- Specifically, when …", then "then conditioning on $X$ …"). Rewrite as prose.

- **L21** [Minor] Blog link (C9).

- **L35** [Minor] The consistency "Detecting violations" paragraph ends with a sentence about **interference** ("Interference violations are harder to detect …"). Interference belongs to SUTVA and is covered again at L49. Move/delete.

- **L37** [Minor] Rubin 1980, Cole & Frangakis 2009, VanderWeele 2009 not in bibliography (C8).

- **L47** [Nit] Good paragraph, but very long; consider splitting the i.i.d.-vs-no-interference discussion into the note.

- **L52** [Build] `{ref}`debias`` → `{doc}`debias`` (C10).

- **L71** [Nit] `{ref}`overlap`` resolves correctly. ✓

- **L88** [Minor] Greenland & Robins 1986 and 2009 not in bibliography.

- **L103** [Nit] "In case of violation, exchangeability often produces severe bias, which is a separate dimension from the probability that it is violated" — grammatically the subject is wrong. Suggest: "The *magnitude* of bias that a violation of exchangeability would cause is a separate dimension from the *probability* that it is violated; a mild but plausible violation and a severe but implausible one warrant very different responses."

- **L110** [Minor] "developed in `sensitivity` and `diagnostics`" (C1).

- **L114–124** [Minor] The identification derivation should also invoke **positivity**: $\mathbb{E}[Y\mid X=x,T=t]$ is only defined where $P(T=t\mid X=x)>0$. Add a "pos." step or a sentence. Also worth noting, given the nice nested-exchangeability note at L84–98, that only *mean* exchangeability is used here.

 

## 6. `tutorial/graphical_models.md`

 

- **L3** [Verify] Shalizi chapter/section numbers (C4).

- **L128** [Major] The faithfulness counter-example is wrong as stated: "in a linear chain $X\to M\to Y$ whose direct and indirect contributions cancel exactly" — a chain has a *single* path, so nothing can cancel. Cancellation needs two paths, e.g. $X\to M\to Y$ **and** $X\to Y$ with $\beta_{XY} = -\beta_{XM}\beta_{MY}$. Rewrite: "e.g. in a linear model with $X\to M\to Y$ and a direct edge $X\to Y$ whose direct and indirect effects cancel exactly, $X$ and $Y$ are marginally independent despite being $d$-connected."

- **L131–154** [Nit] Blocked-path condition 1 says "chain or fork on $p$"; the standard phrasing is "non-collider on $p$" (covers both). Optional.

- **L173** [Nit] Fine. Note that "local Markov ⇔ global Markov (d-separation)" is a theorem (Verma & Pearl 1988); a citation would help since the box says "Equivalently".

- **L236** [Minor] "(see `debias`)" for the mediation formula — `debias.md` L112 discusses NDE/CDE but never states the mediation formula. Either add it there or cite Pearl (2001) / VanderWeele (2015) directly.

- **L273, L281** [Minor] "adjusting for the instrument $I$ … can *amplify* bias" — correct (Z-bias) but uncited. Cite Pearl (2010) "On a class of bias-amplifying variables that endanger effect estimates", UAI, and/or Ding, VanderWeele & Robins (2017), *Biometrika* 104(2), 291–302.

- **L249** [Nit] Collider is $K$ here vs $C$ in the notation table (C3).

 

## 7. `tutorial/methods.md`

 

- **L1** [Nit] File is `methods.md`, title "Identification Strategies"; README calls it "methods". Consider renaming the file to `strategies.md` for consistency (optional).

- **L14** [Major] The "Strategies at a glance" table says front-door adjustment is estimated in `direct_adjustment` — but that chapter contains **no** front-door estimator. Either add a short plug-in front-door estimator (two regressions + the formula at L101) or change the cell to "not covered; see Pearl (2009) §3.3.2 / Fulcher et al. 2020".

- **L27** [Nit] Dangling sentence "The following criteria provide graphical answers" (C2).

- **L27, L83** [Verify] Shalizi "Section 21.1–21.2" → Ch. 20 (C4).

- **L59** [Nit] "paths of the form $T\leftarrow\cdots\leftarrow Y$ or $T\leftarrow\cdots\rightarrow Y$" — a backdoor path is *any* path starting with an arrow into $T$; the interior can contain colliders. Simplify to "any path between $T$ and $Y$ whose first edge points into $T$".

- **L157–163** [Minor] Markov equivalence: cite Verma & Pearl (1990), "Equivalence and synthesis of causal models", UAI.

- **L167** [Minor] "Spirtes, Glymour & Scheines, 1993" is unlinked and not in the bibliography (*Causation, Prediction, and Search*, Springer/MIT Press; 2nd ed. 2000).

- **L213–217** [Minor] Instrument denoted $Z$ (C3).

- **L219** [Minor] "`sensitivity`" → `diagnostics` (C1).

- General [Nit] The Causal Discovery section (L150–211) is a detour in a chapter on identification *strategies*; consider moving it to `graphical_models.md` (which the README already claims covers it).

 

## 8. `tutorial/inference.md`

 

- **L1** [Minor] Title "Causal Inference" for a chapter about **estimation** is confusing in a book whose subject is causal inference. Suggest "Estimation of Causal Effects" (and "Stage 3 – Estimation" in the README).

- **L31–35** [Minor] LATE uses $Z$ for the instrument (C3); and LATE requires **monotonicity** (no defiers), which is nowhere stated in the tutorial — add "under monotonicity, $T(Z{=}1)\ge T(Z{=}0)$" here or in `instrumental_variables.md`.

- **L50** [Major] "Quasi-Experimental (DiD, RD, SC) → ATT": RD does **not** target the ATT; it identifies the effect at the cutoff $\mathbb{E}[Y(1)-Y(0)\mid X=c]$ (correctly stated in `quasi_experimental.md` L37 and L47). Split the row or write "ATT (DiD, SC) / effect at cutoff (RD)".

- **L51** [Minor] "Bayesian (BART/BCF) → CATE": BART is equally used for the ATE; write "ATE, CATE".

- **L43–51** [Minor] Add a "Uncertainty" column or a sentence pointing to where SEs come from (C11).

 

## 9. `tutorial/direct_adjustment.md`

 

- **L11** [Nit] Caption uses $\mu(X)=\mathbb{E}[Y\mid T,X]$ — inconsistent with $\mu(t,x)$ used from L16 onward (C3).

- **L35–43** [Nit] Duplicate propensity definition (C7).

- **L46** [Nit] "the empirical counterpart of the {prf:ref}`positivity`:" — sphinx-proof renders this as "of the Assumption 3", which reads oddly. Write "of the positivity assumption ({prf:ref}`positivity`)".

- **L55** [Minor] "Overlap weighting" appears here without citation (it is cited in `debias.md` L104 — Li, Morgan & Zaslavsky 2018). Add the citation here too, and add it to the bibliography.

- **L90** [Build] `{cite:t}`austin2011`` (C10).

- **L90** [Minor] "IPW is singly robust — consistent **if and only if** $\hat\pi(x)$ is correct" — "only if" is the defensible direction; a misspecified $\hat\pi$ that still balances the relevant covariates can be consistent. Write "consistent only if …".

- **L118** [Minor] "recovers the true (factual) mean $\mathbb{E}[Y(1)]$" — $\mathbb{E}[Y(1)]$ is a mean *potential* outcome, not a factual mean. Also the proof divides by $\pi(X)$ and therefore needs **positivity**; state it next to consistency and exchangeability.

- **L169** [Nit] "the true ATT exceeds the true ATE" holds for $\beta>0$ in the SEM below; add "(for positive $\beta$)" if the slider allows negative values.

- **L253** [Minor] "DML (next section) is essentially AIPW equipped with Neyman-orthogonality and cross-fitting" — the AIPW score *is already* Neyman-orthogonal (the chapter proves it at L272–392). What DML adds is cross-fitting plus the rate conditions ($o_p(n^{-1/4})$) that let ML nuisance estimators be plugged in; and the DML algorithm actually presented (L429–457) is the **PLM/Robinson** version, not AIPW. Rephrase: "DML in its *interactive-model* form is AIPW with cross-fitted ML nuisances; the *partially-linear* form presented below is Robinson's residual-on-residual estimator."

- **L253** [Nit] "Bang & Robins (2005) developed the framework for causal inference" — double robustness was first noted by Scharfstein, Rotnitzky & Robins (1999); Bang & Robins (2005) popularised it for causal models. Consider "extended … to causal inference".

- **L358** [Minor] "Under exchangeability, $\mathbb{E}[TY\mid X]=\pi(X)\mu(1,X)$" — this identity is purely algebraic once $\mu(1,x):=\mathbb{E}[Y\mid T=1,X=x]$ (the *observational* regression), so exchangeability is not needed for the orthogonality proof at all. Say "by definition of $\mu$".

- **L388** [Nit] "$\mathrm{Bias}(\hat\tau)\propto(\hat\mu-\mu)(\hat\pi-\pi)$" is informal; state "the second-order remainder is bounded by $\|\hat\mu-\mu\|_2\,\|\hat\pi-\pi\|_2$".

- **L417–424** [Minor] The TMLE note over-states: (i) the logistic fluctuation is not "invalid" for unbounded $Y$ — the *recommended* practice (Gruber & van der Laan 2010) is to rescale $Y$ to $[0,1]$ and keep the logistic fluctuation, precisely because the linear/identity fluctuation can produce out-of-range predictions and is less stable; (ii) "a count-appropriate family for frequencies" is not a standard TMLE recipe — drop or cite. Suggest reordering: rescale-and-logistic as the default, identity-link as the alternative, plus a caveat that heavy-tailed claim severities make any fluctuation step fragile (consider log-transform or bounded transforms).

- **L441** [Minor] "Split data … *(Cross-fitting/Honesty)*" — *honesty* is the Athey–Imbens term for causal trees, not DML terminology; and the algorithm as written is *sample splitting*, not *cross-fitting*: cross-fitting swaps the roles of $D_{\text{train}}$ and $D_{\text{eval}}$ (or uses $K$ folds) and **averages** the resulting $\hat\tau$'s, recovering full efficiency. Add the swap/average step (also because `heterogeneous_effects.md` L35 says "as in `alg-dml`").

- **L452** [Nit] Step 4.1 should be "no-intercept OLS of $\tilde Y$ on $\tilde T$".

- **L465** [Verify] "Chernozhukov et al., 2018, Sec. 2 vs. 4" — in the *Econometrics Journal* version the PLR model is Section 4 and the interactive regression model (ATE/ATTE) is Section 5. Check.

- **L465** [Nit] "$\tau^*$ equals the ATE only when effects are homogeneous or $\pi(X)$ is constant" — also when $\tau(X)$ is uncorrelated with $\pi(X)(1-\pi(X))$; write "in particular when …".

- General [Major] No standard errors for any estimator (C11).

 

## 10. `tutorial/heterogeneous_effects.md`

 

- **L21** [Minor] "X-learner *(cross fitting on imputed effects)*" — the "X" stands for *crossing* the imputed effects, not for cross-fitting (which is a different concept used two algorithms later). Rename the parenthetical.

- **L45** [Nit] "two patients" (C6).

- **L45–48** [Major] The bullets claim that "causal trees and forests *residualise* the outcome and the treatment" — but the original Athey & Imbens (2016) causal tree does **not** (as L84 itself concedes). The algorithm `alg-causaltree` (L57–71) is therefore a hybrid: Step 1 pre-computes cross-fitted nuisances "needed by the residualised split criterion", yet L53 says it "shows their [Athey & Imbens'] procedure", and the leaf estimator at L88–90 is a plain difference in means. Please choose one presentation: (a) the original honest causal tree (difference-in-means splits, no nuisances) followed by "GRF generalises this with local centering", or (b) an explicitly labelled "GRF-style honest causal tree". As written the reader cannot tell which algorithm is being defined.

- **L53** [Nit] "In contrast to modelling the effect of the treatment on the potential outcome effect linearly" — garbled; suggest "Rather than imposing a parametric form on $\tau(x)$".

- **L64** [Nit] "Subsample data and split into construction and estimation sets" — fine, but the forest algorithm (L141) omits the subsampling step; add it there.

- **L77** [Nit] "the outcome-covariate pair is determined" → "the (covariate, split-point) pair".

- **L77** [Minor] "We denote $\mathbb{E}[Y^{(-i)}\mid X=x^{(i)}]=\hat Y^{(-i)}$" is not well-formed (an expectation of a leave-one-out quantity equated to an estimate). Use the definition already given in Step 1: $\hat Y^{(-i)}=\hat m^{(-i)}(x^{(i)})$.

- **L84** [Nit] "leave-one-out nuisances" vs "K-fold out-of-fold prediction" (L63) — different things; use "cross-fitted" consistently.

- **L86** [Nit] "the algorithm intermediately returns" → "the algorithm returns the current partition".

- **L101** [Minor] "ensures unbiased estimates of CATEs" — honesty removes the *adaptive-selection* bias and yields valid asymptotic inference; the leaf estimates are still subject to sampling variability and to confounding if the leaf is not "as good as random". Soften to "removes the bias induced by selecting the splits on the same data".

- **L120** [Major] "$\hat\tau-\tau=O_p(\|\Delta_m\|_2\|\Delta_\pi\|_2)$" is not correct as an equality: the total error also contains the $O_p(n^{-1/2})$ (or slower, for CATE) sampling term. What is second-order is the *nuisance-induced bias*. Write "the nuisance-induced bias is $O_p(\|\Delta_m\|_2\|\Delta_\pi\|_2)$".

- **L123** [Major] "so the CATE estimator stays $\sqrt n$-consistent and asymptotically normal" — a *nonparametric* CATE $\tau(x)$ estimated by a forest is **not** $\sqrt n$-consistent; its rate is slower (GRF gives asymptotic normality at a rate $\sigma_n(x)\gg n^{-1/2}$). $\sqrt n$ applies to the *parametric* target in the PLM (Robinson) or to averages of the CATE. Rephrase accordingly and cite Wager & Athey (2018, Thm. 3.1) / Athey, Tibshirani & Wager (2019).

- **L125 and L130** [Nit] Paragraph duplicated verbatim (C7).

- **L130** [Nit] "weak learners" — random-forest trees are not weak learners in the boosting sense; write "base learners".

- **L141** [Minor] Forest algorithm: Step 1.1 should read "Draw a subsample; split it into construction and estimation sets"; Steps 1.4–1.5 (per-leaf CATE $\hat\tau^{(\ell,b)}$) are computed but never used, since the final estimate (L166–168) uses only the leaf *memberships* via $\alpha^{(j)}(x)$. Remove them or add "(used only for diagnostics)".

- **L159–161** [Nit] Under honesty, the sum defining $\alpha^{(j)}(x)$ should run over the *estimation-sample* units of tree $b$; say so.

- **L163** [Nit] "and the higher is the weight of patient when estimating" — grammar; also "patients" (C6).

- General [Minor] Missing: how to *evaluate* CATE estimates (no ground truth) — e.g. RATE/Qini or calibration checks (Yadlowsky et al. 2021; Chernozhukov et al. GATES/BLP) — highly relevant for the claims-triage use case.

 

## 11. `tutorial/instrumental_variables.md`

 

- **L17** [Verify] "Shalizi (2025, Ch. 23)" → Ch. 20 (C4).

- **L19–23** [Major] The three conditions identify a LATE **only with monotonicity** (no defiers) — or a constant effect. Neither is mentioned anywhere in the chapter although L23 says "2SLS identifies a local average treatment effect for compliers". Add condition 4, *Monotonicity*: $T(I{=}1)\ge T(I{=}0)$ for all units (Imbens & Angrist 1994; Angrist, Imbens & Rubin 1996).

- **L40** [Nit] "$\hat T$ is now independent of $U$" → "asymptotically uncorrelated with $U$" (it is a linear function of $I$ and $X$; independence is not implied and not needed).

- **L49** [Major] "The bivariate form … is valid only under the strong assumption that **no observed covariate affects $Y$**" — this is not correct. Bivariate IV is valid whenever the instrument is *unconditionally* exogenous (e.g. randomised encouragement, lottery), regardless of whether covariates affect $Y$; covariates then only improve precision. Covariates are *required* when exogeneity holds only *conditionally* on $X$ (i.e. $X$ is correlated with both $I$ and $Y$), which is what the first half of the paragraph correctly says. Rewrite the last sentence.

- **L53** [Major] The standard-error argument omits the cross term. With $\hat\varepsilon=u+\hat\beta(T-\hat T)$, $\mathbb{E}[\hat\varepsilon^2]=\mathbb{E}[u^2]+\beta^2\mathrm{Var}(T-\hat T)+2\beta\,\mathbb{E}[u(T-\hat T)]$, and the cross term is **non-zero precisely because $T$ is endogenous** ($u$ is correlated with the first-stage residual). Its sign is not determined, so "hand-rolled standard errors come out too large" is not a general result — they are simply *wrong*. State that, keep the recommendation to use a dedicated IV routine, and check the Wooldridge (2010) page reference (§5.2.1, around p. 97). Also add Wooldridge 2010 to the bibliography.

- **L58** [Nit] Katan DOI is URL-encoded (`10.1016%2Fs0140-6736%2886%2992972-7`); write it plainly.

- **L76** [Minor] "weighted median estimators" — cite Bowden et al. (2016), *Genetic Epidemiology* 40(4).

- General [Minor] Missing topics that matter in practice: **weak instruments** (first-stage $F$, Staiger & Stock 1997; Stock & Yogo 2005) and **over-identification tests**. Also the only worked example is genetic; an insurance instrument (broker/agent assignment, randomised encouragement to a wellness programme, distance to a claims office, a regulatory cut-over date) would ground the chapter. Also `debias.md` L100 and `diagnostics.md` L307 make LATE points that would sit better here.

 

## 12. `tutorial/quasi_experimental.md`

 

- **L5** [Nit] "These designs are especially relevant for longitudinal data" — DiD and SC yes; RD is typically cross-sectional. Qualify.

- **L5** [Nit] Angrist & Pischke (2015) is linked to the Princeton catalogue here but to DOI 10.2307/j.ctt5vhbqm in `concepts.md`; use one.

- **L9** [Major] "This diagnostic motivates the heterogeneity-robust estimators in `heterogeneous_effects`" — the heterogeneity-robust *DiD* estimators that Goodman-Bacon motivates are Callaway & Sant'Anna (2021), Sun & Abraham (2021), de Chaisemartin & D'Haultfœuille (2020), Borusyak, Jaravel & Spiess (2024) — not meta-learners or causal forests. Fix the pointer.

- **L9** [Nit] Very long paragraph; split the Goodman-Bacon decomposition into its own paragraph or a note.

- **L37–47** [Minor] The LATE definition duplicates `inference.md` L31–35 and uses $I$ instead of $Z$ (C3, C7). Also mention **fuzzy RD**, which *does* identify a LATE at the cutoff (Hahn, Todd & van der Klaauw 2001) — the current text ("This is a different object from the LATE") is only true for sharp RD, which L47 acknowledges but a reader may miss.

- **L65–66** [Nit] "Fit a local regression … $\hat\mu_-(c)=\lim_{x\uparrow c}\mathbb{E}[Y\mid X=x]$" mixes estimator and population target; write "estimate $\mu_-(c)=\lim …$ by local linear regression on $[c-h,c)$".

- **L71–93** [Minor] Synthetic control: add one sentence on inference (placebo-in-space permutation tests, Abadie, Diamond & Hainmueller 2010) — it links naturally to the placebo tests in `diagnostics.md`.

- General [Minor] No actuarial examples at all in this chapter. Suggestions: a bonus-malus or deductible reform as a DiD; a deductible/age eligibility threshold as an RD; a cantonal regulatory change with other cantons as donors for SC.

 

## 13. `tutorial/bayesian.md`

 

- **L5** [Verify] Shalizi Ch. 21 is not about Bayesian causal inference (C4).

- **L13** [Major] "Model comparison via Bayes factors … helps select among competing causal models" — Bayes factors cannot discriminate between Markov-equivalent DAGs, nor test exchangeability; the identifying assumptions remain untestable in the Bayesian framework exactly as in the frequentist one. Qualify: model comparison can select among *outcome models*, not among *causal structures*.

- **L52–66** [Major] The Bayesian propensity-score section omits the well-known difficulty: in a fully Bayesian joint model of $(T,Y)$ the propensity score does not appear in the likelihood for the outcome parameters (Robins & Ritov 1997; Rubin 1985), and naive joint modelling creates *feedback* from the outcome model into the propensity model (Zigler et al. 2013, *Biometrics*; Zigler 2016, *Statistical Science*). "Account for propensity-model uncertainty, unlike plug-in frequentist approaches" is therefore too rosy; state the feedback issue and the usual fix (cut feedback / two-stage).

- **L71** [Nit] "now the most widely used Bayesian method for HTE" — unsupported superlative; "widely used" suffices.

- **L107–121** [Major] Regularisation-induced confounding (RIC) is mis-attributed. In Hahn, Murray & Carvalho (2020) RIC arises because shrinkage of the *prognostic* function $\mu$ biases $\tau$ under targeted selection; their remedy for RIC is **including $\hat\pi(x)$ as a covariate in $\mu$** (L115 says this is "additionally … to reduce confounding bias"). The separate $\tau(x)$ ensemble with its own (stronger) prior is motivated by a *different* goal: allowing $\tau$ to be shrunk towards homogeneity independently of $\mu$. Swap the two motivations at L113 and in the figure caption L121.

- **L150** [Nit] "Exact finite-sample posterior" — exact *conditional on the model and prior*; add the qualifier since the frequentist column is criticised for approximations.

- **L160** [Nit] Add `bcf` (R) and `stochtree` (R/Python) for BCF.

- General [Minor] Two omissions: (i) a sentence that Bayesian methods rely on exchangeability just as much — the prior cannot repair unmeasured confounding — and a pointer to Bayesian sensitivity analysis (McCandless, Gustafson & Levy 2007); (ii) no actuarial example.

 

## 14. `tutorial/sensitivity.md`

 

- **L3–15** [Minor] Fine as a hub, but many chapters send readers here for content that is in `diagnostics.md` (C1). Either re-point those links or give this page substance — the natural candidate is the missing "actuary's end-to-end workflow" (README L42) using the unused `figs/actuary_workflow.svg`.

- **L15** [Minor] "closing with the actuary's end-to-end workflow" — `fairness.md` contains no such section.

 

## 15. `tutorial/diagnostics.md`

 

- **L3** [Nit] "Shalizi (2025)" with no chapter. Shalizi has little on sensitivity analysis; consider dropping or citing Ch. 21's short discussion explicitly.

- **L15** [Build] Heading anchor mismatch with L281 (C10).

- **L19–25** [Nit] Good. "green region"/"red frontier" assume the explainer's colours; fine.

- **L72–88** [Nit] Correct and well argued. ✓

- **L155** [Minor] Rosenbaum (2002) not in bibliography.

- **L149** [Nit] The telematics pre-treatment placebo example is excellent — consider promoting it to a boxed example so it is not lost in a bullet list.

- **L249** [Minor] "analogous E-values can be computed by first converting the effect to an approximate risk ratio scale" — give the recipe from VanderWeele & Ding (2017): for a standardised mean difference $d$, $\mathrm{RR}\approx\exp(0.91\,d)$; for a rate ratio with rare outcomes, use it directly. Claim counts/severities (the actuarial default) deserve one concrete line.

- **L265–277** [Nit] Given specific partial-$R^2$ values the OVB expression is an *equality* up to sign, not merely a bound; "bounded by" is fine as long as the $R^2$'s are read as upper limits, but say so.

- **L279** [Verify] "Cinelli & Hazlett (2020, Sec. 4.3)" — robustness values are defined in their Section 4.2 in the published version, I believe. Check.

- **L281** [Build] Broken self-anchor (C10).

- **L291–309** [Nit] Correct (I verified the bound algebra and the "contains zero" claim). ✓

- **L314** [Nit] Caption mentions two dashed lines ("LATE … shown by the dashed line" and "The dashed line at $\tau=0$"). Distinguish (colour/style) or reword.

- **L319–329** [Nit] Good closing figure.

 

## 16. `tutorial/debias.md`

 

- **L3** [Nit] "… and how to ensure the resulting model is fair" — fairness has been moved to its own chapter; drop the clause or add "(see `fairness`)".

- **L10–17** [Nit] Good table. Consider adding a "Remedy" column linking to Section "How to fix it".

- **L55, L72** [Nit] Two long paragraphs on selection ≡ collider bias say the same thing twice; merge into one and keep one figure.

- **L95** [Nit] "Covered in: -" for cluster/network models — say "not covered" or point to `assumptions.md` L52 note.

- **L96, L120** [Minor] "`sensitivity`" → `diagnostics` (C1).

- **L104** [Minor] Li, Morgan & Zaslavsky (2018) and Kang & Schafer (2007) not in bibliography.

- **L112** [Minor] "(Pearl, 2001; VanderWeele, 2015)" unlinked, not in bibliography. Pearl (2001) "Direct and indirect effects", UAI; VanderWeele (2015) *Explanation in Causal Inference*, OUP.

- **L112** [Verify] "Pearl (2009), Cor. 3.3.4" — the front-door adjustment is **Theorem 3.3.4** in *Causality* (2nd ed.), §3.3.2. Check.

- **L112** [Nit] The mediation discussion is dense and important; consider a small figure (mediator with $U_M$) — `figs/dsep_example2.svg` from `graphical_models.md` could be reused.

 

## 17. `tutorial/fairness.md`

 

- **L1–2** [Build] No H1 title (C10).

- **L4** [Nit] "EU regulation prohibits the use of protected characteristics (e.g. gender, ethnicity)" — sex is covered by Directive 2004/113/EC as interpreted in *Test-Achats*; ethnicity by Directive 2000/43/EC. One sentence citing both would be more precise.

- **L14** [Nit] Switzerland: consider mentioning FINMA supervision and that the Gender Equality Act does not cover private insurance pricing, since that is the crux for Swiss readers.

- **L31** [Nit] Correct (tower property). ✓

- **L48–50** [Major] The definition box states that a price is discrimination-free if $P(Y\le y\mid X,S)=P(Y\le y\mid X)$ for all $y$. That is **not** the Lindholm et al. definition. Their *discrimination-free price* is $\mu^*(x)=\int\mu(x,s)\,\mathrm dP(s)$ — i.e. exactly the formula the text derives later at L78–80. The displayed condition is instead a property of the *data* (no direct dependence of $Y$ on $S$ given $X$) under which best-estimate and discrimination-free prices coincide. Replace the box content with the $\mu^*$ definition (and, if wanted, keep the displayed condition as a remark on when unawareness is already discrimination-free).

- **L31, L48, L70, L162** [Minor] "Lindholm et al. (2021)": the ASTIN Bulletin paper "Discrimination-free insurance pricing" is **2022**, 52(1), 55–89, DOI 10.1017/asb.2021.23 (2021 is the online-first date). `references.md` lists a *different* Lindholm et al. 2022 (the arXiv discussion paper) and not the ASTIN one. Add the ASTIN entry with DOI and make years consistent.

- **L70, L78** [Verify] "Section 3" and "Proposition 15" — numbering differs between the arXiv and published versions; check against the ASTIN version you cite.

- **L93** [Build] `{doc}`../application/pricing`` does not exist; `figure/fairness_price_explainer.html` is never embedded (C10).

- **L93–160** [Minor] The group-fairness section is good but the chapter as a whole is only loosely tied to *causal inference* (one remark at L68–85). Given the book's title, consider foregrounding the causal DAG ($S\to X\to Y$, $S\to Y$) as a figure (`figs/fairness_dag.svg` exists and is unused) and framing proxy discrimination as a path-specific effect from the start.

- **L162** [Nit] "even a genuinely discrimination-free model violates them whenever $X$ and $S$ are statistically dependent" — true for demographic parity; for calibration/equal accuracy it depends. Consider "violates most of them".

- **L166–172** [Nit] Strong closing section. ✓

 

## 18. `papers/references.md`

 

- Missing entries: see C8 (about 20 items) plus Holland (1986), Lindholm et al. (2022, ASTIN), Li, Morgan & Zaslavsky (2018), Pearl (2010) / Ding, VanderWeele & Robins (2017) if added, Verma & Pearl (1990), Sun & Abraham (2021), de Chaisemartin & D'Haultfœuille (2020), Zigler et al. (2013), Abadie & Imbens (2008). **[Minor]**

- Athey & Wager (2019) is listed but never cited. **[Nit]**

- Shalizi (2025): add the draft date (C4). **[Minor]**

- Neyman (1923) entry is correct and complete — mirror it in-text (`concepts.md` L20). **[Nit]**

- "Useful Links": the Causal ML Book link points to a sub-page (`synthetic-did-and-regression-discontinuity.html`) rather than the book root; the uniqcret.com entry (C9). **[Nit]**

- "Data Sets": fine.

 

## 19. `_toc.yml` / `_config.yml`

 

- `_toc.yml` L35–39: orphan and non-existent notebooks (C10). **[Build]**

- `_toc.yml` L10: `maxdepth: 1` with `sections:` nested under chapters — check the sidebar actually shows the sub-pages; if not, use `maxdepth: 2`. **[Verify]**

- `_config.yml` L4 `date: 2026-01-01` and `copyright: "2026"` — fine if intentional. **[Nit]**

- `_config.yml`: no `bibtex_bibfiles` although `{cite:t}` is used once (C10). **[Build]**

 

---

 

## 20. Application notebooks

 

General remarks (apply to all three published notebooks):

 

- **[Build]** Execution counts are non-monotone with gaps and `None`s (e.g. `observational_data` cell 21 has output but no count; `health_interventions` runs 61→85). Do a clean *Restart & Run All* before committing so outputs match the code.

- **[Build]** Kernel metadata differs per notebook (`causalinference`, `.figvenv (3.9.6)`, `3.9.22`). Launch buttons (Binder/Colab, `_config.yml`) need `name: python3`. Also the Mac-specific setup box in `claims_triage` cell 1 should be generic and point at the actual `requirements.txt` (root file lacks `shap`, `lightgbm`, `scikit-learn`; `tutorial/requirements.txt` has them — consolidate into one file).

- **[Build]** Six orphan notebooks in `application/` are drafts (`case_study` — student exercise with a Windows path `C:\Users\Theresa\…` in its outputs; `confounding`, `motivation`, `sensitivity_analysis`, `susceptible_subpopulation`, `tutorial/treatment_effects.ipynb` — one to six cells of notes). They are built as orphan pages and are the targets of `{doc}` links from published notebooks (`claims_triage` cell 3 → `confounding`, cell 27 → `sensitivity_analysis`). Move them out of the source tree (or into `exclude_patterns`) and fix the two links.

- **[Nit]** `from utils import *` in every notebook; `warnings.filterwarnings("ignore")` / `np.seterr(all="ignore")` globally; duplicate imports (`observational_data` cell 3 imports `plotly.graph_objects` twice); emoji check-marks in summary boxes.

- **[Minor]** No frequentist confidence intervals anywhere except econml's `ate_interval`; ties in with C11.

 

### 20.1 `application/observational_data.ipynb` (in TOC)

 

A well-designed notebook that operationalises the four assumptions; the negative-control test and the Rosenbaum matching with a proper assignment solver are good practice. Issues:

 

- **Cell 6** [Major] `Y = Y + np.where(Treatment_Subtype == 1, 1.5, 0.0)` modifies the *main* outcome. The true ATE of the label "treated" is therefore $5 + 0.5\cdot1.5 = 5.75$, not 5.0. Consequences: the "True ATE = 5" line in the cell-11 figure is wrong; cell 23 attributes the whole gap $6.785-5.0$ to $U$, whereas the $U$-induced bias is ≈1.0 (which the placebo estimate in cell 29, 1.005, confirms nicely). Generate a separate `Y_Subtype` for the consistency check, as already done for `Y_Spillover` and `Y_Negative_Control`.

- **Cell 7** [Nit] The printed "DAG" omits X3→T, X4→T and U, which the DGP contains and cell 8 discusses.

- **Cell 8** [Minor] "backdoor paths $X\to T$ and $X\to Y$" — a backdoor path is $T\leftarrow X\to Y$. Pearl (2011) and Myers et al. (2011) are not in `references.md`.

- **Cell 12** [Nit] Concludes "consistency is questionable" although cell 10 carefully explains the diagnostic cannot separate this from effect modification; no test of the sub-type *difference* is run.

- **Cell 13–14** [Minor] "A significant correlation is direct evidence of spillover" — it is also produced by group-level confounding; say "consistent with". `interference_diagnostic(..., 'Y')` is computed twice.

- **Cell 16–17** [Major] The text says "we inspect the *estimated* propensity scores", but the box plots use the DGP's true probabilities (`P_Propensity_Score_Good/Violate`). Estimate them, as the reader would have to.

- **Cell 19** [Minor] Propensity model uses `X1..X5`, i.e. adjusts for the instruments X3–X5, contradicting the "adjust for exactly {X1, X2}" contract of cells 8 and 11 without comment. Also "Naive IPW" in the table is the *stabilised* Hájek estimator (`ipw_ate(stabilized=True)`), and trimming discards 645 of 1000 units — worth stating that the estimand changes (harmless here only because the effect is homogeneous).

- **Cell 20–21** [Major] Love plot: the violated regime estimates the propensity on `{X1, X2}` only, so X3–X5 stay imbalanced *because they are not in the model*, not because of "extreme weights that adjustment cannot remove" as the text claims. Use the same propensity specification as cell 19 or fix the explanation.

- **Cell 23** [Minor] E-value is computed with `sd_outcome = sd(Y)` (total SD, includes the treatment effect); state the convention. "True ATE 5.0 <- bias remains because U is unobserved" — see cell 6.

- **Cell 25** [Nit] The "as strong as X2" benchmark is a simplified version of Cinelli & Hazlett's bounding (which uses relative strengths $k_D,k_Y$); say so.

- **Cell 26–27** [Minor] Text and code comment speak of the *signed-rank* statistic, but `utils.rosenbaum_sensitivity` implements the *sign test* with a normal approximation and a one-sided alternative. Align (Wilcoxon signed-rank bounds are standard and more powerful), and say the test is one-sided.

- **Cell 30** [Minor] LaLonde (1986) and Imbens & Xu (2024) missing from `references.md`; `{doc}`../tutorial/sensitivity`` in cells 1 and 22 → `diagnostics` (C1).

 

### 20.2 `application/claims_triage.ipynb` (in TOC)

 

The strongest notebook: clear business framing, ground truth, policy evaluation against realised savings, econml's OVB sensitivity with a per-stratum RV profile. Issues:

 

- **Cell 8** [Major] `tau_true = -savings_rate * baseline_cost` includes the idiosyncratic lognormal factor that is *unknown at triage*. It is therefore an **individual** effect, not the CATE $\tau(x)=\mathbb{E}[\tau_i\mid x] = -\text{savings\_rate}\cdot\text{size\_scale}\cdot e^{0.08}$. Cells 14 (scatter "recovered individual effects") and 19 ("Predicted −4,449 vs True −2,661") grade the forest against an unattainable target; the oracle curve in cell 23 likewise ranks on realised noise. Add `cate_true` and grade against it; keep `tau_true` for the policy-value evaluation (cell 22), where realised savings are the right yardstick.

- **Cell 11–12** [Major] `LinearDML(..., X=None, W=features)` is the partially-linear model. The tutorial's own note (`direct_adjustment.md` L459–466) says that under heterogeneous effects it targets the overlap-weighted $\tau^*$ and warns against comparing it with averaged causal-forest CATEs — exactly what cells 12 and 14 do ("DML estimate −903 … True ATE −867", "Causal-forest average CATE −908"). Either use an AIPW/IRM estimator for the ATE (`econml.dr.LinearDRLearner().ate()` or `CausalForestDML.ate()`) or relabel the PLM number honestly.

- **Cell 13** [Minor] "staying doubly robust through the same residualisation as DML" — residualisation gives Neyman orthogonality, not double robustness (the tutorial says so itself, `heterogeneous_effects.md` L123).

- **Cell 15** [Nit] "every claim in this group has $\hat\tau>0$" is an empirical claim about the forest output not checked in code.

- **Cell 17** [Nit] Seven tqdm progress-bar stream outputs are committed; silence SHAP's progress bar.

- **Cell 19** [Minor] Picking the claim with the *largest* predicted saving guarantees a winner's-curse over-estimate (−4,449 vs −2,661) — a teachable point that goes unmentioned.

- **Cell 21** [Nit] "*Regelwerk*" (German) in an English text.

- **Cell 24** [Verify] Chernozhukov et al. (2022), DOI 10.3982/ECTA19345 ("Long Story Short") — check publication details; not in `references.md`.

- **Cell 27** [Major] "none of our observed features individually explains anywhere near 12% of the residual variation in both directions" — asserted, not computed. `severity` drives both routing (logit coefficient 1.8) and cost (+CHF 6,000 range) and plausibly exceeds 12% for cost. Compute the benchmark partial $R^2$s (as `observational_data` cell 25 does) and plot them on the contour.

- **Cell 28** [Minor] "confounding bias adds (roughly) the same worst-case shift to every effect" — the bound scales with residual SDs, which differ strongly across severity strata; soften.

- General [Minor] None of the diagnostics from `observational_data` (estimated-propensity overlap, SMD/Love plot) are applied to the claims data; one cell would make the two notebooks consistent.

 

### 20.3 `application/health_interventions.ipynb` (in TOC)

 

This notebook is not at publication standard and, in its current form, contradicts the tutorial. Recommend removing it from `_toc.yml` until rewritten (README L5 promises "assessing whether a health improvement programme is genuinely effective from purely observational data").

 

- **Whole notebook** [Major] One markdown cell (the title, which describes a *dataset generator*); no narrative, no links to the tutorial, no DAG, no diagnostics, no conclusions. Every stream output appears twice (executed twice without clearing); dev scaffolding remains (`# START!!` cell 8, `# END!!` cell 15, empty cell 24).

- **Cell 5** [Major] The DGP gives `itt` a **direct** effect on mortality (`risk_multiplier *= 0.75` for `itt==1`) in addition to the effect through `w`. Cell 21 then uses `itt` as an instrument for `w` — the exclusion restriction is violated by construction, so the "LATE" is not identified. (With one-sided non-compliance, a valid LATE would equal the ATT; worth saying if the design is fixed.)

- **Cells 8–15** [Major] A second dataset is generated by fitting LightGBM models on the first (80–95 % MCAR-missing) dataset and sampling from them. The uptake model has validation AUC **0.520** (cell 12 — essentially random, so confounding is nearly absent in `df_synthetic`), the ITT effect shrinks from 28 % to 12 %, and there is **no ground truth** for `df_synthetic` — unlike the other two notebooks nothing can be graded. "79,732 complete cases" (cell 12) is wrong; the rows are 80–95 % missing.

- **Cells 17–23** [Major] Sign conventions are inconsistent: "naive" is computed as control − treated (positive = reduction), econml effects are treated − control (negative = reduction). `abs()` then hides the sign, so the S-learner's **+0.0053** (a mortality *increase*) is reported as "21.8 % mortality reduction" and tagged "✅ Unbiased (population)" (cell 23). "All unbiased methods converge to similar estimates" is false on the notebook's own output (−0.0004 … +0.0053).

- **Cell 21** [Minor] `DMLIV(model_t_xwz=RandomForestRegressor, ..., discrete_treatment=True)` — first-stage model for a binary treatment should be a classifier; complier effect is divided by the *overall* mortality rate.

- **Cell 22** [Minor] Individual X-learner effects range −0.47 … +0.44 on a 2.4 % outcome; "most reliable for HTE" is unsupported.

- **Cells 4–5** [Nit] Python `for` loops over 100k rows; vectorise.

- **Cell 23** [Nit] "BUSINESS RECOMMENDATIONS" branch on `abs(dml_ate) > 0.01` without any inference.

 

### 20.4 `application/utils.py`

 

- `calculate_smd_weighted` [Major] uses **weighted** variances in the denominator; `diagnostics.md` L72–88 (correctly) prescribes the fixed, unweighted, unadjusted-sample SD. Pass the raw SDs in.

- `rosenbaum_sensitivity` [Minor] sign test, one-sided, normal approximation — see 20.1 cell 26–27; docstring says "sign-test version" but the notebook text says signed-rank.

- `estimate_propensity` [Minor] `LogisticRegression()` default L2 penalty (C=1) shrinks scores toward 0.5, masking positivity problems and biasing IPW weights; use `penalty=None` (or very large `C`) for a propensity model.

- `ipw_ate` [Nit] Hájek normalisation makes `stabilized=True/False` return identical ATEs (only the reported max weight differs); document.

- `ols_treatment_effect` [Nit] homoskedastic SEs; claim-cost outcomes are heteroskedastic — consider HC SEs (`statsmodels` is in the requirements).

- `e_value_from_effect`, `robustness_value`, `adjusted_estimate` [✓] formulas verified against VanderWeele & Ding (2017) and Cinelli & Hazlett (2020).

 

---

 

## Appendix A — Mechanical check log

 

Commands run against the working tree (for reproducibility):

 

- Labels defined: `(overlap)=` (direct_adjustment L44), `(sec:ct)=` (heterogeneous_effects L52), `(sec:cf)=` (L129). No `(debias)=` label exists.

- `{cite:t}` usages: 1 (`direct_adjustment.md` L90). `.bib` files: none.

- `{doc}` targets: all resolve except `../application/pricing`.

- Interactive explainers embedded: `applications_matrix.html` (README), `psm_iptw_explainer.html` (direct_adjustment), `loveplot_explainer.html`, `rosenbaum_explainer.html`, `sensitivity_explainer.html` (diagnostics). **Not** embedded: `fairness_price_explainer.html`.

- Unused figure assets: listed in C10.

- Dash style: `identification.md` uses "—" (5×); all other files use " - ".

- "patient" occurrences: `concepts.md` 1, `heterogeneous_effects.md` 17.

