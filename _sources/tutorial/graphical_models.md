# Graphical Causal Models

This chapter introduces **Directed Acyclic Graphs (DAGs)** as the language for encoding causal assumptions. The presentation follows [Shalizi (2025, Chs. 18–22)](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf), with additional references to [Pearl (2009)](https://doi.org/10.1017/CBO9780511803161). See also the [Python Causality Handbook (Ch. 4)](https://matheusfacure.github.io/python-causality-handbook/04-Graphical-Models.html) for an applied introduction.

## Causal Diagrams

A causal diagram is a graph where **nodes** represent random variables and **directed edges** ($\rightarrow$) represent direct causal effects. The absence of an edge encodes the assumption that there is *no* direct causal effect between two variables.

```{prf:definition} Directed Acyclic Graph (DAG)
:label: dag
:class: dropdown

A **directed acyclic graph** $\mathcal{G} = (V, E)$ consists of:
- a finite set of **vertices** (nodes) $V = \{V_1, V_2, \dots, V_p\}$, each representing a random variable,
- a set of **directed edges** $E \subseteq V \times V$, where $(V_i, V_j) \in E$ is drawn as $V_i \rightarrow V_j$,

subject to the constraint that there are **no directed cycles**: there is no sequence $V_{i_1} \rightarrow V_{i_2} \rightarrow \cdots \rightarrow V_{i_k} \rightarrow V_{i_1}$.
```

The acyclicity constraint reflects the assumption that causes precede their effects - no variable can be its own cause through any chain of intermediate variables ([Shalizi, 2025, Section 18.2](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)).

### Graph Terminology

```{prf:definition} Parents, Children, Ancestors, Descendants
:label: graph-family
:class: dropdown

Given a DAG $\mathcal{G} = (V, E)$ and a node $X \in V$:

- **Parents** of $X$: $\text{Pa}(X) = \{Z \in V : Z \rightarrow X \in E\}$
- **Children** of $X$: $\text{Ch}(X) = \{Z \in V : X \rightarrow Z \in E\}$
- **Ancestors** of $X$: all nodes $Z$ such that there exists a directed path $Z \rightarrow \cdots \rightarrow X$
- **Descendants** of $X$: all nodes $Z$ such that there exists a directed path $X \rightarrow \cdots \rightarrow Z$
```

```{figure} figs/graph_family.svg
:width: 80%
:name: fig-graph-family

Graph terminology: relative to the node of interest $X$, the node $Z$ is a parent, $W$ a child, and $Y$ a descendant.
```

A **path** between two nodes is any sequence of edges connecting them, regardless of direction. A **directed path** follows the arrow directions. A **causal path** from $T$ to $Y$ is a directed path $T \rightarrow \cdots \rightarrow Y$.

## Three Fundamental Path Structures

Every path through three variables takes one of exactly three forms. Understanding these structures is the key to reasoning about confounding and adjustment ([Shalizi, 2025, Section 18.3](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)).

### Chains (Mediation)

```{prf:definition} Chain (Mediator)
:label: chain
:class: dropdown

A **chain** is a path of the form $X \rightarrow M \rightarrow Y$. The variable $M$ is called a **mediator** - it transmits the causal effect of $X$ on $Y$.
```

```{figure} figs/chain.svg
:width: 70%
:name: fig-chain

A chain: the mediator $M$ transmits the causal effect of the cause $X$ on the effect $Y$.
```

In a chain, $X$ and $Y$ are **marginally dependent** (information flows through $M$), but **conditionally independent given $M$**: once we know $M$, learning $X$ provides no additional information about $Y$. (The *dependence* half of each statement below relies on {prf:ref}`faithfulness`, introduced with $d$-separation; see the note after the summary table.)

$$
X \perp\!\!\!\perp Y \mid M \quad \text{(in a chain)}
$$

### Forks (Common Cause / Confounding)

```{prf:definition} Fork (Common Cause)
:label: fork
:class: dropdown

A **fork** is a path of the form $X \leftarrow F \rightarrow Y$. The variable $F$ is a **common cause** (confounder) of $X$ and $Y$.
```

```{figure} figs/fork.svg
:width: 55%
:name: fig-fork

A fork: the common cause $F$ induces a spurious association between $X$ and $Y$.
```

In a fork, $X$ and $Y$ are marginally dependent (the common cause $F$ induces a spurious association), but conditionally independent given $F$:

$$
X \perp\!\!\!\perp Y \mid F \quad \text{(in a fork)}
$$

This is the structure that generates **confounding bias**: if $F$ is not adjusted for, the association between $X$ and $Y$ conflates the causal effect with the spurious path through $F$.

### Colliders (Common Effect)

```{prf:definition} Collider
:label: collider
:class: dropdown

A **collider** on a path is a node $C$ where two arrowheads meet: $X \rightarrow C \leftarrow Y$. The variable $C$ is a **common effect** of $X$ and $Y$.
```

```{figure} figs/collider.svg
:width: 55%
:name: fig-collider

A collider: $C$ is a common effect of $X$ and $Y$. Conditioning on $C$ opens a spurious path between them.
```

Colliders behave **opposite** to chains and forks. In a collider structure, $X$ and $Y$ are **marginally independent** - there is no open path connecting them. However, **conditioning on the collider $C$ (or any descendant of $C$) opens the path** and induces a spurious association:

$$
X \perp\!\!\!\perp Y \quad \text{but} \quad X \not\!\perp\!\!\!\perp Y \mid C \quad \text{(collider)}
$$

This is the source of **collider bias** (also called **selection bias** or **Berkson's paradox**). Adjusting for a collider - or for a descendant of a collider - creates a spurious association where none existed ([Shalizi, 2025, Section 18.3](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)).

### Summary of Path Structures

| Structure | Path | Marginal | Conditional on middle node |
|-----------|------|----------|---------------------------|
| **Chain** (Mediator) | $X \rightarrow M \rightarrow Y$ | Dependent | Independent |
| **Fork** (Common Cause) | $X \leftarrow F \rightarrow Y$ | Dependent | Independent |
| **Collider** (Common Effect) | $X \rightarrow C \leftarrow Y$ | Independent | Dependent |

```{note}
The **Independent** cells (chain/fork conditional on the middle node, collider marginal) follow from the {prf:ref}`causal-markov` alone: $d$-separation implies conditional independence. The **Dependent** cells (chain/fork marginal, conditioned collider) are the *converse* direction - inferring dependence from $d$-connection - and additionally require {prf:ref}`faithfulness`, introduced below. In a non-faithful distribution they can fail: e.g. in a linear chain $X \rightarrow M \rightarrow Y$ whose direct and indirect contributions cancel exactly, $X$ and $Y$ are marginally *independent* despite the open path.
```

## $d$-Separation

The three path structures above give rise to a general graphical criterion for reading off conditional independencies from a DAG.

```{prf:definition} Blocked Path
:label: blocked-path
:class: dropdown

A path $p$ between nodes $X$ and $Y$ in a DAG is **blocked** by a set of nodes $Z$ if and only if $p$ contains a node $W$ such that either:

1. $W$ is a **chain** or a **fork** on $p$, **and** $W \in Z$ (we condition on it), or
2. $W$ is a **collider** on $p$ **and** neither $W$ nor any descendant of $W$ is in $Z$.
```

```{prf:definition} $d$-Separation
:label: d-separation-def
:class: dropdown

Two nodes $X$ and $Y$ are **$d$-separated** by a set $Z$ in a DAG $\mathcal{G}$, written $X \perp_{\mathcal{G}} Y \mid Z$, if **every** path between $X$ and $Y$ is blocked by $Z$.

If $X$ and $Y$ are not $d$-separated by $Z$, they are **$d$-connected** given $Z$.
```

$d$-separation is the graphical analogue of conditional independence. It provides a purely mechanical procedure: to check whether $X \perp\!\!\!\perp Y \mid Z$, enumerate all paths between $X$ and $Y$ and verify that each one is blocked ([Shalizi, 2025, Section 18.3](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)).

### Conditional Independence

The connection between the graphical criterion ($d$-separation) and the probabilistic property (conditional independence) is formalised by two properties.

```{prf:property} Causal Markov Condition
:label: causal-markov
:class: dropdown

If a DAG $\mathcal{G}$ is a causal model for a distribution $P$, then every variable $X$ is conditionally independent of its non-descendants given its parents:

$$
X \perp\!\!\!\perp \text{NonDesc}(X) \mid \text{Pa}(X)
$$

Equivalently: if $X \perp_{\mathcal{G}} Y \mid Z$ ($d$-separation), then $X \perp\!\!\!\perp Y \mid Z$ (conditional independence in $P$).
```

The Causal Markov Condition ensures that $d$-separation implies conditional independence. The converse - that every conditional independence in the data corresponds to a $d$-separation in the graph - requires an additional assumption.

```{prf:assumption} Faithfulness
:label: faithfulness
:class: dropdown

A distribution $P$ is **faithful** to a DAG $\mathcal{G}$ if the *only* conditional independencies in $P$ are those entailed by $d$-separation in $\mathcal{G}$.

Equivalently: if $X \perp\!\!\!\perp Y \mid Z$ in $P$, then $X \perp_{\mathcal{G}} Y \mid Z$.
```

Together, the Causal Markov Condition and faithfulness give a one-to-one correspondence between $d$-separation statements and conditional independence relations ([Shalizi, 2025, Section 19.3](https://www.stat.cmu.edu/~cshalizi/ADAfaEPoV/ADAfaEPoV.pdf)).

### Example 1: $d$-Separation in Practice

Consider the following DAG:

```{figure} figs/dsep_example.svg
:width: 80%
:name: fig-dsep-example

A DAG combining all three path structures: a fork through the confounder $F$, a chain through the mediator $M$, and a collider $C$ that is a common effect of $T$ and $Y$.
```


```{prf:example} $d$-Separation in Practice
:label: dsep-example
:class: dropdown

- **$T$ and $Y$ given $\emptyset$**: The path $T \leftarrow F \rightarrow Y$ is open (fork, $F$ not conditioned on). $T$ and $Y$ are $d$-connected - **not** independent.
- **$T$ and $Y$ given $F$**: The backdoor path $T \leftarrow F \rightarrow Y$ is now blocked. The directed path $T \rightarrow M \rightarrow Y$ remains open (chain, $M$ not conditioned on). $T$ and $Y$ are $d$-connected given $F$ - but now the remaining open paths are *causal*.
- **$T$ and $Y$ given $\{F, C\}$**: Conditioning on the collider $C$ **opens** the path $T \rightarrow C \leftarrow Y$, creating collider bias. This is an **incorrect** adjustment set.

**Correct adjustment set: $\{F\}$.** Conditioning on $F$ blocks the single backdoor path $T \leftarrow F \rightarrow Y$, leaving the causal paths $T \rightarrow Y$ and $T \rightarrow M \rightarrow Y$ open. The mediator $M$ and the collider $C$ must be **left out**: adjusting for $M$ would block the indirect causal effect, and adjusting for $C$ would open the spurious path $T \rightarrow C \leftarrow Y$ ({prf:ref}`backdoor-criterion`).

**Identifying independence.** Blocking the backdoor makes the treated and control groups comparable within levels of $F$, i.e. conditional exchangeability holds:

$$
(Y(1), Y(0)) \perp\!\!\!\perp T \mid F.
$$

Given $F$, treatment is as good as randomly assigned, so $\mathbb{E}[Y \mid T=t, F]$ estimates a genuine causal contrast rather than a confounded one. This is precisely {prf:ref}`exchangeability`, and it is what licenses the backdoor adjustment formula $\mathbb{E}[Y(t)] = \mathbb{E}_F\big[\mathbb{E}[Y \mid T=t, F]\big]$. Without conditioning on $F$ the open fork $T \leftarrow F \rightarrow Y$ violates this independence, and the raw contrast $\mathbb{E}[Y \mid T=1] - \mathbb{E}[Y \mid T=0]$ conflates the causal effect with confounding.
```

### Example 2: A Mediator with Unmeasured Confounding

The next graph looks deceptively similar but teaches the opposite lesson about mediators. Here the treatment $T$ is **randomised** - no arrow points into it - and it affects the outcome $Y$ both directly ($T \rightarrow Y$) and through a mediator ($T \rightarrow M \rightarrow Y$). Crucially, an **unmeasured** variable $U$ confounds the mediator–outcome relationship: $U \rightarrow M$ and $U \rightarrow Y$.

```{figure} figs/dsep_example2.svg
:width: 70%
:name: fig-dsep-example2

A randomised treatment $T$ with a mediator $M$, whose relationship with $Y$ is confounded by an unmeasured variable $U$ (dashed). Because $M$ is a collider on the path $T \rightarrow M \leftarrow U \rightarrow Y$, that path is blocked unless one conditions on $M$.
```

```{prf:example} Mediator under Randomisation
:label: dsep-example-mediator
:class: dropdown

- **Enumerate the paths.** From $T$ to $Y$ there are three: the direct causal edge $T \rightarrow Y$; the indirect causal chain $T \rightarrow M \rightarrow Y$; and $T \rightarrow M \leftarrow U \rightarrow Y$. On the last, $M$ is a **collider**, so the path is *already blocked* when nothing is conditioned on.
- **No backdoor to close.** Since $T$ is randomised, no arrow enters $T$ and there is **no backdoor path** at all - the treatment is unconfounded by design.
- **Why not condition on $M$?** Adjusting for the mediator would do double damage: it (i) blocks the indirect causal effect $T \rightarrow M \rightarrow Y$, and (ii) *opens* the collider path $T \rightarrow M \leftarrow U \rightarrow Y$, injecting spurious association through the unmeasured $U$.

**Correct adjustment set: $\emptyset$ (adjust for nothing).** The total effect of $T$ on $Y$ is identified without conditioning on any variable. Recovering the *direct* effect that does **not** operate through $M$ would instead require the mediation formula and the assumption of no unmeasured $M$–$Y$ confounding - which $U$ violates here (see {doc}`debias`).

**Identifying independence.** Randomisation makes treatment independent of the potential outcomes **unconditionally**:

$$
(Y(1), Y(0)) \perp\!\!\!\perp T.
$$

The effect is therefore identified directly, $\mathbb{E}[Y(t)] = \mathbb{E}[Y \mid T=t]$, with no adjustment term. Conditioning on the mediator $M$ would **destroy** this independence by opening the collider path $T \rightarrow M \leftarrow U \rightarrow Y$ - the resulting $\mathbb{E}[Y \mid T=t, M]$ would no longer be exchangeable in $T$, forfeiting the identification that randomisation supplied for free.
```

### Example 3: A Larger Graph

Realistic problems mix several confounders with variables that look tempting but must be excluded. This graph has eight nodes and the following edges: $Z_1 \rightarrow T$ and $Z_1 \rightarrow Y$; $Z_2 \rightarrow T$, $Z_2 \rightarrow Z_3$, and $Z_3 \rightarrow Y$; an instrument $I \rightarrow T$; a mediator $T \rightarrow M \rightarrow Y$ alongside the direct edge $T \rightarrow Y$; and a collider $T \rightarrow K \leftarrow Y$.

```{figure} figs/dsep_example3.svg
:width: 90%
:name: fig-dsep-example3

A larger DAG: two confounding routes ($T \leftarrow Z_1 \rightarrow Y$ and $T \leftarrow Z_2 \rightarrow Z_3 \rightarrow Y$), an instrument $I$, a mediator $M$, and a collider $K$. Only the confounding routes must be blocked.
```

```{prf:example} Reading Off the Adjustment Set
:label: dsep-example-large
:class: dropdown

List every **backdoor path** (a path leaving $T$ through an arrow pointing *into* $T$) and decide how to block it:

- $T \leftarrow Z_1 \rightarrow Y$ - an open fork; block it by conditioning on $Z_1$.
- $T \leftarrow Z_2 \rightarrow Z_3 \rightarrow Y$ - open; block it by conditioning on $Z_2$ **or** on $Z_3$ (either node lies on the path).
- $T \leftarrow I$ - a dead end: the instrument $I$ reaches $Y$ *only* through $T$, so this path carries no confounding association and needs no adjustment.

Leave the remaining structures untouched:

- $M$ is a **mediator** on the causal path $T \rightarrow M \rightarrow Y$ - conditioning on it would block part of the effect.
- $K$ is a **collider** ($T \rightarrow K \leftarrow Y$) - conditioning on it would open a spurious path.

**Correct minimal adjustment set: $\{Z_1, Z_2\}$** (equivalently $\{Z_1, Z_3\}$). Either choice blocks both backdoor paths while leaving all causal paths open. The instrument $I$, the mediator $M$, and the collider $K$ are all deliberately excluded ({prf:ref}`backdoor-criterion`). Note that adjusting for the instrument $I$ is not merely unnecessary - it can *amplify* bias from any residual unmeasured confounding, so it is left out on purpose.

**Identifying independence.** Blocking both backdoor paths yields conditional exchangeability:

$$
(Y(1), Y(0)) \perp\!\!\!\perp T \mid Z_1, Z_2.
$$

Given $\{Z_1, Z_2\}$, treatment is as good as randomly assigned, which identifies the effect through the backdoor adjustment formula $\mathbb{E}[Y(t)] = \mathbb{E}_{Z_1, Z_2}\big[\mathbb{E}[Y \mid T=t, Z_1, Z_2]\big]$. Adding $M$ or $K$ to the conditioning set would open a non-causal path and break this independence, while adding $I$ would amplify residual confounding bias - in each case $\mathbb{E}[Y \mid T=t, \cdot]$ would cease to recover a causal contrast.
```
