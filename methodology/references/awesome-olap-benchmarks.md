# Summary: awesome-olap, benchmark section

Source: https://samber.github.io/awesome-olap/benchmark/
Author: samber (curated list)
Read status: read from text pasted by the repo owner. The page itself could not be fetched from the environment that wrote this file.

## What it is

A short curated list of five OLAP and database benchmarks, each with a one-line description. It is a map for finding benchmarks, not an analysis and not evidence of anything.

Its own advice, at the top: benchmarks help select a database for a workload, but run them on your own data and query patterns, because published numbers reflect vendor-tuned configurations. This is the same point made in [luminousmen-benchmaxxing.md](luminousmen-benchmaxxing.md).

## What it lists

| Benchmark | Description on the page | Relevance here (my reading) |
|---|---|---|
| [ClickBench](https://benchmark.clickhouse.com/) | De facto OLAP benchmark maintained by ClickHouse. 43 analytical queries on a "100GB" web analytics dataset, results for 50+ engines. | The model for the framing study's "tags, not leaderboards" approach. The page says 100GB while the ClickBench repo describes about 100 million rows. These are different units (size versus rows), so check which is meant, and whether it is raw or compressed size. |
| [Jepsen](https://jepsen.io/) | Testing of distributed databases, queues and consensus protocols. | Tests correctness under failure, not performance. Relevant to the failure scenarios in the framing study (what happens when a worker dies), not to speed comparisons. |
| [TPC-DS](https://www.tpc.org/tpcds/) | Decision support benchmark modeling a retail data warehouse, 99 complex SQL queries across several fact and dimension tables. | Agrees with the 99 queries and the fact/dimension structure in [tpc-ds.md](../../datasets/tpc-ds.md). It does not confirm the 24-table count. |
| [TPC-H](https://www.tpc.org/tpch/) | Business intelligence benchmark, 22 ad-hoc queries on supply-chain data. Called "the most widely cited OLAP benchmark in academic literature". | Matches [tpc-h.md](../../datasets/tpc-h.md). The "most cited" claim is the list author's and is not checked here. |
| [TPC family benchmarks](https://www.tpc.org/information/benchmarks5.asp) | Full catalog of TPC benchmarks for big data and analytical databases. | Where to look for benchmarks beyond TPC-H and TPC-DS. |

## To verify before citing

- The page is a secondary source. Confirm any fact above against the primary page.
- ClickBench's dataset size: "100GB" on this page versus about 100 million rows in the ClickBench repository.
- The "most widely cited" claim for TPC-H.
