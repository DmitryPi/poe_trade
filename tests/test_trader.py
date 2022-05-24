import json

from datetime import datetime
from unittest import TestCase
from pprint import pprint

from main import Trader
from modules.trader import ClientLog


class TestTrader(TestCase, Trader):
    def setUp(self):
        Trader.__init__(self)
        self.item = 'rusted-legion-scarab'
        self.item_0 = 'Bated Breath'
        self.item_type = 'scarab'
        self.item_type_1 = 'Chain Belt'
        self.item_currency = 'chaos'
        self.min_price = 1
        self.max_price = 3
        self.trade_item_addition = {
            "priority": 8.6,
            "min_price": self.min_price,
            "max_price": self.max_price,
            "max_stock_price": 0,
            "min_stock_amount": 1,
            "disabled": False
        }
        self.trade_item = {
            "item_id": self.item,
            "buyout_currency": self.item_currency,
            "type": self.item_type,
        }
        self.trade_item.update(self.trade_item_addition)
        self.trade_item_1 = {
            "item_id": self.item_0,
            "buyout_currency": self.item_currency,
            "type": self.item_type_1,
        }
        self.trade_item_1.update(self.trade_item_addition)
        self.is_bulk = bool(
            self.trade_item['type'] in self.trade_bulk_types)
        self.is_bulk_1 = bool(
            self.trade_item_1['type'] in self.trade_bulk_types)

    def test_load_trade_template(self):
        single_tmplt = str(self.load_trade_template(self.trade_item))
        assert self.item in single_tmplt
        assert self.item_currency not in single_tmplt
        assert 'trade_filters' in single_tmplt
        bulk_tmplt = str(
            self.load_trade_template(self.trade_item, bulk=True))
        assert self.item in bulk_tmplt
        assert self.item_currency in bulk_tmplt
        assert "'status': {'option': 'online'}" in bulk_tmplt

    def test_api_request_bulk(self):
        template = self.load_trade_template(
            self.trade_item, bulk=self.is_bulk)
        assert self.is_bulk
        assert template
        assert self.item_currency in str(template)
        resp = self.api_request(self.trade_item, bulk=self.is_bulk)
        assert resp.status_code == 200
        assert 'result' in str(resp.content)
        resp = json.loads(resp.content)
        assert isinstance(resp['id'], str)

    def test_api_request_notbulk(self):
        template = self.load_trade_template(
            self.trade_item_1, bulk=self.is_bulk_1)
        assert not self.is_bulk_1
        assert template
        assert self.item_currency not in str(template)
        resp = self.api_request(self.trade_item_1, bulk=self.is_bulk_1)
        assert resp.status_code == 200
        assert 'result' in str(resp.content)
        resp = json.loads(resp.content)
        assert isinstance(resp['id'], str)

    def test_api_response_bulk(self):
        resp_bulk = self.api_request(self.trade_item, bulk=True)
        resp = self.api_response(resp_bulk, self.trade_item, bulk=False)
        assert isinstance(resp, tuple)
        assert isinstance(resp[0], str)
        assert len(resp[1]) > 0

    def test_api_response_nobulk(self):
        resp_nobulk = self.api_request(self.trade_item_1, bulk=False)
        resp = self.api_response(
            resp_nobulk, self.trade_item_1, bulk=False)
        assert isinstance(resp, tuple)
        assert isinstance(resp[0], str)

    def test_api_fetch_page_bulk(self):
        resp_bulk = self.api_request(self.trade_item, bulk=True)
        resp_id, resp_pagin = self.api_response(
            resp_bulk, self.trade_item, bulk=True)
        page_resp = self.api_fetch_page(resp_id, resp_pagin[0], bulk=True)
        page_content = json.loads(page_resp.content)
        page_result = page_content.get('result', None)
        assert page_resp.status_code == 200
        assert page_result
        assert len(page_result) >= 10
        item = page_result[0]['item']
        item_id = page_result[0]['id']
        item_listing = page_result[0]['listing']
        assert item_id
        assert item['league'] == self.trade_league
        assert item['typeLine'] == 'Rusted Legion Scarab'
        assert item_listing['price']['exchange']['amount'] >= 1
        assert item_listing['price']['exchange']['currency'] == 'chaos'
        assert item_listing['price']['item']['amount'] >= 1
        assert item_listing['price']['item']['stock'] >= 1
        assert self.item_currency in item_listing['whisper'].lower()

    def test_api_fetch_page_nobulk(self):
        resp_nobulk = self.api_request(self.trade_item_1, bulk=False)
        resp_id, resp_pagin = self.api_response(
            resp_nobulk, self.trade_item_1, bulk=False)
        page_resp = self.api_fetch_page(resp_id, resp_pagin[0], bulk=False)
        page_content = json.loads(page_resp.content)
        page_result = page_content.get('result', None)
        assert page_resp.status_code == 200
        assert page_result
        item = page_result[0]['item']
        item_id = page_result[0]['id']
        item_listing = page_result[0]['listing']
        assert item_id
        assert item['league'] == self.trade_league
        assert item['name'] == self.item_0
        assert item['typeLine'] == self.item_type_1
        assert not item_listing['price'].get('exchange', None)
        assert not item_listing['price'].get('item', None)
        assert item_listing['price']['amount'] >= self.min_price
        assert item_listing['price']['amount'] <= self.max_price
        assert item_listing['price']['currency'] == self.item_currency
        assert self.item_currency in item_listing['whisper'].lower()


