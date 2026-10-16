# Statistics for benchmarking

The subset that covers most real cases. Helpers live in [common/stats.py](../common/stats.py).

## Confidence interval

A 95% confidence interval comes from a method that, repeated many times, would produce intervals containing the true value about 95% of the time. It does not mean there is a 95% probability the true value sits in one particular interval, although in practice people read it that way.

Practical points:

- Wider interval means noisier data or fewer trials. Width shrinks roughly with 1 / sqrt(n), so four times the trials halves the width.
- Compare systems with an interval on the difference or ratio, not by eyeballing two separate intervals.
- If the interval of the ratio contains 1.0, there is no evidence of a difference.

## The unit of analysis is the trial

Your sample size is the number of independent trials, not the number of events. One run with 10 million events is still n = 1 for the question "how fast is system A?". Events inside a run share GC pauses, caches, and network state.

Computing an interval from millions of events in one run is called pseudo-replication. It makes results look far more certain than they are.

## Essentials

1. **Percentiles over averages.** Latency is heavy-tailed, closer to lognormal than normal.
2. **Never average percentiles.** The mean of five p99 values is not the p99 of the combined data. Pool raw data or merge histograms (HdrHistogram).
3. **Standard deviation vs standard error.** SD describes spread of individual measurements. Standard error (SD / sqrt(n)) describes uncertainty of the estimate. Intervals use standard error.
4. **Small samples need the t-distribution.** With 5 trials a normal approximation is too narrow.
5. **Effect size over significance.** With enough trials a 0.5% difference becomes significant. Decide in advance what size matters.
6. **Warmup and stationarity.** Plot the time series. Drift (leaks, growing state) hides inside averages.
7. **Do not silently drop outliers.** In latency work they are often the finding. State any exclusion rule beforehand.
8. **Geometric mean for ratios.** Summarize "A is x times B" across many queries with the geometric mean of ratios.

## Nice to have

- **Multiple comparisons.** With 22 queries at p < 0.05 you expect about one false win. Use Holm or Bonferroni, or report everything.
- **Power.** If trial-to-trial variation is 15% and you care about 5%, five trials will not detect it. Estimate trials needed before running.
- **Bootstrap caveat.** Bootstrap intervals are too narrow with very small samples. With fewer than about 10 trials, prefer a t-interval or permutation test and treat any interval as rough.
- **Medians at small n.** With 5 to 8 trials the median is a coarse statistic. A permutation test on medians can have almost no power even when the groups are clearly separated, so `permutation_test` defaults to the mean. Use `statistic="median"` only with more trials.

## Which tool for which job

| Situation | Use |
|---|---|
| Interval for one system's mean, n < 30 | `t_interval` |
| Is A different from B, no normality assumption | `permutation_test` or Mann-Whitney U |
| Interval for the ratio of medians, n >= 10 | `bootstrap_ratio_ci` |
| Combine latency across runs or nodes | HdrHistogram merge |
| Summarize speedup across many queries | `geometric_mean` |

## Further reading

- Alex Reinhart, *Statistics Done Wrong*
- Raj Jain, *The Art of Computer Systems Performance Analysis*
- Brendan Gregg, *Systems Performance*
- Gil Tene, talk "How NOT to Measure Latency"
