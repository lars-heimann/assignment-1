"""Load and cache the BPIC-17 event log."""

import os

import pandas as pd
import pm4py

from src.config import DATA_PATH, LIFECYCLE_COL, PARQUET_CACHE


def load_event_log() -> pd.DataFrame:
    """Load the BPIC-17 event log, caching as parquet for fast reload."""
    if os.path.exists(PARQUET_CACHE):
        print("Loading from parquet cache...")
        log = pd.read_parquet(PARQUET_CACHE)
    else:
        print("Parsing XES (first time, will cache as parquet)...")
        log = pm4py.read_xes(str(DATA_PATH))
        assert isinstance(log, pd.DataFrame), "expected pm4py to return a DataFrame"
        log.to_parquet(PARQUET_CACHE)
        print("Cached.")

    print(f"Shape: {log.shape}")
    return log


def filter_complete_events(log: pd.DataFrame) -> pd.DataFrame:
    """Filter to 'complete' lifecycle events only for process discovery."""
    log_complete = log[log[LIFECYCLE_COL] == "complete"].copy()
    print(f"Events after filtering to 'complete': {len(log_complete)}")
    return log_complete
