# Benchmark checklist

Copy the relevant parts into a study's README and tick them off as you go.

## 1. Define the question

A benchmark answers one question. "Which is faster?" is not a question.

- [ ] Question written as one sentence, naming the workload and the metric
- [ ] Decision this benchmark will inform (migrate? buy? size a cluster?)
- [ ] Effect size that would change the decision (for example 10%)

Good example: "For a keyed 1-minute tumbling-window count, what is the highest rate each engine sustains, and what is p99 latency at 50% of that rate?"

## 2. Choose the workload

- [ ] Realistic, not only synthetic max throughput
- [ ] Public or self-generated data with a documented distribution
- [ ] Load generator is a separate process from the system under test
- [ ] Data size and key distribution written down (uniform vs skewed)

## 3. Control variables

Change one thing. Write the held-constant list before running anything.

- [ ] Same hardware, instance type, region, and network
- [ ] Same JVM version and flags where relevant
- [ ] Same replication, durability (fsync), and checkpoint settings
- [ ] Same data layout (file size, compression, partitioning)
- [ ] Equal tuning budget per system, with final configs committed
- [ ] Defaults that differ between systems identified and decided on purpose

## 4. Choose metrics

- [ ] Primary metric (sustainable throughput, p99 latency, query time)
- [ ] Secondary metrics (CPU, memory, recovery time, bytes scanned)
- [ ] Cost metric (core-hours per unit of work)
- [ ] Tail latency (p99, p99.9), not only averages
- [ ] Latency measured from intended send time (avoids coordinated omission)

Sustainable throughput means the highest input rate where backlog stays flat for the whole run. Peak throughput of a system that is falling behind is not a result.

## 5. Run protocol

- [ ] Warmup discarded (JIT, caches)
- [ ] Fixed steady-state measurement window
- [ ] At least 5 trials, preferably 10 or more, on fresh environments
- [ ] Cold vs warm cache decided and reported
- [ ] Run order interleaved (A B B A A B), not all A then all B
- [ ] Time series plotted before summarizing, to check for drift

## 6. Analyze

- [ ] Trial is the unit of analysis, not event (see statistics.md)
- [ ] Percentiles merged from raw data or histograms, never averaged
- [ ] Interval reported for the difference or ratio, not two separate intervals
- [ ] Effect size reported, not only a p-value
- [ ] All queries or scenarios reported, no cherry-picking

## 7. Failure tests and reporting

- [ ] At least one failure scenario (kill a worker, concurrent writers, network delay)
- [ ] Full config, versions, hardware, and raw data committed
- [ ] Threats to validity section written
- [ ] List of what was not tested
- [ ] Reproduction command in the README

## Common pitfalls

- Benchmarking the default config of one system against a tuned config of the other.
- Comparing systems that are in different categories (for example micro-batch vs record-at-a-time) without saying so.
- Comparing table formats in isolation. You are measuring format plus engine plus catalog plus maintenance jobs.
- Letting checkpoint or commit intervals differ between systems.
- Reporting one lucky run.
