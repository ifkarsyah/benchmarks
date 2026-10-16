# References: datasets

Reading about the benchmark datasets themselves. Notes on the datasets are in [tpc-h.md](tpc-h.md) and [tpc-ds.md](tpc-ds.md). Critiques of benchmarking in general are in [../methodology/references.md](../methodology/references.md).

Read status:
- **snippet**: only search-result snippets were seen, not the full page.
- **unread**: could not be fetched or summarized.

| Source | Status | What it contains |
|---|---|---|
| [TPC-H vs TPC-DS: Benchmarking Modern Distributed SQL Engines (Presto)](https://prestodb.io/blog/2026/01/30/tpc-h-vs-tpc-ds-benchmarking-modern-distributed-sql-engines-presto/) (PrestoDB blog, 30 Jan 2026) | snippet | Compares the two suites as yardsticks for distributed SQL engines. Frames performance as a mix of I/O throughput, CPU efficiency, network shuffle and optimizer quality. Notes the TPC (founded 1988) replaced vendor claims with audited benchmark data, and that benchmarks need fixed schemas so every engine runs the same tables. The snippets cut off before any results or the actual comparison, so those are not summarized. Written by the Presto project, so read it with that in mind. |

## Related, found while searching (not requested, not read)

- [Presto benchmarking tutorial: TPC-H and TPC-DS on Iceberg with Google Cloud Storage](https://prestodb.io/blog/2026/05/03/presto-benchmarking-tutorial-tpc-h-tpc-ds-on-iceberg-with-google-cloud-storage-gcs/) (PrestoDB, 3 May 2026): by its title, a how-to for running both suites on object storage with Iceberg. Could be useful for the "data in object storage" question in the framing study.

## To do

- Read the Presto post and add what it says about the differences between TPC-H and TPC-DS to [tpc-ds.md](tpc-ds.md), whose table is currently from memory. Check each claim against generated TPC-DS data before relying on it.
