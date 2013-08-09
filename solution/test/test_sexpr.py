import unittest
from nose.exc import SkipTest

from .. import sexpr
from ..lang import Int64, op


class SexprTestCase(unittest.TestCase):

    def test_top_level_const(self):
        self.assertEquals(sexpr.solve("(lambda (t) 0)", 0), 0)
        self.assertEquals(sexpr.solve("(lambda (t) 1)", 0), 1)

    def test_top_level_arg(self):
        self.assertEquals(sexpr.solve("(lambda (t) t)", 31337), 31337)

    def test_top_level_op1(self):
        self.assertEquals(sexpr.solve("(lambda (t) (not 0))", 0), op.not_(0))
        self.assertEquals(sexpr.solve("(lambda (t) (not t))", 8), op.not_(8))
        self.assertEquals(sexpr.solve("(lambda (t) (shl1 t))", 8), op.shl1(8))

    def test_top_level_fold(self):
        self.assertEquals(sexpr.solve("(lambda (x) (fold x 1 (lambda (y z) z)))", 1), 1)
        self.assertEquals(sexpr.solve("(lambda (x_19527) (fold x_19527 0 (lambda (x_19527 x_19528) "
                                      "(shr1 (if0 (and (shr4 x_19528) (and x_19527 x_19527)) "
                                      "x_19527 x_19528)))))", Int64(0x123123)), 0)
        self.assertEquals(sexpr.solve("(lambda (x) (fold x 0 (lambda (y z) (or y z))))",
                                      Int64(0x1122334455667788)), 0x00000000000000FF)
        self.assertEquals(sexpr.solve("(lambda (x_45397) (fold x_45397 0 (lambda (x_45397 x_45398) "
                                      "(if0 (shr1 (plus (plus (shr4 (shr16 (or (or (shl1 x_45398) 0) x_45397))) "
                                      "(shl1 x_45397)) x_45397)) x_45397 x_45397))))", Int64(0x1122334455667788)),
                                      0x0000000000000011)

