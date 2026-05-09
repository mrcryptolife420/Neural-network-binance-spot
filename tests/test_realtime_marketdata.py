import unittest
from decimal import Decimal

from binance_spot_bot.market_data_source import DemoMarketReplaySource, StaticMarketDataSource
from binance_spot_bot.market_stream import (
    ReconnectPolicy,
    combined_stream_url,
    parse_stream_message,
    stream_name,
    subscribe_payload,
    unsubscribe_payload,
)
from binance_spot_bot.orderbook import DepthBookBuilder, TopOfBookFeed
from binance_spot_bot.types import AccountState, Candle, RiskDecisionType, Signal, SignalSide
from binance_spot_bot.risk import RiskEngine, RiskLimits


class RealtimeMarketDataTests(unittest.TestCase):
    def test_stream_url_and_payloads_force_lowercase_symbol(self):
        streams = [stream_name("BTCUSDT", "kline", "1m"), stream_name("BTCUSDT", "bookTicker")]
        self.assertEqual(streams, ["btcusdt@kline_1m", "btcusdt@bookTicker"])
        self.assertIn("btcusdt@kline_1m/btcusdt@bookTicker", combined_stream_url(streams))
        self.assertEqual(subscribe_payload(streams, 7)["method"], "SUBSCRIBE")
        self.assertEqual(unsubscribe_payload(streams, 8)["id"], 8)

    def test_parse_official_shape_kline_and_book_ticker(self):
        kline = parse_stream_message(
            {
                "e": "kline",
                "E": 1672515782136,
                "s": "BNBBTC",
                "k": {
                    "t": 1672515780000,
                    "T": 1672515839999,
                    "s": "BNBBTC",
                    "i": "1m",
                    "o": "0.0010",
                    "c": "0.0020",
                    "h": "0.0025",
                    "l": "0.0015",
                    "v": "1000",
                    "n": 100,
                    "x": False,
                },
            }
        )
        book = parse_stream_message(
            {"u": 400900217, "s": "BNBUSDT", "b": "25.35190000", "B": "31.21000000", "a": "25.36520000", "A": "40.66000000"}
        )
        self.assertEqual(kline.symbol, "BNBBTC")
        self.assertEqual(book.bid, Decimal("25.35190000"))

    def test_reconnect_policy_handles_error_and_24h_rotation(self):
        policy = ReconnectPolicy(base_delay_seconds=1, max_connection_age_ms=100)
        self.assertTrue(policy.evaluate(connected=True, connection_started_ms=0, now_ms=101).should_reconnect)
        decision = policy.evaluate(connected=True, connection_started_ms=0, now_ms=50, last_error="timeout")
        self.assertEqual(decision.reason, "timeout")
        self.assertGreaterEqual(decision.delay_seconds, 1)

    def test_book_ticker_to_market_state_and_stale_risk_block(self):
        event = parse_stream_message(
            {"u": 1, "E": 1_000, "s": "BTCUSDT", "b": "99", "B": "2", "a": "101", "A": "3"}
        )
        feed = TopOfBookFeed()
        feed.update(event, received_time_ms=1_000)
        market = feed.market_state("BTCUSDT", Decimal("100"), now_ms=200_000)
        self.assertEqual(market.bid, Decimal("99"))
        self.assertEqual(market.ask, Decimal("101"))
        engine = RiskEngine(
            RiskLimits(
                max_daily_loss_quote=Decimal("50"),
                max_position_quote=Decimal("25"),
                max_trades_per_day=5,
                min_signal_confidence=0.1,
                max_spread_bps=Decimal("1000"),
                max_data_age_ms=1_000,
            ),
            kill_switch=False,
        )
        decision = engine.decide(
            Signal(SignalSide.BUY, 0.9, "3 bars", "test"),
            account=AccountState(quote_balance=Decimal("100")),
            market=market,
        )
        self.assertEqual(decision.decision, RiskDecisionType.BLOCK)
        self.assertEqual(decision.reason, "market data is stale")

    def test_depth_gap_requires_resync(self):
        builder = DepthBookBuilder()
        builder.apply_snapshot(10)
        self.assertTrue(builder.apply_diff(11, 12))
        self.assertFalse(builder.apply_diff(15, 16))
        self.assertTrue(builder.resync_required)

    def test_data_source_contracts(self):
        candle = Candle(0, Decimal("1"), Decimal("2"), Decimal("1"), Decimal("1.5"), Decimal("10"), 59_999)
        static = StaticMarketDataSource("BTCUSDT", [candle])
        self.assertIsNotNone(static.next_event())
        self.assertEqual(static.snapshot().source, "static")
        demo = DemoMarketReplaySource("BTCUSDT", count=3)
        self.assertIsNotNone(demo.next_event())
        self.assertEqual(demo.status().status, "ok")


if __name__ == "__main__":
    unittest.main()
