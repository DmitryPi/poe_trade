import re
import os
import time
import pytest

from unittest import TestCase

from ..trade import ClientLog, TradeBot


class TestClientLog(TestCase, ClientLog):
    def setUp(self):
        ClientLog.__init__(self)
        self.test_lines = [
            "2022/05/28 17:26:54 326039687 cff9459d [INFO Client 8768] @From <|NOPE|> 匚卄尺丨丂: Hi, I'd like to buy your 20 Gilded Blight Scarab for my 110 Chaos Orb in Sentinel.",
            "2022/05/28 01:48:27 269733406 cff9459d [INFO Client 21168] @From Dpg_CoC: Hi, I'd like to buy your 3 Exalted Orb for my 510 Chaos Orb in Sentinel.",
            "2022/05/28 01:48:59 269764718 cff9459d [INFO Client 21168] @To BremsspurBernhard: sold",
            "2022/05/28 01:45:22 269547718 cff9459d [INFO Client 21168] @From <øJTFø> KluskaNaKlamce: Hi, I'd like to buy your 30 Polished Divination Scarab for my 195 Chaos Orb in Sentinel.",
            "2022/05/28 17:33:19 326425218 cff9459d [INFO Client 8768] @From <~•Lc•~> มาเเจกดวง: Hi, I'd like to buy your 20 Bound Fossil for my 138 Chaos Orb in Sentinel.",
            "2022/05/28 01:43:24 269430328 cff9459d [INFO Client 21168] @From <øJTFø> MarjoNoHope: ty!",
            "2022/05/28 10:39:47 301612937 cff9459d [INFO Client 8220] @From muzzchump: Hi, I'd like to buy your 20 Polished Harbinger Scarab for my 98 Chaos Orb in Sentinel.",
            "2022/05/28 10:40:04 301630281 cff9459d [INFO Client 8220] : muzzchump has joined the area.",
            "2022/05/28 11:15:55 303781140 cff9459d [INFO Client 8220] @From Пюрен: Hi, I'd like to buy your 20 Gilded Blight Scarab for my 110 Chaos Orb in Sentinel.",
            "2022/05/28 11:31:23 304709515 cff9459d [INFO Client 6620] @From 아버지아버지아버지: Hi, I'd like to buy your 27 Gilded Reliquary Scarab for my 135 Chaos Orb in Sentinel.",
            "2022/05/28 11:34:31 304897078 cff9459d [INFO Client 6620] @To 異體字異體字: Hi, I'd like to buy your 27 Gilded Reliquary Scarab for my 135 Chaos Orb in Sentinel.",
            "2022/05/28 17:33:16 326422562 cff9459d [INFO Client 8768] : Trade accepted.",
            "2022/05/28 17:33:08 326414015 cff9459d [INFO Client 8768] : Trade cancelled.",
            "2022/05/28 17:36:55 326641546 cff9459d [INFO Client 8768] : Trade accepted.",
            "2022/05/28 17:36:55 326641546 cff9459d [INFO Client 8768] : Trade cancelled.",
        ]
        self.test_lines_1 = [
            "2022/05/28 17:35:06 326532046 cff9459d [INFO Client 8768] : Daleellaa has joined the area.",
            "2022/05/28 17:34:53 326519609 cff9459d [INFO Client 8768] : Padak_Wp has left the area.",
            "2022/05/28 17:35:06 326532046 cff9459d [INFO Client 8768] : 아버지아버지아버지 has joined the area.",
            "2022/05/28 17:34:53 326519609 cff9459d [INFO Client 8768] : Пюрен has left the area.",
            "2022/05/28 17:33:53 326459093 cff9459d [INFO Client 8768] : มาเเจกดวง has left the area.",
        ]

    def test_log_filter_by_time(self):
        result = []
        for line in self.test_lines:
            log_result = self.log_filter_by_time(line, time_limit=120)
            if log_result:
                result.append(log_result)
        self.assertTrue(not len(result))
        for line in self.test_lines:
            log_result = self.log_filter_by_time(line, time_limit=9999999)
            if log_result:
                result.append(log_result)
        self.assertTrue(len(result) == len(self.test_lines))

    def test_log_filter_datetime(self):
        result = []
        for line in self.test_lines:
            log_result = self.log_filter_datetime(line)
            if log_result:
                self.assertTrue(re.match(r'^\d{4}[/]\d{2}[/]\d{2}$', log_result[0]))
                self.assertTrue(re.match(r'^\d{2}[:]\d{2}[:]\d{2}$', log_result[1]))
                result.append(log_result)
        self.assertTrue(len(result) == len(self.test_lines))

    def test_log_filter_name(self):
        result = []
        for line in self.test_lines:
            log_result = self.log_filter_name(line, msg_type='from')
            if log_result:
                self.assertTrue('<' not in log_result)
                self.assertTrue('>' not in log_result)
                result.append(log_result)
        self.assertTrue(len(result) == 8)

    def test_log_filter_buy_msg(self):
        result = []
        for line in self.test_lines:
            log_result = self.log_filter_buy_msg(line)
            if log_result:
                self.assertTrue(len(log_result) == 4)
                self.assertTrue(re.match(r'^\w+[-]\w+[-]?\w+$', log_result[0]))
                self.assertTrue(isinstance(log_result[1], int))
                self.assertTrue(re.match(r'^\w+[-]\w+$', log_result[2]))
                self.assertTrue(isinstance(log_result[3], int))
                result.append(log_result)
        self.assertTrue(len(result) == 8)

    def test_log_filter_instance_state(self):
        result = []
        for line in self.test_lines_1:
            log_result = self.log_filter_instance_state(line)
            if log_result:
                self.assertTrue(len(log_result) == 3)
                self.assertTrue(log_result[0] == 'joined' or log_result[0] == 'left')
                self.assertTrue(isinstance(log_result[2], tuple))
                self.assertTrue(len(log_result[2]) == 2)
                result.append(log_result)
        self.assertTrue(len(result) == len(self.test_lines_1))

    def test_log_build_buy_msg(self):
        result = []
        for line in self.test_lines:
            log_result = self.log_build_buy_msg(line)
            if log_result:
                self.assertTrue(isinstance(log_result[0], str))
                self.assertTrue(len(log_result[0]))
                self.assertTrue(len(log_result[1]) == 4)
                self.assertTrue(isinstance(log_result[2], tuple))
                self.assertTrue(len(log_result[2]) == 2)
                result.append(log_result)
        self.assertTrue(len(result) == 7)

    @pytest.mark.slow
    def test_log_manage(self):
        log_results = self.log_manage(time_limit=300)
        for log in log_results:
            print(log)


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
    def test_stash_set_price(self):
        scarabs = [
            ('rusted-expedition-scarab', 50),
            ('polished-expedition-scarab', 20),
            ('gilded-divination-scarab', '5/50'),
            ('gilded-breach-scarab', 100),
        ]
        for scarab in scarabs:
            self.stash_set_item_price(scarab[0], scarab[1])

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
