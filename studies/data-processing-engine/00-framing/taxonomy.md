# Taxonomy: axes of variation and where each engine sits

Status: draft. Engine placements come from documentation and general knowledge, not from measurements. Every cell must be verified against the pinned versions before it is cited in a benchmark.

## 1. Axes

| Axis | Values | Why it matters |
|---|---|---|
| Data size relative to memory | fits in RAM; spills to disk; exceeds one machine | Decides whether one machine is enough (D1, D2) |
| Data location | remote object store; local disk; loaded into native storage | Decides who is the bottleneck: network, disk or engine (D3) |
| Workload shape | scan and aggregate; join heavy; shuffle heavy; UDF heavy; incremental or windowed | Engines differ most on joins and shuffles |
| Latency need | batch (minutes); interactive (seconds); streaming (sub-second) | Decides whether a streaming runtime is needed (D4) |
| Consumers | analyst or BI tool; downstream application; another pipeline | Decides the serving interface (D5) |
| Concurrency | one job; many concurrent queries | Single-process engines and clusters behave very differently |
| Reliability | restart is acceptable; needs recovery | Fault tolerance is costly, so not everyone needs it |
| Operations | components to run; skills needed; cost when idle | Part of D6, and often decisive in practice |

## 2. Engine placement (to verify)

Legend: yes, partial, no, ? (not known well enough to claim).

| Axis | Spark | Flink | Polars | DuckDB |
|---|---|---|---|---|
| Runs on one machine | yes (local mode) | yes (local mode) | yes | yes |
| Runs on a cluster | yes | yes | no (open source library) | no (open source library) |
| Out-of-core (data larger than RAM) | yes (spill) | yes in batch mode (spill) | partial (streaming engine, coverage varies by operation) | yes for many operators |
| Query data in object storage in place | yes | yes (via connectors) | yes | yes (httpfs) |
| Native table storage of its own | partial (managed tables, table formats via add-ons) | no (relies on external formats and catalogs) | no | yes (single-file database) |
| Streaming runtime | yes (Structured Streaming, micro-batch by default) | yes (native, record at a time) | no | no |
| Batch and stream with same API | partial (same DataFrame API, different semantics) | yes (same Table API, mode switch) | n/a | n/a |
| Serving interface for consumers | partial (Thrift Server over JDBC/ODBC) | partial (SQL Gateway) | no (library only) | partial (embedded, drivers for BI tools, no server) |
| Fault tolerance | yes | yes (checkpoints) | no | no |
| Components to operate | many on a cluster | many on a cluster | none (a library) | none (a library) |

Cells marked partial or ? are the first things to verify.

## 3. What the table already says

These follow from the structure, before any measurement:

1. Fault tolerance and streaming are capabilities, not speeds. A benchmark cannot rank a tool on a capability it does not have. It can only report the absence.
2. Cluster runs are not available for two of the four. Any "same hardware" comparison across all four must be single machine.
3. "Which is faster" is only meaningful on cells where all engines can run. The overlap cell is batch SQL on one machine, from local files or object storage.
4. Serving is a different role from computing. Two tools here are usually used to write results that something else serves.

## 4. Common mistake to avoid: boxing

It is tempting to rank within categories (single machine versus distributed, batch versus stream). The user's concern is the opposite: categories hide the real choice, since a person picking an engine may consider all of them. The approach is to compare on shared cells and report unsupported cells as findings, with tags on each result, as ClickBench does for its systems.

Reference: ClickBench (https://benchmark.clickhouse.com/) uses one table of about 100 million rows and 43 queries. It does not include Flink and does not vary data size, which are the two gaps this repo's study could fill.

## 5. Axes that may be cut

To keep the later benchmark small, consider cutting or deferring:

- Concurrency (needs a load model for consumers; a large addition).
- Workload shapes beyond TPC-H.
- Reliability tests (relevant only if recovery is a requirement).

The user decides which stay, based on which decisions in `model.md` matter.
