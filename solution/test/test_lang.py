from __future__ import print_function
import unittest
from nose.plugins.attrib import attr
from ..lang import e, Int64, op


class FoldTestCase(unittest.TestCase):

    @attr('fast')
    def test_zero(self):
        self.assertEquals(e.fold(
            Int64(0), Int64(0),
            lambda x, y: x | y
        ), 0)

    @attr('fast')
    def test_common_case(self):
        self.assertEquals(e.fold(
            Int64(2), Int64(1),
            lambda x, y: x | y
        ), 3)

    def test_common_case2(self):
        self.assertEquals(e.fold(
            Int64(0xFFCD00F123), Int64(1),
            lambda x, y: x | y
        ), 255)


    @attr('fast')
    def test_almost_overflow(self):
        self.assertEquals(e.fold(
            Int64(2 ** 63), Int64(1),
            lambda x, y: x | y
        ), 129)

    @attr('fast')
    def test_hexadecimal_input(self):
        self.assertEquals(e.fold(
            Int64(0xFFFFFFFFFFFFFFFF), Int64(0),
            lambda x, y: x | y
        ), 0x00000000000000FF)

    @attr('fast')
    def test_hexadecimal_and_xor(self):
        self.assertEquals(e.fold(
            Int64(0xABCDEF0123456789), Int64(1),
            lambda x, y: x ^ y
        ), 1)

    @attr('fast')
    def test_fold(self):
        self.assertEquals(e.fold(
            Int64(2), Int64(1),
            lambda x, y: y
        ), 1)

    @attr('fast')
    def test_fold_func_application(self):
        def lll(x, y):
            return Int64(y)
        self.assertEquals(e.fold(Int64(1), Int64(1), lll), 1)

class Int64TestCase(unittest.TestCase):
    @attr('fast')
    def test_overflow(self):
        with self.assertRaises(Exception):
            Int64(2 ** 64)

    @attr('fast')
    def test_itter(self):
        expected = [128, 128, 0, 0, 0, 0, 0, 0]
        for i, a in enumerate(Int64(0b1000000010000000)):
            self.assertEquals(a, expected[i])

class OpTestCase(unittest.TestCase):

    @attr('fast')
    def test_shl1(self):
        self.assertEquals(Int64(1) << Int64(1), 2)
        self.assertEquals((Int64(1) << Int64(1)) << Int64(2), 8)

    @attr('fast')
    def test_not_(self):
        self.assertEquals(op.not_(Int64(0)), 0xFFFFFFFFFFFFFFFF)
        self.assertEquals(op.not_(Int64(1)), 0xFFFFFFFFFFFFFFFE)
        self.assertEquals(op.not_(Int64(0xFFFFFFFFFFFFFFFF)), 0)
        self.assertEquals(op.not_(Int64(0xABCDE)), 0xFFFFFFFFFFF54321)

    @attr('fast')
    def test_and_(self):
        self.assertEquals(op.and_(Int64(0), Int64(1)), 0)
        self.assertEquals(op.and_(Int64(1), Int64(1)), 1)
        self.assertEquals(op.and_(Int64(0xFFFFFFFFFFFFFFFF), Int64(1)), 1)
        self.assertEquals(op.and_(Int64(0xFFFFFFFFF), op.shl1(op.not_(Int64(0)))), 0x0000000FFFFFFFFE)

    @attr('fast')
    def test_or_(self):
        self.assertEquals(op.or_(Int64(0), Int64(0)), 0)
        self.assertEquals(op.or_(Int64(1), Int64(0)), 1)
        self.assertEquals(op.or_(Int64(1), Int64(1)), 1)
        self.assertEquals(op.or_(Int64(0xFFFFFFFFFFFFFFFF), Int64(1)), 0xFFFFFFFFFFFFFFFF)
        self.assertEquals(op.or_(Int64(0xFFFFFFFFFFFFFFFE), Int64(0)), 0xFFFFFFFFFFFFFFFE)

    @attr('fast')
    def test_xor(self):
        self.assertEquals(op.xor(Int64(0xFFFF23ABCE234), Int64(1)), 0x000FFFF23ABCE235)
        self.assertEquals(op.xor(Int64(0xFFFF23), Int64(1)), 0x0000000000FFFF22)
        self.assertEquals(op.xor(Int64(0), Int64(1)), 1)

    @attr('fast')
    def test_plus(self):
        self.assertEquals(op.plus(Int64(0xFFFF23ABCE234), Int64(1)), 0x000FFFF23ABCE235)
        self.assertEquals(op.plus(Int64(0xFFFFFFFFFFFFFFFF), Int64(1)), 0)
        self.assertEquals(op.plus(Int64(0xFFFFFFFFFFFFFFFE), Int64(1)), 0xFFFFFFFFFFFFFFFF)
        self.assertEquals(op.plus(Int64(0), Int64(0)), 0)

    @attr('fast')
    def test_shl1(self):
        self.assertEquals(op.shl1(Int64(0)), 0)
        self.assertEquals(op.shl1(Int64(0xFFFFFFFFFFFFFFFF)), 0xFFFFFFFFFFFFFFFE)
        self.assertEquals(op.shl1(Int64(1)), 2)

    @attr('fast')
    def test_shlr1(self):
        self.assertEquals(op.shr1(Int64(0)), 0)
        self.assertEquals(op.shr1(Int64(0xFFFFFFFFFFFFFFFF)), 0x7FFFFFFFFFFFFFFF)
        self.assertEquals(op.shr1(Int64(1)), 0)

    @attr('fast')
    def test_shlr4(self):
        self.assertEquals(op.shr4(Int64(0)), 0)
        self.assertEquals(op.shr4(Int64(0xFFFFFFFFFFFFFFFF)), 0x0FFFFFFFFFFFFFFF)

    @attr('fast')
    def test_shlr16(self):
        self.assertEquals(op.shr16(Int64(0)), 0)
        self.assertEquals(op.shr16(Int64(5)), 0)
        self.assertEquals(op.shr16(Int64(0xFFFFFFFFFFFFFFFF)), 0x0000FFFFFFFFFFFF)

class ETestCase(unittest.TestCase):

    @attr('fast')
    def test_if0(self):
        self.assertEquals(e.if0(Int64(1), Int64(1), Int64(1)), 1)
        self.assertEquals(e.if0(Int64(1), Int64(0), Int64(1)), 1)
        self.assertEquals(e.if0(Int64(0), Int64(1), Int64(1)), 1)
        self.assertEquals(e.if0(Int64(1), Int64(1), Int64(0)), 0)
        self.assertEquals(e.if0(Int64(0xFFFFFFFFFFFFFFFF), Int64(0), Int64(0xFFFFFFFFFFFFFFFF)), 0xFFFFFFFFFFFFFFFF)
        self.assertEquals(e.if0(Int64(0), Int64(0xFFFFFFFFFFFFFFFF), Int64(0xFFFFF)), 0xFFFFFFFFFFFFFFFF)
        self.assertEquals(e.if0(Int64(0), op.shr4(Int64(0xFFFFFFFFFFFFFFFF)), Int64(0xFFFFF)), 0x0FFFFFFFFFFFFFFF)
