from itertools import product

class Operators(object):

    IF0 = 'if0'
    FOLD = 'fold'

    NOT = 'not'
    SHL1 = 'shl1'
    SHR1 = 'shr1'
    SHR4 = 'shr4'
    SHR16 = 'shr16'

    OP1 = 'op1'

    UNARY = set([NOT, SHL1, SHR1, SHR4, SHR16])

    AND = 'and'
    OR = 'or'
    XOR = 'xor'
    PLUS = 'plus'

    OP2 = 'op2'

    BINARY = set([AND, OR, XOR, PLUS])

    ALL_OPS = BINARY | UNARY | set([IF0, FOLD])

    TERMINAL = 'T'

    ZERO = '0'
    ONE = '1'
    ID = 'id'
    ID2 = 'id2'
    ID3 = 'id3'

    TERMINALS = set([ZERO, ONE, ID])
    TERMINALS_FULL = set([ZERO, ONE, ID, ID2, ID3])

    TFOLD = 'tfold'

    ANY = '*'

def one():
    return { 'operator': Operators.ONE, 'ops': [], 'f': Operators.ONE }

def zero():
    return { 'operator': Operators.ZERO, 'ops': [], 'f': Operators.ZERO }

formula_reducers = {
    (Operators.NOT, (Operators.NOT, Operators.ANY)): lambda args: args[0]['args'][0],

    (Operators.SHL1, Operators.ZERO): lambda args: zero(),
    (Operators.SHR1, Operators.ZERO): lambda args: zero(),
    (Operators.SHR4, Operators.ZERO): lambda args: zero(),
    (Operators.SHR16, Operators.ZERO): lambda args: zero(),
    (Operators.SHR1, Operators.ONE): lambda args: zero(),
    (Operators.SHR4, Operators.ONE): lambda args: zero(),
    (Operators.SHR16, Operators.ONE): lambda args: zero(),

    (Operators.AND, Operators.ZERO, Operators.ANY): lambda args: zero(),
    (Operators.AND, Operators.ANY, Operators.ZERO): lambda args: zero(),
    (Operators.AND, Operators.ONE, (Operators.NOT, Operators.ONE)): lambda args: zero(),
    (Operators.AND, Operators.ONE, Operators.ONE): lambda args: one(),

    (Operators.PLUS, Operators.ANY, Operators.ZERO): lambda args: args[0],
    (Operators.PLUS, Operators.ZERO, Operators.ANY): lambda args: args[1],

    (Operators.XOR, Operators.ZERO, Operators.ZERO): lambda args: zero(),
    (Operators.XOR, Operators.ZERO, Operators.ONE): lambda args: one(),
    (Operators.XOR, Operators.ONE, Operators.ZERO): lambda args: one(),
    (Operators.XOR, Operators.ONE, Operators.ONE): lambda args: zero(),

    (Operators.SHR16, (Operators.SHL1, Operators.ONE)): lambda args: zero(),
    (Operators.SHR1, (Operators.SHL1, Operators.ONE)): lambda args: one(),
    (Operators.SHL1, (Operators.SHR1, Operators.ONE)): lambda args: zero(),
    (Operators.SHR4, (Operators.SHL1, Operators.ONE)): lambda args: zero(),
    (Operators.SHR16, (Operators.SHL1, Operators.ZERO)): lambda args: zero(),
    (Operators.SHR1, (Operators.SHL1, Operators.ZERO)): lambda args: zero(),
    (Operators.SHL1, (Operators.SHR1, Operators.ZERO)): lambda args: zero(),
    (Operators.SHR4, (Operators.SHL1, Operators.ZERO)): lambda args: zero(),
  #  (Operators.SHR16, (Operators.SHR16, (Operators.SHR16, (Operators.SHR16, Operators.ANY)))): lambda args: zero(),
    (Operators.SHR16, (Operators.SHR16, (Operators.SHR16, (Operators.SHR16, (Operators.ANY, Operators.ANY))))): lambda args: zero(),
    (Operators.OR, Operators.ZERO, Operators.ANY): lambda args: args[1],
    (Operators.OR, Operators.ANY, Operators.ZERO): lambda args: args[0],
    (Operators.OR, Operators.ONE, Operators.ONE): lambda args: one(),
    (Operators.IF0, Operators.ZERO, Operators.ANY, Operators.ANY): lambda args: args[1],
    (Operators.IF0, Operators.ONE, Operators.ANY, Operators.ANY): lambda args: args[2],
    (Operators.IF0, Operators.ANY, Operators.ONE, Operators.ONE): lambda args: one(),
    (Operators.IF0, Operators.ANY, Operators.ZERO, Operators.ZERO): lambda args: zero(),
}

def formula_reducers_permutation():
    global formula_reducers
    for formula_reducer, answer in formula_reducers.items():
        for formula in formula_reducer_generator(formula_reducer):
            yield formula, answer

def formula_reducer_generator(formula_template):
    variants = []
    for arg in formula_template:
        v = []
        if type(arg) == tuple:
            #v = [a[0] if a is tuple and len(a) == 1 else a for a in list(formula_reducer_generator(arg))]
#a is tuple == False; type(a) == tuple = True
            v = [a[0] if type(a) == tuple and len(a) == 1 else a for a in list(formula_reducer_generator(arg))]
        elif arg == Operators.ANY:
            v = list(Operators.ALL_OPS | Operators.TERMINALS_FULL)
            flag_tmp = 1
        else:
            v = [arg]
        variants.append(v)
    for variant in product(*variants):
        yield variant

def get_formula_reducers():
    return dict(formula_reducers_permutation())

def get_templated_operators(operators):
    '''
    >>> get_templated_operators(["plus", "xor", "if0", "tfold"])
    ('if0', 'op2')
    >>> get_templated_operators(["not", "fold"])
    ('fold', 'op1')
    >>> get_templated_operators(["not", "fold", "xor", "if0", "trash"])
    ('if0', 'fold', 'op1', 'op2', 'trash')
    '''
    templated_operators = set()

    for op in operators:
        if op in Operators.UNARY:
            templated_operators.add(Operators.OP1)
        elif op in Operators.BINARY:
            templated_operators.add(Operators.OP2)
        elif op == 'tfold':
            continue
        else:
            templated_operators.add(op)

    return tuple(sorted(templated_operators))
