import os
import json

from unittest import TestCase

from ..trade import ClientLog, Seller


class TestClientLog(TestCase, ClientLog):
    def setUp(self):
        ClientLog.__init__(self)

    def test_test(self):
        self.assertTrue(1 == 1)


class TestSeller(TestCase, Seller):
    def setUp(self):
        Seller.__init__(self)

    def test_update_trade_summary(self):
        self.update_trade_summary('test')
        self.assertTrue(os.path.exists(self.trade_summary_path))
