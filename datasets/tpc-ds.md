# TPC-DS

Status: **verified at SF1** using the official TPC-DS tools (version 2.10.0) and DuckDB 1.5.6, on one machine, in one session. Facts marked "(spec)" come from the TPC-DS specification v2.10.0 that ships with the tools. Facts marked "(not verified)" were not checked. One result is **unresolved**: query results did not match the shipped answer sets (see "Correctness check").

## What it is

A decision support benchmark from the Transaction Processing Performance Council (TPC). It models a retailer selling through three channels (stores, catalog, web), with returns and inventory. It is harder than TPC-H: more tables, more complex SQL, and less uniform data.

## Tools: where to get a vendor-neutral generator

| Option | What it is | Notes |
|---|---|---|
| **TPC official kit** (tpc.org, "TPC-DS Tools") | `dsdgen` (data generator) and `dsqgen` (query generator), from the non-profit that owns the benchmark. | Neutral, but download requires accepting the TPC license. Could not be fetched from the environment that wrote this file (not verified). |
| [gregrahn/tpcds-kit](https://github.com/gregrahn/tpcds-kit) | A GitHub copy of the official kit, v2.10.0, with small changes: compiles on macOS, fixes two query template bugs (query22a, query77a) and renames one column in `s_web_returns`. Includes the specification, query templates, query variants and answer sets. | **Used for everything below.** It is a third-party copy, so for any published result, state which kit version and source you used. |
| DuckDB `tpcds` extension | `CALL dsdgen(sf=1)` generates the data inside DuckDB. | Not tested here, because the extension host was blocked. It is convenient but ties data generation to one engine, so for a cross-engine comparison, generate files once with the official tool and load them everywhere. |
| Presto `tpcds` connector | Generates data on the fly, with no storage, for testing and education (per the [Presto explainer](references/presto-tpch-vs-tpcds.md)). | Not suitable as a benchmark source. |

Recommendation: use the official kit (or the copy above) to write files once, then load the same files into every engine.

## License terms that affect this repo

From the EULA shipped in the kit (read, not legal advice):
- You may modify the software, and distribute it under the same terms (no fee).
- You may **not** publicly disclose performance results from it, except (1) as an official TPC result, (2) as part of an academic or research effort that does not imply a marketing position, or (3) any other use, **provided results are clearly identified as not being comparable to TPC Benchmark Results**.
- Consequence: results from this repo must carry that label. The kit itself, the query templates and the answer sets are **not** committed here.

## Build and generate (verified)

```bash
sudo apt-get install gcc make flex bison    # lex/yacc needed for the query generator
git clone https://github.com/gregrahn/tpcds-kit
cd tpcds-kit/tools
make OS=LINUX CC="gcc -fcommon"             # -fcommon is needed with GCC 10 or newer
mkdir -p ../../tpcds_sf1
./dsdgen -SCALE 1 -DIR ../../tpcds_sf1 -TERMINATE N -QUIET Y
```

Observed: about 75 seconds for SF1 on this machine. Without `-fcommon` the build fails with "multiple definition" link errors on modern GCC.

## What data is generated (verified)

25 files: 24 tables plus `dbgen_version` (one row of generator metadata, not part of the benchmark). Pipe-delimited text, no header, UTF-8, empty field for NULL. `-TERMINATE N` removes the trailing delimiter.

| Table | Type | Rows at SF1 | Columns |
|---|---|---|---|
| store_sales | fact | 2,880,404 | 23 |
| catalog_sales | fact | 1,441,548 | 34 |
| web_sales | fact | 719,384 | 34 |
| store_returns | fact | 287,514 | 20 |
| catalog_returns | fact | 144,067 | 27 |
| web_returns | fact | 71,763 | 24 |
| inventory | fact | 11,745,000 | 4 |
| customer_demographics | dimension | 1,920,800 | 9 |
| customer | dimension | 100,000 | 18 |
| date_dim | dimension | 73,049 | 28 |
| time_dim | dimension | 86,400 | 10 |
| customer_address | dimension | 50,000 | 13 |
| item | dimension | 18,000 | 22 |
| catalog_page | dimension | 11,718 | 9 |
| household_demographics | dimension | 7,200 | 5 |
| promotion | dimension | 300 | 19 |
| web_page | dimension | 60 | 14 |
| web_site | dimension | 30 | 26 |
| store | dimension | 12 | 29 |
| ship_mode | dimension | 20 | 6 |
| income_band | dimension | 20 | 3 |
| reason | dimension | 35 | 3 |
| call_center | dimension | 6 | 31 |
| warehouse | dimension | 5 | 14 |

All 24 row counts match Table 3-2 of the specification for the 1GB column exactly (spec). The 7 fact and 17 dimension split matches the [Presto explainer](references/presto-tpch-vs-tpcds.md).

### Size

| SF1 format | Size |
|---|---|
| Raw text from `dsdgen` | about 1.2 GB |
| Parquet, Snappy (exported from DuckDB) | about 368 MiB |

So Parquet is roughly 3.3x smaller than raw text. As with TPC-H, "X GB" must say whether it means raw or Parquet. Three tables dominate: store_sales (137 MB as Parquet), catalog_sales (104 MB), web_sales (50 MB), then inventory (41 MB).

### Scaling is not linear (spec)

Unlike TPC-H, dimension tables scale much more slowly than fact tables. From Table 3-2:

| Table | 1GB | 1TB | Growth |
|---|---|---|---|
| store_sales | 2.88 M | 2.88 B | about 1000x |
| catalog_sales | 1.44 M | 1.44 B | about 1000x |
| inventory | 11.7 M | 783 M | about 67x |
| customer | 100 K | 12 M | 120x |
| item | 18 K | 300 K | about 17x |
| store | 12 | 1,002 | about 84x |
| customer_demographics, date_dim, time_dim, household_demographics, income_band, ship_mode | fixed | same | none |

Consequence: the join mix changes with scale. A result at SF1 does not predict SF1000.

### Official scale factors (spec)

The only valid scale factors for an official TPC-DS result are 1TB, 3TB, 10TB, 30TB and 100TB (SF 1000 to 100000). The 1GB size exists only for the qualification (query validation) database, and `dsqgen` prints "This scale factor is valid for QUALIFICATION ONLY" at SF1. Any smaller scale is useful for development, but results are not comparable with official ones, and the spec states that results at different scale factors are not comparable.

### Data properties (measured on store_sales at SF1)

| Property | Measured |
|---|---|
| Seasonality | Strong. Share of rows by month: Jan 5.8%, Feb to Jul 4.5% to 4.9% each, Aug to Oct 10.7% to 11.2%, Nov 15.9%, Dec 17.0%. Nov plus Dec is 33% of all sales. |
| NULLs | About 4.5% of rows have a NULL customer, quantity and sold date. |
| Item skew | Mild: 18,000 items, average 160 rows per item, maximum 384 (2.4x the average). |
| Customer skew | Mild: 90,858 customers, average 30.3 rows each, maximum 139 (about 4.6x). |
| Sold date range | 1998-01-02 to 2003-01-02 |

So the Presto explainer's "significant data skew" claim holds for **time** (seasonality) and for NULLs, but key skew on items and customers is modest at SF1. Skew at larger scales was not measured.

## What queries are executed (verified)

99 query templates, `query1.tpl` to `query99.tpl`, plus 14 variant templates (10a, 14a, 18a, 22a, 27a, 35a, 36a, 51a, 5a, 67a, 70a, 77a, 80a, 86a) for engines that cannot run the original. Four templates (14, 23, 24, 39) produce two statements each, so there are 103 result sets.

How queries are produced:
- `dsqgen` fills a template with random parameter values from a seed (`-RNGSEED`). Different seeds give different literal values in the same query shape.
- `-QUALIFY Y` uses the official fixed parameter values, which the specification (Appendix B) defines for validation.
- A stream is the 99 queries in a random permutation. "Query 90" in the output file was template `query18`, so the position in a stream is not the template number. The comment line before each query names the template.

```bash
# all 99 queries, one stream, official qualification parameters
./dsqgen -DIRECTORY ../query_templates -INPUT ../query_templates/templates.lst \
  -OUTPUT_DIR ../../ds_queries -DIALECT duckdb -SCALE 1 -QUALIFY Y
```

What the queries contain (counted with regular expressions on the generated SQL, so approximate):

| Feature | Queries |
|---|---|
| Common table expressions (`WITH`) | 30 |
| Window functions (`OVER`) | 15 |
| `UNION` | 18 |
| `ROLLUP` | 11 |
| `EXISTS` | 5 |
| `INTERSECT` | 3 |
| `EXCEPT` | 1 |
| `GROUPING` | 4 |

Joins: most queries touch 3 to 6 tables (distribution: 3 tables 17 queries, 4: 24, 5: 21, 6: 18, 7 or more: 19). The widest touches 13 tables (query 64). Channel coverage: 62 queries use one sales channel, 14 use two, 22 use all three, and one (query 41) uses no fact table at all. Fact table use: store_sales 67 queries, catalog_sales 39, web_sales 36, store_returns 16, catalog_returns 13, web_returns 11, inventory 6.

Query templates are **not** copied into this repo. Generate them from the kit.

### Dialect changes needed (DuckDB 1.5.6, verified)

A dialect file defines how the generator prints SQL. I used a copy of `ansi.tpl` with the row limit moved to the end (`limit N`). With that, 83 of 99 queries ran as generated. The rest failed for two reasons, and a mechanical rewrite fixed all of them:

| Problem | Queries | Fix |
|---|---|---|
| `date + 30 days` interval syntax | 15 (5, 12, 16, 20, 21, 32, 37, 40, 77, 80, 82, 92, 94, 95, 98) | rewrite to `date + INTERVAL 30 DAY` |
| `at` used as a table alias, which is a reserved word in DuckDB | 1 (query 90) | rename the alias |
| `returns` used as a column alias | query 77 | rename the alias |

After these three rewrites, all 99 queries execute. This is a sign that dialect rewrites are an unavoidable part of running TPC-DS on a new engine. Under the spec, any change to a template must follow its modification rules (Clause 4.2), and this repo should publish every rewrite it applies.

## Correctness check (unresolved)

The kit ships official answer sets (`answer_sets/`, 129 files; some queries have two files for NULL ordering). I compared my results, using the official qualification parameters, with them by a loose test (same row count and numeric sums within 0.1%).

- Result: **4 of 99 matched**. 95 differed.
- Eight queries (8, 24, 25, 29, 37, 41, 54, 58) returned **zero rows** on my data, though their answer sets have rows.
- My row counts match the spec exactly (see above), and the query parameters match the official ones (for example query 3 uses manufacturer 436 and month 12 in both). The answers have the same structure (same brands, same years) but different amounts.
- **Cause not determined.** Candidates, none checked: the answer sets were produced from data created with different generator settings or a different generator version; my comparison is too crude; a DuckDB semantic difference (unlikely to explain zero-row results).

Until this is resolved, do **not** claim that TPC-DS results on this setup are validated. The only claims supported are that the data has the specified row counts and that all 99 queries execute.

Spec rule for reference (Clause 7.3): validation uses the qualification database (SF1, populated by `dsdgen`), the official qualification parameters, and compares output to the answer sets (a sample of rows must match in position, with allowance for NULL ordering).

## When to prefer which

| Use TPC-H when | Use TPC-DS when |
|---|---|
| you want a simple, widely compared baseline | you want to stress the optimizer and SQL coverage |
| every engine must run the same SQL with little change | you accept dialect rewrites per engine |
| you can verify results easily (known answers for Q1 and Q6) | you can afford 99 queries per trial and have a validation plan |

For the first study in this repo, TPC-H remains the pragmatic choice. TPC-DS becomes realistic once the correctness check above is resolved.

## What it does not represent

Like TPC-H: no concurrency in a single stream, no streaming, no wide or nested data, and results are tuned-for because engines optimize for TPC benchmarks. Its data is synthetic, and its key skew is mild at SF1.

## To verify before relying on it

1. Why results do not match the answer sets (generator version or seed, comparison method).
2. Skew and NULL behavior at larger scale factors.
3. The DuckDB `tpcds` extension route (`CALL dsdgen(sf=1)`), in an environment where it can be installed.
4. Whether the official tpc.org download is identical to the GitHub copy.
