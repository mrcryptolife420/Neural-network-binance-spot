from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class TrainingStep:
    step_id: str
    instruction: str
    safe_command: str = ""
    live_trading_enabled: bool = False


@dataclass(frozen=True)
class TrainingLesson:
    lesson_id: str
    title: str
    mode: str
    steps: list[TrainingStep]
    no_live_banner: str = "OPERATOR TRAINING - NO LIVE TRADING"
    live_trading_enabled: bool = False


def build_training_lessons(level: str = "beginner") -> dict[str, Any]:
    lessons = [
        TrainingLesson(
            "lesson-no-live",
            "Verify no-live safety",
            level,
            [
                TrainingStep("step-1", "Run config validation", "python -m binance_spot_bot.cli validate-config"),
                TrainingStep("step-2", "Run no-live proof", "python -m binance_spot_bot.cli no-live-proof-pack --json"),
            ],
        ),
        TrainingLesson(
            "lesson-dashboard",
            "Open and inspect dashboard safely",
            level,
            [TrainingStep("step-1", "Run dashboard smoke", "python -m binance_spot_bot.cli dashboard-smoke --seconds 1")],
        ),
    ]
    return {"status": "ok", "lessons": [asdict(lesson) for lesson in lessons], "live_trading_enabled": False}


def operator_training(topic: str) -> dict[str, Any]:
    payload = build_training_lessons(topic)
    payload["topic"] = topic
    return payload
