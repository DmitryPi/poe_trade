import pyautogui
import pygetwindow as gw
import pyperclip
import random
import json
import time

from pynput import keyboard, mouse
from pynput.keyboard import Key

from modules.base import Base

inventory_cells = [(1271, 588), (1271, 640), (1271, 692), (1271, 745), (1271, 798), (1324, 586), (1324, 640), (1324, 692), (1324, 745), (1324, 798), (1377, 586), (1377, 640), (1377, 692), (1377, 745), (1377, 798), (1429, 586), (1429, 640), (1429, 692), (1429, 745), (1429, 798), (1482, 586), (1482, 640), (1482, 692), (1482, 745), (1482, 798), (1535, 586), (1535, 640), (1535, 692), (1535, 745), (1535, 798), (1587, 586), (1587, 640), (1587, 692), (1587, 745), (1587, 798), (1640, 586), (1640, 640), (1640, 692), (1640, 745), (1640, 798), (1693, 586), (1693, 640), (1693, 692), (1693, 745), (1693, 798), (1745, 586), (1745, 640), (1745, 692), (1745, 745), (1745, 798), (1798, 586), (1798, 640), (1798, 692), (1798, 745), (1798, 798), (1851, 586), (1851, 640), (1851, 692), (1851, 745), (1851, 798)]
# inventory_cells = [(1272, 588), (1325, 588), (1378, 588), (1430, 588), (1483, 588), (1536, 588), (1588, 588), (1641, 588), (1694, 588), (1746, 588), (1799, 588), (1852, 588), (1272, 640), (1325, 640), (1378, 640), (1430, 640), (1483, 640), (1536, 640), (1588, 640), (1641, 640), (1694, 640), (1746, 640), (1799, 640), (1852, 640), (1272, 693), (1325, 693), (1378, 693), (1430, 693), (1483, 693), (1536, 693), (1588, 693), (1641, 693), (1694, 693), (1746, 693), (1799, 693), (1852, 693), (1272, 746), (1325, 746), (1378, 746), (1430, 746), (1483, 746), (1536, 746), (1588, 746), (1641, 746), (1694, 746), (1746, 746), (1799, 746), (1272, 798), (1325, 798), (1378, 798), (1430, 798), (1483, 798), (1536, 798), (1588, 798), (1641, 798), (1694, 798), (1746, 798), (1799, 798)]


