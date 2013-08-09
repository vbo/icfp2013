import re

import _sexpr
from _sexpr import Atom, SExpr as Exp, symbol as Symbol
from lang import Int64, op, e


id_table = {}

def solve(st, arg):
    top_level_items = _sexpr.parse(st)[0].items
    top_arg_id = top_level_items[1].items[0].value
    id_table[top_arg_id] = arg
    body_e = top_level_items[2]
    return parse_exp(body_e)

def parse_exp(exp):
    print "Parsing exp: ", exp
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
            print args[0]
            args_exp_items = args[0].items
            id_table[args_exp_items[0].value] = x
            id_table[args_exp_items[1].value] = y
            res = parse_exp(args[1])
            print "fold_func_ret:", res
            return res
        return fold_func
    else:
        raise
    parsed_args = (parse_exp(arg) for arg in args)
    return func(*list(parsed_args))

def parse_atom(atom):
    if atom.type == Symbol:
        return Int64(id_table[atom.value])
    elif atom.type == int:
        return Int64(int(atom.value))

