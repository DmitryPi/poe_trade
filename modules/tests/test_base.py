from unittest import TestCase

from ..base import Base


class TestBase(TestCase, Base):
    def setUp(self):
        Base.__init__(self)
