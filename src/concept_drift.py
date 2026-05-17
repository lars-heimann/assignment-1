"""Concept drift detection analysis for BPIC-17."""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from scipy import stats

from src.config import (
    ACTIVITY_COL,
    CASE_COL,
    FIGURES_DIR,
    TIMESTAMP_COL,
)
from src.statistics import get_case_durations

QUARTER_LABELS = ["Q1-2016", "Q2-2016", "Q3-2016", "Q4-2016"]


def assign_quarters(log: pd.DataFrame) -> pd.DataFrame:
    """Add a 'quarter' column based on case start time."""
    case_start = log.groupby(CASE_COL)[TIMESTAMP_COL].min()
    quarters = pd.cut(case_start, bins=4, labels=QUARTER_LABELS)
    quarters.name = "quarter"
    return log.join(quarters, on=CASE_COL)


def activity_distribution_by_quarter(log_q: pd.DataFrame) -> pd.DataFrame:
    """Compute normalised activity distributions per quarter."""
    counts = log_q.groupby(["quarter", ACTIVITY_COL]).size().unstack(fill_value=0)
    return counts.div(counts.sum(axis=1), axis=0)


def plot_activity_drift(activity_norm: pd.DataFrame) -> Figure:
    """Bar chart of activity proportions per quarter."""
    fig, ax = plt.subplots(figsize=(14, 6))
    activity_norm.T.plot(kind="bar", ax=ax, width=0.8)
    ax.set_xlabel("Activity")
    ax.set_ylabel("Proportion")
    ax.set_title("Activity Distribution by Quarter (Concept Drift)")
    ax.legend(title="Quarter")
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.tight_layout()
    fig.savefig(f"{FIGURES_DIR}/concept_drift_activities.png", dpi=150)
    return fig


def plot_duration_drift(log: pd.DataFrame, quarters: pd.Series) -> Figure:
    """Overlaid histograms of case duration per quarter."""
    case_durations = get_case_durations(log)
    dur_df = case_durations.to_frame("duration_sec").join(quarters)
    dur_df["duration_days"] = dur_df["duration_sec"] / 86400

    fig, ax = plt.subplots(figsize=(10, 5))
    for q in QUARTER_LABELS:
        subset = dur_df[dur_df["quarter"] == q]["duration_days"]
        ax.hist(
            subset,
            bins=40,
            alpha=0.5,
            label=f"{q} (n={len(subset)}, mean={subset.mean():.1f}d)",
        )
    ax.set_xlabel("Case Duration (days)")
    ax.set_ylabel("Frequency")
    ax.set_title("Case Duration Distribution by Quarter")
    ax.legend()
    plt.tight_layout()
    fig.savefig(f"{FIGURES_DIR}/concept_drift_durations.png", dpi=150)
    return fig


def plot_amount_drift(log: pd.DataFrame, quarters: pd.Series) -> Figure:
    """Box plot of RequestedAmount per quarter."""
    case_amt = log.groupby(CASE_COL)["case:RequestedAmount"].first()
    amt_df = case_amt.to_frame().join(quarters)

    fig, ax = plt.subplots(figsize=(10, 5))
    data = [
        amt_df[amt_df["quarter"] == q]["case:RequestedAmount"].dropna()
        for q in QUARTER_LABELS
    ]
    ax.boxplot(data, tick_labels=QUARTER_LABELS)
    ax.set_ylabel("Requested Amount")
    ax.set_title("Requested Amount Distribution by Quarter")
    plt.tight_layout()
    fig.savefig(f"{FIGURES_DIR}/concept_drift_amount.png", dpi=150)
    return fig


def test_duration_drift(log: pd.DataFrame, quarters: pd.Series) -> dict:
    """Kruskal-Wallis test on case durations across quarters."""
    case_durations = get_case_durations(log)
    dur_df = case_durations.to_frame("duration_days")
    dur_df["duration_days"] = dur_df["duration_days"] / 86400
    dur_df = dur_df.join(quarters)

    groups = [
        dur_df[dur_df["quarter"] == q]["duration_days"].dropna() for q in QUARTER_LABELS
    ]
    stat, p_value = stats.kruskal(*groups)
    return {"H-statistic": stat, "p-value": p_value, "significant": p_value < 0.05}


def test_activity_drift(activity_counts: pd.DataFrame) -> dict:
    """Chi-squared test on activity distributions between Q1 and Q4."""
    contingency = pd.DataFrame(
        {"Q1": activity_counts.loc["Q1-2016"], "Q4": activity_counts.loc["Q4-2016"]}
    )
    chi2, p_val, dof, _ = stats.chi2_contingency(contingency.T)
    return {"chi2": chi2, "p-value": p_val, "dof": dof, "significant": p_val < 0.05}


def test_amount_drift(log: pd.DataFrame, quarters: pd.Series) -> dict:
    """Kruskal-Wallis test on RequestedAmount across quarters."""
    case_amt = log.groupby(CASE_COL)["case:RequestedAmount"].first()
    amt_df = case_amt.to_frame().join(quarters)

    groups = [
        amt_df[amt_df["quarter"] == q]["case:RequestedAmount"].dropna()
        for q in QUARTER_LABELS
    ]
    stat, p_val = stats.kruskal(*groups)
    return {"H-statistic": stat, "p-value": p_val, "significant": p_val < 0.05}
