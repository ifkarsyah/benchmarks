# Framing: what should we compare, and why

Status: draft, awaiting review
Phase: 0 (tool-agnostic framing, before any benchmark)

## Why this exists

The first attempt at planning a benchmark of Spark, Flink, Polars and DuckDB kept uncovering missing dimensions: category boxing, business value and serving, whether input data sits in object storage or is already loaded, and batch versus stream switching. That means the question was not right yet. This study fixes the question from first principles, before any code, infra or cloud cost.

## Contents

| File | Purpose |
|---|---|
| [model.md](model.md) | What a data processing engine is, the decisions metrics must serve, a cost model, and bounds |
| [taxonomy.md](taxonomy.md) | Axes of variation and a first placement of the four engines (to verify) |
| [hypotheses.md](hypotheses.md) | Falsifiable predictions the benchmark would test |

## Findings so far

1. **The comparable cell is smaller than four engines suggest.** Two of the four do not run on a cluster, two have no streaming runtime, and two have no native table storage. A ranking across all four is only meaningful where all can run: batch SQL on one machine, on files in local storage or object storage.
2. **Capabilities are not speeds.** Streaming, fault tolerance and a query server for consumers are capabilities. The report states where an engine lacks one, and does not score it.
3. **Data size should be measured relative to memory**, not absolute. Absolute sizes (1, 100, 500, 1000 GB) are still useful as labels, but the interesting boundary is where the working set exceeds RAM.
4. **Remote storage can hide the engine.** At large sizes the network may be the bottleneck for every tool. The benchmark needs a measured bandwidth floor before it interprets any remote-storage result.
5. **Compute and serving are different roles.** Business users and downstream apps rarely read from the compute engine directly. This is handled as a separate, mostly qualitative, question.

One earlier claim in the planning conversation was too strong and is corrected here: business users cannot "read DuckDB directly" either. DuckDB is embedded, not a server, so it needs a driver or an application in front of it, like the others.

## Candidate benchmark questions

Each one is written to trace to a decision in [model.md](model.md) (D1 to D6). They are candidates, to be cut or edited by the user. Target after review: two to four.

| ID | Question | Decision | Primary metric | Controlled variables |
|---|---|---|---|---|
| Q1 | At each data size, which engines complete the same TPC-H SQL on one machine, in what time, and at what cost? | D1, D2 | wall time and cost per run, success or failure | hardware, data files, SQL, tuning budget |
| Q2 | How does the answer to Q1 change when the data is in object storage versus on local disk, and how close does each engine get to the bandwidth floor? | D3 | time and read throughput vs the measured floor | region, instance type, file layout |
| Q3 | For engines with native storage, after how many queries does loading beat reading files in place? | D3 | load time, per-query saving, break-even count | same data, same queries |
| Q4 | At what data size does a cluster of Spark or Flink beat the best single machine, and at what cost? | D2, D6 | wall time and cost, size at crossover | cluster sized to match one machine first |
| Q5 | How much code and operational change does it take to run one aggregation job in both batch and streaming mode? | D4 | lines changed, output equality, extra components | same logical job |
| Q6 | How do consumers read results through each engine, and how does a query endpoint compare under concurrent clients? | D5 | interface support, latency at 1, 10, 50 clients | same output data |

Q5 and Q6 are mostly qualitative. Q1 to Q4 are measured.

## What is not decided yet

1. Which decisions in `model.md` actually matter to the user. The question list depends on them.
2. Effect-size thresholds (`T`, `N` in `hypotheses.md`).
3. Budget and cloud account, which limit Q2 and Q4 at 500 GB and above.
4. Whether ClickHouse appears as a reference row in Q6 only, or elsewhere.

## Gate

No infra, harness or cloud work starts until the question list above is approved or edited. After approval, Phase 1 rewrites the benchmark study around the approved questions.

## Spikes

Any exploratory measurement made during this phase is a spike, not a result. It is recorded next to the item it informs and never used in a published conclusion.
