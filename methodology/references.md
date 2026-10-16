# References: critiques of benchmarking

Reading that applies to every study in this repo, not to one dataset or tool. Read these before trusting a published benchmark, including your own.

Read status:
- **snippet**: only search-result snippets or third-party summaries were seen, not the full page.
- **unread**: the page could not be fetched and no summary was found. The description is inferred from the title only and may be wrong. Open the link and replace it.

The hosts are blocked from the environment that wrote this file. Only Benchmaxxing was read, from text the repo owner pasted. The others are snippet-level or unread.

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
| [awesome-olap: benchmark](https://samber.github.io/awesome-olap/benchmark/) | unread | Title and domain suggest a curated list of OLAP benchmarks. Verify what it lists, and use it as a map to find benchmarks, not as evidence of anything. |

## How to use these

1. Before relying on a published number, ask what was held constant, which run was reported (first, fastest, median), who ran it, and whether the author sells one of the systems.
2. Compare a source's method with [checklist.md](checklist.md). Each gap is a question to ask of that result.
3. Prefer sources that publish scripts and raw data, so a reader can re-run them.

## To do

- Read the awesome-olap page and replace the "title suggests" text.
- Read the full QuestDB and ClickHouse posts to confirm the snippet-level claims above, and to check the Benchmaxxing author's account of the ClickBench cold-run skew against the QuestDB original.
- Verify the third-party claims in the Benchmaxxing summary against the primary posts. The list of claims to verify is in the summary file.
