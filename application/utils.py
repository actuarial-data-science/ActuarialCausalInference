import os

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind, norm, pearsonr
from scipy.stats import t as tdist
import plotly.graph_objects as go
import plotly.subplots as sp
import seaborn as sns
from sklearn.tree import _tree
from sklearn.linear_model import LogisticRegression

# ---------------------------------------------------------------------------
# SAV / ASA brand palette (Swiss Association of Actuaries logo)
# ---------------------------------------------------------------------------
# Colours sampled from figure/logo.png. Use these (and shades of them) for all
# plotting so the book has a consistent, on-brand look.
SAV_GREEN = "#98C21F"   # primary lime green
SAV_CHARCOAL = "#5F625F"  # dark grey from the logo triangles / wordmark
SAV_BLACK = "#000000"

# Shades / tints derived from the three brand colours
SAV_GREEN_DARK = "#6E8C16"
SAV_GREEN_LIGHT = "#C5DE7A"
SAV_GREY = "#7E817E"
SAV_GREY_LIGHT = "#A8ABA8"

# Ordered categorical palette (used for the default colour cycle and seaborn)
SAV_PALETTE = [
    SAV_GREEN,
    SAV_CHARCOAL,
    SAV_GREEN_DARK,
    SAV_GREY_LIGHT,
    SAV_GREEN_LIGHT,
    SAV_BLACK,
    SAV_GREY,
]


def _register_sav_colormaps():
    """Register brand colormaps once: 'sav', 'sav_r', 'sav_div'."""
    import matplotlib as mpl
    from matplotlib.colors import LinearSegmentedColormap

    cmaps = {
        # sequential: light -> green -> dark green (good for "more = greener")
        "sav": LinearSegmentedColormap.from_list(
            "sav", ["#F4F8E6", SAV_GREEN, SAV_GREEN_DARK]),
        # diverging: charcoal <-> light <-> green (e.g. bad <-> neutral <-> good)
        "sav_div": LinearSegmentedColormap.from_list(
            "sav_div", [SAV_CHARCOAL, "#EDEDEA", SAV_GREEN]),
    }
    for name, cmap in cmaps.items():
        try:
            mpl.colormaps.register(cmap, name=name, force=True)
            mpl.colormaps.register(cmap.reversed(), name=name + "_r", force=True)
        except Exception:
            pass  # already registered


def apply_sav_theme():
    """Apply the SAV/ASA brand palette to matplotlib and seaborn.

    Call this once near the top of a notebook (after importing utils) so every
    subsequent plot uses the brand colours by default.
    """
    import matplotlib as mpl
    from cycler import cycler

    _register_sav_colormaps()
    sns.set_style("whitegrid")
    sns.set_palette(SAV_PALETTE)
    mpl.rcParams.update({
        "axes.prop_cycle": cycler(color=SAV_PALETTE),
        "image.cmap": "sav",
        "figure.figsize": (8, 5),
    })
    _apply_sav_plotly_template()
    return SAV_PALETTE


def _apply_sav_plotly_template():
    """Register and activate a Plotly template using the brand colours."""
    try:
        import plotly.io as pio
        import plotly.graph_objects as go
    except Exception:
        return
    tmpl = go.layout.Template()
    tmpl.layout.colorway = SAV_PALETTE
    tmpl.layout.font = dict(color=SAV_CHARCOAL)
    # sequential + diverging colourscales matching the matplotlib colormaps
    tmpl.layout.colorscale.sequential = [[0.0, "#F4F8E6"], [0.5, SAV_GREEN], [1.0, SAV_GREEN_DARK]]
    tmpl.layout.colorscale.diverging = [[0.0, SAV_CHARCOAL], [0.5, "#EDEDEA"], [1.0, SAV_GREEN]]
    pio.templates["sav"] = tmpl
    # layer on top of the default so gridlines/background stay sensible
    pio.templates.default = "plotly_white+sav"


def plot_causal_dag(causal_model_dict, title, node_color=SAV_GREEN):
    """Generates and displays a causal DAG from a dictionary of causal relationships and weights.

    Args:
        causal_model_dict (dict): A dictionary where keys are strings like 'Source -> Target'
                                  and values are the weights of the causal effect.
        title (str): The title for the DAG plot.
        node_color (str): The color for the nodes in the DAG.
    """
    G = nx.DiGraph()

    # Add nodes and edges with weights from the causal_model_dict
    for path, weight in causal_model_dict.items():
        source, target = path.split(' -> ')
        G.add_edge(source, target, weight=weight)

    # Define node positions for a clear layout
    pos = {
        'X1': (0, 0.5),   # Top left
        'X2': (1, 0.5),   # Top right
        'T': (0.5, 1), # Middle
        'Y': (0.5, 0)    # Bottom
    }

    # Create a figure and axes object
    fig, ax = plt.subplots(figsize=(8, 6))

    # Draw the graph
    nx.draw_networkx(
        G,
        pos,
        ax=ax,
        node_color=node_color,
        node_size=2000,
        font_size=10,
        with_labels=True,
        arrowstyle='->',
        arrowsize=20,
        edge_color='gray'
    )

    # Extract edge labels and format them
    edge_labels = nx.get_edge_attributes(G, 'weight')
    formatted_edge_labels = {
        (u, v):
        f'{d["weight"]:.1f}' for u, v, d in G.edges(data=True)
    }

    # Draw edge labels
    nx.draw_networkx_edge_labels(G, pos, edge_labels=formatted_edge_labels, ax=ax, font_color='gray')


    # Set title and turn off axes
    ax.set_title(title, fontsize=16)
    ax.axis('off')

    # Display the plot
    plt.show()

