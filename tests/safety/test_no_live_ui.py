import unittest

from binance_spot_bot.ui.state import SELECTABLE_MODES


class NoLiveUiTests(unittest.TestCase):
    def test_dashboard_modes_do_not_include_live(self):
        self.assertNotIn("live", SELECTABLE_MODES)


if __name__ == "__main__":
    unittest.main()
