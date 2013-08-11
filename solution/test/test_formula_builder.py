import unittest
from ..tools import build_formula_index
from nose.plugins.attrib import attr
import re

class FormulaBuilderTestCase(unittest.TestCase):

    tree_index_root = './tree_index'

    formulas = [
       # ('\(lambda \(id\) \(not \(not 1\)\)\)', 4, None, 1),
       # ('\(lambda \(id\) \(plus id 1\)\)', 4, None, 2),
        ('\(lambda \(id\) \(if0 .*and', 7, None, 3),
        ('\(lambda \(id\) \(if0 .*or', 7, None, 4),
        ('\(lambda \(id\) \(if0 .*xor', 7, None, 5),
        ('\(lambda \(id\) \(fold', 7, None, 6),
        ('\(lambda \(id\) \(fold id 0 \(lambda \(id\d id\d\) \(not \(not id\)\)\)\)\)', 8, ['tfold', 'not'], 7),
        ('\(lambda \(id\) \(fold', 9, ['tfold', 'if0'], 8),
        ('\(lambda \(id\) \(xor id \(or 0 \(shr4 \(shr16 id\)\)\)\)\)', 8, ['xor', 'or', 'shr4', 'shr16'], 9),
        ('\(lambda \(id\) \(fold id 0 \(lambda \(id2 id3\) \(not \(plus id2 id3\)\)\)\)\)', 9, ['tfold', 'plus', 'not'], 11),
        ('\(lambda \(id\) \(fold id 0 \(lambda \(id2 id3\) \(shl1 \(xor 1 id2\)\)\)\)\)', 9, ['shl1', 'tfold', 'xor'], 12),
        ('\(lambda \(id\) \(fold id 0 \(lambda \(id2 id3\) \(if0 id2 id2 id2\)\)\)\)', 9, ['tfold', 'if0'], 13),
    ]

    @classmethod
    def setUpClass(cls):
        cls.index = build_formula_index.TreeTemplatesIndex(cls.tree_index_root)
        cls.formulas_cache = {}
        
    def _get_cached_formulas(self, size, operators):
        
        key = (size, tuple(sorted(operators))) if operators is not None else size
        if key not in self.formulas_cache:
            self.formulas_cache[key] = list(self.index.generate_formulas(size, operators))

        return self.formulas_cache[key]

    def _check_formula_is_present(self, formula_regexp_text, size, operators, number):
        formulas = self._get_cached_formulas(size, operators)
        formula_regexp = re.compile(formula_regexp_text)
        equals = 0
       # if (number == 3):
       #    print formulas

        for f in formulas:
            if (number == 3):
               print f['s']
            if formula_regexp.match(f['s']):
               equals = 0
               break

        self.assertEqual(equals, 1, "Test number: " + str(number) + "\n\t\tFormula not found: '%s'" % formula_regexp_text)

    @attr('fast')
    def test_formulas(self):
        for f_regexp, size, operators, number in self.formulas:
            self._check_formula_is_present(f_regexp, size, operators, number)
