import itertools
import json

from . import operators
from .operators import Operators


def get_problems_without_dupes(getter=None):
    if not getter:
        getter = lambda: original_problems
    for group_id, problems in itertools.groupby(getter(), lambda p: p['group_id']):
        yield problems.next()


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
    {'operators': ['shr4'], 'group_id': -2, 'id': '8iACnU9ZszMfCA4IAoSu5Sdc', 'size': 3},
    {'operators': ['plus', 'not'], 'group_id': -1, 'id': 'fixture__8RSpib2HhbZulX2t5iPN7oud', 'size': 5},
    {'operators': None, 'group_id': -10, 'id': 'fixture__8RSpib2HhbZulX2t5iPN7oud', 'size': 9},
]


original_problems = list(load_from_json())
