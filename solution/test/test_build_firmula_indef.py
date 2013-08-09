import unittest
from ..tools import build_formula_index 
import re

class FormulaBuilderTestCase(unittest.TestCase):

    def test_test(self):
        p = re.compile('\(lambda \(id\) \(not \(not 1\)\)\)')
        a = build_formula_index.get_formulas_from_index(4)
        equels = 0
        for b in a:
            if p.match(b['s']):
               equels = 1 
        self.assertEquals(equels,1)

    def test_test1(self):
        p = re.compile('\(lambda \(id\) \(plus id 1\)\)')
        a = build_formula_index.get_formulas_from_index(4)
        equels = 0
        for b in a:
            if p.match(b['s']):
               equels = 1 
        self.assertEquals(equels,1)

#    def test_test1(self):
#        p = re.compile('\(lambda')
#        a = build_formula_index.get_formulas_from_index(5)
#        equels = 0
#        for b in a:
#            print b['s']
#            if p.match(b['s']):
#               equels = 1 
#        self.assertEquals(equels,1)
        
    def test_7_level_if0_and(self):
        p = re.compile('\(lambda \(id\) \(if0 .*and')
        a = build_formula_index.get_formulas_from_index(7)
        equels = 0
        for b in a:
            if p.search(b['s']):
               equels = 1 
        self.assertEquals(equels, 1)
        
    def test_7_level_if0_or(self):
        p = re.compile('\(lambda \(id\) \(if0 .*or')
        a = build_formula_index.get_formulas_from_index(7)
        equels = 0
        for b in a:
            if p.search(b['s']):
               equels = 1 
        self.assertEquals(equels, 1)

    def test_7_level_if0_xor(self):
        p = re.compile('\(lambda \(id\) \(if0 .*xor')
        a = build_formula_index.get_formulas_from_index(7)
        equels = 0
        for b in a:
            if p.search(b['s']):
               equels = 1 
        self.assertEquals(equels, 1)

    def test_7_level_Tfold(self):
        p = re.compile('\(lambda \(id\) \(fold')
        a = build_formula_index.get_formulas_from_index(7)
        equels = 0
        for b in a:
            if p.search(b['s']):
                equels = 1 
        self.assertEquals(equels, 1)
