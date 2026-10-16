# Summary: "TPC-H vs TPC-DS: Benchmarking Modern Distributed SQL Engines like Presto"

Source: https://prestodb.io/blog/2026/01/30/tpc-h-vs-tpc-ds-benchmarking-modern-distributed-sql-engines-presto/
Author: Saurabh Mahawar, Developer Relations Engineer at IBM (PrestoDB blog, 30 January 2026)
Read status: read from a PDF print of the page provided by the repo owner (17 pages, printed 16 October 2026). Two images on pages 6 and 13 did not render, and pages 7, 14 and 15 have blank areas where images were. Any charts or diagrams there are not covered below.

This is a summary in my own words, not a copy. Read the original for the full text. The author works on the Presto project, so treat the post as an explainer from an interested party.

## What it is

An introductory explainer on TPC-H and TPC-DS for people evaluating distributed SQL engines. It contains no benchmark results and no measurements. Its value for this repo is as a secondary description of the two datasets, and it agrees with what is in [tpc-h.md](../tpc-h.md) and [tpc-ds.md](../tpc-ds.md).

## Structure of the post

1. **Why benchmarks exist.** Before standardization, vendors cherry-picked simple queries. The TPC (founded 1988) is credited with replacing marketing claims with audited, reproducible data. Three ingredients are named: fixed schemas, deterministic data generation, and queries fixed at the SQL level.
2. **What performance depends on.** I/O throughput (reading from S3 or HDFS), CPU efficiency (serialization and compression), network shuffle, and optimizer quality.
3. **TPC-H.** A wholesale supplier model with a normalized (3NF) schema of 8 tables and 22 queries, generated with `dbgen`. Reported with Power and Throughput metrics. The queries are said to test scans, filters and group by, multi-way joins, skew and selectivity, sorting and top-N, and subqueries.
4. **TPC-DS.** A retailer with store, web and catalog sales. A snowflake or constellation schema of 24 tables (7 fact, 17 dimension), generated with `dsdgen`, and 99 queries ("with variations totaling ~100+"). Uses CTEs, window functions, `GROUPING SETS`, `ROLLUP`, `INTERSECT`, `EXCEPT` and joins of 10 or more tables. Reported with query response time, throughput and data maintenance time.
5. **Data skew.** The post's main claimed differentiator: TPC-H data is uniform, TPC-DS data has real-world skew (some items, dates or customers appear far more often than others), which punishes naive plans.
6. **Presto C++.** A promotional section on Presto's native C++ worker (Velox) and why the JVM is a performance ceiling. No numbers are given.
7. **Comparison table.** TPC-H is described as join efficiency and raw scan speed, for system validation and regression testing. TPC-DS is described as optimizer intelligence and skew handling, for production readiness and optimizer tuning.

## Facts the post gives that are useful here

| Fact | In the post | How it relates to this repo |
|---|---|---|
| SF1 size | "SF1 = 1GB of raw data". Engines commonly benchmark at SF100, SF1000, SF10000 or higher. | Matches my measurement of 1.1 GB raw text at SF1. Parquet is much smaller (about 362 MB), so the "X GB" ambiguity noted in [tpc-h.md](../tpc-h.md) still applies. |
| TPC-H rows at SF1000 | lineitem about 6 billion, orders about 1.5 billion, partsupp about 800 million, part about 200 million, customer about 150 million, supplier about 10 million, nation 25, region 5. | Consistent with linear scaling of my measured SF1 counts (lineitem 6,001,215 and so on). |
| TPC-H data distribution | Uniform. | Agrees broadly with my SF1 check (ship modes at 14.3% each). Not perfectly uniform: one third of customers have no orders, and orders per customer range from 1 to 41. |
| TPC-DS table count | 24 tables: 7 fact, 17 dimension. The comparison table says "24+ tables", which is inconsistent with the 24 in the text. | Agrees with the 24-table count and the 7/17 split in [tpc-ds.md](../tpc-ds.md). |
| TPC-DS fact tables | store_sales, store_returns, web_sales, web_returns, catalog_sales, catalog_returns, inventory. | Same seven names as in [tpc-ds.md](../tpc-ds.md). |
| TPC-DS dimension tables | customer, customer_address, customer_demographics, household_demographics, income_band, item, catalog_page, promotion, warehouse, ship_mode, date_dim, time_dim, store, call_center, web_site, web_page, reason. | Same seventeen names as in [tpc-ds.md](../tpc-ds.md). |
| TPC-DS skew | Significant, non-uniform, with hot spots. | Supports the "unsure" note in [tpc-ds.md](../tpc-ds.md). Still not measured here. |
| Presto connectors | Presto's built-in `tpch` and `tpcds` connectors generate data on the fly, are "zero-storage", and are for testing and education only. | Not directly relevant. Shows that generation need not produce files. |

## Claims to treat with caution

- **Query complexity tiers.** The post says queries 1 to 30 are simple, 31 to 60 medium and 61 to 99 complex. I could not confirm this, and I do not believe query numbers in TPC-DS are ordered by complexity. Treat it as the author's claim, not a property of the benchmark.
- **"Use case" row.** Describing TPC-H as for "system validation and regression testing" and TPC-DS as for "production readiness" is the author's opinion.
- **TPC as audited truth.** The post presents TPC benchmarks as objective and audited. That applies to official, audited results. Runs by other parties, including this repo, are not audited, and results should be called "TPC-H-like" (see [tpc-h.md](../tpc-h.md)). The essay summarized in [../../methodology/references/luminousmen-benchmaxxing.md](../../methodology/references/luminousmen-benchmaxxing.md) argues that standard workloads are still gamed by choice of scenario and configuration.
- **Presto C++ section.** Promotional, with no measurements.

## What it adds to the dataset notes

- Corroborates the TPC-DS schema counts and table names (a secondary source, not a check against generated data).
- Gives a second statement that TPC-H is uniform and TPC-DS is skewed, which matters for this repo's concern that results may not transfer to skewed real data.
- Confirms the usual practice of benchmarking at SF100 to SF10000.

## To verify before citing

- TPC-DS skew: generate data and measure it (the same checks used for TPC-H in [tpc-h.md](../tpc-h.md)).
- The query complexity tiers, against the TPC-DS specification.
- The "24+" versus 24 tables inconsistency, against the specification.
