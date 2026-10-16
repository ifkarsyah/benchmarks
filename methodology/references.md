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
| [Benchmaxxing](https://luminousmen.substack.com/p/benchmaxxing) (luminousmen, Substack) | read (text pasted by the repo owner, not fetched) | Essay on how headline benchmark numbers mislead even when honest. It is about database and data infrastructure benchmarks, not AI model benchmarks. Summary below. |

### Benchmaxxing: summary

The author's thesis: a number can be real and reproducible and still measure something other than what a reader assumes. The essay works through three vendor posts and one cross-vendor benchmark. All specifics below are the author's reports, not checked here.

| Case | What the author says | The mechanism |
|---|---|---|
| Databricks "Reyden" (June keynote) | Claimed up to 16x better than existing real-time serving stacks, with a live demo where a competitor crashed. No hardware, cluster size, cache state or config disclosed. A ClickHouse engineer could not reproduce the crash from the only named detail (TPC-H, SF1, Q6). A Snowflake engineer reconfigured the comparison and reported 12.5 s vs 13.2 s at 100 GB and 28.2 s vs 71 s at 1 TB. | Undisclosed environment: a benchmark nobody can rerun is a claim taken on faith. |
| WarpStream "40x" | The 40x is create plus write plus close in isolation (80 to 100 ms down to 2 to 3 ms). The production cluster figure in the same post is 2 to 3 times faster than regional GCS. The faster storage tier costs over 10x more per GiB. | Isolated operation in the title, system-level number in the text. |
| Spotify RAP | O(1) describes the lookup, not the read. Per the post, it reads the whole page containing the row (potentially 4 MB to get 100 bytes). Much of the design is about arranging data at write time so O(1) pays off. | A true property that hides a cost. |
| ClickBench cold runs | Restates the QuestDB critique: the harness clears the page cache and restarts a self-hosted database between cold runs, but cannot restart a managed service, so its three "cold" runs hit the same live server. The cold ranking then reflects who the harness can restart, not architecture. | The experiment's own conditions favor one side. |

Other points from the essay:
- **Benchmarketing** is old. The author cites a piece tracing hidden hardware, unrealistic scenarios, hidden costs and test-specific tuning back to Oracle and Sybase in the early 1980s.
- **The DeWitt clause:** many licenses restrict publishing independent benchmarks without vendor approval. The author quotes SQL Server's license and says Oracle's has a similar term. This can make vendor benchmarks the only legally publishable ones.
- **Cost of trusting a headline:** the author argues people size clusters and justify migrations from multipliers measured on very different configurations (for example 32 cores per node versus the 4 they actually run), and that almost nobody publishes the null result ("it came out to 8%").
- **The author's rule:** when you see a multiplier in a title, find the configuration. It is in the text, not the title.

### What this means for this repo (my reading, not the author's)

1. **Report system-level and isolated numbers together.** The headline must be the end-to-end figure. An isolated-operation number is secondary and labeled as such. This fits the per-stage timing (read, process, write) planned in the framing study.
2. **Name the scenario and publish the configuration** so a reader can rerun it. Already required by the checklist (step 7). The Reyden case is the failure it prevents.
3. **Cold runs need a fairness check.** Only report a cold-cache result when the harness can reset the engine and the cache the same way for every system. Otherwise report hot only, and say so. Relevant when comparing embedded engines (easy to restart) with managed or long-running services.
4. **Test at the size the reader runs.** The framing study proposes one large single node (about 32 vCPU). The "4 cores versus 32" point suggests also reporting a small node, or stating clearly that results do not transfer to small deployments.
5. **Publish null results.** Repo rule 5 ("if a result is not distinguishable from noise, say so") already covers this.
6. **Check engine licenses before publishing** comparisons. The DeWitt clause is mostly a commercial-database issue, and I have not checked the licenses of the engines in this repo's studies.

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
- Verify the third-party claims in the Benchmaxxing summary (Databricks Reyden, Snowflake numbers, WarpStream, Spotify RAP) against the primary posts before citing any of them.
