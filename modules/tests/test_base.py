from unittest import TestCase

from ..base import Base


class TestBase(TestCase, Base):
    def setUp(self):
        Base.__init__(self)

    def test_mouse_move(self):
        self.mouse_move(1000, 500)
