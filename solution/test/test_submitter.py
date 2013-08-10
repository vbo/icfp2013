import unittest
import tempfile

from .. import api
from .. import submitter
from .. import util
from ..tools import build_formula_index
from ..lang.int64 import generate_inputs
from .. import solver
from ..lang import Int64

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
        #problem = {u'challenge': u'(lambda (x_3739) (fold x_3739 0 (lambda (x_3739 x_3740) (if0 x_3740 x_3739 0))))', u'operators': [u'if0', u'tfold'], u'id': u'blgr5ZCVLyCPe1Ms48fGhMnv', u'size': 9}
        #{u'challenge': u'(lambda (x_5313) (fold x_5313 0 (lambda (x_5313 x_5314) (shl1 (xor 1 x_5313)))))', u'operators': [u'shl1', u'tfold', u'xor'], u'id': u'6p6JluUDsRl7Aqmg8ox0xndw', u'size': 9}
        #{u'challenge': u'(lambda (x_5803) (fold x_5803 0 (lambda (x_5803 x_5804) (shr4 (xor x_5803 1)))))', u'operators': [u'shr4', u'tfold', u'xor'], u'id': u'PXTAy0CMrVJB9vXB525Coyoa', u'size': 9}
        if not problem:
            for i in range(10):
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
            raise





















