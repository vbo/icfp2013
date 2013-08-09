import json
import unittest
from .. import solver
from ..tools import build_formula_index

class SolverTestWithFixture(unittest.TestCase):

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
            for line in fixture:
                if not line.strip():
                    continue
                conf = json.loads(line)
                program = conf["request"]["challenge"]
                size = conf["request"]["size"]
                if size > 10:
                    continue
                print '.'
                programs = []
                for data in build_formula_index.get_formulas_from_index(size):
                    programs.append(data)
                self.assertTrue(program in programs, '%s not found. Size: %s' % (program, size))




