"""Plot style helpers used across notebooks.

phinx: Sphinx documentation tool.
"""

from __future__ import annotations

from typing import Any, Dict


def apply_plot_style() -> None:
    """Apply consistent matplotlib/seaborn styling.

    :returns: None.
    :rtype: None
    """
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    mpl.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "black",
            "axes.labelcolor": "black",
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "xtick.color": "black",
            "ytick.color": "black",
            "grid.color": "0.85",
            "grid.alpha": 0.5,
            "font.size": 10,
            "savefig.dpi": 140,
        }
    )

    try:
        import seaborn as sns

        sns.set_theme(style="whitegrid")
    except Exception:
        pass


DEFAULT_LINESTYLES: Dict[str, str] = {
    "primary": "-",
    "secondary": "--",
    "tertiary": ":",
}

DEFAULT_MARKERS: Dict[str, str] = {
    "primary": "o",
    "secondary": "s",
    "tertiary": "^",
}


def _normalize_period_value(value: str, period_col: str) -> "pd.Period":
    import pandas as pd

    if isinstance(value, pd.Period):
        return value
    if period_col == "month":
        return pd.Period(value, freq="M")
    if period_col == "quarter":
        return pd.Period(value, freq="Q")
    return pd.Period(value)


def counts_for_period(terms_df, period_value: str, period_col: str) -> "pd.DataFrame":
    """Aggregate term counts per newspaper for a given period.

    :param terms_df: DataFrame with at least newspaper_name, begriff, and period_col.
    :param period_value: Period label (e.g., 2023Q2 or 2023-06).
    :param period_col: Column containing pandas Period values.
    :returns: Counts table (index newspaper_name, columns begriff).
    """
    import pandas as pd

    target = _normalize_period_value(period_value, period_col)
    if pd.api.types.is_period_dtype(terms_df[period_col]):
        mask = terms_df[period_col] == target
    else:
        mask = terms_df[period_col] == period_value
    subset = terms_df.loc[mask]
    return (
        subset.groupby("newspaper_name")["begriff"].value_counts().unstack(fill_value=0)
    )


def shares_from_counts(counts_df: "pd.DataFrame") -> "pd.DataFrame":
    """Convert term counts to row-wise percentage shares."""
    totals = counts_df.sum(axis=1).replace(0, 1)
    return counts_df.div(totals, axis=0) * 100


def delta_between_periods(
    terms_df,
    period_a: str,
    period_b: str,
    period_col: str,
) -> "pd.DataFrame":
    """Compute delta in shares between two periods per newspaper.

    :returns: DataFrame with delta_{term} columns and total_sum for sizing.
    """
    import pandas as pd

    counts_a = counts_for_period(terms_df, period_a, period_col)
    counts_b = counts_for_period(terms_df, period_b, period_col)

    papers = sorted(set(counts_a.index).union(counts_b.index))
    counts_a = counts_a.reindex(papers, fill_value=0)
    counts_b = counts_b.reindex(papers, fill_value=0)

    shares_a = shares_from_counts(counts_a)
    shares_b = shares_from_counts(counts_b)

    terms = sorted(set(shares_a.columns).union(shares_b.columns))
    shares_a = shares_a.reindex(columns=terms, fill_value=0)
    shares_b = shares_b.reindex(columns=terms, fill_value=0)

    df_delta = pd.DataFrame({"newspaper_name": papers})
    for term in terms:
        df_delta[f"delta_{term}"] = shares_b[term].values - shares_a[term].values

    df_delta["total_sum"] = counts_a.sum(axis=1).values + counts_b.sum(axis=1).values
    return df_delta


def scatter_delta(
    dfc,
    term_x: str,
    term_y: str,
    title: str,
    *,
    plot_dir=None,
    outname: str | None = None,
    label_threshold: int = 20,
    size_scale: float = 12,
) -> None:
    """Scatter plot for delta shares of two terms."""
    import os

    import matplotlib.pyplot as plt
    import numpy as np

    x = dfc[f"delta_{term_x}"]
    y = dfc[f"delta_{term_y}"]

    fig, ax = plt.subplots(figsize=(12, 9))

    total_sum = dfc.get("total_sum")
    if total_sum is None:
        total_sum = np.ones(len(dfc))

    sizes = np.clip(np.sqrt(total_sum), 1, 200) * size_scale
    ax.axhline(0, color="black", linewidth=1.0)
    ax.axvline(0, color="black", linewidth=1.0)
    ax.scatter(
        x,
        y,
        s=sizes,
        facecolors="0.75",
        edgecolors="0.35",
        linewidths=0.6,
        alpha=0.7,
    )

    label_dset = dfc[total_sum > label_threshold]
    for _, row in label_dset.iterrows():
        dx = row[f"delta_{term_x}"]
        dy = row[f"delta_{term_y}"]
        ax.annotate(
            row["newspaper_name"],
            xy=(dx, dy),
            xytext=(6, 6),
            textcoords="offset points",
            fontsize=8,
            ha="left",
            va="bottom",
            color="black",
        )

    ax.set_xlabel(f"Delta {term_x} (pp)")
    ax.set_ylabel(f"Delta {term_y} (pp)")
    ax.set_title(title)
    ax.grid(True, alpha=0.5)

    legend_vals = np.quantile(total_sum, [0.25, 0.6, 0.9])
    legend_vals = np.unique(np.round(legend_vals).astype(int))
    legend_vals = [v for v in legend_vals if v > 0]
    if legend_vals:
        handles = [
            plt.scatter(
                [],
                [],
                s=np.clip(np.sqrt(v), 1, 200) * size_scale,
                facecolors="0.75",
                edgecolors="0.35",
                linewidths=0.6,
                alpha=0.7,
            )
            for v in legend_vals
        ]
        ax.legend(handles, [str(v) for v in legend_vals], title="total_sum")

    plt.tight_layout()
    if outname and plot_dir is not None:
        outpath = os.path.join(plot_dir, outname)
        plt.savefig(outpath, dpi=300, bbox_inches="tight")
        print("Grafik gespeichert:", outpath)
    plt.show()
