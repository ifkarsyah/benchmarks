import numpy as np
import pytest

from common.loadgen.fixed_rate import run_fixed_rate
from common.stats import (
    bootstrap_ratio_ci,
    find_sustainable_rate,
    geometric_mean,
    holm_correction,
    percentiles,
    permutation_test,
    t_interval,
)


def test_percentiles_basic():
    p = percentiles(range(1, 101))
    assert p[50] == pytest.approx(50.5)
    assert p[99] == pytest.approx(99.01)


def test_t_interval_contains_mean():
    r = t_interval([10, 11, 9, 10, 12])
    assert r["low"] < r["mean"] < r["high"]
    assert r["n"] == 5


def test_permutation_detects_clear_difference():
    a = [100, 102, 101, 99, 103, 100, 101]
    b = [120, 121, 119, 122, 118, 120, 121]
    assert permutation_test(a, b)["p_value"] < 0.01


def test_permutation_no_difference():
    rng = np.random.default_rng(1)
    a = rng.normal(100, 5, 10)
    b = rng.normal(100, 5, 10)
    assert permutation_test(a, b)["p_value"] > 0.05


def test_bootstrap_flags_small_samples():
    r = bootstrap_ratio_ci([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    assert r["reliable"] is False


def test_geometric_mean():
    assert geometric_mean([2, 8]) == pytest.approx(4.0)


def test_holm_monotone_and_bounded():
    adj = holm_correction([0.01, 0.04, 0.03])
    assert all(0 <= x <= 1 for x in adj)
    assert adj[0] == pytest.approx(0.03)


def test_find_sustainable_rate():
    # System keeps up at or below 1000 events/sec
    rate = find_sustainable_rate(lambda r: r <= 1000, low=100, high=5000)
    assert 900 <= rate <= 1000


def test_loadgen_charges_stalls_to_latency():
    # Fake clock: send() takes 0 time except the 3rd call, which stalls 1s.
    t = {"now": 0.0}

    def clock():
        return t["now"]

    def sleep(s):
        t["now"] += s

    def send(i):
        if i == 2:
            t["now"] += 1.0

    lat = run_fixed_rate(send, rate_per_sec=10, duration_sec=1, clock=clock, sleep=sleep)
    # The stalled request and the ones queued behind it must show high latency.
    assert max(lat) >= 900
    assert lat[3] > 800
