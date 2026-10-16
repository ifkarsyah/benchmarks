# References

External reading collected for the framing study. Descriptions are marked by how much was actually read, because this is background, not evidence.

Read status:
- **read**: the page was fetched and read.
- **snippet**: only search-result snippets were seen, not the full page.
- **unread**: the page could not be fetched and no summary was found. The description is inferred from the title only and may be wrong. Open the link and replace it.

| # | Source | Status | What it contains |
|---|---|---|---|
| 1 | [DuckDB vs Apache Spark: The Fall of the Cluster](https://medium.com/@mamidipaka2003/duckdb-vs-apache-spark-the-fall-of-the-cluster-c28bea3e4d38) (Medium) | unread | Title suggests an opinion piece arguing that single-node DuckDB can replace Spark clusters for many workloads. Check whether it gives numbers or only argument. |
| 2 | [DuckDB vs ClickHouse: Why we use both at PostHog](https://posthog.com/blog/duckdb-vs-clickhouse) (PostHog, Mathew Pregasen, May 2026) | snippet | Argues the two are tangential products, not direct competitors, and that PostHog runs both. ClickHouse is described as a configurable multi-instance database for large data, DuckDB as an embeddable single-node engine for files or data that fits on one machine. A separate PostHog post about rebuilding their data warehouse on single-tenant DuckDB was mentioned by a third party and is not covered here. |
| 3 | [ClickBench](https://github.com/ClickHouse/ClickBench) (GitHub, ClickHouse) | read | Open-source benchmark of analytical databases on load time, storage size and query speed across many systems and hardware setups. One anonymized web analytics table of about 100 million rows, 43 queries, each run three times (first cold, next two hot). The model for the "tags, not leaderboards" approach in this study. |
| 4 | [DuckDB vs Spark: Pushing SQL to the Source](https://medium.com/@duckweave/duckdb-vs-spark-pushing-sql-to-the-source-6d958cd0f019) (Medium, duckweave) | unread | Title suggests a comparison focused on pushing SQL down to the data source (predicate and query pushdown) rather than moving data into the engine. Relevant to the X to engine feasibility gate. Verify. |
| 5 | [Building a data platform solo: Ansaar teardown](https://hikmahtechnologies.com/blog/building-a-data-platform-solo-ansaar-teardown/) (Hikmah Technologies) | unread | Title suggests a case study of one person building a full data platform. Possibly relevant to operations cost and team-size constraints. Verify. |
| 6 | [DuckDB vs Spark](https://hikmahtechnologies.com/blog/duckdb-vs-spark/) (Hikmah Technologies) | unread | Title suggests a head-to-head comparison of DuckDB and Spark. Verify whether it includes measurements. |

## Why these are here

- Items 1, 2, 4 and 6 sit in the same debate this study tries to answer without boxing: when does a single-node engine suffice, and when is a cluster needed.
- Item 3 is the structural model for the study: one workload every system can run, systems tagged instead of ranked in separate categories. Two gaps this repo could fill relative to it are that it has one data size and no Flink.
- Item 5 informs the operations and team-size constraints in [feasibility.md](feasibility.md).

## How to treat them

These are opinions and vendor posts, not benchmarks, unless a page shows methodology and raw data. Several come from authors with a stake in one tool (for example a ClickHouse repo and a PostHog post about its own stack). Claims drawn from them should be tested against the hypotheses in [hypotheses.md](hypotheses.md), not cited as results.

## To do

- Read items 1, 4, 5 and 6 and replace the "title suggests" text with an actual summary. They could not be fetched from the environment that wrote this file.
