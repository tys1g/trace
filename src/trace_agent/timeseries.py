from dataclasses import dataclass
from datetime import datetime
from math import isfinite


@dataclass(frozen=True)
class Observation:
    timestamp: datetime
    metric: str
    value: float

    def __post_init__(self) -> None:
        if not isinstance(self.timestamp, datetime):
            raise TypeError("timestamp must be a datetime")

        if not isinstance(self.metric, str) or not self.metric.strip():
            raise ValueError("metric must be a non-empty string")

        if not isinstance(self.value, int | float) or not isfinite(self.value):
            raise ValueError("value must be a finite number")