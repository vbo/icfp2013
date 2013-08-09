import unittest
from nose.exc import SkipTest

from .. import sexpr
from ..lang import Int64, op


class SexprTestCase(unittest.TestCase):

    def test_top_level_const(self):
        self.assertEquals(sexpr._solve("(lambda (t) 0)", 0), 0)
        self.assertEquals(sexpr._solve("(lambda (t) 1)", 0), 1)

    def test_top_level_arg(self):
        self.assertEquals(sexpr._solve("(lambda (t) t)", 31337), 31337)

    def test_top_level_op1(self):
        self.assertEquals(sexpr._solve("(lambda (t) (not 0))", 0), op.not_(0))
        self.assertEquals(sexpr._solve("(lambda (t) (not t))", 8), op.not_(8))
        self.assertEquals(sexpr._solve("(lambda (t) (shl1 t))", 8), op.shl1(8))

    def test_top_level_fold(self):
        self.assertEquals(sexpr._solve("(lambda (x) (fold x 1 (lambda (y z) z)))", 1), 1)
        self.assertEquals(sexpr._solve("(lambda (x_19527) (fold x_19527 0 (lambda (x_19527 x_19528) "
                                       "(shr1 (if0 (and (shr4 x_19528) (and x_19527 x_19527)) "
                                       "x_19527 x_19528)))))", Int64(0x123123)), 0)
        self.assertEquals(sexpr._solve("(lambda (x) (fold x 0 (lambda (y z) (or y z))))",
                                       Int64(0x1122334455667788)), 0x00000000000000FF)
        self.assertEquals(
            sexpr._solve("(lambda (x_45397) (fold x_45397 0 (lambda (x_45397 x_45398) "
                         "(if0 (shr1 (plus (plus (shr4 (shr16 (or (or (shl1 x_45398) 0) x_45397))) "
                          "(shl1 x_45397)) x_45397)) x_45397 x_45397))))", Int64(0x1122334455667788)), 0x0000000000000011)

        self.assertEquals(sexpr._solve("(lambda (x_31742) (or (or (shr16 (or (shr16 (shr4 0)) " 
                                        "(xor (and (if0 (xor (or 1 0) x_31742) 1 1) x_31742) x_31742))) 0) x_31742))", 
                                        Int64(0xABCDEF1234567890)), 0xABCDEFDFFF567CD6)
        self.assertEquals(sexpr._solve("(lambda (x_36979) (and (shr16 (plus x_36979 (if0 (shr4 (shl1 x_36979))"
                                        " (shr4 0) (shr4 (shr1 (shr1 (not (if0 (plus (shr4 (xor 1 x_36979)) x_36979)"
                                        " x_36979 x_36979)))))))) x_36979))", 
                                        Int64(0xABCDEF1234567890)), 0x0000AD1234546880)
        self.assertEquals(sexpr._solve("(lambda (x_36979) (and (shr16 (plus x_36979 (if0 (shr4 (shl1 x_36979))"
                                        " (shr4 0) (shr4 (shr1 (shr1 (not (if0 (plus (shr4 (xor 1 x_36979)) x_36979)"
                                        " x_36979 x_36979)))))))) x_36979))", 
                                        Int64(0xFFFFFFFFFFFFFFFF)), 0x0000FFFFFFFFFFFF)
