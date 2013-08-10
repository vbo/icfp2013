import unittest
import tempfile
import itertools

from .. import api
from .. import submitter
from .. import util
from ..tools import build_formula_index
from ..lang.int64 import generate_inputs
from .. import solver
from ..lang import Int64
from nose.plugins.attrib import attr

api.request_delay = 0

class Mock(object):

    def __init__(self, inputs, index):
        self.inputs = inputs
        self.index = index
        self.generated_variants = 0

    def load_inputs_from_index(self, size, operators):
        return self.inputs, self.inputs

    def load_variants_from_index(self, size, operators, inputs_hash, outputs_hash):
        for formula in self.index.generate_formulas(size, allowed_ops=operators):
            self.generated_variants += 1
            outputs = list(solver.solve_formula(formula, map(lambda x: Int64(int(x, base=16)), self.inputs)))
            if util.get_int64_array_hash(outputs) == outputs_hash:
                yield formula['s']

submitter.get_variants_count = lambda x: 0


class SubmitterTestCase(unittest.TestCase):

    def test_with_train(self):
        problem = None
        if not problem:
            for i in range(5):
                problem = api.train(9)
                self._try_solve(problem)
        else:
            self._try_solve(problem)

    def _try_solve(self, problem):
        try:
            index_dispatcher = build_formula_index.TreeIndexDispatcher(tempfile.gettempdir())
            index = index_dispatcher.get_index(problem['operators'])
            inputs = list(generate_inputs(64))
            inputs = map(lambda x: str(x.as_hex()), inputs)
            mock = Mock(inputs, index)
            submitter.load_variants_from_index = mock.load_variants_from_index
            submitter.load_inputs_from_index = mock.load_inputs_from_index
            submitter.submit(problem)
        except BaseException as e:
            print "Exception: %s\nProblem was: %s\nVariants generated: %s" % (e, problem, mock.generated_variants)
            if isinstance(e, submitter.NotSolvedError):
                print "Variants: %s\nInputs=>Outputs:\n%s" % (
                    e.variants, "\n".join(map(lambda (x, y): "%s=>%s" % (x, y), itertools.izip(e.inputs, e.outputs)))
                )
            raise
