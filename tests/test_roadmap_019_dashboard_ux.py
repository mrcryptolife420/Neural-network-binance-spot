from __future__ import annotations

import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from binance_spot_bot.demo_pilot import operator_checklist, pipeline_rows
from binance_spot_bot.session_report import export_session_report
from binance_spot_bot.session_store import SessionStore
from binance_spot_bot.types import Candle
from binance_spot_bot.ui.charts import candlestick_figure


class Roadmap019DashboardUxTests(unittest.TestCase):
    def payload(self) -> dict[str, object]:
        return {
            "exchange_profile": {"name": "binance-demo-spot"},
            "credential_status": {
                "profile": "binance-demo-spot",
                "has_api_key": True,
                "has_api_secret": True,
                "capability": "Credentials loaded for signed checks",
            },
            "demo_connection": {
                "profile": "binance-demo-spot",
                "base_url": "https://demo-api.binance.com/api",
                "armed": True,
                "connected": True,
                "authenticated": True,
                "gate": {"reason": "allowed", "checks": {"demo_base_url": True}},
            },
            "demo_account": {"status": "ok", "can_trade": True, "balances": []},
            "reconciliation": {"status": "ok", "orphan_orders": 0, "failures": 0, "needs_operator_action": False},
            "testnet_prechecks": {"risk_limits_set": True},
            "demo_pilot": {
                "config": {"pilot_name": "smoke", "max_demo_orders": 5},
                "counters": {"orders": 1, "rejects": 0},
            },
            "latest_signal": {"signal": "BUY", "model_version": "baseline"},
            "latest_risk_decision": {
                "decision": "ALLOW",
                "reason": "risk ok",
                "intent": {"side": "BUY", "quote_size": "10"},
            },
            "latest_execution_result": {
                "status": "ACCEPTED",
                "order_request": {"client_order_id": "demo-1"},
                "response": {"orderId": 1001, "status": "NEW"},
            },
            "resume_required": False,
        }

    def test_operator_checklist_and_pipeline_payloads(self):
        payload = self.payload()
        checklist = operator_checklist(payload)
        pipeline = pipeline_rows(payload)

        self.assertTrue(any(row["check"] == "Profile" and row["status"] == "pass" for row in checklist))
        self.assertTrue(any(row["check"] == "Armed" and row["status"] == "pass" for row in checklist))
        self.assertEqual([row["step"] for row in pipeline][0], "Signal")
        self.assertTrue(any(row["step"] == "Demo order" and row["reference"] == "1001" for row in pipeline))

    def test_chart_accepts_empty_data_and_demo_markers(self):
        empty = candlestick_figure([], [], [], open_orders=[], reconciliation_events=[])
        self.assertEqual(len(empty.data), 0)

        candle = Candle(
            open_time_ms=1_000,
            open=Decimal("100"),
            high=Decimal("110"),
            low=Decimal("90"),
            close=Decimal("105"),
            volume=Decimal("1"),
            close_time_ms=61_000,
        )
        fig = candlestick_figure(
            [candle],
            [{"side": "BUY", "timestamp_ms": 61_000, "price": "105"}],
            [{"timestamp_ms": 61_000, "price": "106"}],
            open_orders=[{"orderId": 1001, "price": "107"}],
            reconciliation_events=[{"type": "QUERY_ORDER", "checked_at_ms": 61_000}],
        )
        self.assertIn("Open demo orders", [trace.name for trace in fig.data])
        self.assertIn("Reconciliation", [trace.name for trace in fig.data])

    def test_session_report_contains_demo_pilot_operator_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = SessionStore(Path(tmp) / "sessions")
            session = store.start_session(
                mode="demo",
                symbol="BTCUSDT",
                interval="1m",
                model_version="baseline",
                metadata={
                    "demo_pilot": self.payload()["demo_pilot"],
                    "reconciliation": self.payload()["reconciliation"],
                    "cancel_on_stop_status": [],
                },
            )
            store.record_snapshot(session.session_id, self.payload())
            paths = export_session_report(store, session.session_id)
            pilot = json.loads(Path(paths["demo_pilot_json"]).read_text(encoding="utf-8"))
            markdown = Path(paths["demo_pilot_md"]).read_text(encoding="utf-8")

        self.assertIn("operator_checklist", pilot)
        self.assertIn("pipeline", pilot)
        self.assertIn("## Operator checklist", markdown)
        self.assertIn("## Signal to order pipeline", markdown)

    def test_dashboard_module_imports(self):
        import binance_spot_bot.ui.streamlit_app as streamlit_app

        self.assertTrue(callable(streamlit_app.main))


if __name__ == "__main__":
    unittest.main()
