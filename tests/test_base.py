import pytest
import mouse
import time

from unittest import TestCase

from modules.base import Base


class TestBase(TestCase, Base):
    def setUp(self):
        Base.__init__(self)
        self.app_hwnds = self.get_app_windows(self.app_title)
        self.app_hwnd = self.sort_app_windows(self.app_hwnds)
        self.dimensions = self.get_app_rect()

    def test_config(self):
        config = self.setup_load_config()
        assert config.sections()
        config = self.build_config(config)
        assert config.sections()
        assert config['BASE']['app_title'] == 'Path of Exile'

    def test_action_commands(self):
        assert 'Path of Exile' == self.app_title

    def test_get_app_windows(self):
        if self.app_hwnd:
            assert len(self.app_hwnds) >= 1

    def test_sort_app_windows(self):
        if self.app_hwnd:
            assert self.app_hwnd
            assert self.app_hwnd.title.lower() == self.app_title.lower()
        else:
            assert not self.app_hwnd

    def test_get_app_rect(self):
        if self.app_hwnd:
            assert self.dimensions
            assert len(self.dimensions) == 4
        else:
            assert not self.dimensions

    def test_get_mouse_position(self):
        assert len(self.get_mouse_position()) == 2

    @pytest.mark.skip()
    def test_set_app_focus(self):
        assert not self.check_app_window()
        a, b, c, d = self.dimensions
        m_x, m_y = self.get_mouse_position()
        if m_x < a or m_x > c or m_y < b or m_y > d:
            x_mp = round((a + c) / 2)
            y_mp = round((b + d) / 2)
            mouse.move(x_mp, y_mp + 150)
            self.app_hwnd.activate()
            time.sleep(0.5)
            assert self.check_app_window()
