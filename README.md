# benchmarks

Personal, vendor-neutral benchmarks of data infrastructure tools, plus the methodology and reusable harness behind them.

Everything here is built from public data and my own hardware or cloud account. Nothing comes from an employer.

## Studies

| Study | Question | Status | Conclusion |
|---|---|---|---|
| [kafka-vs-redpanda](studies/_template/) | (planned) | not started | |
| [spark-vs-flink](studies/_template/) | (planned) | not started | |
| [iceberg-vs-delta](studies/_template/) | (planned) | not started | |

Update this table when a study is finished. One line of conclusion per study, with a link to its report.

## Methodology

Start here before running anything.

- [methodology/checklist.md](methodology/checklist.md): the 7-step process for a fair benchmark
- [methodology/statistics.md](methodology/statistics.md): the statistics a data infrastructure engineer actually needs
- [methodology/report-template.md](methodology/report-template.md): structure for writing results honestly
- [methodology/references.md](methodology/references.md): critiques of benchmarking and vendor results to read critically

## Datasets

Reference notes on the public datasets used here: [datasets/](datasets/) (TPC-H, TPC-DS).

## Shared code

- [common/stats.py](common/stats.py): percentiles, confidence intervals, permutation test, sustainable-rate search
- [common/loadgen/fixed_rate.py](common/loadgen/fixed_rate.py): fixed-rate load generator that avoids coordinated omission

## Repo layout

```
benchmarks/
├── methodology/     # process, statistics, report template
├── common/          # reusable Python helpers
└── studies/
    └── _template/   # copy this to start a new study
```

## Starting a new study

```bash
cp -r studies/_template studies/2026-<name>
```

Then fill in `README.md` (the report) starting with the question, and keep raw results in `results/`.

## Rules for this repo

1. Public data only (TPC-DS, TPC-H, documented synthetic generators).
2. Pin every version and record hardware.
3. Commit raw results, not only summaries.
4. Every report has a "threats to validity" section, including what was not tested.
5. If a result is not distinguishable from noise, say so instead of declaring a winner.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest common
```
