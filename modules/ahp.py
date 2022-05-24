import pyautogui
import pytesseract
import time

from PIL import Image

from modules.base import Base


class AutoFlask(Base):
    def __init__(self):
        Base.__init__(self)
        self.hp = 50
        self.app_title = 'Path of Exile'
        self.flask_binds = ['num4', 'num5', 'num6', 'num7', 'num8', 't']
        self.flask_used = False
        self.flask_use_delay = 3.6
        self.ahp_switch = False
        self.ahp_switch_timer = 0

    def action_flask_macro(self, flask_binds=[], flask_delay=0):
        flask_delay = 0.04 if not flask_delay else flask_delay
        if not flask_binds:
            print('- Specify flask binds')
            return False
        for flask_bind in flask_binds:
            pyautogui.press(str(flask_bind), interval=flask_delay)
        print('- AutoFlask Triggered')

    def ahp(self):
        """
        PIL screenshot
        crop hp values
        calculate current percentage
        """
        img = Image.open('assets/icons/hpbardiglow.png')
        print(pytesseract.image_to_string(img))

    def run_autoflask(self):
        print('- AutoFlask is Running')
        elapsed = 0
        while True:
            if self.check_no_window():
                self.ahp_switch = False
                self.ahp_switch_timer = 0
                elapsed = 0
                self.flask_used = False
            elif self.ahp_switch:  # if app_window and ahp_switch
                if not self.flask_used:
                    self.action_flask_macro(flask_binds=self.flask_binds)
                    self.flask_used = True
                if elapsed >= self.flask_use_delay:
                    self.ahp_switch = False
                    self.ahp_switch_timer = 0
                    self.flask_used = False
                    elapsed = 0
                else:
                    elapsed = time.time() - self.ahp_switch_timer
            time.sleep(self.main_loop_delay)
