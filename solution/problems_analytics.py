import itertools
from operator import itemgetter
import pprint

from .problems import original_problems, get_problems_without_dupes
from .operators import Operators


def get_problems_distribution(problems, grouper):
    grouped = itertools.groupby(
        sorted(problems, key=grouper),
        grouper)

    histogram = [
        (len(list(group)), key)
        for (key, group) in grouped
    ]
    histogram.sort()

    return histogram


def get_operators_distribution(problems):
    return get_problems_distribution(problems, lambda p: tuple(sorted(p['operators'])))


def get_size_distribution(problems):
    return get_problems_distribution(problems, itemgetter('size'))


def get_templated_operators_distribution(problems):
    return get_problems_distribution(problems, lambda p: get_templated_operators(p['operators']))


def get_templated_operators(operators):
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


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        min_size = sys.argv[1]
    else:
        min_size = 0

    problems = [p for p in get_problems_without_dupes()
                if p['size'] > min_size]

    print len(problems)
    print len(original_problems)

    print 'Problems by size:'
    pprint.pprint(get_size_distribution(problems))

    print 'Problems by operators:'
    pprint.pprint(get_operators_distribution(problems))

    print 'Problems by templated operators:'
    pprint.pprint(get_templated_operators_distribution(problems))
