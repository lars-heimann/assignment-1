# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: aprops-ass1 (3.12.13)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # BPIC-17 Process Mining Analysis
# ## TUM - Business Process Prediction, Simulation, and Optimization (SS2026)

# %%
import os
import sys

# Add project root to path so we can import src/
sys.path.insert(0, os.path.dirname(os.getcwd()))

import pandas as pd
import pm4py
from pandas import DataFrame

from src.concept_drift import (
    activity_distribution_by_quarter,
    assign_quarters,
    plot_activity_drift,
    plot_amount_drift,
    plot_duration_drift,
    test_activity_drift,
    test_amount_drift,
    test_duration_drift,
)
from src.config import FIGURES_DIR
from src.data_loading import filter_complete_events, load_event_log
from src.decision_mining import find_xor_splits, mine_decisions
from src.discovery import (
    build_final_model,
    build_metrics_table,
    compute_all_metrics,
    discover_models,
    export_model,
    sweep_thresholds,
)
from src.statistics import (
    compute_basic_statistics,
    print_attribute_overview,
)
from src.visualization import (
    plot_activity_frequencies,
    plot_case_distributions,
    plot_events_over_time,
    plot_threshold_sweep,
)

# %matplotlib inline

# %% [markdown]
# ## 1. Load Event Log

# %%
log: DataFrame = load_event_log()
log.head()

# %% [markdown]
# ## 2. Simple Event Log Analysis (Section 3.2)

# %%
stats = compute_basic_statistics(log)
stats["summary"]

# %%
print_attribute_overview(log)

# %% [markdown]
# ### Visualizations

# %%
plot_case_distributions(stats["case_lengths"], stats["case_durations"])

# %%
plot_activity_frequencies(stats["activity_counts"])

# %%
plot_events_over_time(log)

# %% [markdown]
# ### Derived figures referenced in the report
#
# All values come from the single `compute_basic_statistics` call above.

# %%
print(f"Top 4 activity events: {stats['top4_activity_sum']} ({stats['top4_activity_share']:.2%})")
print(f"Distinct resources:        {stats['num_resources']}")
print(f"Distinct start activities: {stats['num_start_activities']}")
print(f"Distinct end activities:   {stats['num_end_activities']}")

# %% [markdown]
# ## 3. Process Model Creation and Validation (Section 3.3)
#
# ### 3.1 Filter to "complete" lifecycle events
#
# The BPIC-17 log has lifecycle transitions (start, complete, etc.). For process discovery we use only "complete" events to get a clean activity sequence per case.

# %%
log_complete: DataFrame = filter_complete_events(log)
print(f"Cases: {log_complete['case:concept:name'].nunique()}")
print(f"Activities: {log_complete['concept:name'].nunique()}")
print(f"Distinct activities: {sorted(log_complete['concept:name'].unique())}")

# %% [markdown]
# ### 3.2 Process Discovery
#
# Apply three algorithms: Inductive Miner, Heuristics Miner, and Inductive Miner (infrequent).

# %%
models = discover_models(log_complete)

# %%
# Visualize each discovered model
for net, im, fm, name in models:
    print(f"\n{'=' * 60}\n{name}\n{'=' * 60}")
    pm4py.view_petri_net(net, im, fm, format="png")

# %% [markdown]
# ### 3.3 Quality Metrics
#
# Compute fitness, precision, generalization, simplicity (PM4Py + 2 custom metrics) for all models.

# %%
metrics_df: DataFrame = build_metrics_table(log_complete, models)
metrics_df

# %% [markdown]
# ### 3.4 Threshold Sweep for Final Model Selection
#
# Sweep noise thresholds on the Inductive Miner to find the best balance of fitness (~80%), precision, and simplicity.

# %%
sweep_df: DataFrame = sweep_thresholds(log_complete)
sweep_df

# %%
plot_threshold_sweep(sweep_df)

# %% [markdown]
# ### 3.5 Final Model
#
# Build the final model, compute all metrics, and export as BPMN 2.0.

# %%
BEST_THRESHOLD: float = 0.9  # picked from the extended sweep: dominates 0.5 on precision, fitness still well above the 80% target

net_final, im_final, fm_final = build_final_model(
    log_complete, noise_threshold=BEST_THRESHOLD
)
final_metrics = compute_all_metrics(
    log_complete, net_final, im_final, fm_final, "Final Model"
)

print("Final model metrics:")
for k, v in final_metrics.items():
    if k != "Model":
        print(f"  {k:30s}: {v}")

