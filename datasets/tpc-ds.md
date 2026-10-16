# TPC-DS

Status: **from memory, not verified.** Unlike TPC-H, no TPC-DS data could be generated in this repo's environment (the DuckDB `tpcds` extension host and tpc.org were blocked, and no PyPI generator was found). Every number below needs checking against generated data before it is cited. Items I am less sure about are marked "unsure".

## What it is

A decision support benchmark from the TPC, newer and harder than TPC-H. It models a retailer that sells through three channels: physical stores, a catalog and the web. It is designed to be closer to a real data warehouse than TPC-H.

## Schema

24 tables:

- **7 fact tables:** `store_sales`, `store_returns`, `catalog_sales`, `catalog_returns`, `web_sales`, `web_returns`, `inventory`.
- **17 dimension tables:** for example `date_dim`, `time_dim`, `item`, `customer`, `customer_address`, `customer_demographics`, `household_demographics`, `store`, `warehouse`, `promotion`, `web_site`, `web_page`, `call_center`, `catalog_page`, `ship_mode`, `reason`, `income_band`.

The shape is a set of star schemas (one per channel) that share dimensions, sometimes called a snowflake or constellation schema. Queries often join facts from different channels through shared dimensions.

## Queries

99 query templates (unsure whether any are counted as variants; some templates are commonly run in two parts, so you may see a count slightly above 99). The query generator fills in random parameter values, so the exact query text depends on a seed.

Compared with TPC-H, the SQL is more demanding: common table expressions, subqueries, window functions, `ROLLUP`, set operations (`INTERSECT`, `EXCEPT`), and many multi-way joins. This stresses query optimizers and SQL feature coverage much more than TPC-H does. Some engines cannot run all 99 queries unmodified.

## Data properties (unsure)

- The data has some non-uniform distributions and seasonality in sales, and contains NULLs. It is less uniform than TPC-H, but still synthetic. Check how skewed it actually is before relying on this.
- The scale factor works like TPC-H's: it is a label, and raw data at SF1 is roughly 1 GB as text. The Parquet size, row counts per table and the SF to GB mapping all need measuring.

## Generation (not run here)

DuckDB bundles a generator in its `tpcds` extension. This is the usual route, and I could not run it in this environment, so treat it as untested:

```python
import duckdb

con = duckdb.connect()
con.execute("INSTALL tpcds; LOAD tpcds;")
con.execute("CALL dsdgen(sf=1)")  # creates the 24 tables in the database
print(con.execute("select count(*) from store_sales").fetchone())
```

DuckDB can also run the 99 queries through the extension. The official tools are `dsdgen` (data) and `dsqgen` (queries), available from tpc.org.

## When to prefer which

| Use TPC-H when | Use TPC-DS when |
|---|---|
| you want a simple, widely compared baseline | you want to stress the optimizer and SQL coverage |
| engines must all run the same SQL easily | you accept that some engines will fail some queries |
| you need small effort to set up and verify | you can afford 99 queries per trial |

For the first study in this repo, TPC-H is the pragmatic choice. TPC-DS is a candidate for a later phase, once a harness exists and the engines under test can run enough of its queries.

## What it still does not represent

Like TPC-H: no concurrency by default, no streaming, no real-world skew at scale, and no wide or nested data. Its results are also tuned-for, since engines optimize for TPC benchmarks.

## To verify before citing

1. Table count (24) and the fact versus dimension split.
2. Query count and whether variants exist. (A secondary source, the [awesome-olap list](../methodology/references.md), also says 99 queries across fact and dimension tables. That agrees with this file but is not a primary check.)
3. Row counts and Parquet size at SF1.
4. How non-uniform the generated data actually is.
5. The `dsdgen` call above, in an environment where the extension can be downloaded.
