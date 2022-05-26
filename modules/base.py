import cv2
import configparser
import json
import re
import logging
import numpy as np
import random
import time
import pyautogui
import pydirectinput
import pygetwindow as gw
import pytesseract
import win32gui
import win32con

from datetime import datetime
from difflib import SequenceMatcher
from PIL import ImageGrab
from colorthief import ColorThief
from win10toast import ToastNotifier


class Base:
    def __init__(self):
        self.app_config_name = 'config.ini'
        self.app_config = self.setup_load_config()
        self.app_title = self.app_config['BASE']['app_title']
        self.char_name = self.app_config['BASE']['char_name']
        self.trade_league = self.app_config['BASE']['trade_league']
        self.autogui_delay = float(self.app_config['BASE']['autogui_delay'][1:-1])
        self.template_dir = 'templates/'
        self.trade_summary_path = 'temp/trade_summary.json'
        self.date_fmt = '%Y-%m-%d %H:%M:%S'
        self.main_loop_delay = 0.05
        pyautogui.PAUSE = self.autogui_delay

    def setup_load_config(self):
        config = configparser.ConfigParser()
        config.read(self.app_config_name)
        if not config.sections():
            config = self.build_config(config)
        return config

    def build_config(self, config):
        config['BASE'] = {
            'app_title': 'Path of Exile',
        }
        config['TRADER'] = {
            'trade_api_url': 'https://www.pathofexile.com/api/trade',
            'trade_api_pagin_step': 10,
            'trade_api_pagin_step_bulk': 20,
            'trade_league': 'Harvest',
            'trade_items_file': 'trade_items.json',
            'trade_single_tmplt': 'exchange_nobulk.json',
            'trade_bulk_tmplt': 'exchange_bulk.json',
            'trade_bulk_types': [
                'fragment',
                'oil',
                'incubator',
                'scarab',
                'resonator',
                'fossil',
                'vial',
                'essence',
                'card',
                'map',
                'shaped map'
                'elder map',
                'blighted map',
            ],
            'client_log_path': 'a:/games/Path of Exile/logs/Client.txt'
        }
        with open(self.app_config_name, 'w') as configfile:
            config.write(configfile)
        return config

    def load_json_file(self, filepath):
        try:
            with open(f'{filepath}', 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                return data
        except FileNotFoundError:
            print('- File not found:', filepath)

    def update_json_file(self, data, filepath):
        with open(f'{filepath}', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)

    def get_datetime_passed_seconds(self, time_stamp, time_now=None, reverse=False):
        time_now = time_now if time_now else datetime.now()
        time_now = datetime.strptime(str(time_now).split('.')[0], self.date_fmt)
        time_stamp = datetime.strptime(str(time_stamp).split('.')[0], self.date_fmt)
        if reverse:
            time_passed = time_stamp - time_now
        else:
            time_passed = time_now - time_stamp
        return int(time_passed.total_seconds())

    def check_no_window(self):
        if not gw.getActiveWindow():
            return True
        elif gw.getActiveWindow().title != self.app_title:
            return True
        return False

    def check_app_window(self):
        if gw.getActiveWindow():
            if gw.getActiveWindow().title == self.app_title:
                return True
        return False

    def check_string_similarity(self, a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def get_app_windows(self, window):
        hwnds = gw.getWindowsWithTitle(window)
        return hwnds

    def sort_app_windows(self, hwnds):
        ignore_windows = ['chrome', 'twitch', 'mozilla', 'opera']
        for hwnd in hwnds:
            hwnd_title = hwnd.title.lower()
            if not any(w in hwnd_title for w in ignore_windows):
                return hwnd

    def get_app_rect(self):
        loc = tuple()
        try:
            hwnds = self.get_app_windows(self.app_title)
            hwnd = self.sort_app_windows(hwnds)
            if hwnd:
                loc = (
                    hwnd.topleft[0],
                    hwnd.topleft[1],
                    hwnd.bottomright[0],
                    hwnd.bottomright[1])
        except Exception as e:
            self.log_error(e)
            self.show_toast(e)
        return loc

    def get_mouse_position(self, delayed=False):
        if delayed:
            for i in range(2):
                time.sleep(1)
        return pydirectinput.position()

    def set_app_focus(self, win32=False):
        if not gw.getActiveWindow():
            print('- Window not found:', gw.getActiveWindow())
            return False

        a, b, c, d = self.get_app_rect()
        m_x, m_y = self.get_mouse_position()

        # move mouse if out of screen
        if m_x < a or m_x > c or m_y < b or m_y > d:
            x_mp = round((a + c) / 2)
            y_mp = round((b + d) / 2)
            pydirectinput.moveTo(x_mp, y_mp + 150)

        if self.check_no_window():
            try:
                print('- Activating window')
                if win32:
                    hwnds = self.get_app_windows(self.app_title)
                    hwnd = self.sort_app_windows(hwnds)
                    hwnd.activate()
                else:
                    pydirectinput.click()
            except Exception as e:
                self.log_error(e)
                self.show_toast(e)

    def app_window_focus(self, sleep=1):
        if not self.get_app_windows(self.app_title):
            print(f'- Error! Window {self.app_title} not found.')
            return False
        if self.check_no_window():
            hwnd = win32gui.FindWindow(None, r'Path Of Exile')
            try:
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(sleep)
            except Exception as e:
                self.log_error(e)
                self.show_toast(e)
                self.focus_window_fallback(hwnd)
                time.sleep(sleep)

    def focus_window_fallback(self, hwnd):
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        except Exception as e:
            self.log_error(e)
            self.show_toast(e)

    def log_error(self, e):
        return logging.exception(str(e))

    def show_toast(self, msg, msg_type='ERROR', duration=4):
        toaster = ToastNotifier()
        toaster.show_toast(
            msg_type,
            str(msg),
            duration=duration,
            threaded=True
        )

    def mouse_move(self, x, y, delay=True):
        pyautogui.moveTo(x, y)
        if delay:
            time.sleep(0.05)

    def mouse_move_click(
            self, x=None, y=None,
            clicks=1, ctrl=False, delay=False, interval=0.03, btn='left'):
        if ctrl:
            pyautogui.keyDown("ctrl")
            if delay:
                pyautogui.moveTo(x, y)
                time.sleep(0.06)
                pyautogui.click(None, None, clicks=clicks, button=btn)
                pyautogui.keyUp("ctrl")
            else:
                pyautogui.click(x, y, clicks=clicks, interval=interval, button=btn)
                pyautogui.keyUp("ctrl")
        else:
            pyautogui.click(x, y, interval=interval, clicks=clicks, button=btn)

    def cv_process_template(self, tmplt):
        template = cv2.imread(tmplt, 0)
        w, h = template.shape[::-1]
        return (template, w, h)

    def cv_cvt_img_gray(self, img_path=None, dimensions=None):
        if not img_path:
            dimensions = dimensions if dimensions \
                else self.get_app_rect()
            printscreen = np.array(ImageGrab.grab(dimensions))
        else:
            printscreen = cv2.imread(img_path)
        printscreen_gray = cv2.cvtColor(
            printscreen,
            cv2.COLOR_BGR2GRAY
        )
        return (printscreen, printscreen_gray)

    def cv_match_template(
            self, img, tmplt,
            method=cv2.TM_CCOEFF_NORMED, threshold=0.65):
        res = cv2.matchTemplate(
            img,
            tmplt,
            method)
        loc = np.where(res >= threshold)
        return loc

    def cv_detect_boilerplate(
            self, tmplt,
            img_path=None, method=cv2.TM_CCOEFF_NORMED,
            threshold=0.65, lst=True, calc_mp=False,
            onlyone=False, abcd=False, dimensions=None, crop=[]):
        detected_objects = list() if lst else set()

        template, w, h = self.cv_process_template(tmplt)
        printscreen, printscreen_gray = self.cv_cvt_img_gray(
            img_path=img_path, dimensions=dimensions)
        dimensions = self.get_app_rect()

        if crop:
            printscreen = printscreen[crop[1]:crop[3], crop[0]:crop[2]]
            printscreen_gray = printscreen_gray[
                crop[1]:crop[3],
                crop[0]:crop[2]]
            # cv2.imshow("cropped", printscreen)
            # cv2.waitKey(0)
            # return None

        loc = self.cv_match_template(
            printscreen_gray,
            template,
            method=method,
            threshold=threshold
        )
        mask = np.zeros(printscreen.shape[:2], np.uint8)

        for pt in zip(*loc[::-1]):
            if mask[pt[1] + h // 2, pt[0] + w // 2] != 255:
                if calc_mp:
                    x_mp = int((pt[0] + pt[0] + w) / 2)
                    y_mp = int((pt[1] + pt[1] + h) / 2)
                    if isinstance(detected_objects, set):
                        detected_objects.add((x_mp, y_mp))
                    elif isinstance(detected_objects, list):
                        detected_objects.append((x_mp, y_mp))
                elif abcd:
                    a = pt[0] + dimensions[0]
                    b = pt[1] + dimensions[1]
                    c = a + w
                    d = b + h
                    if isinstance(detected_objects, set):
                        detected_objects.add((a, b, c, d))
                    elif isinstance(detected_objects, list):
                        detected_objects.append((a, b, c, d))
                else:
                    if isinstance(detected_objects, set):
                        detected_objects.add(pt)
                    elif isinstance(detected_objects, list):
                        detected_objects.append(pt)
            mask[pt[1]:pt[1] + h, pt[0]:pt[0] + w] = 255
            if onlyone and len(detected_objects) >= 1:
                break
        if crop:
            for i, pt in enumerate(detected_objects):
                detected_objects[i] = (pt[0] + crop[0], pt[1] + crop[1])
        return (detected_objects, w, h, printscreen_gray)

    def tesseract_img_to_text(self, img, psm=1):
        rep = {"(": "", ")": "", ".": "", ",": "", "@": "", "&": ""}
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        config = f"--psm {psm} -l eng"
        text = pytesseract.image_to_string(
            img,
            config=config)
        text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text).strip()
        return text


class OCRChecker(Base):
    def __init__(self):
        Base.__init__(self)
        self.crop = {
            "stash": [5, 85, 655, 810],
            "stash_top": [50, 0, 550, 130],
            "trade": [290, 140, 955, 815],
            "inventory": [1260, 575, 1915, 865],
            "party_box": [0, 160, 260, 500],
        }

    def check_fragment_tab(self, threshold=0.8, tab_open=False, scarab=True):
        template = 'assets/tabs/tab_fragment.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold, calc_mp=True, lst=True, crop=self.crop['stash'])[0]
        if detected_objects and tab_open:
            self.mouse_move_click(detected_objects[0][0], detected_objects[0][1], clicks=2, delay=True)
            if scarab:
                self.mouse_move_click(485, 150, delay=True)
        return True if detected_objects else False

    def check_fragment_tab_opened(self, threshold=0.75):
        template = 'assets/tabs/tab_fragment_scarab_item.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold, calc_mp=True, lst=True, crop=self.crop['stash'])[0]
        return True if detected_objects else False

    def check_fossil_tab(self, threshold=0.8, tab_open=True):
        template = 'assets/tabs/tab_fossil.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold, calc_mp=True, lst=True, crop=self.crop['stash'])[0]
        if detected_objects and tab_open:
            self.mouse_move_click(detected_objects[0][0], detected_objects[0][1], clicks=2, delay=True)
        return True if detected_objects else False

    def check_fossil_tab_opened(self, threshold=0.75):
        template = 'assets/tabs/tab_fossil_item.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold, calc_mp=True, lst=True, crop=self.crop['stash'])[0]
        return True if detected_objects else False

    def check_loading(self, threshold=0.8):
        template = 'assets/ui/loading.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold, crop=[555, 0, 1300, 110])[0]
        if not detected_objects:
            template = 'assets/ui/loading_1.png'
            detected_objects = self.cv_detect_boilerplate(
                template, threshold=threshold, crop=[1120, 840, 1590, 1080])[0]
        return True if detected_objects else False

    def check_hideout(self, threshold=0.5):
        template = 'assets/ui/ho.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold, crop=[640, 0, 1915, 285])[0]
        return True if detected_objects else False

    def check_empty_slot(self, stash=True, inventory=False, threshold=0.5):
        if inventory:
            crop = self.crop['inventory']
        elif stash:
            crop = self.crop['stash']
        else:
            crop = []

        template = 'assets/ui/inventory_cell.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold,
            calc_mp=True, crop=crop)[0]
        filtered_objects = list()
        for pt in detected_objects:
            filtered_objects.append(pt)
        return sorted(filtered_objects)

    def check_remove_alerts(self, threshold=0.77):
        template = 'assets/ui/btn_x.png'
        detected_objects, w, h = self.cv_detect_boilerplate(
            template, threshold=threshold, calc_mp=True)[:3]
        for pt in sorted(detected_objects):
            self.mouse_move_click(pt[0], pt[1], delay=True)

    def check_remove_surplus(self, max_amount, threshold=0.85):
        template = 'assets/items/c_chaos_10.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold,
            calc_mp=True, crop=self.crop['inventory'])[0]
        if len(detected_objects) >= max_amount:
            sorted_surplus = sorted(
                detected_objects,
                reverse=False,
                key=lambda x: x[0])[max_amount:]
            for pt in sorted_surplus:
                self.mouse_move_click(
                    pt[0], pt[1], clicks=2, ctrl=True)
            return True
        return False

    def check_remove_trails(self, threshold=0.89):
        """
        TODO: refactor into remove_surplus
        """
        for i in range(1, 10):
            template = f'assets/items/c_chaos_{i}_{i}.png'
            detected_objects = self.cv_detect_boilerplate(
                template, threshold=threshold,
                calc_mp=True, lst=True, crop=self.crop['inventory'])[0]
            for pt in sorted(detected_objects):
                self.mouse_move_click(
                    pt[0], pt[1], clicks=2, ctrl=True)

    def check_dump_items(self, threshold=0.6):
        items = [
            ('tab_dump', 'scarab-gilded-half'),
            ('tab_dump', 'scarab-polished-half'),
            ('tab_dump', 'scarab-rusted-half'),
            ('tab_dump', 'card_half'),
            ('tab_fossil', random.choice(
                ['shuddering-fossil-half', 'bound-fossil-half'])),
            ('tab_fossil', 'corroded-fossil'),
            ('tab_money', ''),
        ]
        dump_items = []
        for tab, item in items:
            tab_template = f'assets/ui/{tab}.png'
            item_template = f'assets/items/{item}.png'
            if tab == 'tab_money':
                tab_coords = self.cv_detect_boilerplate(
                    tab_template, threshold=threshold,
                    calc_mp=True, lst=True, crop=self.crop['stash'])[0]
                if not tab_coords:
                    break
                self.mouse_move_click(
                    tab_coords[0][0], tab_coords[0][1],
                    clicks=2, interval=0.15, delay=True)
            else:
                item_coords = self.cv_detect_boilerplate(
                    item_template, threshold=0.58,
                    calc_mp=True, crop=self.crop['inventory'])[0]
                print(f'- Found {item}: {len(item_coords)}')
                for i in item_coords:
                    dump_items.append(i)
        dump_items = sorted(list(dict.fromkeys(dump_items)))
        for pt in dump_items:
            self.mouse_move_click(
                pt[0], pt[1], clicks=2, delay=False, ctrl=True)

    def check_open_inventory(self, threshold=0.95):
        template = 'assets/ui/inventory.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold, crop=[1340, 0, 1800, 110])[0]
        if not detected_objects:
            print('- Opening inventory')
            pyautogui.press('i')
            time.sleep(0.3)
        return True if detected_objects else False

    def check_stash_opened(self, threshold=0.9):
        template = 'assets/ui/stash.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold, crop=self.crop['stash_top'])[0]
        return True if detected_objects else False

    def check_stash_currency(self, threshold=0.8):
        template = 'assets/items/stash_chaos_empty.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold, crop=self.crop['stash'])[0]
        return bool(detected_objects)

    def check_trade_opened(self, threshold=0.75, accept=False):
        template = 'assets/ui/trade.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold, crop=[460, 15, 800, 150])[0]
        if accept:
            if not self.check_trade_accepted() and detected_objects:
                self.mouse_move(370, 835)
                time.sleep(0.15)
                pyautogui.click(interval=0.1)
                print('- Trade accepted')
                self.mouse_move(1350, 500)
        return True if detected_objects else False

    def check_trade_accepted(self, threshold=0.7):
        template = 'assets/ui/btn_cancel_accept.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold, crop=[285, 790, 625, 865])[0]
        return True if detected_objects else False

    def check_chat_opened(self, threshold=0.8):
        template = f'assets/ui/chat_arrow.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold, crop=[35, 750, 820, 830])[0]
        return True if detected_objects else False

    def check_invite(self, check_type=False, threshold=0.55):
        template = f'assets/ui/trade_invite.png'
        detected_objects, w, h = self.cv_detect_boilerplate(
            template, threshold=threshold, lst=True, abcd=True)[:3]
        if check_type:
            if detected_objects:
                detected_objects = self.check_invite_type(
                    detected_objects)
        return sorted(detected_objects)

    def check_invite_account_name(self, coords):
        img_path = 'assets/tests/tesseract/current_account_name.png'
        printscreen, printscreen_gray = self.cv_cvt_img_gray()
        thresh = 120
        img_bw = cv2.threshold(printscreen_gray, thresh, 255, cv2.THRESH_BINARY)[1]
        crop_img = img_bw[
            coords[1]:coords[1] + 26,
            coords[0] + 34:coords[0] + 250]
        cv2.imwrite(img_path, crop_img)
        raw_text = self.tesseract_img_to_text(crop_img, psm=1)
        account_name = raw_text.lower().split(' ')[0]
        return account_name

    def check_invite_type(self, detected_objects):
        templates = [
            ('trade', 'assets/ui/trade_invite_sm_1.png'),
            ('party', 'assets/ui/party_invite_sm_1.png'),
            ('friend', 'assets/ui/friend_invite_sm.png'),
            ('challenge', 'assets/ui/challenge_invite_sm.png'),
        ]
        invite_type = None
        for i, pt in enumerate(detected_objects):
            for ii in range(len(templates)):
                invites = self.cv_detect_boilerplate(
                    templates[ii][1],
                    threshold=0.94,
                    dimensions=pt)[0]
                if invites:
                    invite_type = templates[ii][0]
                    break
            if not invite_type:
                invite_type = 'unknown'
            detected_objects[i] = (pt[0], pt[1], invite_type)
        return detected_objects

    def check_in_party(self, threshold=0.7):
        template = 'assets/ui/party_icon.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold, crop=self.crop['party_box'])[0]
        return detected_objects

    def check_not_in_party(self):
        img_path = 'assets/ui/current_party_icon.png'
        printscreen, printscreen_gray = self.cv_cvt_img_gray()
        crop = [0, 200, 95, 280]
        crop_img = cv2.cvtColor(printscreen[crop[1]:crop[3], crop[0]:crop[2]], cv2.COLOR_BGR2RGB)
        cv2.imwrite(img_path, crop_img)
        color_thief = ColorThief(img_path)
        palette = color_thief.get_palette(color_count=2, quality=5)
        for color in palette:
            if color[0] < 165:
                continue
            if color[1] < 50 and color[2] < 50:
                print('- Not in party')
                return True

    def check_open_stash(self, threshold=0.80):
        template = 'assets/ui/ho_stash.png'
        detected_objects = self.cv_detect_boilerplate(
            template, threshold=threshold, calc_mp=True, lst=True)[0]
        if detected_objects:
            print('- Stash found')
            pt_0 = detected_objects[0][0]
            pt_1 = detected_objects[0][1]
            self.mouse_move(pt_0, pt_1)
            time.sleep(0.2)
            pyautogui.click()