def plot_positivity_check_plotly(df, ps_column, treatment_column, title):
    """Generates a mirrored histogram plot using Plotly for a given propensity score distribution, vertically oriented."""

    ps_treated = df[df[treatment_column] == 1][ps_column]
    ps_control = df[df[treatment_column] == 0][ps_column]

    # Use 30 bins spanning 0 to 1
    bins = np.linspace(0, 1, 30)

    # Calculate histograms for density and counts
    hist_control_density, bins_control = np.histogram(ps_control, bins=bins, density=True)
    hist_control_counts, _ = np.histogram(ps_control, bins=bins, density=False)

    hist_treated_density, bins_treated = np.histogram(ps_treated, bins=bins, density=True)
    hist_treated_counts, _ = np.histogram(ps_treated, bins=bins, density=False)

    # Create figure
    fig = go.Figure()

    # Plot Control Group (positive frequencies on x-axis)
    fig.add_trace(go.Bar(
        y=bins_control[:-1], # Propensity score on Y-axis
        x=hist_control_density, # Density on X-axis
        width=np.diff(bins_control), # Bar height corresponds to bin width
        orientation='h',
        marker_color=SAV_GREEN,
        name='Control',
        customdata=hist_control_counts,
        hovertemplate='Propensity Score: %{y:.2f}<br>' +
                      'Relative Frequency: %{x:.2f}<br>' +
                      'Absolute Frequency: %{customdata:.0f}<extra></extra>'
    ))

    # Plot Treated Group (negative frequencies on x-axis, mirrored)
    fig.add_trace(go.Bar(
        y=bins_treated[:-1], # Propensity score on Y-axis
        x=-hist_treated_density, # Mirror by making negative on X-axis
        width=np.diff(bins_treated),
        orientation='h',
        marker_color=SAV_CHARCOAL,
        name='Treated',
        customdata=hist_treated_counts,
        hovertemplate='Propensity Score: %{y:.2f}<br>' +
                      'Relative Frequency: %{x:.2f}<br>' +
                      'Absolute Frequency: %{customdata:.0f}<extra></extra>'
    ))

    # Calculate separate min/max/median limits for each group
    min_ps_treated = ps_treated.min()
    max_ps_treated = ps_treated.max()
    median_ps_treated = ps_treated.median()
    min_ps_control = ps_control.min()
    max_ps_control = ps_control.max()
    median_ps_control = ps_control.median()

    # Add horizontal lines for treated group min/max/median
    fig.add_hline(y=min_ps_treated, line_width=1.5, line_dash='dot', line_color='darkblue', annotation_text=f'Treated Min ({min_ps_treated:.2f})', annotation_position='bottom right')
    fig.add_hline(y=max_ps_treated, line_width=1.5, line_dash='dot', line_color='darkblue', annotation_text=f'Treated Max ({max_ps_treated:.2f})', annotation_position='top right')
    fig.add_hline(y=median_ps_treated, line_width=1.5, line_dash='dash', line_color='darkblue', annotation_text=f'Treated Median ({median_ps_treated:.2f})', annotation_position='right')

    # Add horizontal lines for control group min/max/median
    fig.add_hline(y=min_ps_control, line_width=1.5, line_dash='dot', line_color=SAV_GREEN, annotation_text=f'Control Min ({min_ps_control:.2f})', annotation_position='bottom left')
    fig.add_hline(y=max_ps_control, line_width=1.5, line_dash='dot', line_color=SAV_GREEN, annotation_text=f'Control Max ({max_ps_control:.2f})', annotation_position='top left')
    fig.add_hline(y=median_ps_control, line_width=1.5, line_dash='dash', line_color=SAV_GREEN, annotation_text=f'Control Median ({median_ps_control:.2f})', annotation_position='left')

    fig.update_layout(
        title_text=title,
        xaxis_title='Frequency (Density)', # Swapped axis titles
        yaxis_title='Propensity Score',
        bargap=0,
        hovermode='y unified' # Changed hovermode for vertical plot
    )

    # Adjust x-axis tick labels to show absolute values (since density is now on x)
    current_max_x = max(np.max(hist_control_density), np.max(hist_treated_density))
    fig.update_xaxes(range=[-1.1 * current_max_x, 1.1 * current_max_x], showticklabels=True)

    # Customizing tick labels to show absolute values for negative ticks on the new x-axis
    current_xtickvals = list(fig.layout.xaxis.tickvals) if fig.layout.xaxis.tickvals is not None else []
    if not current_xtickvals:
        x_min, x_max = fig.layout.xaxis.range
        current_xtickvals = np.linspace(x_min, x_max, 5).tolist() # Generate 5 ticks
    new_xtickvals = sorted(list(set([t for t in current_xtickvals if t >= 0] + [-t for t in current_xtickvals if t > 0])))
    fig.update_xaxes(tickvals=new_xtickvals, ticktext=[f'{abs(t):.2f}' for t in new_xtickvals], tickmode='array')

    # Propensity score (y-axis) should always be 0-1
    fig.update_yaxes(range=[0, 1])

    return fig

