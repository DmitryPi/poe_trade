from unittest import TestCase

from modules.keys import KeyActions


class TestKeyActions(TestCase, KeyActions):
    def setUp(self):
        KeyActions.__init__(self)

    def test_action_commands(self):
        assert '/hideout' == self.cmd_hideout
        assert f'/kick {self.char_name}' == self.cmd_kick
        assert '/exit' == self.cmd_logout
        assert '/invite ' == self.cmd_invite
        assert '/trade' == self.cmd_trade
        assert '/tradewith' == self.cmd_tradewith

    def test_action_flask_macro(self):
        if self.check_no_window():
            assert self.check_no_window()
            assert not self.action_flask_macro(flask_binds=[])
