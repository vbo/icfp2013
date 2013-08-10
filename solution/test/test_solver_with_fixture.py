import json, unittest, re, sys
from .. import solver, api, config
from ..tools import build_formula_index

ex_train = config.example_train

api.request_delay = 5

class SolutionTestRange(unittest.TestCase):

    tree_index_root = './tree_index'


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
                for i, result in enumerate(solver.solve(conf["request"]["challenge"], inputs, parallelize=True)):
                    expected = int(results[i], base=16)
                    self.assertEquals(result, expected, "%s is not %s for %s" % (
                        result, expected, conf["request"]["challenge"]))

    def test_program_existance(self):
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
                program = self._transformXsToIds(program)
                combinations = index.generate_formulas(
                    size, allowed_ops=conf["request"]["operators"])
                self.assertTrue(any(program == possible_program['s']
                                    for possible_program in combinations),
                                '%s not found. Size: %s' % (program, size))

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

    def _test_range(self,size):
        programs = []
        index = build_formula_index.TreeTemplatesIndex(self.tree_index_root)
        for data in index.generate_formulas(size):
            programs.append(data["s"])
        result = api.train(size)
        program = result["challenge"]
        program = self._transformXsToIds(program)
        self.assertTrue(program in programs, '%s not found' % (program))

    def test_range3(self):
        self._test_range(3)