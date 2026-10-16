# References: datasets

Reading about the benchmark datasets themselves. Notes on the datasets are in [tpc-h.md](tpc-h.md) and [tpc-ds.md](tpc-ds.md). Critiques of benchmarking in general are in [../methodology/references.md](../methodology/references.md).

Read status:
- **snippet**: only search-result snippets were seen, not the full page.
- **unread**: could not be fetched or summarized.

| Source | Status | What it contains |
|---|---|---|
| [TPC-H vs TPC-DS: Benchmarking Modern Distributed SQL Engines (Presto)](https://prestodb.io/blog/2026/01/30/tpc-h-vs-tpc-ds-benchmarking-modern-distributed-sql-engines-presto/) (PrestoDB blog, Saurabh Mahawar of IBM, 30 Jan 2026) | read (PDF print provided by the repo owner; some images did not render) | Introductory explainer on TPC-H and TPC-DS: schemas, query sets, data generation, and the claim that TPC-DS has real-world skew while TPC-H is uniform. No benchmark results. Written by a Presto project author. **Full summary, facts and cautions: [references/presto-tpch-vs-tpcds.md](references/presto-tpch-vs-tpcds.md).** |

## Related, found while searching (not requested, not read)

- [Presto benchmarking tutorial: TPC-H and TPC-DS on Iceberg with Google Cloud Storage](https://prestodb.io/blog/2026/05/03/presto-benchmarking-tutorial-tpc-h-tpc-ds-on-iceberg-with-google-cloud-storage-gcs/) (PrestoDB, 3 May 2026): by its title, a how-to for running both suites on object storage with Iceberg. Could be useful for the "data in object storage" question in the framing study.

## To do

- Check the TPC-DS claims in [tpc-ds.md](tpc-ds.md) (table counts, skew) against generated data. The Presto post agrees with them but is a secondary source.
