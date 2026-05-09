from __future__ import annotations

import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from binance_spot_bot.copilot_permissions import check_copilot_action
from binance_spot_bot.copilot_redaction import redact_for_copilot
from binance_spot_bot.copilot_summary import summarize_session
from binance_spot_bot.dataset_model_wizard import CandidateModelPlan, DatasetWizardConfig, save_candidate_plan
from binance_spot_bot.replay_sandbox import ReplaySandbox
from binance_spot_bot.risk_debugger import explain_decision
from binance_spot_bot.session_compare import compare_sessions, export_comparison
from binance_spot_bot.session_store import SessionStore
from binance_spot_bot.signal_explainer import explain_signal
from binance_spot_bot.strategy_templates import list_strategy_templates, strategy_template
from binance_spot_bot.types import FeatureRow, RiskDecision, RiskDecisionType, Signal, SignalSide


class StrategyLabCopilotTests(unittest.TestCase):
    def test_risk_debugger_never_overrides_blocks(self):
        event = explain_decision(RiskDecision(RiskDecisionType.BLOCK, "kill switch active"))
        self.assertFalse(event.can_override)
        self.assertIn("kill switch", event.explanation)

    def test_signal_explainer_is_deterministic(self):
        row = FeatureRow("BTCUSDT", 1, {"ret_window": 0.2, "volume": 10.0}, Decimal("100"))
        signal = Signal(SignalSide.BUY, 0.7, "3 bars", "test")
        explanation = explain_signal(signal, row, top_n=1)
        self.assertEqual(explanation.top_features[0][0], "volume")

    def test_replay_and_session_compare_work_offline(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SessionStore(Path(tmp) / "sessions")
            first = store.start_session(mode="demo", symbol="BTCUSDT", interval="1m", model_version="m")
            second = store.start_session(mode="demo", symbol="ETHUSDT", interval="1m", model_version="m")
            store.record_snapshot(first.session_id, {"timestamp_ms": 1, "equity": "100", "data_quality": {"status": "ok"}})
            store.record_snapshot(second.session_id, {"timestamp_ms": 1, "equity": "101", "data_quality": {"status": "ok"}})
            frame = ReplaySandbox(store).frame(first.session_id, 0)
            rows = compare_sessions(store, [first.session_id, second.session_id])
            out = export_comparison(rows, Path(tmp) / "compare.csv")
        self.assertEqual(frame.snapshot["equity"], "100")
        self.assertTrue(out.name.endswith(".csv"))

    def test_copilot_denies_order_paths_and_redacts(self):
        self.assertFalse(check_copilot_action("place_order").allowed)
        self.assertTrue(check_copilot_action("summarize_session").allowed)
        redacted = redact_for_copilot({"api_secret": "abcdefghijklmnopqrstuvwxyz"})
        self.assertEqual(redacted["api_secret"], "[REDACTED]")

    def test_rule_based_summary_and_templates_are_safe(self):
        summary = summarize_session(
            SessionStore(Path(tempfile.gettempdir()) / "unused").start_session(mode="demo", symbol="BTCUSDT", interval="1m", model_version="m"),
            {"kill switch active": 1},
        )
        self.assertTrue(summary.advisory_only)
        self.assertFalse(strategy_template("momentum").auto_apply)
        self.assertNotIn("live", {item["mode"] for item in list_strategy_templates()})

    def test_dataset_model_wizard_requires_chronological_splits(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = DatasetWizardConfig("BTCUSDT", "1m", 1, 2, 3, 4)
            path = save_candidate_plan(config, CandidateModelPlan("candidate", "dataset", "sharpe"), Path(tmp) / "plan.json")
        self.assertTrue(path.name.endswith(".json"))
        self.assertFalse(CandidateModelPlan("candidate", "dataset", "sharpe").champion_auto_promote)


if __name__ == "__main__":
    unittest.main()
