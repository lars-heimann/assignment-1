# BPIC-17 Process Mining Assignment

TUM - Business Process Prediction, Simulation, and Optimization (Summer 2026)

## What

Individual assignment analyzing the [BPIC-17 event log](https://ais.win.tue.nl/bpi/2017/challenge.html): event log analysis, process discovery, conformance checking, decision mining, and one advanced analysis (concept drift detection).

Full assignment spec: [docs/assignment.md](docs/assignment.md)
Task checklist: [TODO.md](TODO.md)

## Project Structure

```
├── src/                    # Python source modules
│   ├── config.py           # Shared constants, paths, seeds
│   ├── data_loading.py     # XES loading with parquet caching
│   ├── statistics.py       # Basic event log statistics
│   ├── visualization.py    # Plotting functions
│   ├── discovery.py        # Process discovery algorithms
│   ├── metrics.py          # Custom simplicity metrics
│   ├── decision_mining.py  # Decision mining on XOR gateways
│   └── concept_drift.py    # Advanced analysis: concept drift
├── notebooks/
│   └── analysis.ipynb      # Main analysis notebook
├── data/                   # Event log (gitignored)
├── output/                 # Generated plots and models (gitignored)
├── pm4py-source/           # Local editable pm4py clone (gitignored)
├── docs/                   # Assignment spec and PDF
├── pyproject.toml          # Dependencies (managed with uv)
```

## Setup

```bash
uv sync
```

pm4py is installed as a local editable dependency from `pm4py-source/`. This means you can modify pm4py source files directly and changes take effect without reinstalling. The clone is gitignored. To re-create it:

```bash
git clone https://github.com/process-intelligence-solutions/pm4py pm4py-source
uv sync
```

Download the BPIC-17 event log into `data/`:
```bash
mkdir -p data
# Place BPI_Challenge_2017.xes.gz in data/
```

Run the notebook:
```bash
cd notebooks
uv run jupyter lab analysis.ipynb
```

## Links

- pm4py docs: https://processintelligence.solutions/pm4py
- pm4py repo: https://github.com/process-intelligence-solutions/pm4py
- BPIC-17 challenge: https://ais.win.tue.nl/bpi/2017/challenge.html

## Rules

- Report max 5 pages (excl. references + appendix)
- Include GenAI usage declaration
- Public repo required for submission
