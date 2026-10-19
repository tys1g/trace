import pytest

from trace_agent.anomaly import detect_anomalies


def test_detects_extreme_drop():
    values = [102, 98, 105, 101, 42]

    anomalies = detect_anomalies(values)

    assert len(anomalies) == 1

    anomaly = anomalies[0]

    assert anomaly.index == 4
    assert anomaly.value == 42
    assert anomaly.expected_value == 101
    assert anomaly.deviation_percent < 0


def test_returns_empty_list_for_stable_data():
    values = [100, 101, 99, 100, 102]

    assert detect_anomalies(values) == []


def test_rejects_short_series():
    with pytest.raises(ValueError, match="at least 4"):
        detect_anomalies([10, 20, 30])


def test_rejects_non_finite_values():
    with pytest.raises(ValueError, match="finite"):
        detect_anomalies([10, 11, float("nan"), 12])


def test_rejects_non_positive_threshold():
    with pytest.raises(ValueError, match="positive"):
        detect_anomalies([10, 11, 12, 13], threshold=0)

def test_detects_anomaly_when_mad_is_zero():
    values = [100, 100, 100, 100, 10]

    anomalies = detect_anomalies(values)

    assert len(anomalies) == 1
    assert anomalies[0].index == 4
    assert anomalies[0].value == 10
    assert anomalies[0].expected_value == 100
    assert anomalies[0].severity == "high"