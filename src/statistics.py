"""Compute basic and additional event log statistics."""

import pandas as pd
import pm4py

from src.config import ACTIVITY_COL, CASE_COL, RESOURCE_COL, TIMESTAMP_COL

CATEGORICAL_MAX_CARDINALITY = 50


def _is_categorical(series: pd.Series) -> bool:
    """Return True if a column is a categorical event attribute.

    A column counts as categorical when it is non-numeric, non-temporal,
    and has at most CATEGORICAL_MAX_CARDINALITY (50) distinct values.
    The threshold excludes org:resource (149 unique employees, not seen as
    categorical) as well as identifier-like columns such as EventID (1.2M unique) and
    OfferID (43k unique). A pure dtype check is insufficient: most string
    columns are stored as the pandas `string` extension dtype rather than
    `object`, and string-typed identifiers would otherwise be miscounted.
    """
    if pd.api.types.is_numeric_dtype(series):
        return False
    if pd.api.types.is_datetime64_any_dtype(series):
        return False
    return series.nunique(dropna=True) <= CATEGORICAL_MAX_CARDINALITY


def compute_basic_statistics(log: pd.DataFrame) -> dict:
    """Compute all required and additional statistics from the event log.

    Returns a dict containing the assignment-style `summary` table plus the
    raw series and derived scalars used in plots and report prose.
    """
    # Number of cases
    num_cases = log[CASE_COL].nunique()

    # Number of events
    num_events = len(log)

    # Number of process variants
    variants = pm4py.get_variants(
        log,
        activity_key=ACTIVITY_COL,
        timestamp_key=TIMESTAMP_COL,
        case_id_key=CASE_COL,
    )
    num_variants = len(variants)

    # Number of distinct activities (Additional statistic)
    num_activities = log[ACTIVITY_COL].nunique()

    # Number of distinct case and event attribute labels
    case_attrs = [c for c in log.columns if c.startswith("case:")]
    event_attrs = [c for c in log.columns if not c.startswith("case:")]
    num_case_attrs = len(case_attrs)
    num_event_attrs = len(event_attrs)

    # Number of categorical event attributes
    num_categorical_event_attrs = sum(_is_categorical(log[c]) for c in event_attrs)

    # Mean and standard deviation of case length
    case_lengths = log.groupby(CASE_COL).size()

    # Mean and standard deviation of case duration (in days, minutes, and seconds)
    case_start = log.groupby(CASE_COL)[TIMESTAMP_COL].min()
    case_end = log.groupby(CASE_COL)[TIMESTAMP_COL].max()
    case_durations = (case_end - case_start).dt.total_seconds()

    # Top 4 activity dominance (Additional statistic)
    activity_counts = log[ACTIVITY_COL].value_counts()
    top4 = activity_counts.head(4)
    top4_activity_sum = int(top4.sum())
    top4_activity_share = top4_activity_sum / num_events

    # Distinct resources (Additional statistic)
    num_resources = log[RESOURCE_COL].nunique() if RESOURCE_COL in log.columns else 0

    # Distinct start / end activities per case (Additional statistic)
    log_sorted = log.sort_values([CASE_COL, TIMESTAMP_COL])
    start_activities = log_sorted.groupby(CASE_COL)[ACTIVITY_COL].first()
    end_activities = log_sorted.groupby(CASE_COL)[ACTIVITY_COL].last()
    num_start_activities = start_activities.nunique()
    num_end_activities = end_activities.nunique()

    summary = pd.DataFrame(
        {
            "Metric": [
                # Required by assignment spec
                "Number of cases",
                "Number of events",
                "Number of process variants",
                "Number of case attributes",
                "Number of event attributes",
                "Number of categorical event attributes",
                "Mean case length (events)",
                "Std case length (events)",
                "Mean case duration (days)",
                "Std case duration (days)",
                # Additional statistics
                "Distinct activities",
                "Median case duration (days)",
                "Min case length (events)",
                "Max case length (events)",
                "Distinct resources (org:resource)",
                "Distinct start activities",
                "Distinct end activities",
                "Top 4 activity events",
                "Top 4 activity share",
            ],
            "Value": [
                num_cases,
                num_events,
                num_variants,
                num_case_attrs,
                num_event_attrs,
                num_categorical_event_attrs,
                f"{case_lengths.mean():.2f}",
                f"{case_lengths.std():.2f}",
                f"{case_durations.mean() / 86400:.2f}",
                f"{case_durations.std() / 86400:.2f}",
                num_activities,
                f"{case_durations.median() / 86400:.2f}",
                int(case_lengths.min()),
                int(case_lengths.max()),
                num_resources,
                num_start_activities,
                num_end_activities,
                top4_activity_sum,
                f"{top4_activity_share:.2%}",
            ],
        }
    )

    return {
        "summary": summary,
        "case_lengths": case_lengths,
        "case_durations": case_durations,
        "activity_counts": activity_counts,
        "num_cases": num_cases,
        "num_events": num_events,
        "num_variants": num_variants,
        "num_activities": num_activities,
        "num_case_attrs": num_case_attrs,
        "num_event_attrs": num_event_attrs,
        "num_categorical_event_attrs": num_categorical_event_attrs,
        "num_resources": num_resources,
        "num_start_activities": num_start_activities,
        "num_end_activities": num_end_activities,
        "top4_activity_sum": top4_activity_sum,
        "top4_activity_share": top4_activity_share,
    }


def get_case_durations(log: pd.DataFrame) -> pd.Series:
    """Return case durations in seconds. Used by `concept_drift`."""
    case_start = log.groupby(CASE_COL)[TIMESTAMP_COL].min()
    case_end = log.groupby(CASE_COL)[TIMESTAMP_COL].max()
    return (case_end - case_start).dt.total_seconds()


def print_attribute_overview(log: pd.DataFrame) -> None:
    """Print case and event attribute details."""
    case_attrs = [c for c in log.columns if c.startswith("case:")]
    event_attrs = [c for c in log.columns if not c.startswith("case:")]

    print("=== Case Attributes ===")
    for attr in case_attrs:
        print(f"  {attr}: {log[attr].nunique()} unique values")

    print("\n=== Event Attributes ===")
    for attr in event_attrs:
        print(
            f"  {attr:40s} dtype={log[attr].dtype!s:20s} unique={log[attr].nunique()}"
        )
