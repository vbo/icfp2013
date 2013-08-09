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

    TERMINAL = 'T'

    ZERO = '0'
    ONE = '1'
    ID = 'id'
    ID2 = 'id2'
    ID3 = 'id3'

    TERMINALS = set([ZERO, ONE, ID])
