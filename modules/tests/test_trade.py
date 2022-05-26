import os
import json

from unittest import TestCase

from ..trade import ClientLog, Seller, TradeBot


class TestClientLog(TestCase, ClientLog):
    def setUp(self):
        ClientLog.__init__(self)

    def test_test(self):
        self.assertTrue(1 == 1)


class TestSeller(TestCase, Seller):
    def setUp(self):
        pass


class TestTradeBot(TestCase, TradeBot):
    def setUp(self):
        Seller.__init__(self)
        self.trade_summary_path = 'temp/test_trade_summary.json'

    def test_update_trade_summary(self):
        self.update_trade_summary('test')
        data = self.load_json_file(self.trade_summary_path)
        self.assertTrue(os.path.exists(self.trade_summary_path))
        self.assertTrue(len(data) == 1)
        self.assertTrue(data[0]['item_id'] == 'test')
        self.assertTrue(data[0]['item_amount'] == 1)
        self.update_trade_summary('test')
        data = self.load_json_file(self.trade_summary_path)
        self.assertTrue(data[0]['item_amount'] == 2)

        self.update_trade_summary('test1')
        data = self.load_json_file(self.trade_summary_path)
        self.assertTrue(len(data) == 2)
        self.update_trade_summary('test1')
        self.update_trade_summary('test1')
        data = self.load_json_file(self.trade_summary_path)
        self.assertTrue(data[1]['item_amount'] == 3)

        self.update_trade_summary('test2')
        data = self.load_json_file(self.trade_summary_path)
        self.assertTrue(len(data) == 3)
        self.update_trade_summary('test2')
        self.update_trade_summary('test2')
        self.update_trade_summary('test2')

        data = self.load_json_file(self.trade_summary_path)
        self.assertTrue(data[0]['item_amount'] == 2)
        self.assertTrue(data[1]['item_amount'] == 3)
        self.assertTrue(data[2]['item_amount'] == 4)

        os.remove(self.trade_summary_path)
