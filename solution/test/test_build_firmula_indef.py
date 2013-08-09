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

    def test_8_level_Tfold_params_const(self):
        p = re.compile('\(lambda \(id\) \(fold 1 id')
        a = build_formula_index.get_formulas_from_index(8)
        equels = 0
        for b in a:
            if p.search(b['s']):
                equels = 1 
        self.assertEquals(equels, 1)

    def test_param(self):
        p = re.compile('\(lambda')
        opers = ['not', 'shl1', 'shr1']
        a = build_formula_index.get_formulas_from_index(3, opers)
        mas=[]
        mas_equels=['(lambda (id) (not 1))',
                '(lambda (id) (not 0))',
                '(lambda (id) (not id))',
                '(lambda (id) (shl1 1))',
                '(lambda (id) (shl1 0))',
                '(lambda (id) (shl1 id))',
                '(lambda (id) (shr1 1))',
                '(lambda (id) (shr1 0))',
                '(lambda (id) (shr1 id))'
        ]
        for b in a:
            if p.search(b['s']):
                mas.append(b['s']);
        self.assertEquals(mas_equels, mas)

    def test_8_level_Tfold_params_const(self):
        p = re.compile('\(lambda \(id\).*shr1[^6]')
        opers = ['fold', 'if0', 'shr16', 'shr4']
        a = build_formula_index.get_formulas_from_index(8, opers)
        equels = 0
        for b in a:
            if p.search(b['s']):
                equels = 1 
        self.assertEquals(equels, 0)
