"""Statistics helpers for benchmark analysis.

Conventions:
- The unit of analysis is the TRIAL. Pass one number per trial, not one per event.
- Never average percentiles. Compute percentiles on pooled raw data or merged histograms.
"""

from __future__ import annotations

from typing import Callable, Dict, Iterable, Sequence

import numpy as np
from scipy import stats as sps

DEFAULT_PERCENTILES = (50, 90, 99, 99.9)


def percentiles(values: Iterable[float], ps: Sequence[float] = DEFAULT_PERCENTILES) -> Dict[float, float]:
    """Percentiles of raw values (for example latencies in ms from one pooled run)."""
    a = np.asarray(list(values), dtype=float)
    if a.size == 0:
        raise ValueError("no values")
    return {p: float(np.percentile(a, p)) for p in ps}


def t_interval(trials: Sequence[float], confidence: float = 0.95) -> Dict[str, float]:
    """t-based confidence interval for the mean of per-trial values. Suitable for small n."""
    a = np.asarray(trials, dtype=float)
    if a.size < 2:
        raise ValueError("need at least 2 trials")
    mean = float(a.mean())
    sem = float(sps.sem(a))
    lo, hi = sps.t.interval(confidence, df=a.size - 1, loc=mean, scale=sem)
    return {"mean": mean, "low": float(lo), "high": float(hi), "n": int(a.size)}


def permutation_test(
    a: Sequence[float],
    b: Sequence[float],
    n_perm: int = 20_000,
    seed: int = 0,
    statistic: str = "mean",
) -> Dict[str, float]:
    """Two-sided permutation test on the difference of per-trial values.

    Makes no normality assumption and stays honest at small n.
    Returns the observed difference (stat(a) - stat(b)) and a p-value.

    statistic: "mean" (default) or "median". Prefer "mean" when n is small:
    with few trials the median is a coarse statistic and the test loses almost
    all power, because shuffled groups often produce a large median gap anyway.
    """
    if statistic not in ("mean", "median"):
        raise ValueError("statistic must be 'mean' or 'median'")
    stat = np.mean if statistic == "mean" else np.median
    rng = np.random.default_rng(seed)
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    observed = float(stat(a) - stat(b))
    pooled = np.concatenate([a, b])
    count = 0
    for _ in range(n_perm):
        rng.shuffle(pooled)
        diff = stat(pooled[: a.size]) - stat(pooled[a.size :])
        if abs(diff) >= abs(observed):
            count += 1
    # +1 smoothing so the p-value is never exactly zero
    p = (count + 1) / (n_perm + 1)
    return {"observed_diff": observed, "p_value": float(p)}


def bootstrap_ratio_ci(
    a: Sequence[float],
    b: Sequence[float],
    confidence: float = 0.95,
    n_boot: int = 10_000,
    seed: int = 0,
) -> Dict[str, float]:
    """Bootstrap interval for median(a) / median(b), resampling trials.

    Warning: with fewer than ~10 trials per side the interval is too narrow.
    A ValueError is NOT raised, but `reliable` is False in that case.
    """
    rng = np.random.default_rng(seed)
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    ratios = np.empty(n_boot)
    for i in range(n_boot):
        ra = np.median(rng.choice(a, a.size, replace=True))
        rb = np.median(rng.choice(b, b.size, replace=True))
        ratios[i] = ra / rb
    alpha = (1 - confidence) / 2 * 100
    low, high = np.percentile(ratios, [alpha, 100 - alpha])
    return {
        "ratio": float(np.median(a) / np.median(b)),
        "low": float(low),
        "high": float(high),
        "reliable": bool(min(a.size, b.size) >= 10),
    }


def geometric_mean(ratios: Sequence[float]) -> float:
    """Geometric mean, the right way to summarize speedup ratios across many queries."""
    r = np.asarray(ratios, dtype=float)
    if np.any(r <= 0):
        raise ValueError("ratios must be positive")
    return float(np.exp(np.mean(np.log(r))))


def holm_correction(p_values: Sequence[float]) -> list:
    """Holm-Bonferroni adjusted p-values, returned in the original order."""
    p = np.asarray(p_values, dtype=float)
    m = p.size
    order = np.argsort(p)
    adjusted = np.empty(m)
    running_max = 0.0
    for rank, idx in enumerate(order):
        val = (m - rank) * p[idx]
        running_max = max(running_max, val)
        adjusted[idx] = min(1.0, running_max)
    return adjusted.tolist()


def find_sustainable_rate(
    run_at_rate: Callable[[float], bool],
    low: float,
    high: float,
    tolerance: float = 0.05,
) -> float:
    """Binary search for the highest input rate where backlog stays flat.

    run_at_rate(rate) must run a full trial at that rate and return True if the
    system kept up (for example consumer lag did not grow during steady state).
    `low` should be a rate known to be sustainable, `high` one known to fail.
    """
    best = low
    while (high - low) / high > tolerance:
        mid = (low + high) / 2
        if run_at_rate(mid):
            best, low = mid, mid
        else:
            high = mid
    return best
