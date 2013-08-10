import argparse

from . import build_formula_index
from ..lang.int64 import generate_inputs
from .. import solver
from .. import problems

parser = argparse.ArgumentParser()

parser.add_argument("index_basedir")
parser.add_argument("--ninputs", type=int, dest='ninputs', default=256)
parser.add_argument("--dry-run", action='store_true', dest='dry_run')
parser.add_argument("--offset", type=int, dest='offset', default=0)
parser.add_argument("--limit", type=int, dest='limit', default=1)
parser.add_argument("--parallel", action='store_true', dest='parallelize')
args = parser.parse_args()

if not args.dry_run:
    from .. import db

index = build_formula_index.TreeTemplatesIndex(args.index_basedir)
inputs = list(generate_inputs(args.ninputs))
offset = args.offset
limit = args.limit
problems_without_dupes = list(problems.get_problems_without_dupes())

cnt = 0
for problem_conf in problems_without_dupes[offset:offset + limit]:
    for data in index.generate_formulas(problem_conf["size"], allowed_ops=problem_conf["operators"]):
        cnt += 1

        outputs = list(solver.solve(data["s"], inputs, parallelize=args.parallelize))

        db_inputs = "|".join(map(lambda x: ("%016x" % int(str(x), base=16)), inputs))
        db_outputs = "|".join(map(lambda x: "%016x" % int(hex(x).rstrip("L"), base=16), outputs))
        operators = list(data["ops"])
        operators.sort()
        operators = "_".join(operators)
        assert len(db_outputs)

        query = (
            "INSERT INTO program"
            "(size, operators, code, inputs, outputs)"
            "VALUES (%s, '%s', '%s', '%s', '%s');" %
            (data["size"], operators, data["s"], db_inputs, db_outputs)
        )

        if not args.dry_run:
            db.query(query)
        else:
            print query

if not args.dry_run:
    print cnt
