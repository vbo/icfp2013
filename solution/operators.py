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