def plot_propensity_score_boxplots(df, ps_column, treatment_column, title):
    """Generates boxplots for propensity scores for treated and control groups."""

    fig = go.Figure()

    # Common hover template for both boxplots
    hover_template_str = '<b>%{y.name}</b><br>Min: %{y.min:.4f}<br>Q1: %{y.q1:.4f}<br>Median: %{y.median:.4f}<br>Q3: %{y.q3:.4f}<br>Max: %{y.max:.4f}<extra></extra>'

    # Boxplot for Control Group
    fig.add_trace(go.Box(
        y=df[df[treatment_column] == 0][ps_column],
        name='Control',
        marker_color=SAV_GREEN,
        boxpoints=False,
        hovertemplate=hover_template_str
    ))

    # Boxplot for Treated Group
    fig.add_trace(go.Box(
        y=df[df[treatment_column] == 1][ps_column],
        name='Treated',
        marker_color=SAV_CHARCOAL,
        boxpoints=False,
        hovertemplate=hover_template_str
    ))

    fig.update_layout(
        title_text=title,
        yaxis_title='Propensity Score',
        showlegend=True
    )

    # Ensure y-axis is from 0 to 1 for propensity scores
    fig.update_yaxes(range=[0, 1])

    return fig


def calculate_smd(df, covariates, treatment_column):
    """Calculates Standardized Mean Differences (SMD) for covariates.

    Args:
        df (pd.DataFrame): The input DataFrame.
        covariates (list): A list of covariate column names.
        treatment_column (str): The name of the treatment column (binary: 0 or 1).

    Returns:
        pd.Series: A Series containing the SMD for each covariate.
    """

    smd_values = {}
    treated_group = df[df[treatment_column] == 1]
    control_group = df[df[treatment_column] == 0]

    for cov in covariates:
        mean_treated = treated_group[cov].mean()
        mean_control = control_group[cov].mean()
        std_treated = treated_group[cov].std()
        std_control = control_group[cov].std()

        # Pooled standard deviation (assuming unequal sample sizes)
        n_treated = len(treated_group)
        n_control = len(control_group)

        pooled_std = np.sqrt(((n_treated - 1) * std_treated**2 + (n_control - 1) * std_control**2) / (n_treated + n_control - 2))

        smd = (mean_treated - mean_control) / pooled_std
        smd_values[cov] = smd

    return pd.Series(smd_values)



def plot_love_plot(smd_series, title, subplot_fig, row, col, x_limit, dot_color=SAV_GREEN):
    """Generates a Love Plot (SMD plot) for covariate balance using Plotly.

    Args:
        smd_series (pd.Series): A Series of SMD values for covariates.
        title (str): The title for the plot. (Note: This title is now handled by make_subplots's subplot_titles)
        subplot_fig (go.Figure): The Plotly figure object to add the subplot to.
        row (int): The row index for the subplot.
        col (int): The column index for the subplot.
        x_limit (float): The maximum absolute value for the x-axis limits.
        dot_color (str): The color for the scatter plot dots.
    """
    covariates = smd_series.index.tolist()

    # Add scatter trace for SMD values
    subplot_fig.add_trace(go.Scatter(
        x=smd_series,
        y=covariates,
        mode='markers',
        marker=dict(color=dot_color, size=10),
        name='SMD',
        hovertemplate='Covariate: %{y}<br>SMD: %{x:.4f}<extra></extra>'
    ), row=row, col=col)

    # Add vertical line for SMD = 0
    subplot_fig.add_vline(x=0, line_dash="dash", line_color="gray", line_width=1, row=row, col=col)
    # Add vertical line for SMD = 0.1 (threshold)
    subplot_fig.add_vline(x=0.1, line_dash="dash", line_color="red", line_width=1.5,
                          annotation_text='SMD = 0.1', annotation_position='top right', row=row, col=col)
    # Add vertical line for SMD = -0.1 (threshold)
    subplot_fig.add_vline(x=-0.1, line_dash="dash", line_color="red", line_width=1.5,
                          annotation_text='SMD = -0.1', annotation_position='top left', row=row, col=col)

    # Update layout for the specific subplot's axes
    subplot_fig.update_xaxes(title_text='Standardized Mean Difference', range=[-x_limit, x_limit], row=row, col=col)
    subplot_fig.update_yaxes(title_text='Covariate', categoryorder='array', categoryarray=covariates, row=row, col=col)
    # Removed subplot_fig.update_layout(title_text=title, row=row, col=col) as 'row' is not a valid layout property

    return subplot_fig


