import pyautogui
import pytest

from unittest import TestCase

from ..mouse import wind_mouse


class TestMouse(TestCase):
    def setUp(self):
        pass

    @pytest.mark.slow
    def test_wind_mouse(self):
        pos_x, pos_y = pyautogui.position()
        wind_mouse(pos_x, pos_y, 1000, 500, move_mouse=pyautogui.moveTo)
