# References: critiques of benchmarking

Reading that applies to every study in this repo, not to one dataset or tool. Read these before trusting a published benchmark, including your own.

Read status:
- **snippet**: only search-result snippets or third-party summaries were seen, not the full page.
- **unread**: the page could not be fetched and no summary was found. The description is inferred from the title only and may be wrong. Open the link and replace it.

The hosts are blocked from the environment that wrote this file. Benchmaxxing and the awesome-olap page were read from text the repo owner pasted. The others are snippet-level only.

## Critiques

| Source | Status | What it contains |
|---|---|---|
| [Lies, Damn Lies and Database Benchmarks](https://questdb.com/blog/lies-damn-lies-and-database-benchmarks/) (QuestDB, Andrey Pechkurov, 18 June 2026) | snippet | Uses ClickBench as the example. Changes one fair-but-different setup detail per scenario and shows hot-run rankings shift. Central claim: a perfectly fair benchmark is practically unattainable, especially across very different kinds of databases. Per a third-party summary, it notes that self-hosted versus managed cloud setups skew cold runs, and that more query iterations or keeping a process alive change results. Advice: do not choose a database on a benchmark alone, test your own workload. The author works for a vendor (QuestDB) that appears in ClickBench. |
| [Benchmaxxing](https://luminousmen.substack.com/p/benchmaxxing) (luminousmen, Substack) | read (text pasted by the repo owner, not fetched) | Essay on how headline benchmark numbers mislead even when honest: undisclosed environments, isolated operations in titles, unfair cold-run conditions. About database benchmarks, not AI models. **Full summary and takeaways for this repo: [references/luminousmen-benchmaxxing.md](references/luminousmen-benchmaxxing.md).** |

## Vendor results (read critically, do not cite as findings)

| Source | Status | What it contains |
|---|---|---|
| [TPC-H for less than a cent: ClickHouse Cloud vs. Snowflake, Databricks, BigQuery, and Redshift](https://clickhouse.com/blog/tpc-h-clickhouse-cloud-vs-snowflake-databricks-bigquery-redshift) (ClickHouse) | snippet | Vendor-run TPC-H comparison. Reported: on SF100, a single 59-core ClickHouse Cloud node competitive on runtime and first on cost-performance; on SF10, the full workload in 2.9 s for $0.009. Method per the snippet: each query run three times, result caching disabled, charts use the fastest hot run, cold runs not compared. Competitor systems used warehouse or serverless capacity settings, so hardware is approximate. The scripts and results are reportedly public on GitHub. No independent check was found. |

Why it is here: it is a useful example to critique against [checklist.md](checklist.md) and [statistics.md](statistics.md). Two points of contrast, from the snippet and subject to checking against the full post:
- Charting the fastest hot run discards variability. This repo reports trial-level data with an interval, and treats the trial as the unit of analysis.
- Comparing a fixed node with other vendors' serverless or warehouse sizes is not a controlled hardware comparison. This repo requires held-constant variables.

## Catalogs

| Source | Status | What it contains |
|---|---|---|
| [awesome-olap: benchmark](https://samber.github.io/awesome-olap/benchmark/) (samber) | read (text pasted by the repo owner, not fetched) | A short curated list of five OLAP and database benchmarks, with one-line descriptions. Its own advice at the top: run benchmarks on your own data and query patterns, because published numbers reflect vendor-tuned configurations. A map to find benchmarks, not evidence of anything. Entries are listed below. |

### What the awesome-olap page lists

| Benchmark | Description on the page | Relevance here (my reading) |
|---|---|---|
| [ClickBench](https://benchmark.clickhouse.com/) | De facto OLAP benchmark maintained by ClickHouse. 43 analytical queries on a "100GB" web analytics dataset, results for 50+ engines. | The model for the framing study's "tags, not leaderboards" approach. The page says 100GB while the ClickBench repo describes about 100 million rows. These are different units (size versus rows), so check which is meant, and whether it is raw or compressed size. |
| [Jepsen](https://jepsen.io/) | Testing of distributed databases, queues and consensus protocols. | Tests correctness under failure, not performance. Relevant to the failure scenarios in the framing study (what happens when a worker dies), not to speed comparisons. |
| [TPC-DS](https://www.tpc.org/tpcds/) | Decision support benchmark modeling a retail data warehouse, 99 complex SQL queries across several fact and dimension tables. | Corroborates the 99 queries and the fact/dimension structure in [../datasets/tpc-ds.md](../datasets/tpc-ds.md). It does not confirm the 24 tables. |
| [TPC-H](https://www.tpc.org/tpch/) | Business intelligence benchmark, 22 ad-hoc queries on supply-chain data. "The most widely cited OLAP benchmark in academic literature." | Matches [../datasets/tpc-h.md](../datasets/tpc-h.md). The "most cited" claim is the list author's and is not checked here. |
| [TPC family benchmarks](https://www.tpc.org/information/benchmarks5.asp) | Full catalog of TPC benchmarks for big data and analytical databases. | Where to look for benchmarks beyond TPC-H and TPC-DS. |

The page is a secondary source. Confirm any fact above against the primary page before citing it.

## How to use these

1. Before relying on a published number, ask what was held constant, which run was reported (first, fastest, median), who ran it, and whether the author sells one of the systems.
2. Compare a source's method with [checklist.md](checklist.md). Each gap is a question to ask of that result.
3. Prefer sources that publish scripts and raw data, so a reader can re-run them.

## To do

- Read the full QuestDB and ClickHouse posts to confirm the snippet-level claims above, and to check the Benchmaxxing author's account of the ClickBench cold-run skew against the QuestDB original.
- Verify the third-party claims in the Benchmaxxing summary against the primary posts. The list of claims to verify is in the summary file.