def draw_causal_dag(edges, title):
    """Draws a causal DAG from a list of edges.
    
    Args:
        edges: List of tuples representing edges in the DAG, e.g., [('A', 'B'), ('B', 'C')]
        title: Title for the plot
    """
    G = nx.DiGraph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 4))
    nx.draw(G, pos, with_labels=True, node_size=3500, node_color=SAV_GREEN, 
            font_size=10, font_weight='bold', arrowsize=20, connectionstyle='arc3, rad=0.1')
    plt.title(title)
    plt.show()


def extract_tree_rules(interpreter, feature_names):
    """Extracts segmentation rules and CATE estimates from a decision tree interpreter.
    
    Args:
        interpreter: A SingleTreeCateInterpreter object with a fitted tree_model_
        feature_names: List of feature names corresponding to the tree features
        
    Returns:
        List of dictionaries with keys: 'rule', 'cate', 'n_samples'
    """
    tree_ = interpreter.tree_model_.tree_
    feature_name = [feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!" for i in tree_.feature]
    
    def recurse(node, parent_rule=""):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            rule_left = f"{parent_rule} & {name} <= {threshold:.2f}" if parent_rule else f"{name} <= {threshold:.2f}"
            rule_right = f"{parent_rule} & {name} > {threshold:.2f}" if parent_rule else f"{name} > {threshold:.2f}"
            return recurse(tree_.children_left[node], rule_left) + recurse(tree_.children_right[node], rule_right)
        else:
            return [{'rule': parent_rule or "All", 'cate': tree_.value[node][0][0], 'n_samples': tree_.n_node_samples[node]}]
    
    return recurse(0)


def extract_tree_rules_native(interpreter, feature_names):
    """Extracts segmentation rules and CATE estimates from a decision tree interpreter (native version).
    
    Similar to extract_tree_rules but uses "Global" instead of "All" for the default rule.
    
    Args:
        interpreter: A SingleTreeCateInterpreter object with a fitted tree_model_
        feature_names: List of feature names corresponding to the tree features
        
    Returns:
        List of dictionaries with keys: 'rule', 'cate', 'n_samples'
    """
    tree_ = interpreter.tree_model_.tree_
    feature_name = [feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!" for i in tree_.feature]
    def recurse(node, parent_rule=""):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            rule_left = f"{parent_rule} & {name} <= {threshold:.2f}" if parent_rule else f"{name} <= {threshold:.2f}"
            rule_right = f"{parent_rule} & {name} > {threshold:.2f}" if parent_rule else f"{name} > {threshold:.2f}"
            return recurse(tree_.children_left[node], rule_left) + recurse(tree_.children_right[node], rule_right)
        else:
            return [{'rule': parent_rule or "Global", 'cate': tree_.value[node][0][0], 'n_samples': tree_.n_node_samples[node]}]
    return recurse(0)


def get_pdp_speed(model, X_data, feature_name):
    """Gets partial dependence plot data for a causal forest model.
    
    Args:
        model: A fitted causal forest model with an .effect() method
        X_data: DataFrame with feature columns (dummy-encoded)
        feature_name: Prefix of feature columns to analyze (e.g., 'Road_Condition')
        
    Returns:
        labels: List of feature value labels
        effects: List of average treatment effects for each feature value
    """
    unique_vals = [c for c in X_data.columns if c.startswith(feature_name)]
    labels = [c.split('_')[-1] for c in unique_vals]
    effects = []
    for col in unique_vals:
        X_tmp = X_data.copy(); X_tmp.iloc[:, :] = 0; X_tmp[col] = 1
        effects.append(np.mean(model.effect(X_tmp)))
    return labels, effects


def encode_categorical_for_causal_forest(df, columns, drop_first=True):
    """Encode categorical variables for CausalForestDML compatibility.
    
    This function ensures categorical variables are properly one-hot encoded
    as numeric factors that work with sklearn models used by CausalForestDML.
    
    Args:
        df: DataFrame containing the columns to encode
        columns: List of column names to encode (can be string or list)
        drop_first: Whether to drop the first category to avoid multicollinearity
        
    Returns:
        DataFrame with one-hot encoded categorical variables (all numeric dtypes)
    """
    if isinstance(columns, str):
        columns = [columns]
    
    # Filter to only columns that exist in dataframe
    available_cols = [col for col in columns if col in df.columns]
    if not available_cols:
        raise ValueError(f"None of the specified columns {columns} found in dataframe")
    
    # One-hot encode categorical columns
    encoded = pd.get_dummies(df[available_cols], drop_first=drop_first, dtype=float)
    
    # Ensure all columns are numeric (float64) for sklearn compatibility
    encoded = encoded.astype(float)
    
    return encoded


# =========================================================================== #
# Causal graphs as embeddable SVG figures
# =========================================================================== #

# Colour palette for the different roles a node can play in a causal DAG.
# Built from the SAV/ASA brand palette and tuned to read on BOTH the light and
# the dark Jupyter Book theme. The figures are saved with a transparent
# background and embedded as <img> (so page CSS cannot reach their internals);
# the only way to stay legible on a dark page is to make every node a *light*
# box with *dark* text. The focus nodes (treatment / sensitive attribute) keep
# the bright brand green — light enough to read against a dark background — while
# the remaining roles use light greys with charcoal text.
_DAG_TEXT_GREEN = '#2c3608'   # dark olive, readable on the lime-green faces
_DAG_TEXT_DARK = '#2e2f2e'    # near-charcoal text for the grey faces
_DAG_PALETTE = {
    'treatment':  dict(face=SAV_GREEN,       edge=SAV_GREEN_DARK, text=_DAG_TEXT_GREEN, dashed=False),
    'outcome':    dict(face='#D4D7D4',       edge=SAV_CHARCOAL,   text=SAV_CHARCOAL,    dashed=False),
    'confounder': dict(face='#BFC2BF',       edge=SAV_CHARCOAL,   text=_DAG_TEXT_DARK,  dashed=False),
    'covariate':  dict(face=SAV_GREY_LIGHT,  edge=SAV_GREY,       text=_DAG_TEXT_DARK,  dashed=False),
    'mediator':   dict(face=SAV_GREEN_LIGHT, edge=SAV_GREEN_DARK, text=_DAG_TEXT_GREEN, dashed=False),
    'collider':   dict(face='#D4D7D4',       edge=SAV_CHARCOAL,   text=SAV_CHARCOAL,    dashed=False),
    'sensitive':  dict(face=SAV_GREEN,       edge=SAV_GREEN_DARK, text=_DAG_TEXT_GREEN, dashed=False),
    'unobserved': dict(face='none',          edge=SAV_GREY,       text=SAV_GREY,        dashed=True),
}

# Neutral "ink" colour for arrows, titles and legends. A mid brand grey keeps
# these elements legible on both the light and the dark Jupyter Book theme
# (the figures are saved with a transparent background, so the page colour
# always shows through).
_DAG_INK = SAV_GREY


def draw_causal_graph_svg(edges, positions, node_styles, filepath, title=None,
                          figsize=(7.2, 4.8), node_radius=0.18, font_size=13,
                          legend_types=None):
    """Render a causal DAG to a stand-alone ``.svg`` file and return its path.

    The resulting vector graphic can be embedded directly in a notebook with
    ``IPython.display.SVG(filepath)`` so that it appears crisply in the rendered
    Jupyter Book.

    Args:
        edges: Iterable of edges. Each edge is ``(src, dst)`` for a causal arrow
            or ``(src, dst, kind)`` where ``kind`` is ``'causal'`` (solid black)
            or ``'biasing'`` (dashed red — e.g. a confounding path).
        positions: Dict mapping each node name to an ``(x, y)`` coordinate.
        node_styles: Dict mapping each node name to a role in ``_DAG_PALETTE``
            (``'treatment'``, ``'outcome'``, ``'confounder'``, ``'covariate'``,
            ``'mediator'``, ``'collider'`` or ``'unobserved'``).
        filepath: Destination path for the ``.svg`` file (folders are created).
        title: Optional figure title.
        figsize: Figure size in inches.
        node_radius: Radius of each node circle in data coordinates.
        font_size: Font size for node labels.
        legend_types: Optional list of role keys to display as a legend.

    Returns:
        The ``filepath`` that was written.
    """
    fig, ax = plt.subplots(figsize=figsize)

    # --- Edges ---------------------------------------------------------- #
    for edge in edges:
        if len(edge) == 3:
            src, dst, kind = edge
        else:
            src, dst = edge
            kind = 'causal'
        x0, y0 = positions[src]
        x1, y1 = positions[dst]
        dx, dy = x1 - x0, y1 - y0
        dist = np.hypot(dx, dy)
        if dist == 0:
            continue
        ux, uy = dx / dist, dy / dist
        start = (x0 + ux * node_radius, y0 + uy * node_radius)
        end = (x1 - ux * node_radius, y1 - uy * node_radius)
        if kind == 'biasing':
            color, style = '#d62728', (0, (5, 4))
        else:
            color, style = _DAG_INK, 'solid'
        ax.add_patch(FancyArrowPatch(
            start, end, arrowstyle='-|>', mutation_scale=16,
            color=color, lw=1.8, linestyle=style, zorder=1,
            connectionstyle='arc3,rad=0.0'))

    # --- Nodes ---------------------------------------------------------- #
    for node, (x, y) in positions.items():
        st = _DAG_PALETTE[node_styles.get(node, 'covariate')]
        ax.add_patch(Circle(
            (x, y), node_radius, facecolor=st['face'], edgecolor=st['edge'],
            lw=2, linestyle='--' if st['dashed'] else '-', zorder=2))
        ax.text(x, y, node, ha='center', va='center', color=st['text'],
                fontsize=font_size, fontweight='bold', zorder=3)

    # --- Axes / title / legend ------------------------------------------ #
    xs = [p[0] for p in positions.values()]
    ys = [p[1] for p in positions.values()]
    pad = node_radius * 2.8
    ax.set_xlim(min(xs) - pad, max(xs) + pad)
    ax.set_ylim(min(ys) - pad, max(ys) + pad)
    ax.set_aspect('equal')
    ax.axis('off')
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', color=_DAG_INK)

    if legend_types:
        from matplotlib.lines import Line2D
        handles = []
        for key in legend_types:
            st = _DAG_PALETTE[key]
            handles.append(Line2D(
                [0], [0], marker='o', linestyle='None', markersize=11,
                markerfacecolor=st['face'], markeredgecolor=st['edge'],
                label=key.capitalize()))
        ax.legend(handles=handles, loc='upper center',
                  bbox_to_anchor=(0.5, -0.02), ncol=len(handles),
                  frameon=False, fontsize=9, labelcolor=_DAG_INK)

    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)
    fig.savefig(filepath, format='svg', bbox_inches='tight', transparent=True)
    plt.close(fig)
    return filepath


# =========================================================================== #
# Estimation helpers (OLS / propensity / IPW)
# =========================================================================== #

def ols_treatment_effect(df, outcome, treatment, covariates):
    """Estimate a regression-adjusted treatment effect via ordinary least squares.

    Returns a dict with the treatment coefficient, its standard error,
    t-statistic, two-sided p-value and the residual degrees of freedom — the
    latter is needed for the partial-:math:`R^2` sensitivity analysis.

    The covariates are standardised before fitting purely for numerical
    stability (variables on very different scales can overflow ``matmul`` on
    some BLAS backends). Standardising the covariates leaves the treatment
    coefficient and its standard error unchanged.
    """
    Xc = df[list(covariates)].astype(float).values
    mean = Xc.mean(axis=0)
    std = Xc.std(axis=0)
    std[std == 0] = 1.0  # guard against constant columns
    Xc = (Xc - mean) / std

    t = df[treatment].astype(float).values.reshape(-1, 1)
    X = np.column_stack([np.ones(len(df)), t, Xc])
    y = df[outcome].astype(float).values

    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = len(y) - X.shape[1]
    sigma2 = (resid @ resid) / dof
    cov = sigma2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))

    idx = 1  # treatment is the first column after the intercept
    tstat = beta[idx] / se[idx]
    pval = 2 * (1 - tdist.cdf(abs(tstat), dof))
    return {'coef': beta[idx], 'se': se[idx], 't': tstat, 'p': pval, 'dof': dof}


