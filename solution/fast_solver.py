import ctypes

bvfast = ctypes.CDLL('./lib/libbvsolve.so')

bvfast.bv_parse.restype = ctypes.c_void_p
bvfast.bv_eval.restype = ctypes.c_uint64


class ParsedFormula(object):

    def __init__(self, formula_str):
        if isinstance(formula_str, unicode):
            formula_str = formula_str.encode('latin1')
        self._formula = bvfast.bv_parse(formula_str)

    def __del__(self):
        bvfast.bv_free(self._formula)

    def eval(self, inp):
        return bvfast.bv_eval(self._formula, ctypes.c_uint64(inp))


def solve(formula_str, inputs):
    formula = ParsedFormula(formula_str)
    return (formula.eval(inp) for inp in inputs)


if __name__ == '__main__':
    f = "(lambda (id) (fold id 0 (lambda (id2 id3) (not 1))))"
    print list(solve(f, range(3)))
