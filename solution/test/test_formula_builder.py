import unittest
from ..tools import build_formula_index
import re

class FormulaBuilderTestCase(unittest.TestCase):

    tree_index_root = './tree_index'

    formulas = [
        ('\(lambda \(id\) \(not \(not 1\)\)\)', 4, None),
        ('\(lambda \(id\) \(plus id 1\)\)', 4, None),
        ('\(lambda \(id\) \(if0 .*and', 7, None),
        ('\(lambda \(id\) \(if0 .*or', 7, None),
        ('\(lambda \(id\) \(if0 .*xor', 7, None),
        ('\(lambda \(id\) \(fold', 7, None),
        ('\(lambda \(id\) \(fold id 0 \(lambda \(id\d id\d\) \(not \(not id\)\)\)\)\)', 8, ['tfold', 'not']),
        ('\(lambda \(id\) \(fold', 9, ['tfold', 'if0']),
    ]

    @classmethod
    def setUpClass(cls):
        cls.index = build_formula_index.TreeTemplatesIndex(cls.tree_index_root)
        cls.formulas_cache = {}

    def _get_cached_formulas(self, size, operators):
        if size not in self.formulas_cache:
            self.formulas_cache[size] = list(self.index.generate_formulas(size, operators))

        return self.formulas_cache[size]

    def _check_formula_is_present(self, formula_regexp_text, size, operators):
        formulas = self._get_cached_formulas(size, operators)
        formula_regexp = re.compile(formula_regexp_text)
        equals = 0

        for f in formulas:
            if formula_regexp.match(f['s']):
               equals = 1
               break

        self.assertEqual(equals, 1, "Formula not found: '%s'" % formula_regexp_text)

    def test_formulas(self):
        for f_regexp, size, operators in self.formulas:
            self._check_formula_is_present(f_regexp, size, operators)