def estimate_propensity(df, treatment, covariates, max_iter=1000):
    """Fit a logistic-regression propensity model and return P(T=1 | X).

    Covariates are standardised before fitting so that variables on very
    different scales (e.g. X1 ~ 40, X3 in [0, 100]) do not cause numerical
    overflow in the optimiser.
    """
    X = df[covariates].astype(float).values
    mean = X.mean(axis=0)
    std = X.std(axis=0)
    std[std == 0] = 1.0  # guard against constant columns
    X_scaled = (X - mean) / std
    model = LogisticRegression(max_iter=max_iter)
    model.fit(X_scaled, df[treatment].astype(int).values)
    return model.predict_proba(X_scaled)[:, 1]


def ipw_ate(df, treatment, outcome, ps, stabilized=True):
    """Inverse-probability-weighted ATE. ``ps`` is an array of propensity scores."""
    t = df[treatment].astype(int).values
    y = df[outcome].astype(float).values
    ps = np.asarray(ps, dtype=float)
    if stabilized:
        pt = t.mean()
        w = np.where(t == 1, pt / ps, (1 - pt) / (1 - ps))
    else:
        w = np.where(t == 1, 1.0 / ps, 1.0 / (1.0 - ps))
    ate = (np.sum(w * t * y) / np.sum(w * t)
           - np.sum(w * (1 - t) * y) / np.sum(w * (1 - t)))
    return ate, w


