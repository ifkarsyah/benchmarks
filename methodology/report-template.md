# <System A> vs <System B>: <workload>

Date: YYYY-MM-DD
Status: draft | final

## Question

One sentence. State the workload, the metric, and the decision it informs.

## Summary

Three to five lines. State the result with its interval, and say if the difference is within noise.

## Setup

| Item | Value |
|---|---|
| Hardware / instance type | |
| Region / network | |
| Versions (system A, system B, JVM, OS) | |
| Data size and distribution | |
| Replication / durability settings | |
| Checkpoint / commit interval | |

Held constant: list every variable held equal across systems.

Tuning: what was tuned for each system, how much time each got, and link to the final configs in `configs/`.

## Workload

Describe the workload, how load is generated, and the rates or scale factors used.

## Method

- Warmup length and steady-state window
- Number of trials and run order
- Cold or warm cache
- How latency is measured (intended send time or actual)

## Results

Tables and plots. For each comparison give the ratio with its interval, not only point values.

| Metric | System A | System B | Ratio A/B (95% interval) |
|---|---|---|---|
| | | | |

Raw data is in `results/`.

## Failure scenarios

What was killed or stressed, and what happened.

## Cost

Core-hours or dollars per unit of work, with the pricing assumptions.

## Threats to validity

Be specific. Examples: single region, small cluster, synthetic data, versions that have since changed, defaults that favor one side.

## Not tested

List what was out of scope so readers do not assume it.

## Reproduce

```bash
# exact commands, from a clean checkout
```
