import json
import unittest
from .. import solver


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