class KeyActions(Base):
    def __init__(self):
        Base.__init__(self)
        self.keyboard = keyboard.Controller()
        self.mouse = mouse.Controller()
        self.keyactions_config = self.app_config['KEYACTIONS']
        self.cmd_hideout = '/hideout'
        self.cmd_kick = f'/kick {self.char_name}'
        self.cmd_logout = '/exit'
        self.cmd_invite = '/invite '
        self.cmd_trade = '/trade'
        self.cmd_tradewith = '/tradewith'
        self.ty_msgs = json.loads(self.keyactions_config['ty_msgs'])
        self.trade_msg = self.keyactions_config['trade_msg']

    def check_inventory(self, threshold=0.95):
        """
        TODO: remove this func (duplicate)
        """
        template = 'assets/ui/inventory.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold)[0]
        return True if detected_objects else False

    def action_autoclick_onspot(self):
        if self.check_no_window():
            return False

        print('- Clicker Activated')
        while True:
            if not self.current_keypress:
                print('- Clicker Stopped')
                break
            pyautogui.click(None, None, clicks=5, interval=0.03)

    def action_flask_macro(self, flask_binds=[], flask_delay=0):
        if self.check_no_window():
            return False

        flask_delay = 0.04 if not flask_delay else flask_delay
        if not flask_binds:
            print('- Specify flask binds')
            return True
        for flask_bind in flask_binds:
            pyautogui.press(str(flask_bind), interval=flask_delay)

    def action_inventory_move_click(self, coords, calc_mp=False):
        pyautogui.PAUSE = 0
        pyautogui.moveTo(1350, 500)
        for coord in sorted(coords):
            pyautogui.keyDown('ctrl')
            if calc_mp:
                pyautogui.click(
                    coord[0] + 15, coord[1] + 15, clicks=2, interval=0.015)
            else:
                pyautogui.click(coord[0], coord[1], clicks=2, interval=0.015)
        pyautogui.keyUp('ctrl')

    def action_paste_inventory_all(self, threshold=0.68):
        if self.check_no_window():
            return False
        template = 'assets/ui/inventory_cell.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold)[0]
        detected_objects = sorted(set(inventory_cells) - set(detected_objects))
        self.action_inventory_move_click(detected_objects, calc_mp=True)

    def action_paste_inventory_currency(self, threshold=0.9):
        if self.check_no_window():
            return False
        template = 'assets/items/c_chaos_cut.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold, calc_mp=True)[0]
        self.action_inventory_move_click(detected_objects)

    def action_confirm_items(self, threshold=0.7, delay=0.01):
        items = [
            'c_chaos_cut', 'scarab-polished-half-top',
            'card_half', 'bound-fossil-half', 'exalt-half', 'corroded-fossil', 'perfect-fossil'
        ]
        pyautogui.PAUSE = delay
        crop = [290, 140, 955, 480]
        detected_objects = []
        for item in items:
            item_template = f'assets/items/{item}.png'
            item_coords = self.cv_detect_boilerplate(
                item_template, threshold=threshold,
                calc_mp=True, crop=crop)[0]
            for i in item_coords:
                detected_objects.append(i)
        detected_objects = sorted(list(dict.fromkeys(detected_objects)))
        for pt in detected_objects:
            self.mouse_move(pt[0], pt[1], humanlike=True)
            time.sleep(delay)

    def action_trade(self):
        """
        TODO:
            /tradewith <character>
            save previous copy and change after command ended
        """
        pass

    def action_hideout_tp(self):
        self.app_window_focus()
        print('- Hideout Teleport')
        self.action_command_chat(self.cmd_hideout)

    def action_hideout_join(self, user_name):
        self.app_window_focus()
        print('- Hideout Teleport to %s' % user_name)
        self.pyperclip_copy(f'/hideout {user_name}')
        self.keyboard_enter()
        self.keyboard_paste()
        self.keyboard_enter()

    def action_command_chat(self, cmd):
        if self.check_no_window():
            return False
        self.pyperclip_copy(str(cmd))
        self.keyboard_enter()
        self.keyboard_paste()
        self.keyboard_enter()

    def action_ingame_paste(self):
        if self.check_no_window():
            return False
        if self.cmd_logout in pyperclip.paste():
            return False
        self.keyboard_enter()
        self.keyboard_select_text()
        self.keyboard_paste()
        self.keyboard_enter()

    def action_party_invite(self):
        if self.check_no_window():
            return False
        self.pyperclip_copy(self.cmd_invite)
        self.keyboard_ctrl_enter()
        with self.keyboard.pressed(Key.ctrl_l):
            self.keyboard.press(Key.left)
            self.keyboard.release(Key.left)
        self.keyboard.press(Key.right)
        self.keyboard.release(Key.right)
        self.keyboard.press(Key.backspace)
        self.keyboard.release(Key.backspace)
        self.keyboard_paste()
        self.keyboard_select_text()
        self.keyboard_copy()
        self.keyboard_paste()
        self.keyboard_enter()

    def action_send_ty(self, char_name=''):
        if self.check_no_window():
            return False
        ty_msg = random.choice(self.ty_msgs)
        if char_name:
            self.pyperclip_copy(f'@{char_name} ' + ty_msg)
            self.keyboard_enter()
        else:
            self.pyperclip_copy(ty_msg)
            self.keyboard_ctrl_enter()
        self.keyboard_paste()
        self.keyboard_enter()

    def action_msg_spam(self, cmd):
        app_window = gw.getWindowsWithTitle(self.app_title)
        prev_window = gw.getActiveWindow()
        if not gw.getActiveWindow() or gw.getActiveWindow().title != app_window:
            return False
        app_window[0].activate()
        time.sleep(1)
        if gw.getActiveWindow().title == self.app_title:
            for i in range(1, 5):
                self.keyboard_enter()
                self.keyboard_select_text()
                self.pyperclip_copy(f'{cmd} {i}')
                self.keyboard_paste()
                self.keyboard_enter()
                time.sleep(.500)
                self.keyboard_enter()
                self.pyperclip_copy(self.trade_msg)
                self.keyboard_paste()
                self.keyboard_enter()
                time.sleep(random.randint(1, 2))
            self.keyboard_enter()
            self.pyperclip_copy(f'{cmd} 1')
            self.keyboard_paste()
            self.keyboard_enter()
            time.sleep(.500)
            prev_window.activate()

    def keyboard_enter(self):
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

    def keyboard_ctrl_enter(self):
        with self.keyboard.pressed(Key.ctrl_l):
            self.keyboard.press(Key.enter)
            self.keyboard.release(Key.enter)

    def keyboard_select_text(self):
        with self.keyboard.pressed(Key.ctrl_l):
            self.keyboard.press('a')
            self.keyboard.release('a')

    def pyperclip_copy(self, text):
        pyperclip.copy(text)

    def keyboard_copy(self):
        with self.keyboard.pressed(Key.ctrl_l):
            self.keyboard.press('c')
            self.keyboard.release('c')

    def keyboard_paste(self):
        with self.keyboard.pressed(Key.ctrl_l):
            self.keyboard.press('v')
            self.keyboard.release('v')
