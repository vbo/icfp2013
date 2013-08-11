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
]

test_problems = [
    {u'challenge': u'(lambda (x_4779) (fold x_4779 0 (lambda (x_4779 x_4780) (not (xor 1 x_4779)))))', u'operators': [u'not', u'tfold', u'xor'], u'id': u'TcnLcSP6y2IuPxmBMZwsOyjl', u'size': 9},
    {u'challenge': u'(lambda (x_8126) (if0 (shl1 (and (shr1 x_8126) 1)) x_8126 1))', u'operators': [u'and', u'if0', u'shl1', u'shr1'], u'id': u'jFMbk8x2vR3qmbgDB2MRwphj', u'size': 9},
    {u'challenge': u'(lambda (x_8898) (if0 (and (plus 0 x_8898) 1) x_8898 0))', u'operators': [u'and', u'if0', u'plus'], u'id': u'0scfjr7jk8cC4YtrcwSauDcg', u'size': 9},
    {u'challenge': u'(lambda (x_3493) (fold x_3493 0 (lambda (x_3493 x_3494) (shr1 (xor 1 x_3493)))))', u'operators': [u'shr1', u'tfold', u'xor'], u'id': u'9PBjaU9p2sc67drC1PBBMU29', u'size': 9},
    {u'challenge': u'(lambda (x_4595) (fold x_4595 0 (lambda (x_4595 x_4596) (not (and x_4595 x_4596)))))', u'operators': [u'and', u'not', u'tfold'], u'id': u'oC80rvyJCIf1l8V0fbVUTbnv', u'size': 9},
    {u'challenge': u'(lambda (x_6151) (fold x_6151 0 (lambda (x_6151 x_6152) (plus (shr16 x_6152) x_6151))))', u'operators': [u'plus', u'shr16', u'tfold'], u'id': u'LLFqEtb4cAyiBEPCfLVkEQVf', u'size': 9},
    {u'challenge': u'(lambda (x_3597) (fold x_3597 0 (lambda (x_3597 x_3598) (and (shr4 x_3597) x_3597))))', u'operators': [u'and', u'shr4', u'tfold'], u'id': u'4uxgf7IySl3FJeoR2V9lROwK', u'size': 9},
    {u'challenge': u'(lambda (x_4235) (fold x_4235 0 (lambda (x_4235 x_4236) (if0 x_4236 1 x_4235))))', u'operators': [u'if0', u'tfold'], u'id': u'moaBf56AVnpjDQZQ3vYMqs6Z', u'size': 9},
    {u'challenge': u'(lambda (x_8816) (if0 (shl1 (shr16 (shl1 x_8816))) 1 (not x_8816)))', u'operators': [u'if0', u'not', u'shl1', u'shr16'], u'id': u'SJO2zI0Q6W3eskb6gWUK7fuz', u'size': 9},
    {u'challenge': u'(lambda (x_4431) (fold x_4431 0 (lambda (x_4431 x_4432) (xor (shl1 x_4431) 0))))', u'operators': [u'shl1', u'tfold', u'xor'], u'id': u'EQPeq8KtjXWIcQB6Vh0GfhY9', u'size': 9},
]


original_problems = list(load_from_json())
