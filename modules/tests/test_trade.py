import os
import time
import pytest

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
        TradeBot.__init__(self)
        self.trade_summary_path = 'temp/test_trade_summary.json'

    @pytest.mark.slow
    def test_stash_activate_tab(self):
        self.stash_activate_tab('currency', subtab='exotic')
        time.sleep(1)
        self.stash_activate_tab('fragment', subtab='breach')
        time.sleep(1)
        self.stash_activate_tab('fragment', subtab='scarab')
        time.sleep(1)
        self.stash_activate_tab('hdf')

    @pytest.mark.slow
    def test_stash_take_item(self):
        scarabs = [
            ('rusted-expedition-scarab', 50),
            ('polished-expedition-scarab', 20),
            ('gilded-divination-scarab', 30),
            ('gilded-breach-scarab', 100),
        ]
        for scarab in scarabs:
            print('- Scarab:', scarab)
            self.stash_take_item(scarab[0], amount=scarab[1])
            time.sleep(1)

    @pytest.mark.slow
    def test_unstuck_currency(self):
        self.unstuck_currency((1297, 615), 5)

    def test_update_trade_summary(self):
        self.update_trade_summary('test', 2)  # 0 += 2
        data = self.load_json_file(self.trade_summary_path)
        self.assertTrue(os.path.exists(self.trade_summary_path))
        self.assertTrue(len(data) == 1)
        self.assertTrue(data[0]['item_id'] == 'test')
        self.assertTrue(data[0]['item_amount'] == 2)

        self.update_trade_summary('test', 5)  # 2 += 5
        data = self.load_json_file(self.trade_summary_path)
        self.assertTrue(data[0]['item_amount'] == 7)

        self.update_trade_summary('test1', 5)  # 0 += 5
        data = self.load_json_file(self.trade_summary_path)
        self.assertTrue(len(data) == 2)
        self.update_trade_summary('test1', 5)  # 5 += 5
        self.update_trade_summary('test1', 3)  # 10 += 3
        data = self.load_json_file(self.trade_summary_path)
        self.assertTrue(data[1]['item_amount'] == 13)

        self.update_trade_summary('test2', 2)  # 0 += 2
        data = self.load_json_file(self.trade_summary_path)
        self.assertTrue(len(data) == 3)
        self.update_trade_summary('test2', 10)
        self.update_trade_summary('test2', 1)
        self.update_trade_summary('test2', 111)

        data = self.load_json_file(self.trade_summary_path)
        self.assertTrue(data[0]['item_amount'] == 7)
        self.assertTrue(data[1]['item_amount'] == 13)
        self.assertTrue(data[2]['item_amount'] == 124)

        os.remove(self.trade_summary_path)
