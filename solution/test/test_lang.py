from __future__ import print_function
import unittest

from ..lang import e, Int64


class FoldTestCase(unittest.TestCase):

    def test_zero(self):
        self.assertEquals(e.fold(
            Int64(0), Int64(0),
            lambda x, y: x | y
        ), 0)

    def test_common_case(self):
        self.assertEquals(e.fold(
            Int64(2), Int64(1),
            lambda x, y: x | y
        ), 3)

    def test_overflow(self):
        self.assertEquals(e.fold(
            Int64(2 ** 64), Int64(1),
            lambda x, y: x | y
        ), 1)

    def test_almost_overflow(self):
        self.assertEquals(e.fold(
            Int64(2 ** 63), Int64(1),
            lambda x, y: x | y
        ), 129)


class OpTestCase(unittest.TestCase):

    def test_shl1(self):
        self.assertEquals(Int64(1) << Int64(1), 2)
        self.assertEquals((Int64(1) << Int64(1)) << Int64(2), 8)
