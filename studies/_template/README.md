# <System A> vs <System B>: <workload>

Status: not started
Date started: YYYY-MM-DD

Copy this folder to `studies/YYYY-<name>/`. Write the question first and do not run anything until sections 1 to 3 are filled in.

## 1. Question

One sentence. Workload, metric, and the decision it informs.

## 2. Hypothesis and decision threshold

What do you expect, and what size of difference would change a decision?

## 3. Held constant

- Hardware:
- Versions:
- Durability / replication:
- Checkpoint / commit interval:
- Data layout:

## 4. Run protocol

- Warmup:
- Steady-state window:
- Trials per system (at least 5, preferably 10+):
- Run order (interleaved):

## 5. Results

See [methodology/report-template.md](../../methodology/report-template.md) for the full report structure. Fill it in here once data exists.

## 6. Threats to validity

## 7. Not tested

## Reproduce

```bash
# commands from a clean checkout
```

## Folder contents

```
infra/      docker-compose or terraform for the environment
configs/    final tuned configs for each system
run.py      one command that executes the protocol
results/    raw data (CSV or JSON), one file per trial
analysis.py summarizes results using common/stats.py
```
