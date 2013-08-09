from __future__ import print_function
import unittest

from ..lang import e, Int64, op


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
        with self.assertRaises(Exception):
            e.fold(Int64(2 ** 64))

    def test_almost_overflow(self):
        self.assertEquals(e.fold(
            Int64(2 ** 63), Int64(1),
            lambda x, y: x | y
        ), 129)

    def test_hexadecimal_input(self):
        self.assertEquals(e.fold(
            Int64(0xFFFFFFFFFFFFFFFF), Int64(0),
            lambda x, y: x | y
        ), 0x00000000000000FF)

    def test_hexadecimal_and_xor(self):
        self.assertEquals(e.fold(
            Int64(0xABCDEF0123456789), Int64(1),
            lambda x, y: x ^ y
        ), 1)


class OpTestCase(unittest.TestCase):

    def test_shl1(self):
        self.assertEquals(Int64(1) << Int64(1), 2)
        self.assertEquals((Int64(1) << Int64(1)) << Int64(2), 8)

    def test_not_(self):
        self.assertEquals(op.not_(Int64(0)), 0xFFFFFFFFFFFFFFFF)
        self.assertEquals(op.not_(Int64(1)), 0xFFFFFFFFFFFFFFFE)
        self.assertEquals(op.not_(Int64(0xFFFFFFFFFFFFFFFF)), 0)
        self.assertEquals(op.not_(Int64(0xABCDE)), 0xFFFFFFFFFFF54321)

    def test_and_(self):
        self.assertEquals(op.and_(Int64(0), Int64(1)), 0)
        self.assertEquals(op.and_(Int64(1), Int64(1)), 1)
        self.assertEquals(op.and_(Int64(0xFFFFFFFFFFFFFFFF), Int64(1)), 1)
        self.assertEquals(op.and_(Int64(0xFFFFFFFFF), op.shl1(op.not_(Int64(0)))), 0x0000000FFFFFFFFE)

    def test_or_(self):
        self.assertEquals(op.or_(Int64(0), Int64(0)), 0)
        self.assertEquals(op.or_(Int64(1), Int64(0)), 1)
        self.assertEquals(op.or_(Int64(1), Int64(1)), 1)
        self.assertEquals(op.or_(Int64(0xFFFFFFFFFFFFFFFF), Int64(1)), 0xFFFFFFFFFFFFFFFF)
        self.assertEquals(op.or_(Int64(0xFFFFFFFFFFFFFFFE), Int64(0)), 0xFFFFFFFFFFFFFFFE)

    def test_xor(self):
        self.assertEquals(op.xor(Int64(0xFFFF23ABCE234), Int64(1)), 0x000FFFF23ABCE235)
        self.assertEquals(op.xor(Int64(0xFFFF23), Int64(1)), 0x0000000000FFFF22)
        self.assertEquals(op.xor(Int64(0), Int64(1)), 1)

    def test_plus(self):
        self.assertEquals(op.plus(Int64(0xFFFF23ABCE234), Int64(1)), 0x000FFFF23ABCE235)
        self.assertEquals(op.plus(Int64(0xFFFFFFFFFFFFFFFF), Int64(1)), 0)
        self.assertEquals(op.plus(Int64(0xFFFFFFFFFFFFFFFE), Int64(1)), 0xFFFFFFFFFFFFFFFF)
        self.assertEquals(op.plus(Int64(0), Int64(0)), 0)

    def test_shl1(self):
        self.assertEquals(op.shl1(Int64(0)), 0)
        self.assertEquals(op.shl1(Int64(0xFFFFFFFFFFFFFFFF)), 0xFFFFFFFFFFFFFFFE)
        self.assertEquals(op.shl1(Int64(1)), 2)

    def test_shlr1(self):
        self.assertEquals(op.shr1(Int64(0)), 0)
        self.assertEquals(op.shr1(Int64(0xFFFFFFFFFFFFFFFF)), 0x7FFFFFFFFFFFFFFF)
        self.assertEquals(op.shr1(Int64(1)), 0)

    def test_shlr4(self):
        self.assertEquals(op.shr4(Int64(0)), 0)
        self.assertEquals(op.shr4(Int64(0xFFFFFFFFFFFFFFFF)), 0x0FFFFFFFFFFFFFFF)

    def test_shlr16(self):
        self.assertEquals(op.shr16(Int64(0)), 0)
        self.assertEquals(op.shr16(Int64(5)), 0)
        self.assertEquals(op.shr16(Int64(0xFFFFFFFFFFFFFFFF)), 0x0000FFFFFFFFFFFF)


        self.assertEquals(op.shr1(Int64(1)), 0)