def trim_common_support(df, ps, eps=0.05):
    """Restrict to the overlap region by trimming units with extreme propensity.

    Returns ``(trimmed_df, ps_trimmed, keep_mask)``.
    """
    ps = np.asarray(ps, dtype=float)
    keep = (ps > eps) & (ps < 1 - eps)
    return df.loc[keep].copy(), ps[keep], keep


def overlap_weighted_ate(df, treatment, outcome, ps):
    """ATE estimated with Li-Morgan-Zaslavsky overlap weights (focal: overlap population)."""
    t = df[treatment].astype(int).values
    y = df[outcome].astype(float).values
    ps = np.asarray(ps, dtype=float)
    w = np.where(t == 1, 1 - ps, ps)
    ate = (np.sum(w * t * y) / np.sum(w * t)
           - np.sum(w * (1 - t) * y) / np.sum(w * (1 - t)))
    return ate, w


def calculate_smd_weighted(df, covariates, treatment, weights):
    """Standardised mean differences after applying weights (for balance checks)."""
    t = df[treatment].astype(int).values
    w = np.asarray(weights, dtype=float)
    out = {}
    for cov in covariates:
        x = df[cov].astype(float).values
        wt, wc = w[t == 1], w[t == 0]
        xt, xc = x[t == 1], x[t == 0]
        mt = np.average(xt, weights=wt)
        mc = np.average(xc, weights=wc)
        vt = np.average((xt - mt) ** 2, weights=wt)
        vc = np.average((xc - mc) ** 2, weights=wc)
        pooled = np.sqrt((vt + vc) / 2)
        out[cov] = (mt - mc) / pooled if pooled > 0 else 0.0
    return pd.Series(out)


