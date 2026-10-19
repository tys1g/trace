from datetime import UTC, datetime

import pytest

from trace_agent.timeseries import Observation


def test_creates_observation():
    observation = Observation(
        timestamp=datetime(2026, 10, 19, tzinfo=UTC),
        metric="sales",
        value=42.0,
    )

    assert observation.metric == "sales"
    assert observation.value == 42.0


def test_rejects_invalid_timestamp():
    with pytest.raises(TypeError, match="datetime"):
        Observation(timestamp="2026-10-19", metric="sales", value=42.0)


def test_rejects_empty_metric():
    with pytest.raises(ValueError, match="non-empty"):
        Observation(
            timestamp=datetime(2026, 10, 19, tzinfo=UTC),
            metric=" ",
            value=42.0,
        )


def test_rejects_non_finite_value():
    with pytest.raises(ValueError, match="finite"):
        Observation(
            timestamp=datetime(2026, 10, 19, tzinfo=UTC),
            metric="sales",
            value=float("nan"),
        )