from .operators import Operators


def get_formula(operator, args):
    if operator in Operators.TERMINALS_FULL:
        return operator

    return (operator, args)


def get_operator(formula):
    if isinstance(formula, tuple):
        return formula[0]
    else:
        return formula


def get_args(formula):
    if isinstance(formula, tuple):
        return formula[1:]
    else:
        return []


def formula_to_string(formula):
    '''
    :param formula:
        formula is a representation of \BV program with following attributes:
            "operator" - one of `Operators` fields, representing operator tag.
            "args" - tuple with subexpressions of the same form. Empty for terminals.
    :return:
        \BV program source code.
    '''
    op = get_operator(formula)
    args = get_args(formula)

    if op in Operators.UNARY:
        return '(%s %s)' % (op, formula_to_string(args[0]))
    elif op in Operators.BINARY:
        return '(%s %s %s)' % (op, formula_to_string(args[0]), formula_to_string(args[1]))
    elif op == Operators.IF0:
        return '(if0 %s %s %s)' % (
            formula_to_string(args[0]),
            formula_to_string(args[1]),
            formula_to_string(args[2]),
        )
    elif op == Operators.FOLD:
        return '(fold %s %s (lambda (%s %s) %s))' % (
            formula_to_string(args[0]),
            formula_to_string(args[1]),
            Operators.ID2,
            Operators.ID3,
            formula_to_string(args[2]),
        )
    else:
        # Assuming it is terminal
        return op
