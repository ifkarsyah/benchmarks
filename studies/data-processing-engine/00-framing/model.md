# Model: what a data processing engine is, and what it costs

Tool-agnostic. No engine is named in this file on purpose.

## 1. Definition

A data processing engine takes (data, logic, resources) and returns (result, time, cost).

| Input | Examples of variation |
|---|---|
| Data | size, format, location, skew, schema width |
| Logic | scan and filter, aggregate, join, window, UDF |
| Resources | cores, memory, disk, network, number of machines |

| Output | Examples of variation |
|---|---|
| Result | correctness, freshness, who can read it and how |
| Time | total wall time, time to first result, tail latency |
| Cost | money, operator effort, idle cost |

## 2. Parts that can differ

These are the places two engines can genuinely differ. A benchmark is only useful if it can tell these apart.

1. **Storage access.** How bytes get from the source (remote object store, local disk, native format) into memory. Includes connector quality and caching.
2. **Execution model.** Row at a time, vectorized batches, or compiled code.
3. **Parallelism.** Threads on one machine, or many machines with network shuffle.
4. **Memory management.** What happens when the working set exceeds RAM: spill, fail, or stream.
5. **Fault tolerance.** Restart from scratch, or recover from a checkpoint.
6. **State.** Whether the engine keeps long-lived state (needed for streaming and incremental work).
7. **API surface.** SQL, dataframe, or both, and how much code changes when the mode changes (batch vs stream).
8. **Serving interface.** Whether a person or another application can query results directly.

## 3. Decisions the benchmark must support

Metrics exist to serve decisions. Each decision below is a candidate. The user should confirm, cut or add.

| ID | Decision | Who decides |
|---|---|---|
| D1 | Which engine to use for a given data volume | data engineer |
| D2 | One machine or a cluster | data engineer, budget owner |
| D3 | Query data in place (for example in object storage) or load it into the engine first | data engineer |
| D4 | Batch or streaming for a given job, and how costly it is to switch later | data engineer, product owner |
| D5 | How business users and downstream applications read the results | platform owner |
| D6 | What the pipeline costs to run and to operate | budget owner |

Rule: a metric that does not feed at least one decision above is dropped.

## 4. Cost model

Treat run time as limited by the slowest of three resources, plus fixed overhead:

```
time ~= max(t_io, t_cpu, t_shuffle) + t_fixed
```

- `t_io = bytes_read / read_bandwidth`
- `t_cpu = work / (cores * per_core_rate)`
- `t_shuffle = bytes_exchanged / network_bandwidth` (zero on one machine)
- `t_fixed`: startup, planning, scheduling, JIT. Dominates at small data sizes.

This is a first-order model. It will be wrong in the details (overlap of IO and CPU is imperfect, spilling changes `t_io`). Its value is to give predictions that real measurements can contradict.

## 5. Bounds the model gives before any run

### Bandwidth floor

No engine can read faster than the link or disk allows.

```python
def min_read_seconds(size_gb: float, bandwidth_gbit_per_s: float) -> float:
    """Lower bound on read time, ignoring everything but raw bandwidth."""
    gb_per_s = bandwidth_gbit_per_s / 8
    return size_gb / gb_per_s


# 1000 GB over a 25 Gbit/s link:
print(min_read_seconds(1000, 25))  # 320.0 seconds, about 5.3 minutes
```

Consequence: if remote storage results at 1000 GB sit near this floor, the benchmark is measuring the network, not the engine. Real S3 throughput per instance is often below the instance network limit, so the true floor is higher. It must be measured, not assumed.

### Single-machine limit

When the working set exceeds RAM, the engine either spills to disk, streams through, or fails. Time then depends on disk bandwidth and on how well the engine overlaps IO with CPU. The data size where this happens, relative to RAM, is more informative than the absolute size.

### When distribution pays off

Using Amdahl's law, speedup from `n` machines is limited by the part that cannot be parallelized, plus the added shuffle and coordination cost. Distribution pays off when parallel gain exceeds that overhead. Below some data size it never does, which is why a distributed engine on small data can lose to one process on one machine.

### Break-even for loading data into native storage

```python
def break_even_queries(load_seconds: float, query_seconds_in_place: float, query_seconds_native: float) -> float:
    """Number of queries after which loading into native storage has paid for itself."""
    saving = query_seconds_in_place - query_seconds_native
    if saving <= 0:
        return float("inf")  # native storage never repays the load
    return load_seconds / saving
```

A native format that is faster per query but expensive to load is only a win if the data is queried often enough.

## 6. What this model cannot say

- Whether results transfer to skewed or very wide data.
- Real behavior under concurrent users.
- Engine quality when it has had less tuning effort than another.
- Anything about correctness or developer experience beyond what is listed in section 2.

These are limits to restate in any later benchmark report.
