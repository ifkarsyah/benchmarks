# TPC-H

Status: facts marked **verified** were checked by generating SF1 data in this repo's environment (generator: `tpchgen-cli` 2.0.2, a Rust port of dbgen, output read with DuckDB 1.5.6). Facts marked **from memory** were not checked here. Anything not marked is a plain definition.

## What it is

An ad hoc decision support benchmark from the Transaction Processing Performance Council (TPC). It models a wholesale supplier: customers place orders, orders contain line items, line items are parts supplied by suppliers. The workload is 22 read-only analytical queries.

It is the most widely used analytical benchmark. That is its main advantage (you can compare with many published results) and its main weakness (engines have been tuned for it for decades).

## Schema

8 tables.

```
region (5) --< nation (25) --< customer --< orders --< lineitem >-- partsupp >-- part
                          \--< supplier -------------------------------/
```

Relationships:
- `region` 1 to many `nation`.
- `nation` 1 to many `customer`, and 1 to many `supplier`.
- `customer` 1 to many `orders`; `orders` 1 to many `lineitem`.
- `part` and `supplier` many to many, through `partsupp`.
- `lineitem` references `partsupp` by (`l_partkey`, `l_suppkey`).

## Size at SF1 (verified)

| Table | Rows | Parquet size (Snappy) | Columns |
|---|---|---|---|
| lineitem | 6,001,215 | 231.7 MB | 16 |
| orders | 1,500,000 | 63.5 MB | 9 |
| partsupp | 800,000 | 44.8 MB | 5 |
| customer | 150,000 | 13.9 MB | 8 |
| part | 200,000 | 6.9 MB | 9 |
| supplier | 10,000 | 0.9 MB | 7 |
| nation | 25 | under 0.1 MB | 4 |
| region | 5 | under 0.1 MB | 3 |

`lineitem` is 69% of all rows and about 64% of Parquet bytes. Most queries are dominated by scanning and joining it.

## Scale factor is not GB (verified)

The scale factor (SF) is a label, and SF1 is about 1 GB only as raw text.

| SF1 format | Size |
|---|---|
| Raw `.tbl` text | 1.1 GB |
| Parquet, Snappy | about 362 MB (345 MiB) |

So Parquet is about 3.0x smaller than the raw text. Different generators and compression codecs will change the Parquet number.

Consequence for this repo: "1, 100, 500, 1000 GB" is ambiguous. Define it as raw or as Parquet before running anything. Linear extrapolation from SF1 (not verified beyond SF1):

| Target Parquet size | Approx. SF |
|---|---|
| 1 GB | 3 |
| 100 GB | 290 |
| 500 GB | 1,450 |
| 1000 GB | 2,900 |

Row counts scale linearly with SF, except `nation` and `region`, which are fixed (from the specification, from memory).

## The data is nearly uniform (verified at SF1)

| Property | Measured |
|---|---|
| Orders per customer (among customers who ordered) | min 1, max 41, mean 15.0 |
| Customers with no orders | 50,004 of 150,000 (one third) |
| Line items per order | min 1, max 7, mean 4.0 |
| Ship mode share | 14.27% to 14.30% for each of the 7 modes |
| Order date range | 1992-01-01 to 1998-08-02 |

Almost everything is evenly spread. Real data is usually skewed (a few customers account for most orders, hot keys, long tails). That means TPC-H cannot tell you how an engine handles skew, and join and shuffle behavior will look better than on production data.

## The 22 queries

Q1 and Q6 scan only `lineitem`. Most of the others join several tables. Two worth knowing first:

- **Q6** is a single-table filter and sum. It measures how fast an engine can scan and filter.
- **Q1** is a scan with a group by over almost all of `lineitem`, producing 4 rows. It measures scan and aggregation throughput.

Verified answers at SF1, useful as a correctness check:

| Query | Check |
|---|---|
| Q6 | revenue = 123141078.2283 |
| Q1 | 4 result rows; first row `A`, `F`, sum quantity 37734107, count 1478493 |

For reference, on this environment DuckDB ran Q6 in about 0.06 s and Q1 in about 0.10 s on SF1 Parquet. That is a single warm run, not a benchmark result.

## Generate and inspect it

```bash
pip install tpchgen-cli duckdb
tpchgen-cli parquet -s 1 --output-dir=tpch_sf1   # SF1 as Parquet, one file per table
```

```python
import duckdb

con = duckdb.connect()
path = lambda table: f"read_parquet('tpch_sf1/{table}.parquet')"

# Q6, expected result at SF1: 123141078.2283
q6 = con.execute(f"""
    select sum(l_extendedprice * l_discount)
    from {path('lineitem')}
    where l_shipdate >= date '1994-01-01' and l_shipdate < date '1995-01-01'
      and l_discount between 0.05 and 0.07 and l_quantity < 24
""").fetchone()
print(q6)
```

For other scale factors, change `-s`. Use `--parts` to write several files per table when the data is large.

## What it does not represent

- **Skew:** nearly uniform data (see above).
- **Wide or nested data:** narrow, flat tables only.
- **Concurrency and mixed workloads:** the 22 queries are run in sequence in the usual setup.
- **Updates:** the official benchmark has refresh functions (RF1, RF2), from memory. This repo runs read queries only.
- **Streaming and incremental processing:** none.

## Official rules (from memory, not verified)

The official benchmark defines a power test, a throughput test and refresh functions, and the TPC restricts how results from non-audited runs may be labeled. This repo runs the queries on its own setup, so call results "TPC-H-like" and do not present them as official TPC-H results.

## Sources

- TPC-H specification and tools: tpc.org (could not be fetched from this environment, so spec details above that are marked "from memory" are unchecked).
- Generator used for verification: https://github.com/clflushopt/tpchgen-rs
