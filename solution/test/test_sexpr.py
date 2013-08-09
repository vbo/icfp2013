import unittest
from nose.exc import SkipTest

from .. import sexpr
from ..lang import Int64, op


class SexprTestCase(unittest.TestCase):

    def test_top_level_const(self):
        raise SkipTest()
        self.assertEquals(sexpr.solve("(lambda (t) 0)", 0), 0)
        self.assertEquals(sexpr.solve("(lambda (t) 1)", 0), 1)

    def test_top_level_arg(self):
        raise SkipTest()
        self.assertEquals(sexpr.solve("(lambda (t) t)", 31337), 31337)

    def test_top_level_op1(self):
        raise SkipTest()
        self.assertEquals(sexpr.solve("(lambda (t) (not 0))", 0), op.not_(0))
        self.assertEquals(sexpr.solve("(lambda (t) (not t))", 8), op.not_(8))
        self.assertEquals(sexpr.solve("(lambda (t) (shl1 t))", 8), op.shl1(8))

    def test_top_level_fold(self):
        self.assertEquals(sexpr.solve("(lambda (x) (fold x 1 (lambda (y z) z)))", 1), 1)