pm4py.view_petri_net(net_final, im_final, fm_final, format="png")

# %%
# Export BPMN and Petri net image into the LaTeX figure directory
bpmn_model = export_model(net_final, im_final, fm_final, FIGURES_DIR)
pm4py.view_bpmn(bpmn_model, format="png")

# %% [markdown]
# ### 3.6 Decision Mining
#
# For each XOR gateway in the final model, train a decision tree classifier to identify which branch is taken based on case attributes.

# %%
xor_places = find_xor_splits(net_final)
print(f"Found {len(xor_places)} XOR split places in the final model")

for i, place in enumerate(xor_places):
    out_labels = [
        arc.target.label or f"tau_{arc.target.name}" for arc in place.out_arcs
    ]
    print(f"  XOR {i + 1}: {place.name} -> {out_labels}")

# %%
decision_results = mine_decisions(log_complete, net_final)

for key, result in decision_results.items():
    print(f"\n{'=' * 60}")
    print(f"{key} ({result['place']})")
    print(f"  Branches: {result['branches']}")
    print(f"  Cases: {result['n_cases']}")
    print(f"  Class distribution: {result['class_distribution']}")
    print(f"  Train accuracy: {result['train_accuracy']:.4f}")
    print(f"  Test accuracy:  {result['test_accuracy']:.4f}")
    print(f"\nDecision tree:\n{result['tree_text']}")

# %% [markdown]
# ## 4. Advanced Analysis: Concept Drift Detection (Section 3.4)
#
# **Hypothesis:** The loan application process exhibits concept drift over time -- the distribution of process behavior (activity frequencies, case durations, routing probabilities) shifts between quarters of 2016. This is relevant for simulation because a model trained on drifted data may not accurately represent the current process state.
#
# **Approach:** Split the log into time windows, compare activity distributions and case duration distributions across windows, and use statistical tests to detect significant drift.

# %%


log_q = assign_quarters(log_complete)

print("Cases per quarter:")
print(log_q.groupby("quarter")["case:concept:name"].nunique())

# %%

# Activity distribution drift
activity_norm = activity_distribution_by_quarter(log_q)
plot_activity_drift(activity_norm)

# %%
# Duration drift
quarters = (
    log_complete.groupby("case:concept:name")["time:timestamp"]
    .min()
    .pipe(
        lambda s: pd.cut(s, bins=4, labels=["Q1-2016", "Q2-2016", "Q3-2016", "Q4-2016"])
    )
)
quarters.name = "quarter"

plot_duration_drift(log_complete, quarters)

# %%

# RequestedAmount drift
plot_amount_drift(log_complete, quarters)

# %% [markdown]
# ### Statistical Tests

# %%
# Kruskal-Wallis on case durations
dur_result = test_duration_drift(log_complete, quarters)
print("Kruskal-Wallis test (case duration across quarters):")
print(f"  H-statistic: {dur_result['H-statistic']:.4f}")
print(f"  p-value: {dur_result['p-value']:.2e}")
print(f"  Significant drift: {'YES' if dur_result['significant'] else 'NO'}")

# Chi-squared on activity distributions Q1 vs Q4
activity_counts_q = (
    log_q.groupby(["quarter", "concept:name"]).size().unstack(fill_value=0)
)
act_result = test_activity_drift(activity_counts_q)
print("\nChi-squared test (activity distribution Q1 vs Q4):")
print(f"  Chi2: {act_result['chi2']:.4f}")
print(f"  p-value: {act_result['p-value']:.2e}")
print(f"  Significant drift: {'YES' if act_result['significant'] else 'NO'}")

# Kruskal-Wallis on RequestedAmount
amt_result = test_amount_drift(log_complete, quarters)
print("\nKruskal-Wallis test (RequestedAmount across quarters):")
print(f"  H-statistic: {amt_result['H-statistic']:.4f}")
print(f"  p-value: {amt_result['p-value']:.2e}")
print(f"  Significant drift: {'YES' if amt_result['significant'] else 'NO'}")

# %% [markdown]
# ### Interpretation
#
# The concept drift analysis results feed directly into simulation design:
# - If **activity distributions** shift significantly across quarters, a simulation model should be parameterized on the most recent data window rather than the full log.
# - If **case durations** drift, time distributions in the simulation need to be time-window-specific or use a rolling calibration approach.
# - If **requested amounts** shift, the input generation for the simulation must reflect the current distribution, not the historical average.
#
# These findings determine whether a single stationary simulation model is appropriate, or whether time-varying parameters are needed for accurate process simulation.
