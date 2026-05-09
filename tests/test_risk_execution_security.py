import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from binance_spot_bot.audit import AuditLog
from binance_spot_bot.config import BotSettings
from binance_spot_bot.execution import ExecutionBlocked, ExecutionEngine, quantize_down
from binance_spot_bot.risk import RiskEngine, RiskLimits
from binance_spot_bot.security import scan_for_secrets
from binance_spot_bot.types import (
    AccountState,
    MarketState,
    RiskDecisionType,
    Signal,
    SignalSide,
    SymbolFilters,
    TradingMode,
)


def limits():
    return RiskLimits(
        max_daily_loss_quote=Decimal("50"),
        max_position_quote=Decimal("25"),
        max_trades_per_day=3,
        min_signal_confidence=0.6,
        max_spread_bps=Decimal("20"),
    )


def filters():
    return SymbolFilters(
        symbol="BTCUSDT",
        status="TRADING",
        tick_size=Decimal("0.01"),
        step_size=Decimal("0.00001"),
        min_qty=Decimal("0.00001"),
        max_qty=Decimal("100"),
        min_notional=Decimal("5"),
    )


class RiskExecutionSecurityTests(unittest.TestCase):
    def test_kill_switch_blocks(self):
        engine = RiskEngine(limits(), kill_switch=True)
        decision = engine.decide(
            Signal(SignalSide.BUY, 0.9, "3 bars", "test"),
            AccountState(quote_balance=Decimal("100")),
            MarketState("BTCUSDT", Decimal("100"), Decimal("99.9"), Decimal("100.1"), 1, 1),
        )
        self.assertEqual(decision.decision, RiskDecisionType.BLOCK)

    def test_risk_allows_valid_buy(self):
        engine = RiskEngine(limits(), kill_switch=False)
        decision = engine.decide(
            Signal(SignalSide.BUY, 0.9, "3 bars", "test"),
            AccountState(quote_balance=Decimal("100")),
            MarketState("BTCUSDT", Decimal("100"), Decimal("99.99"), Decimal("100.01"), 1, 1),
        )
        self.assertEqual(decision.decision, RiskDecisionType.ALLOW)

    def test_execution_quantizes_and_paper_fills(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = BotSettings(
                app_env="paper",
                trading_mode=TradingMode.PAPER,
                binance_base_url="https://api.binance.com",
                binance_testnet_base_url="https://testnet.binance.vision",
                binance_api_key="",
                binance_api_secret="",
                live_trading_enabled=False,
                kill_switch=False,
                manual_live_approval="",
                max_daily_loss_quote=Decimal("50"),
                max_position_quote=Decimal("25"),
                max_trades_per_day=3,
                min_signal_confidence=0.6,
                max_spread_bps=Decimal("20"),
                data_dir=Path(tmp) / "data",
                audit_log_path=Path(tmp) / "audit.jsonl",
            )
            risk = RiskEngine(limits(), kill_switch=False)
            decision = risk.decide(
                Signal(SignalSide.BUY, 0.9, "3 bars", "test"),
                AccountState(quote_balance=Decimal("100")),
                MarketState("BTCUSDT", Decimal("100"), Decimal("99.99"), Decimal("100.01"), 1, 1),
            )
            result = ExecutionEngine(settings, AuditLog(settings.audit_log_path)).execute(
                decision, MarketState("BTCUSDT", Decimal("100")), filters()
            )
            self.assertEqual(result.status, "FILLED")
            self.assertEqual(quantize_down(Decimal("1.234567"), Decimal("0.001")), Decimal("1.234"))

    def test_execution_blocks_below_min_notional(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = BotSettings(
                app_env="paper",
                trading_mode=TradingMode.PAPER,
                binance_base_url="https://api.binance.com",
                binance_testnet_base_url="https://testnet.binance.vision",
                binance_api_key="",
                binance_api_secret="",
                live_trading_enabled=False,
                kill_switch=False,
                manual_live_approval="",
                max_daily_loss_quote=Decimal("50"),
                max_position_quote=Decimal("1"),
                max_trades_per_day=3,
                min_signal_confidence=0.6,
                max_spread_bps=Decimal("20"),
                data_dir=Path(tmp) / "data",
                audit_log_path=Path(tmp) / "audit.jsonl",
            )
            risk_limits = limits()
            risk_limits = RiskLimits(
                max_daily_loss_quote=risk_limits.max_daily_loss_quote,
                max_position_quote=Decimal("1"),
                max_trades_per_day=risk_limits.max_trades_per_day,
                min_signal_confidence=risk_limits.min_signal_confidence,
                max_spread_bps=risk_limits.max_spread_bps,
                default_quote_size=Decimal("1"),
            )
            decision = RiskEngine(risk_limits, kill_switch=False).decide(
                Signal(SignalSide.BUY, 0.9, "3 bars", "test"),
                AccountState(quote_balance=Decimal("100")),
                MarketState("BTCUSDT", Decimal("100"), Decimal("99.99"), Decimal("100.01"), 1, 1),
            )
            with self.assertRaises(ExecutionBlocked):
                ExecutionEngine(settings, AuditLog(settings.audit_log_path)).execute(
                    decision, MarketState("BTCUSDT", Decimal("100")), filters()
                )

    def test_secret_scan_finds_obvious_secret(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.py"
            fake_secret = "sk-" + "test_1234567890abcdef123456"
            path.write_text(f'OPENAI_API_KEY="{fake_secret}"\n', encoding="utf-8")
            findings = scan_for_secrets(Path(tmp))
        self.assertEqual(len(findings), 1)


if __name__ == "__main__":
    unittest.main()
