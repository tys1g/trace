from dataclasses import dataclass, replace
from datetime import datetime

import numpy as np
import pandas as pd

from trace_agent.timeseries import Observation


@dataclass(frozen=True)
class Anomaly:
    index: int
    value: float
    expected_value: float
    deviation_percent: float
    severity: str
    timestamp: datetime | None = None
    metric: str | None = None


def detect_anomalies(
    values: list[float],
    threshold: float = 3.0,
) -> list[Anomaly]:
    """Detect anomalous values using a robust MAD-based score."""
    if threshold <= 0:
        raise ValueError("threshold must be positive")

    if len(values) < 4:
        raise ValueError("at least 4 values are required")

    series = pd.Series(values, dtype="float64")

    if not np.isfinite(series.to_numpy()).all():
        raise ValueError("values must be finite numbers")

    median = float(series.median())
    absolute_deviations = (series - median).abs()
    mad = float(absolute_deviations.median())

    if mad == 0:
        candidates = series[series != median]
        return [
            Anomaly(
                index=int(index),
                value=float(value),
                expected_value=median,
                deviation_percent=(
                    (float(value) - median) / abs(median) * 100
                    if median != 0
                    else 0.0
                ),
                severity="high",
            )
            for index, value in candidates.items()
        ]

    robust_scores = 0.6745 * (series - median) / mad
    anomalies = []

    for index, score in robust_scores.items():
        if abs(score) < threshold:
            continue

        value = float(series.iloc[index])
        deviation_percent = (
            (value - median) / abs(median) * 100
            if median != 0
            else 0.0
        )

        anomalies.append(
            Anomaly(
                index=int(index),
                value=value,
                expected_value=median,
                deviation_percent=deviation_percent,
                severity="high" if abs(score) >= 5 else "medium",
            )
        )

    return anomalies


def detect_observation_anomalies(
    observations: list[Observation],
    threshold: float = 3.0,
) -> list[Anomaly]:
    """Detect anomalies and attach each result's timestamp and metric."""
    if not all(isinstance(item, Observation) for item in observations):
        raise TypeError("observations must contain Observation objects")

    anomalies = detect_anomalies(
        [observation.value for observation in observations],
        threshold=threshold,
    )

    return [
        replace(
            anomaly,
            timestamp=observations[anomaly.index].timestamp,
            metric=observations[anomaly.index].metric,
        )
        for anomaly in anomalies
    ]