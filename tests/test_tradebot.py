from unittest import TestCase

from modules.base import Base


class TestTradeBot(TestCase, Base):
    def setUp(self):
        Base.__init__(self)

    def check_item_currency(self):
        threshold = {
            1: 0.9,  # 60
            2: 0.9,  # 59
            3: 0.9,
            4: 0.9,
            5: 0.9,
            6: 0.9,
            7: 0.9,
            8: 0.9,
            9: 0.9,
            10: 0.9,
        }
        for i in range(1, 11):
            template = f'assets/items/c_chaos_{i}_{i}.png'
            for amount in range(1, 11):
                img_inv = f'assets/tests/currency/inv_{amount}.png'
                img_trade = f'assets/tests/currency/trade_{amount}.png'
                detected_inv = self.cv_detect_boilerplate(
                    template, threshold=threshold[amount],
                    lst=True, calc_mp=True,
                    img_path=img_inv)[0]
                detected_trade = self.cv_detect_boilerplate(
                    template, threshold=threshold[amount],
                    lst=True, calc_mp=True,
                    img_path=img_trade)[0]
                filtered_inv = list()
                filtered_trade = list()
                for pt in detected_inv:
                    filtered_inv.append((pt[0], pt[1], amount))
                for pt in detected_trade:
                    filtered_trade.append((pt[0], pt[1], amount))
                print(amount, len(filtered_inv), len(filtered_trade))

            print('\n')

    def check_item_scarab(self):
        item_names = [
            'rusted-bestiary-scarab-1',
            'polished-bestiary-scarab-1',
            'rusted-sulphite-scarab-1',
            'polished-sulphite-scarab-1',
        ]
        for item_name in item_names:
            template = f'assets/items/{item_name}.png'
            threshold = {
                'rusted-bestiary-scarab-1': 0.9,
                'polished-bestiary-scarab-1': 0.9,
                'gilded-bestiary-scarab-1': 0.81,
                'rusted-sulphite-scarab-1': 0.9,
                'polished-sulphite-scarab-1': 0.9,
                'rusted-legion-scarab-1': 0.75,
                'polished-legion-scarab-1': 0.75,
                'polished-breach-scarab-1': 0.75
            }
            threshold = threshold[item_name]
            img_inv = f'assets/tests/scarabs/inv_mix_2.png'
            img_trade = f'assets/tests/scarabs/trade_mix_2.png'
            detected_inv = self.cv_detect_boilerplate(
                template, threshold=threshold,
                lst=True, calc_mp=True,
                img_path=img_inv)[0]
            detected_trade = self.cv_detect_boilerplate(
                template, threshold=threshold,
                lst=True, calc_mp=True,
                img_path=img_trade)[0]
            filtered_inv = list()
            filtered_trade = list()
            for pt in detected_inv:
                filtered_inv.append((pt[0], pt[1]))
            for pt in detected_trade:
                filtered_trade.append((pt[0], pt[1]))
            print(item_name, len(filtered_inv), len(filtered_trade))
        print('\n')

    def test_check_scarab(self):
        item_names = [
            'rusted-bestiary',
            'polished-bestiary',
            'gilded-bestiary',
        ]
        for item_name in item_names:
            template = f'assets/items/{item_name}-scarab.png'
            threshold = {
                'rusted-bestiary': 0.77,
                'polished-bestiary': 0.79,
                'gilded-bestiary': 0.83,
            }
            threshold = threshold[item_name]
            img_inv = f'assets/tests/scarabs/inv-gilded-bestiary.png'
            detected_inv = self.cv_detect_boilerplate(
                template, threshold=threshold,
                lst=True, calc_mp=True,
                img_path=img_inv)[0]
            filtered_inv = list()
            for pt in detected_inv:
                filtered_inv.append((pt[0], pt[1]))
            print(item_name, len(filtered_inv))
        print('\n')

    def check_item_fossil(self):
        threshold = {
            1: 0.9,
            2: 0.9,
            3: 0.9,
            4: 0.9,
            5: 0.9,
            6: 0.9,
            7: 0.9,
            8: 0.9,
            9: 0.9,
            10: 0.9,
            11: 0.9,
            12: 0.9,
            13: 0.9,
            14: 0.9,
            15: 0.9,
            16: 0.9,
            17: 0.9,
            18: 0.9,
            19: 0.9,
            20: 0.9,
        }
        for i in range(1, len(threshold) + 1):
            template = f'assets/items/bound-fossil-{i}.png'
            print(template)
            for amount in range(1, len(threshold) + 1):
                img_inv = f'assets/tests/fossils/inv-bound-{amount}.png'
                detected_inv = self.cv_detect_boilerplate(
                    template, threshold=threshold[amount],
                    lst=True, calc_mp=True,
                    img_path=img_inv)[0]
                filtered_inv = list()
                for pt in detected_inv:
                    filtered_inv.append((pt[0], pt[1], amount))
                print(amount, len(filtered_inv))
            print('\n')
