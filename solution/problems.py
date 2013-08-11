import itertools
import json

from . import operators
from .operators import Operators


def get_problems_without_dupes(getter=None):
    if not getter:
        getter = lambda: original_problems
    return getter()
    # NO group_id anymore :(
    #for group_id, problems in itertools.groupby(getter(), lambda p: p['group_id'],):
    #    yield problems.next()


def estimate_simplicity(problem):
    problem_size = problem['size']

    problem['operators']
    distrib = operators.get_operators_distribution(problem['operators'])

    has_fold = Operators.FOLD in problem['operators']
    has_if0 = Operators.IF0 in problem['operators']
    has_tfold = Operators.TFOLD in problem['operators']

    op1count = distrib.get(Operators.OP1, 0)
    op2count = distrib.get(Operators.OP2, 0)
    foldcost = 3 if has_fold else 0
    if0cost = 2 if has_if0 else 0

    tfold_size_compensation = -4 if has_tfold else 0

    return (op1count + 2*op2count + foldcost + if0cost)*(problem_size - tfold_size_compensation)


def load_from_json(path='fixture/problems.jsons'):
    with open(path) as fp:
        for line in fp:
            yield json.loads(line)


def dump_to_json(problems, path='fixture/problems.jsons'):
    with open(path, 'w') as fp:
        for p in problems:
            fp.write(json.dumps(p))
            fp.write('\n')


fixture_problems = [
    {'operators': None, 'group_id': -3, 'size': 3},
    {'operators': None, 'group_id': -4, 'size': 4},
    {'operators': None, 'group_id': -5, 'size': 5},
    {'operators': None, 'group_id': -6, 'size': 6},
    {'operators': None, 'group_id': -7, 'size': 7},
    {'operators': None, 'group_id': -8, 'size': 8},
    {'operators': None, 'group_id': -9, 'size': 9},
    {'operators': None, 'group_id': -10, 'size': 10},
    {'operators': None, 'group_id': -11, 'size': 11},
    {'operators': None, 'group_id': -12, 'size': 12},
    {'operators': None, 'group_id': -13, 'size': 13},
    {'operators': None, 'group_id': -14, 'size': 14},
    {'operators': None, 'group_id': -15, 'size': 15},
    {'operators': None, 'group_id': -16, 'size': 16},
    {'operators': None, 'group_id': -17, 'size': 17},
]

original_problems = list(load_from_json())