class TestClientLog(TestCase, ClientLog):
    def setUp(self):
        ClientLog.__init__(self)
        self.test_lines = [
            '2020/07/05 13:19:33 [INFO Client 18568] @To Tyo_: ty, gl',
            'asdfsadf asdfsadf sdafsdaf',
            '{0} [INFO Client 18568] @From Tyo_: ty',
            '2020/07/05 20:06:40 [INFO Client 4756] @To RealMadJack: 123',
            '2020/07/05 20:06:40 [INFO Client 4756] @To 문자: 123',
            '2020/07/05 19:52:16 [DEBUG Client 4756] Connect time to instance',
            '2020/07/05 19:07:39 [INFO Client 4756] @To โล้นซ่าท้าทวยเทพ: สวัสดี',
            '2020/07/05 20:06:40 [INFO Client 4756] @From RealMadJack: 123',
            '2020/07/05 20:06:40 [INFO Client 4756] @From 문자: 123',
            '2020/07/05 19:07:39 [INFO Client 4756] @From โล้นซ่าท้า: สวัสดี',
        ]

    def test_log_datetime_filter(self):
        assert not self.log_datetime_filter(self.test_lines[0], time_limit=120)
        assert not self.log_datetime_filter(self.test_lines[1], time_limit=120)
        line_2 = self.test_lines[2].format(str(datetime.now()))
        assert self.log_datetime_filter(line_2, time_limit=120)

    def test_log_to_filter(self):
        assert not self.log_to_filter(self.test_lines[1])
        assert not self.log_to_filter(self.test_lines[2])
        assert not self.log_to_filter(self.test_lines[5])
        assert self.log_to_filter(self.test_lines[0]) == 'Tyo_'
        assert self.log_to_filter(self.test_lines[3]) == 'RealMadJack'
        assert self.log_to_filter(self.test_lines[4]) == '문자'
        assert self.log_to_filter(self.test_lines[6]) == 'โล้นซ่าท้าทวยเทพ'

    def test_log_from_filter(self):
        assert not self.log_from_filter(self.test_lines[0])
        assert not self.log_from_filter(self.test_lines[1])
        assert not self.log_from_filter(self.test_lines[4])
        assert self.log_from_filter(self.test_lines[7]) == 'RealMadJack'
        assert self.log_from_filter(self.test_lines[8]) == '문자'
        assert self.log_from_filter(self.test_lines[9]) == 'โล้นซ่าท้า'
