import unittest, re, sys
from ..tools import build_formula_index
from .. import api, config

ex_train = config.example_train

api.request_delay = 5

class SolutionTestRange(unittest.TestCase):

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
        for data in build_formula_index.get_formulas_from_index(size):
            programs.append(data["s"])
        result = api.train(size)
        program = result["challenge"]
        program = self._transformXsToIds(program)
        self.assertTrue(program in programs, '%s not found' % (program))

    def test_range3(self):
        self._test_range(3)

    def test_range4(self):
        self._test_range(4)

    def test_range5(self):
        self._test_range(5)

    def test_range6(self):
        self._test_range(6)

    def test_range7(self):
        self._test_range(7)

    def test_range8(self):
        self._test_range(8)

    def test_range9(self):
        self._test_range(9)

# skip to not DDoS game server
SolutionTestRange.__test__ = False
