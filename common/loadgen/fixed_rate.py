"""Fixed-rate load generator that avoids coordinated omission.

Each request has an INTENDED send time on a fixed schedule. Latency is measured
from the intended time, not from when the send actually happened. If the sender
stalls, the delay is charged to the system instead of being hidden.

The generator is transport-agnostic: pass any `send(i)` callable (Kafka produce,
HTTP call, file write). Run it in a separate process from the system under test.
"""

from __future__ import annotations

import time
from typing import Callable, List


def run_fixed_rate(
    send: Callable[[int], None],
    rate_per_sec: float,
    duration_sec: float,
    clock: Callable[[], float] = time.perf_counter,
    sleep: Callable[[float], None] = time.sleep,
) -> List[float]:
    """Send at a fixed rate and return per-request latencies in milliseconds.

    `send` must block until the request is acknowledged. For fire-and-forget
    producers, record latency in the ack callback instead of using this helper.
    """
    interval = 1.0 / rate_per_sec
    total = int(rate_per_sec * duration_sec)
    start = clock()
    latencies: List[float] = []

    for i in range(total):
        intended = start + i * interval
        now = clock()
        if now < intended:
            sleep(intended - now)
        send(i)
        done = clock()
        # Measured from the intended time, so a stall shows up as latency.
        latencies.append((done - intended) * 1000.0)

    return latencies
