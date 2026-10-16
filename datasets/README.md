# Datasets

Reference notes on the public datasets used by studies in this repo. Learning material, not a study: nothing here is a benchmark result.

| Dataset | Notes | Verified? |
|---|---|---|
| TPC-H | [tpc-h.md](tpc-h.md) | schema, row counts, sizes, uniformity and two query answers checked on SF1 |
| TPC-DS | [tpc-ds.md](tpc-ds.md) | from memory only, with a list of what to verify |

Further reading: [references.md](references.md).

Note: TPC-H and TPC-DS are two separate benchmarks, there is no "TPC-H-DS".

## Which to read first

Read [tpc-h.md](tpc-h.md) first. It is simpler, it is what the framing study currently proposes, and its notes are checked against real data. Then read [tpc-ds.md](tpc-ds.md) to see how the workload becomes harder.

## Three things to keep in mind

1. **Scale factor is not GB.** SF1 is 1.1 GB as raw text but about 362 MB as Parquet (TPC-H, verified). Any "X GB" statement in a study must say whether it means raw or Parquet.
2. **Both datasets are synthetic.** TPC-H data is close to uniform (verified), which hides skew and hot keys. Results may not transfer to real data.
3. **Engines are tuned for these benchmarks.** A good TPC result shows the engine is competent on a classic workload, not that it fits yours.

## Conventions for new dataset notes

- State which facts were verified and how (tool, version, scale factor).
- Mark anything from memory.
- Include a short, runnable generation snippet in Python or a CLI command.
- End with what the dataset does not represent.
