import json
import unittest
from .. import solver
from ..tools import build_formula_index

class SolverTestWithFixture(unittest.TestCase):

    tree_index_root = './tree_index'

    def test_all(self):
        with open("./fixture/solver_fixture.jsons") as fixture:
            for line in fixture:
                if not line.strip():
                    continue
                conf = json.loads(line)
                inputs = conf["request"]["input"]
                results = conf["outputs"]
                for i, result in enumerate(solver.solve(conf["request"]["challenge"], inputs)):
                    expected = int(results[i], base=16)
                    self.assertEquals(result, expected, "%s is not %s for %s" % (
                        result, expected, conf["request"]["challenge"]))

    def test_FunctionExistance(self):
        with open("./fixture/solver_fixture.jsons") as fixture:
            index = build_formula_index.TreeTemplatesIndex(self.tree_index_root)

            for line in fixture:
                if not line.strip():
                    continue
                conf = json.loads(line)
                program = conf["request"]["challenge"]
                size = conf["request"]["size"]
                if size > 10:
                    continue
                print '.'

                self.assertTrue(any(program == possible_program for possible_program in
                                    index.generate_formulas(size)),
                                '%s not found. Size: %s' % (program, size))




