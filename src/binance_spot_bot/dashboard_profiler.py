from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from typing import Iterator


@dataclass(frozen=True)
class ProfileSample:
    name: str
    elapsed_ms: float

    def to_dict(self) -> dict[str, float | str]:
        return asdict(self)


class DashboardProfiler:
    def __init__(self) -> None:
        self.samples: list[ProfileSample] = []

    @contextmanager
    def measure(self, name: str) -> Iterator[None]:
        started = time.perf_counter()
        try:
            yield
        finally:
            self.samples.append(ProfileSample(name, (time.perf_counter() - started) * 1000))

    def to_dict(self) -> dict[str, list[dict[str, float | str]]]:
        return {"samples": [sample.to_dict() for sample in self.samples]}
