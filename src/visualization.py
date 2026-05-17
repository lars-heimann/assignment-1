"""Plotting functions for BPIC-17 analysis."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

from src.config import FIGURES_DIR, TIMESTAMP_COL

sns.set_style("whitegrid")


def plot_case_distributions(
    case_lengths: pd.Series, case_durations: pd.Series
) -> Figure:
    """Plot case length and duration distributions side by side."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].hist(case_lengths, bins=50, edgecolor="black", alpha=0.7, color="steelblue")
    axes[0].axvline(
        case_lengths.mean(),
        color="red",
        linestyle="--",
        label=f"Mean: {case_lengths.mean():.1f} events",
    )
    axes[0].axvline(
        case_lengths.median(),
        color="darkorange",
        linestyle="-.",
        label=f"Median: {case_lengths.median():.1f} events",
    )
    axes[0].set_xlabel("Case Length (events)")
    axes[0].set_ylabel("Frequency")
    axes[0].set_title("Distribution of Case Lengths")
    axes[0].legend()

    duration_days = case_durations / 86400
    axes[1].hist(
        duration_days, bins=50, edgecolor="black", alpha=0.7, color="steelblue"
    )
    axes[1].axvline(
        duration_days.mean(),
        color="red",
        linestyle="--",
        label=f"Mean: {duration_days.mean():.1f} days",
    )
    axes[1].axvline(
        duration_days.median(),
        color="darkorange",
        linestyle="-.",
        label=f"Median: {duration_days.median():.1f} days",
    )
    axes[1].set_xlabel("Case Duration (days)")
    axes[1].set_ylabel("Frequency")
    axes[1].set_title("Distribution of Case Durations")
    axes[1].legend()

    plt.tight_layout()
    fig.savefig(f"{FIGURES_DIR}/distributions.png", dpi=150)
    return fig


def plot_activity_frequencies(activity_counts: pd.Series) -> Figure:
    """Plot horizontal bar chart of activity frequencies."""
    fig, ax = plt.subplots(figsize=(12, 7))
    top = activity_counts.head(26)
    ax.barh(range(len(top)), top.to_numpy(), color="steelblue")
    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(top.index, fontsize=9)
    ax.set_xlabel("Frequency")
    ax.set_title("Activity Frequencies (all activities)")
    ax.invert_yaxis()
    plt.tight_layout()
    fig.savefig(f"{FIGURES_DIR}/activity_frequencies.png", dpi=150)
    return fig


def plot_events_over_time(log: pd.DataFrame) -> Figure:
    """Plot monthly event counts as a bar chart."""
    log_sorted = log.sort_values(TIMESTAMP_COL)
    log_sorted["month"] = log_sorted[TIMESTAMP_COL].dt.to_period("M")
    events_per_month = log_sorted.groupby("month").size()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(
        range(len(events_per_month)),
        events_per_month.to_numpy(),
        color="steelblue",
    )
    ax.set_xticks(range(len(events_per_month)))
    ax.set_xticklabels(
        [str(p) for p in events_per_month.index], rotation=45, ha="right"
    )
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Events")
    ax.set_title("Events Over Time")
    plt.tight_layout()
    fig.savefig(f"{FIGURES_DIR}/events_over_time.png", dpi=150)
    return fig


def plot_threshold_sweep(sweep_df: pd.DataFrame) -> Figure:
    """Plot quality metrics vs. noise threshold for model selection."""
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        sweep_df["Threshold"],
        sweep_df["Fitness (log)"],
        "o-",
        color="blue",
        label="Fitness",
    )
    ax.plot(
        sweep_df["Threshold"],
        sweep_df["Precision"],
        "s-",
        color="green",
        label="Precision",
    )
    ax.plot(
        sweep_df["Threshold"],
        sweep_df["Simplicity"],
        "^-",
        color="orange",
        label="Simplicity",
    )
    ax.axhline(0.8, color="red", linestyle="--", alpha=0.5, label="80% target")
    ax.set_xlabel("Noise Threshold")
    ax.set_ylabel("Score")
    ax.set_title("Inductive Miner: Quality Metrics vs. Noise Threshold")
    ax.legend()
    ax.set_ylim(0, 1.05)

    plt.tight_layout()
    fig.savefig(f"{FIGURES_DIR}/threshold_sweep.png", dpi=150)
    return fig
