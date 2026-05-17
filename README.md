# BPIC-17 Process Mining Analysis

This repository contains my submission for the Business Process Prediction, Simulation, and Optimization course (Summer 2026) at TUM.

## Overview
The goal of this assignment is to analyze the BPIC-17 event log, which captures loan applications from a Dutch financial institute. I've set up a full pipeline here to do everything from basic log statistics to process discovery, metrics calculation, decision mining, and concept drift detection.

## Structure
- `src/` contains all the Python code for data loading, calculating metrics, plotting, and the advanced analysis logic.
- `notebooks/analysis.ipynb` is where everything is pulled together and executed.
- `docs/` has the original assignment spec.

## Running the Code
The project uses `uv` for dependency management.

1. **Install dependencies:**
   ```bash
   uv sync
   ```
   Note: I'm using `pm4py` as an editable dependency directly from my GitHub fork because I needed to make sure it was completely reproducible. `uv sync` handles this automatically.

2. **Get the Data:**
   You'll need the original `BPI_Challenge_2017.xes.gz` file. 
   Create a `data/` folder in the root directory and drop the `.xes.gz` file in there. The first time you run the code, it will parse the XML and cache it as a Parquet file to make subsequent runs much faster.

3. **Run the Notebook:**
   ```bash
   cd notebooks
   uv run jupyter lab analysis.ipynb
   ```