# =========================================================================== #
# Assumption diagnostics
# =========================================================================== #

def consistency_diagnostic(df, treatment, outcome, subtype_col, covariates):
    """Probe {prf:ref}`consistency` by re-estimating the effect per treatment sub-type.

    A well-defined treatment should yield a stable effect across sub-types. Each
    sub-type's treated units are compared against the *common* control group with
    regression adjustment. Large variation flags an ambiguous (multi-version)
    treatment.
    """
    rows = []
    overall = ols_treatment_effect(df, outcome, treatment, covariates)
    rows.append({'Group': 'Overall (pooled)', 'Effect': overall['coef'],
                 'Std. Error': overall['se'], 'n_treated': int((df[treatment] == 1).sum())})

    controls = df[df[treatment] == 0]
    for s in sorted(df.loc[df[treatment] == 1, subtype_col].unique()):
        treated_s = df[(df[treatment] == 1) & (df[subtype_col] == s)]
        sub = pd.concat([treated_s, controls])
        res = ols_treatment_effect(sub, outcome, treatment, covariates)
        rows.append({'Group': f'Sub-type {s}', 'Effect': res['coef'],
                     'Std. Error': res['se'], 'n_treated': len(treated_s)})
    return pd.DataFrame(rows)


def interference_diagnostic(df, cluster_col, treatment, outcome):
    """Probe {prf:ref}`sutva` by correlating control outcomes with neighbours' treatment.

    For each unit we compute the leave-one-out treatment intensity in its cluster.
    Under no interference, control units' outcomes should be uncorrelated with how
    treated their cluster is. A significant correlation signals spillover.

    Returns ``(pearson_r, p_value, control_frame)``.
    """
    csum = df.groupby(cluster_col)[treatment].transform('sum')
    csize = df.groupby(cluster_col)[treatment].transform('count')
    loo_intensity = (csum - df[treatment]) / (csize - 1).clip(lower=1)

    ctrl = df[df[treatment] == 0].copy()
    ctrl['cluster_treat_intensity'] = loo_intensity[df[treatment] == 0].values
    r, p = pearsonr(ctrl['cluster_treat_intensity'], ctrl[outcome])
    return r, p, ctrl


def negative_control_test(df, neg_control_outcome, treatment, covariates):
    """Placebo / negative-control test: the treatment should have *no* effect here.

    A statistically significant effect on an outcome that the treatment cannot
    plausibly affect signals residual confounding (a violation of
    {prf:ref}`exchangeability`).
    """
    return ols_treatment_effect(df, neg_control_outcome, treatment, covariates)


# =========================================================================== #
# Sensitivity analysis for unmeasured confounding
# =========================================================================== #

def e_value(rr):
    """E-value for a risk ratio (VanderWeele & Ding, 2017)."""
    rr = float(rr)
    if rr < 1:
        rr = 1.0 / rr
    return rr + np.sqrt(rr * (rr - 1))


def e_value_from_effect(coef, se, sd_outcome, ci_mult=1.96):
    """E-value for a continuous effect, via the standardised-mean-difference → RR map.

    Uses the approximation ``RR ≈ exp(0.91 * d)`` where ``d`` is the standardised
    effect size (VanderWeele, 2017). Returns the E-value for the point estimate
    and for the confidence-interval limit nearest the null.
    """
    d = coef / sd_outcome
    rr_point = np.exp(0.91 * d)
    lo = (coef - ci_mult * se) / sd_outcome
    hi = (coef + ci_mult * se) / sd_outcome
    rr_lo, rr_hi = np.exp(0.91 * lo), np.exp(0.91 * hi)
    # If the confidence interval crosses RR = 1 the E-value for the limit is 1
    # (the observed association is already compatible with the null).
    if min(rr_lo, rr_hi) <= 1 <= max(rr_lo, rr_hi):
        rr_ci, ev_ci = 1.0, 1.0
    elif rr_point >= 1:
        rr_ci = min(rr_lo, rr_hi)   # limit closest to the null from above
        ev_ci = e_value(rr_ci)
    else:
        rr_ci = max(rr_lo, rr_hi)   # limit closest to the null from below
        ev_ci = e_value(rr_ci)
    return {'rr_point': rr_point, 'e_value': e_value(rr_point),
            'rr_ci': rr_ci, 'e_value_ci': ev_ci}


