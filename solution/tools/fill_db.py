import argparse
import os

from . import build_formula_index
from ..lang.int64 import generate_inputs
from .. import solver
from .. import problems
from ..util import get_int64_array_hash


def generate_sql_for_problem(problem, index):
    for formula in index.generate_formulas(problem_conf["size"], allowed_ops=problem_conf["operators"]):
        outputs = list(solver.solve_formula(formula, inputs, parallelize=args.parallelize))

        db_outputs = get_int64_array_hash(outputs)

        operators = list(formula["ops"])
        operators.sort()
        operators = "_".join(operators)
        assert len(db_outputs)

        query = (
            "INSERT INTO program"
            "(size, operators, code, inputs, outputs)"
            "VALUES (%s, '%s', '%s', '%s', '%s');\n" %
            (formula["size"], operators, formula["s"], inputs_hash, db_outputs)
        )

        yield query


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("index_basedir")
    parser.add_argument("sql_basedir")
    parser.add_argument("--ninputs", type=int, dest='ninputs', default=256)
    parser.add_argument("--offset", type=int, dest='offset', default=0)
    parser.add_argument("--limit", type=int, dest='limit', default=1)
    parser.add_argument("--parallel", action='store_true', dest='parallelize')
    parser.add_argument("--force", action='store_true', dest='force', help='Do not skip problem if SQL file already exists')
    args = parser.parse_args()

    if not os.path.isdir(args.sql_basedir):
        os.makedirs(args.sql_basedir)

    index = build_formula_index.TreeTemplatesIndex(args.index_basedir)
    inputs = list(generate_inputs(args.ninputs))
    offset = args.offset
    limit = args.limit
    problems_without_dupes = list(problems.get_problems_without_dupes())

    inputs_hash = get_int64_array_hash(inputs)
    inputs_readable = '|'.join('%016x' % x for x in inputs)

    query = (
        "INSERT INTO inputs"
        "(inputs_hash, inputs)"
        "VALUES ('%s', '%s');\n" %
        (inputs_hash, inputs_readable)
    )

    with open(os.path.join(args.sql_basedir, 'inputs.sql'), 'a') as fp:
        fp.write(query)

    for problem_conf in problems_without_dupes[offset:offset + limit]:
        group_id = problem_conf['group_id']
        problem_sql_path = os.path.join(args.sql_basedir, 'problem.%s.sql' % group_id)

        if not args.force and os.path.isfile(problem_sql_path):
            print 'Skipping generating SQL for problem group %d.' % group_id
            continue

        print 'Generating SQL for problem group %d, saving to "%s"' % (group_id, problem_sql_path)
        try:
            with open(problem_sql_path, 'w') as fp:
                for query in generate_sql_for_problem(problem_conf, index):
                    fp.write(query)
        except Exception as e:
            if os.path.isfile(problem_sql_path):
                os.remove(problem_sql_path)
            raise
