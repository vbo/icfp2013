import json, unittest, re, sys
from .. import solver, api, config
from ..tools import build_formula_index

ex_train = config.example_train

api.request_delay = 5

class SolutionTestRange(unittest.TestCase):

    tree_index_root = './tree_index'


class SolverTestWithFixture(unittest.TestCase):

    tree_index_root = './tree_index'

    def test_solver(self):
        with open("./fixture/solver_fixture.jsons") as fixture:
            for line in fixture:
                if not line.strip():
                    continue
                conf = json.loads(line)
                inputs = conf["request"]["input"]
                results = conf["outputs"]
                for i, result in enumerate(solver.solve(conf["request"]["challenge"], inputs, parallelize=True)):
                    expected = int(results[i], base=16)
                    self.assertEquals(result, expected, "%s is not %s for %s" % (
                        result, expected, conf["request"]["challenge"]))

    def _transformXsToIds(self, text):
        idsToTransform = re.findall(r'x_[0-9]*', text)
        uniqIds = []
        if (len(idsToTransform) > 0):
            for x in idsToTransform:
                if x not in uniqIds:
                    uniqIds.append(x)
        for i in range(len(uniqIds)):
            if (i == 0):
                text = text.replace(uniqIds[i], 'id')
            else:
                text = text.replace(uniqIds[i], 'id' + str(i+1))
        return text

SolverTestWithFixture.__test__ = False
