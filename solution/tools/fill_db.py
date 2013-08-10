import argparse
import os
import tempfile
import filecmp
import sys

from ..operators import get_templated_operators
from . import build_formula_index
from ..lang.int64 import generate_inputs
from .. import solver
from .. import problems
from ..util import get_int64_array_hash


def generate_sql_for_problem(problem, index, parallelize=False, use_parser=True):
    for formula in index.generate_formulas(problem["size"], allowed_ops=problem["operators"]):
        if use_parser:
            outputs = list(solver.solve(formula["s"], inputs, parallelize=parallelize))
        else:
            outputs = list(solver.solve_formula(formula, inputs, parallelize=parallelize))


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

    parser.add_argument("--index", type=str, dest='index_basedir', default='./tree_index')
    parser.add_argument("--outdir", type=str, default='./sql/problems')
    parser.add_argument("--ops", type=str, dest='commaseparated_ops', default='')
    parser.add_argument("--ninputs", type=int, dest='ninputs', default=256)
    parser.add_argument("--offset", type=int, dest='offset', default=0)
    parser.add_argument("--limit", type=int, dest='limit', default=1)
    parser.add_argument("--group_id", type=int, dest='group_id', default=None)
    parser.add_argument("--parallel", action='store_true', dest='parallelize')
    parser.add_argument("-f", "--force", action='store_true', dest='force',
            help='Do not skip problem if SQL file already exists')
    parser.add_argument("--fixture", action='store_true', dest='fixture', default=False)
    parser.add_argument("--assert", action="store_true", dest="assert_only", default=False)
    parser.add_argument("--assert-dir", type=str, dest="assert_dir", default=tempfile.gettempdir())
    parser.add_argument("--nocompress", action="store_true", dest="nocompress", default=False,
            help='Do not call gzip after outputting sql')
    parser.add_argument("--noparse", action="store_true", dest="noparse", default=False,
            help="Don't use parser - use solve_formula to evaluate programs")

    args = parser.parse_args()

    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    index_dispatcher = build_formula_index.TreeIndexDispatcher(args.index_basedir)

    ops_to_filter = set(args.commaseparated_ops.split(','))

    offset = args.offset
    limit = args.limit
    group_id = args.group_id
    #TODO: fill_db by group_id
    assert_sql_path = None
    problems_getter = None

    if args.assert_only:
        args.force = True

    if args.fixture:
        problems_getter = lambda: problems.fixture_problems

    if ops_to_filter:
        problems_filter = lambda problem: not (set(get_templated_operators(problem['operators'])) - ops_to_filter)
    else:
        problems_filter = None

    problems_without_dupes = filter(problems_filter, problems.get_problems_without_dupes(problems_getter))

    print 'Total number of problems after applying filter:', len(problems_without_dupes)

    for problem_conf in problems_without_dupes[offset:offset + limit]:
        group_id = problem_conf['group_id']

        inputs = list(generate_inputs(args.ninputs, seed=group_id))
        inputs_hash = get_int64_array_hash(inputs)
        inputs_readable = '|'.join('%016x' % x for x in inputs)

        inputs_query = (
            "INSERT INTO inputs"
            "(inputs_hash, inputs)"
            "VALUES ('%s', '%s');\n" %
            (inputs_hash, inputs_readable)
        )

        problem_sql_path = os.path.join(args.outdir, 'problem.%s.sql' % group_id)
        if args.assert_only:
            if not os.path.isfile(problem_sql_path):
                print "Generate %s first to assert" % (problem_sql_path,)
                continue
            assert_sql_path = problem_sql_path
            problem_sql_path = os.path.join(args.assert_dir, 'problem.%s.assert.sql' % group_id)

        if not args.force and (os.path.isfile(problem_sql_path) or os.path.isfile(problem_sql_path + '.gz')):
            print 'Skipping generating SQL for problem group %d: file exists. Use --force to override.' % group_id
            continue

        print 'Generating SQL for problem group %d, saving to "%s"' % (group_id, problem_sql_path)
        # Pick specialized index to reduce space for problems without certain elements (like fold)
        index = index_dispatcher.get_index(problem_conf['operators'])

        try:
            with open(problem_sql_path, 'w') as fp:
                fp.write(inputs_query)
                for program_query in generate_sql_for_problem(problem_conf, index, args.parallelize, use_parser=not args.noparse):
                    fp.write(program_query)
        except Exception as e:
            if os.path.isfile(problem_sql_path):
                os.remove(problem_sql_path)
            raise

        if not args.nocompress:
            cmd = 'gzip -f "%s"' % problem_sql_path
            print cmd
            os.system(cmd)

        if args.assert_only:
            diff = "diff %s %s" % (problem_sql_path, assert_sql_path)
            print "Performing", diff
            sys.stdout.flush()
            cmp = filecmp.cmp(problem_sql_path, assert_sql_path)
            if not cmp:
                os.system(diff)
                print "Diff not empty:"
                print diff
                sys.exit(1)
            print "Empty diff: OK"
