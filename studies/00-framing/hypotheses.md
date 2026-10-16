# Hypotheses

Predictions from `model.md` and `taxonomy.md` that a benchmark could prove wrong. They are written before any measurement. A hypothesis that no result could contradict is rewritten or dropped.

Status of all items: untested. The thresholds marked `T` are placeholders to set with the user, since the right size of effect depends on the decision it informs.

| ID | Hypothesis | Falsified if | Decision |
|---|---|---|---|
| H1 | Below the single-machine RAM limit, the two single-process engines finish the same SQL workload faster than the two engines run in local mode | any local-mode engine is within `T`% of the fastest single-process engine on the geometric mean across queries | D1, D2 |
| H2 | A cluster of Spark or Flink only beats the best single machine once the working set exceeds one machine's RAM and disk bandwidth | a cluster beats the best single machine at a size that fits in RAM, by more than `T`% | D2 |
| H3 | Reading 1000 GB from object storage on one machine takes within 1.5x of the measured read bandwidth floor for every engine, so results at that size mostly measure the network | any engine's time exceeds 1.5x the floor, in which case the engine matters, not only the network | D3 |
| H4 | Loading into native storage repays itself only after more than `N` queries over the same data, where `N` is computed from measured load time and per-query saving | break-even is below `N` for the fastest engine, or native storage is slower than reading files | D3 |
| H5 | An engine's data size limit on one machine is where the working set exceeds RAM, not an absolute size, and different engines fail in different ways (error, slowdown, success via spill) | an engine fails or slows sharply well below RAM, or runs past RAM without slowdown | D1, D2 |
| H6 | Switching one aggregation job from batch to streaming changes fewer lines of code in the engine with a unified API than in one with separate APIs | lines changed do not differ by more than `T` lines, or output differs between modes | D4 |
| H7 | For consumer-style queries (small result, high concurrency), a server with a native query endpoint outperforms the same data served through a batch engine's SQL gateway | the batch engine's gateway matches latency and throughput at 10 and 50 clients | D5 |

## How to read this

- H1, H2 and H5 are about where categories actually matter. If H1 holds and H2 holds, then "single node vs distributed" is a function of data size, not a fixed category, which answers the objection to boxing.
- H3 is the control for every remote-storage result. If it is falsified, the effect size needed for S3 results changes.
- H4 turns "already loaded or not" into a number.
- H6 and H7 are the qualitative sections from earlier planning. They are kept because they correspond to decisions D4 and D5.

## Cheap spikes to calibrate predictions

Allowed before the benchmark exists, labeled as spikes and never published as results:

1. Measure read throughput from object storage to one machine, to replace the assumed bandwidth in H3.
2. Run a handful of queries at small scale on the current machine to check that all four engines can run the same SQL.
3. Check each cell in the `taxonomy.md` table that is marked partial or ? against the pinned versions.

## Open items

- Set the `T` and `N` thresholds with the user.
- Confirm which decisions (D1 to D6 in `model.md`) matter, because hypotheses for unneeded decisions can be cut.
