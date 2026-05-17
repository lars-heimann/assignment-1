"""Shared constants, paths, and configuration."""

import os
import warnings
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore")

# Reproducibility
SEED: int = 42
np.random.seed(SEED)

# Paths (relative to project root)
PROJECT_ROOT: str = str(Path(__file__).parent.parent)
DATA_DIR: str = os.path.join(PROJECT_ROOT, "data")
OUTPUT_DIR: str = os.path.join(PROJECT_ROOT, "output")
FIGURES_DIR: str = os.path.join(PROJECT_ROOT, "overleaf", "figures")
DATA_PATH: str = os.path.join(DATA_DIR, "BPI_Challenge_2017.xes.gz")
PARQUET_CACHE: str = os.path.join(DATA_DIR, "BPI_Challenge_2017.parquet")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

# Standard XES column names
CASE_COL: str = "case:concept:name"
ACTIVITY_COL: str = "concept:name"
TIMESTAMP_COL: str = "time:timestamp"
LIFECYCLE_COL: str = "lifecycle:transition"
RESOURCE_COL: str = "org:resource"
