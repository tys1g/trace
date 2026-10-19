from datetime import UTC, datetime, timedelta

from trace_agent.anomaly import detect_observation_anomalies
from trace_agent.timeseries import Observation


def run_demo() -> None:
    """Run TRACE against a clearly labeled synthetic time series."""
    start = datetime(2026, 10, 19, 9, tzinfo=UTC)
    values = [98, 102, 101, 99, 100, 165]

    observations = [
        Observation(
            timestamp=start + timedelta(hours=index),
            metric="api_requests_per_minute",
            value=value,
        )
        for index, value in enumerate(values)
    ]

    anomalies = detect_observation_anomalies(observations)

    print("TRACE demo — synthetic data")
    print(f"Metric: {observations[0].metric}")
    print(f"Observations: {len(observations)}")
    print(f"Anomalies found: {len(anomalies)}")

    for anomaly in anomalies:
        print(
            f"- {anomaly.timestamp.isoformat()} | "
            f"value={anomaly.value:.1f}, "
            f"expected≈{anomaly.expected_value:.1f}, "
            f"deviation={anomaly.deviation_percent:+.1f}%, "
            f"severity={anomaly.severity}"
        )


if __name__ == "__main__":
    run_demo()