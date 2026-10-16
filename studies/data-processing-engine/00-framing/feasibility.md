# Feasibility gate: can the engine connect X to Y at all

Status: draft. Every cell below is from general knowledge and is NOT verified against pinned versions. Verify each one with a small end-to-end spike (one tiny run per pair) before treating it as fact.

## Why this comes first

The setup is fixed by the user: `X -> data processing engine -> Y`. Source and sink are given, not chosen. An engine that cannot connect them is out before any benchmark runs. This gate costs documentation reading and small spikes, not cloud money, and may remove most of the matrix.

Order of questions:

1. **Feasibility gate (pass or fail).** Can the engine connect this X to this Y?
2. **Constraint gate.** Among feasible engines, which meet the hard requirements?
3. **Benchmark the survivors**, on the real pipeline, with per-stage timing.

The approach is feasibility filtering followed by ranking: hard constraints remove options, soft preferences rank what is left.

## The setup

| | Values |
|---|---|
| X (source) | Postgres (OLTP database), Kafka, an API |
| Y (sink) | OLAP store, Kafka topic, ML system, user and tenant analytics |

That is 3 x 4 = 12 pairs per engine, 48 cells for four engines. Do not benchmark all of them. The gate prunes first, and the benchmark covers only pairs the user actually has.

## Grades

Use four grades, not pass/fail:

| Grade | Meaning |
|---|---|
| native | first-party connector, documented, supported |
| third-party | works through a separate library or connector, maintained outside the engine |
| custom code | the user writes and owns the glue |
| no | not possible, or only by adding another system in between |

"Custom code" counts as possible, but it is a cost: the user now maintains it. Record it as a constraint violation if the team cannot own it.

## Source side (X -> engine), to verify

| X | Spark | Flink | DuckDB | Polars |
|---|---|---|---|---|
| Postgres, bulk read | native (JDBC) | native (JDBC connector) | native-ish (Postgres extension) | third-party (ConnectorX, ADBC) |
| Postgres, change stream (CDC) | third-party (for example Debezium via Kafka) | third-party (Flink CDC) | no | no |
| Kafka | native | native | no first-party consumer | no first-party consumer |
| API | custom code | custom code | custom code | custom code |

## Sink side (engine -> Y), to verify

Sink requirements matter more than the sink name: what must the write do?

| Write need | Meaning |
|---|---|
| append | add new rows |
| overwrite | replace a table or partition |
| upsert | update by key, needed for tenant analytics and many ML serving stores |
| idempotent | rerun after failure without duplicates |

| Y | Spark | Flink | DuckDB | Polars |
|---|---|---|---|---|
| OLAP store | depends on target; JDBC or connector | depends on target; connector | depends on target; usually via files or driver | depends on target; usually via files or driver |
| Kafka topic | native | native | no | no |
| ML system | depends on target; usually custom code | depends on target; usually custom code | custom code | custom code |
| Tenant analytics (low latency, upserts) | depends on target store | depends on target store | depends on target store | depends on target store |

The "depends on target" cells need the user's actual target system. The gate cannot be finished for those without it.

## Hard constraints to collect

Hard constraints are pass/fail. Collect them per pair:

| Constraint | Question |
|---|---|
| Freshness | How old can the result be when the consumer reads it? (seconds, minutes, hours) |
| Delivery semantics | At-most-once, at-least-once or exactly-once? |
| Write semantics | Append, overwrite, upsert, idempotent? |
| Topology | Is a staging step allowed (for example Kafka to object storage to engine), or must the connection be direct? Staging adds latency and one more component to operate. |
| Source impact | May the engine read the production OLTP database, and at what load? |
| Volume | Rows or GB per day, peak rate |
| Operations | How many components can the team run? Is on-call possible? |
| Cost ceiling | Monthly budget |
| Skills | Which languages and APIs the team can maintain |

Soft preferences (rank survivors, do not remove them): developer experience, ecosystem, existing infrastructure.

## Pair-specific notes

- **Postgres -> engine.** The bottleneck is usually Postgres, so the benchmark must report read time separately from process time. Add a rule: a read from a production database must not exceed an agreed load, otherwise use a replica or CDC.
- **Kafka -> engine.** Unbounded input changes the metrics from wall time per query to sustainable throughput, latency, state size and recovery. Only engines that pass the gate here belong in this benchmark.
- **API -> engine.** Rate limits and latency dominate. All engines need custom code, so the engine is not what is measured. Treat as out of scope for performance, and record only how awkward the custom code is.

## Output of this gate

A completed matrix for the user's real pairs, with a grade and a source (doc link or spike result) in every cell, and a list of engines that pass the hard constraints for each pair. The benchmark questions in the README then run only on those survivors.

## Spikes needed (no results, only feasibility)

For each pair in use, one tiny end-to-end run with a few rows: source to engine to sink, checking that data arrives and that the write semantics hold (for example a rerun does not duplicate). Record outcome as pass or fail, with the version used. Spikes are not published as performance results.
