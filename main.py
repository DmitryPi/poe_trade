import logging
import pygetwindow as gw
import sys
import time

from datetime import datetime
from threading import Thread
from pynput import keyboard, mouse

from modules.ahp import AutoFlask
from modules.base import Base
from modules.keys import KeyActions
from modules.trade import Prices, ClientLog, TradeBot


class KeyPresser(AutoFlask, TradeBot):
    def __init__(self):
        AutoFlask.__init__(self)
        KeyActions.__init__(self)
        TradeBot.__init__(self)
        self.current_keypress = []

    def on_press(self, key):
        if key not in self.current_keypress:
            self.current_keypress.append(key)
        if keyboard.Key.ctrl_l in self.current_keypress:
            key = str(key)
            if key == '<49>':  # code for [ctrl + 1]
                if gw.getActiveWindow().title != self.app_title:
                    return None
                clicker_thread = Thread(target=self.action_autoclick_onspot, daemon=True)
                clicker_thread.start()
            elif key == '<50>':  # code for [ctrl + 2]
                pass
            elif key == '<51>':  # code for [ctrl + 3]
                self.trader_switch = 0 if self.trader_switch else 1
                msg = 'Activated' if self.trader_switch else 'Stopped'
                print(f'- Trader {msg}')

    def on_release(self, key):
        if key:
            try:
                self.current_keypress.remove(key)
            except (KeyError, ValueError):
                self.current_keypress = []

        if key == keyboard.Key.end:
            return False
        elif key == keyboard.Key.f1:
            self.action_ingame_paste()
        elif key == keyboard.Key.f2:
            self.action_party_invite()
        elif key == keyboard.Key.f3:
            self.action_send_ty()
        elif key == keyboard.Key.f4:
            self.action_command_chat(self.cmd_kick)
        elif key == keyboard.Key.f5:
            self.action_command_chat(self.cmd_hideout)
        elif key == keyboard.Key.f6:
            self.action_paste_inventory_currency()
        elif key == keyboard.Key.f7:
            self.action_paste_inventory_all()
        elif key == keyboard.Key.f8:
            self.action_confirm_items()
        elif key == keyboard.Key.shift_r:
            self.action_command_chat(self.cmd_logout)
        elif key == keyboard.KeyCode(char='`') and 'ahp' in sys.argv:
            self.action_flask_macro(flask_binds=['num4', 'num5', 'num6', 'num7', 'num8'])

    def on_move(self, x, y):
        # print('Pointer moved to {0}'.format((x, y)))
        pass

    def on_click(self, x, y, button, pressed):
        if pressed and button == mouse.Button.right:
            if not self.ahp_switch_timer:
                self.ahp_switch = True
                self.ahp_switch_timer = time.time()

    def on_scroll(self, x, y, dx, dy):
        # print('Scrolled {0}'.format((x, y)))
        pass

    def run(self):
        """
            Start independent Mouse/Keyboard listener
            Keyboard level is higher - will stop all nested chain
        """
        print('- KeyPresser is Running')

        with mouse.Listener(
                on_move=self.on_move,
                on_click=self.on_click,
                on_scroll=self.on_scroll) as listener:
            with keyboard.Listener(
                    on_press=self.on_press,
                    on_release=self.on_release) as listener:
                listener.join()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(name)-24s: %(levelname)-8s %(message)s')
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)
    start = datetime.now()

    trade_item_files = [
        'trade_items_1.json',
        'trade_items_2.json',
    ]
    key_presser = KeyPresser()

    if 'config' in sys.argv:
        base = Base()
        base.setup_load_config()
    elif 'prices' in sys.argv:
        prices = Prices()
        prices.run()
    elif 'log' in sys.argv:
        client_log = ClientLog()
        client_log.run()
    elif 'afk' in sys.argv:
        afk_thread = Thread(target=key_presser.run_afk)
        afk_thread.daemon = True
        afk_thread.start()
        key_presser.run()
    elif 'trader' in sys.argv:
        for trade_file in trade_item_files:
            print(f'- Trader thread starting : {trade_file}')
            trader_thread = Thread(
                target=key_presser.run_trader, args=(trade_file,))
            trader_thread.daemon = True
            trader_thread.start()
        whisper_queue_thread = Thread(target=key_presser.manage_trade_whisper_queue, daemon=True).start()
        key_presser.run()
    elif 'bot' in sys.argv:
        for trade_file in trade_item_files:
            print(f'- Trader thread starting : {trade_file}')
            trader_thread = Thread(
                target=key_presser.run_trader, args=(trade_file,))
            trader_thread.daemon = True
            trader_thread.start()
        trade_buyer_thread = Thread(target=key_presser.run_buyer, daemon=True).start()
        whisper_queue_thread = Thread(target=key_presser.manage_trade_whisper_queue, daemon=True).start()
        key_presser.run()
    elif 'seller' in sys.argv:
        trade_seller_thread = Thread(target=key_presser.run_seller)
        trade_seller_thread.daemon = True
        trade_seller_thread.start()
        key_presser.run()
    elif 'ahp' in sys.argv:
        auto_flask = AutoFlask()
        auto_flask = Thread(target=key_presser.run_autoflask)
        auto_flask.daemon = True
        auto_flask.start()
        key_presser.run()

    finish = datetime.now() - start
    logging.info(f'Done in: {finish}')
