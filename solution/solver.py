import multiprocessing

from . import _sexpr
from ._sexpr import Atom, symbol as Symbol
from .lang import Int64, op, e
from operators import Operators


id_table = {}
_pool = None

POOL_PROCESSCOUNT = 4
POOL_CHUNKSIZE = 64


def solve(st, args, parallelize=False):
    if parallelize:

        global _pool
        if _pool is None:
            _pool = multiprocessing.Pool(POOL_PROCESSCOUNT)

        return _pool.imap(_solve_tuple,
                          ((st, arg) for arg in args),
                          chunksize=POOL_CHUNKSIZE)
    else:
        return map(_solve_tuple,
                   ((st, arg) for arg in args))


def _solve(st, arg):
    return _solve_tuple((st, arg))


def _solve_tuple((st, arg)):
    top_level_items = _sexpr.parse(st)[0].items
    top_arg_id = top_level_items[1].items[0].value
    id_table[top_arg_id] = arg
    body_e = top_level_items[2]
    res = parse_exp(body_e)
    id_table.clear()
    return res

def parse_exp(exp):
    if isinstance(exp, Atom):
        return parse_atom(exp)
    items = exp.items
    term = items[0]
    args = items[1:]
    if hasattr(op, term.value):
        func = getattr(op, term.value)
    elif term.value in op.renames:
        func = op.renames[term.value]
    elif hasattr(e, term.value):
        func = getattr(e, term.value)
    elif term.value == 'lambda':
        def fold_func(x, y):
            args_exp_items = args[0].items
            id_table[args_exp_items[0].value] = x
            id_table[args_exp_items[1].value] = y
            res = parse_exp(args[1])
            return res
        return fold_func
    else:
        raise
    parsed_args = map(parse_exp, args)
    return Int64(func(*parsed_args))

def parse_atom(atom):
    if atom.type == Symbol:
        try:
            return Int64(id_table[atom.value])
        except ValueError:
            return Int64(int(id_table[atom.value], base=16))
    elif atom.type == int:
        return Int64(int(atom.value))


def solve_formula(formula, args, parallelize=False):
    '''
    :param formula:
        formula is a representation of \BV program with following attributes:
            "operator" - one of `Operators` fields, representing operator tag.
            "args" - tuple with subexpressions of the same form. Empty for terminals.
    :return:
        Value of evaluating formula on argument arg.
    '''

    if parallelize:
        global _pool
        if _pool is None:
            _pool = multiprocessing.Pool(POOL_PROCESSCOUNT)

        return _pool.imap(_solve_formula_tuple,
                          ((formula, arg) for arg in args),
                          chunksize=POOL_CHUNKSIZE)
    else:
        return map(_solve_formula_tuple,
                   ((formula, arg) for arg in args))


def solve_formula_for_one(formula, arg):
    if not isinstance(arg, Int64):
        arg = Int64(arg)
    return _solve_formula_tuple((formula, arg))


def _solve_formula_tuple((formula, arg)):
    id_table.clear()
    id_table[Operators.ID] = arg
    return _solve_formula(formula)


def _solve_formula(formula):
    operator = formula['operator']
    args = formula.get('args')

    if operator in Operators.UNARY or operator in Operators.BINARY:

        operator_func = op.renames[operator] \
            if operator in op.renames \
            else getattr(op, operator)

        return operator_func(*map(_solve_formula, args))

    elif operator == Operators.IF0:
        predicate = _solve_formula(args[0])
        if predicate == 0:
            return _solve_formula(args[1])
        else:
            return _solve_formula(args[2])

    elif operator == Operators.FOLD:
        def fold_helper(id2, id3):
            id_table[Operators.ID2] = id2
            id_table[Operators.ID3] = id3
            return _solve_formula(args[2])

        return e.fold(
            _solve_formula(args[0]),
            _solve_formula(args[1]),
            fold_helper)

    elif operator == Operators.ZERO:
        return Int64.ZERO
    elif operator == Operators.ONE:
        return Int64.ONE
    else:
        return id_table[operator]
