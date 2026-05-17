"""Process discovery algorithms and quality metric computation."""

from typing import Any

import pandas as pd
import pm4py

from src.metrics import simplicity_cnc, simplicity_weighted_place_degree

# Noise threshold for the final Inductive Miner (infrequent) model.
# Picked from the extended threshold sweep: dominates the 0.5 candidate on
# precision (0.71 vs 0.57) at only 2 fitness points lower (0.86 vs 0.89),
# still safely above the 80% fitness target.
FINAL_NOISE_THRESHOLD: float = 0.9


def discover_models(log: pd.DataFrame) -> list[tuple]:
    """Run the three discovery algorithms and return (net, im, fm, name) tuples."""
    print("Running Inductive Miner...")
    net_ind, im_ind, fm_ind = pm4py.discover_petri_net_inductive(log)

    print("Running Heuristics Miner...")
    net_heur, im_heur, fm_heur = pm4py.discover_petri_net_heuristics(log)

    print("Running Inductive Miner (infrequent, noise_threshold=0.2)...")
    net_imf, im_imf, fm_imf = pm4py.discover_petri_net_inductive(
        log, noise_threshold=0.2
    )

    return [
        (net_ind, im_ind, fm_ind, "Inductive Miner"),
        (net_heur, im_heur, fm_heur, "Heuristics Miner"),
        (net_imf, im_imf, fm_imf, "Inductive Miner (infrequent, 0.2)"),
    ]


def compute_all_metrics(
    log: pd.DataFrame, net, im, fm, name: str
) -> dict[str, Any]:
    """Compute all PM4Py and custom quality metrics for a Petri net."""
    results: dict[str, Any] = {"Model": name}

    fitness = pm4py.fitness_token_based_replay(log, net, im, fm)
    results["Fitness (log)"] = fitness["log_fitness"]
    results["Fitness (avg trace)"] = fitness["average_trace_fitness"]

    results["Precision"] = pm4py.precision_token_based_replay(log, net, im, fm)

    try:
        results["Generalization"] = pm4py.algo.evaluation.generalization.algorithm.apply(
            log, net, im, fm
        )
    except Exception:
        results["Generalization"] = "N/A"

    try:
        results["Simplicity (PM4Py)"] = pm4py.algo.evaluation.simplicity.algorithm.apply(
            net
        )
    except Exception:
        results["Simplicity (PM4Py)"] = "N/A"

    results["Simplicity (CNC)"] = simplicity_cnc(net)
    results["Simplicity (Place Degree)"] = simplicity_weighted_place_degree(net)

    results["Places"] = len(net.places)
    results["Transitions"] = len(net.transitions)
    results["Arcs"] = len(net.arcs)

    return results


def build_metrics_table(log: pd.DataFrame, models: list[tuple]) -> pd.DataFrame:
    """Compute metrics for all models and return a comparison DataFrame."""
    rows = [compute_all_metrics(log, net, im, fm, name) for net, im, fm, name in models]

    col_order = [
        "Model",
        "Fitness (log)",
        "Fitness (avg trace)",
        "Precision",
        "Generalization",
        "Simplicity (PM4Py)",
        "Simplicity (CNC)",
        "Simplicity (Place Degree)",
        "Places",
        "Transitions",
        "Arcs",
    ]
    df = pd.DataFrame(rows)
    return df[[c for c in col_order if c in df.columns]]


def sweep_thresholds(
    log: pd.DataFrame,
    thresholds: list[float] | None = None,
) -> pd.DataFrame:
    """Sweep noise thresholds for Inductive Miner (infrequent) and return metrics."""
    if thresholds is None:
        thresholds = [0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]

    rows = []
    for t in thresholds:
        print(f"Threshold {t}...")
        net, im, fm = pm4py.discover_petri_net_inductive(log, noise_threshold=t)
        fitness = pm4py.fitness_token_based_replay(log, net, im, fm)
        precision = pm4py.precision_token_based_replay(log, net, im, fm)
        simp = pm4py.algo.evaluation.simplicity.algorithm.apply(net)

        rows.append(
            {
                "Threshold": t,
                "Fitness (log)": fitness["log_fitness"],
                "Precision": precision,
                "Simplicity": simp,
                "Places": len(net.places),
                "Transitions": len(net.transitions),
                "Arcs": len(net.arcs),
            }
        )

    return pd.DataFrame(rows)


def build_final_model(log: pd.DataFrame, noise_threshold: float = FINAL_NOISE_THRESHOLD):
    """Discover the final model with the chosen noise threshold."""
    return pm4py.discover_petri_net_inductive(log, noise_threshold=noise_threshold)


def export_model(net, im, fm, output_dir: str):
    """Export the model as BPMN and a Petri net image. Returns the BPMN object."""
    bpmn = pm4py.convert_to_bpmn(net, im, fm)
    pm4py.write_bpmn(bpmn, f"{output_dir}/final_model.bpmn")
    pm4py.save_vis_petri_net(net, im, fm, f"{output_dir}/final_petri_net.png")
    print(f"Model exported to {output_dir}/")
    return bpmn
