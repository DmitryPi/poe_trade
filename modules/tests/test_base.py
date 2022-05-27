import pytest

from unittest import TestCase

from ..base import Base


class TestBase(TestCase, Base):
    def setUp(self):
        Base.__init__(self)

    @pytest.mark.slow
    def test_mouse_move(self):
        self.mouse_move(1000, 500)
        self.mouse_move(1500, 500, delay=True)
        self.mouse_move(1000, 500, humanlike=False)