def robustness_value(t_stat, dof, q=1.0):
    """Cinelli & Hazlett (2020) robustness value (RV) for reducing the effect by ``q``.

    The RV is the partial :math:`R^2` that an unmeasured confounder would need to
    have with *both* treatment and outcome to bring the estimate to ``(1-q)`` of
    its value (q=1 → to zero).
    """
    f = abs(t_stat) / np.sqrt(dof)
    fq = q * f
    return 0.5 * (np.sqrt(fq ** 4 + 4 * fq ** 2) - fq ** 2)


def adjusted_estimate(coef, se, dof, r2_tu, r2_yu):
    """Cinelli & Hazlett bias-adjusted estimate given confounder partial-R² strengths."""
    r2_tu = np.clip(r2_tu, 0, 0.999)
    bias = se * np.sqrt(dof) * np.sqrt((r2_yu * r2_tu) / (1 - r2_tu))
    return np.sign(coef) * (abs(coef) - bias)


def plot_sensitivity_contour(coef, se, dof, title='Sensitivity Contours',
                             grid=40, benchmark=None):
    """Plotly contour of the bias-adjusted estimate over a grid of confounder strengths."""
    r2_vals = np.linspace(0, 0.6, grid)
    Z = np.array([[adjusted_estimate(coef, se, dof, rt, ry) for rt in r2_vals]
                  for ry in r2_vals])
    fig = go.Figure(data=go.Contour(
        z=Z, x=r2_vals, y=r2_vals,
        colorscale=[[0.0, SAV_CHARCOAL], [0.5, "#EDEDEA"], [1.0, SAV_GREEN]],
        contours=dict(showlabels=True),
        colorbar=dict(title='Adjusted<br>effect')))
    # Highlight the line where the effect is driven to zero
    fig.add_trace(go.Contour(
        z=Z, x=r2_vals, y=r2_vals, showscale=False,
        contours=dict(start=0, end=0, coloring='lines'),
        line=dict(color='black', width=3), name='effect = 0'))
    fig.add_trace(go.Scatter(
        x=[0], y=[0], mode='markers+text', text=['Unadjusted'],
        textposition='top right', marker=dict(color='black', size=10),
        name='Observed estimate'))
    if benchmark is not None:
        fig.add_trace(go.Scatter(
            x=[benchmark['r2_tu']], y=[benchmark['r2_yu']],
            mode='markers+text', text=[benchmark.get('label', 'benchmark')],
            textposition='top right',
            textfont=dict(color=SAV_CHARCOAL),
            marker=dict(color=SAV_CHARCOAL, size=13, symbol='diamond',
                        line=dict(color='white', width=1.5)),
            name='Benchmark covariate'))
    fig.update_layout(
        title_text=title,
        xaxis_title='Partial R² of confounder with Treatment',
        yaxis_title='Partial R² of confounder with Outcome',
        legend=dict(bgcolor='rgba(255,255,255,0.85)', bordercolor=SAV_GREY,
                    borderwidth=1, font=dict(color=SAV_CHARCOAL)))
    return fig


def rosenbaum_sensitivity(differences, gammas):
    """Rosenbaum bounds (sign-test version) for matched-pair differences.

    For each :math:`\\Gamma`, returns the worst-case (upper-bound) one-sided
    p-value for the null of no effect. The largest :math:`\\Gamma` keeping the
    p-value below the significance level is the *critical* :math:`\\Gamma`.
    """
    diffs = np.asarray(differences, dtype=float)
    diffs = diffs[diffs != 0]
    n = len(diffs)
    t_obs = int(np.sum(diffs > 0))
    rows = []
    for g in gammas:
        p_plus = g / (1 + g)
        mu = n * p_plus
        sd = np.sqrt(n * p_plus * (1 - p_plus))
        z = (t_obs - mu) / sd
        rows.append({'Gamma': g, 'p_upper_bound': float(1 - norm.cdf(z))})
    return pd.DataFrame(rows)


def plot_rosenbaum(bounds_df, alpha=0.05, title='Rosenbaum Sensitivity Bounds'):
    """Plot worst-case p-value vs. the sensitivity parameter Gamma."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=bounds_df['Gamma'], y=bounds_df['p_upper_bound'],
        mode='lines+markers', line=dict(color=SAV_GREEN, width=2),
        name='Worst-case p-value'))
    fig.add_hline(y=alpha, line_dash='dash', line_color='red',
                  annotation_text=f'α = {alpha}', annotation_position='bottom right')
    fig.update_layout(
        title_text=title, xaxis_title='Γ (allowed confounding)',
        yaxis_title='Upper-bound p-value', yaxis_range=[0, 1])
    return fig

def show(fig):
    """Display a Plotly figure that auto-resizes to the page width."""
    import plotly.offline
    fig.update_layout(autosize=True, width=None)
    plotly.offline.iplot(fig, config={"responsive": True})