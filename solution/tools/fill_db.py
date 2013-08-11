import argparse
import os
import tempfile
import filecmp
import sys
import time
import shutil

from solution.operators import get_templated_operators
from solution.tools import build_formula_index
from solution.lang.int64 import generate_inputs
from solution import fast_solver, solver
from solution import problems
from solution.util import get_int64_array_hash

home_directory = os.environ['HOME']
dropbox_directory = os.path.join(home_directory, 'Dropbox', 'Icfp2013', 'problems_index')


def generate_sql_for_problem(problem, index, inputs, inputs_hash, parallelize=False, use_parser=True):
    for formula in index.generate_formulas(problem["size"], allowed_ops=problem["operators"]):
        if use_parser:
            outputs = fast_solver.solve(formula["s"], inputs)
        else:
            outputs = solver.solve_formula(formula["formula"], inputs, parallelize=parallelize)


        db_outputs = get_int64_array_hash(outputs)
        if problem['operators'] is None:
            operators = '*'
        else:
            operators = list(problem['operators'])
            operators.sort()
            operators = "_".join(operators)
        assert len(db_outputs)

        query = (
            "INSERT INTO program"
            "(size, operators, code, inputs, outputs)"
            "VALUES (%s, '%s', '%s', '%s', '%s');\n" %
            (problem["size"], operators, formula["s"], inputs_hash, db_outputs)
        )

        yield query


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--index", type=str, dest='index_basedir', default='./tree_index')
    parser.add_argument("--outdir", type=str, default=dropbox_directory)
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
    parser.add_argument("--assert-dir", type=str, dest="assert_dir", default=tempfile.mkdtemp())
    parser.add_argument("--nocompress", action="store_true", dest="nocompress", default=False,
            help='Do not call gzip after outputting sql')
    parser.add_argument("--noparse", action="store_true", dest="noparse", default=False,
            help="Don't use parser - use solve_formula to evaluate programs")
    parser.add_argument("--timeout", type=int, default=0)
    parser.add_argument("--dry-run", action='store_true', dest='dry_run',
            help='Do not perform any computations - just print what will happen')

    args = parser.parse_args()

    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    index_dispatcher = build_formula_index.TreeIndexDispatcher(args.index_basedir)

    if args.commaseparated_ops:
        ops_to_filter = set(args.commaseparated_ops.split(','))
    else:
        ops_to_filter = None

    if os.path.abspath(args.assert_dir) == os.path.abspath(args.outdir):
        print "ASSERT DIR CANNOT BE SAME AS OUTDIR"
        sys.exit(1)

    offset = args.offset
    limit = args.limit
    problems_getter = None

    if args.assert_only:
        args.force = True

    if args.fixture:
        problems_getter = lambda: problems.fixture_problems

    if ops_to_filter:
        problems_filter = lambda problem: not (set(get_templated_operators(problem['operators'])) - ops_to_filter)
    else:
        problems_filter = lambda problem: True

    if args.group_id:
        original_problems_filter = problems_filter
        problems_filter = lambda problem: original_problems_filter(problem) and problem.get('group_id', 0) >= args.group_id

    problems_without_dupes = filter(problems_filter, problems.get_problems_without_dupes(problems_getter))

    print 'Total number of problems after applying filter:', len(problems_without_dupes)

    # We use GLOBALLY equal inputs to get inputs->outputs mapping for all problems which we can query GLOBALLY. i.e. if we don't know SIZE and OPERATORS (for bonus problems) we could just use our existing database to query only by INPUTS and OUTPUTS.
    inputs = list(generate_inputs(args.ninputs, seed=42))
    inputs_hash = get_int64_array_hash(inputs)
    inputs_readable = '|'.join('%016x' % x for x in inputs)

    inputs_query = (
        "INSERT INTO inputs"
        "(inputs_hash, inputs)"
        "VALUES ('%s', '%s');\n" %
        (inputs_hash, inputs_readable)
    )

    for problem_conf in problems_without_dupes[offset:offset + limit]:
        group_id = problem_conf['id']

        final_problem_sql_path = os.path.join(args.outdir, 'problem.%s.sql' % group_id)
        problem_sql_path = os.path.join(args.assert_dir, 'problem.%s.sql' % group_id)

        if args.assert_only:
            if not os.path.isfile(final_problem_sql_path):
                print "Generate %s first to assert" % (final_problem_sql_path,)
                continue
            problem_sql_path = os.path.join(args.assert_dir, 'problem.%s.assert.sql' % group_id)

        if not args.force and not args.assert_only and (os.path.isfile(final_problem_sql_path) or os.path.isfile(final_problem_sql_path + '.gz')):
            print 'Skipping generating SQL for problem group %s: file exists. Use --force to override.' % group_id
            continue

        print 'Generating SQL for problem group %s, saving to "%s"' % (group_id, problem_sql_path)
        if args.dry_run:
            continue

        # Pick specialized index to reduce space for problems without certain elements (like fold)
        index = index_dispatcher.get_index(problem_conf['operators'])

        need_to_delete_sql = False

        try:
            with open(problem_sql_path, 'w') as fp:
                fp.write(inputs_query)
                start_time = time.time()
                for program_query in generate_sql_for_problem(problem_conf, index, inputs, inputs_hash, parallelize=args.parallelize, use_parser=not args.noparse):
                    fp.write(program_query)
                    if args.timeout:
                        elapsed = time.time() - start_time
                        if elapsed > args.timeout:
                            print "Skipping problem because of timeout"
                            need_to_delete_sql = True
                            break
        except BaseException as e:
            #if os.path.isfile(problem_sql_path):
                #os.remove(problem_sql_path)
            raise

        if need_to_delete_sql:
            if os.path.isfile(problem_sql_path):
                os.remove(problem_sql_path)
            continue

        if args.assert_only:
            diff = "diff %s %s" % (problem_sql_path, final_problem_sql_path)
            print "Performing", diff
            sys.stdout.flush()
            cmp = filecmp.cmp(problem_sql_path, final_problem_sql_path)
            if not cmp:
                os.system(diff)
                print "Diff not empty:"
                print diff
                sys.exit(1)
            print "Empty diff: OK"
            continue


        if not args.nocompress:
            cmd = 'gzip -f "%s"' % problem_sql_path
            print cmd
            if (os.system(cmd) != 0):
                print "GZIP FAILED"
                sys.exit(1)

            if os.path.isfile(final_problem_sql_path):
                print "Removing previous uncompressed version %s" % final_problem_sql_path
                os.remove(final_problem_sql_path)

            final_problem_sql_path += ".gz"
            problem_sql_path += ".gz"

        print "Move %s => %s" % (problem_sql_path, final_problem_sql_path)
        shutil.move(problem_sql_path, final_problem_sql_path)
