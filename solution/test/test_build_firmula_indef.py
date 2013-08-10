import unittest
from ..tools import build_formula_index
import re

class FormulaBuilderTestCase(unittest.TestCase):

    tree_index_root = './tree_index'

    formulas = [
        ('\(lambda \(id\) \(not \(not 1\)\)\)', 4),
        ('\(lambda \(id\) \(plus id 1\)\)', 4),
        ('\(lambda \(id\) \(if0 .*and', 7),
        ('\(lambda \(id\) \(if0 .*or', 7),
        ('\(lambda \(id\) \(if0 .*xor', 7),
        ('\(lambda \(id\) \(fold', 7),
    ]

    @classmethod
    def setUpClass(cls):
        cls.index = build_formula_index.TreeTemplatesIndex(cls.tree_index_root)
        cls.formulas_cache = {}

    def _get_cached_formulas(self, size):
        if size not in self.formulas_cache:
            self.formulas_cache[size] = list(self.index.generate_formulas(size))

        return self.formulas_cache[size]

    def _check_formula_is_present(self, formula_regexp_text, size):
        formulas = self._get_cached_formulas(size)

        formula_regexp = re.compile(formula_regexp_text)
        equals = 0

        for f in formulas:
            if formula_regexp.match(f['s']):
               equals = 1
               break

        self.assertEqual(equals, 1, "Formula not found: '%s'" % formula_regexp_text)

    def test_formulas(self):
        for f_regexp, size in self.formulas:
            self._check_formula_is_present(f_regexp, size)
