import argparse
import time

from . import build_formula_index
from ..lang.int64 import generate_inputs, Int64
from .. import solver

parser = argparse.ArgumentParser()

parser.add_argument("index_basedir")
parser.add_argument("size", type=int)
parser.add_argument("--inputs", type=int, dest='ninputs', default=256)
parser.add_argument("--dry-run", action='store_true', dest='dry_run')
args = parser.parse_args()

if not args.dry_run:
    from .. import db

index = build_formula_index.TreeTemplatesIndex(args.index_basedir)

size = args.size

inputs = list(generate_inputs(args.ninputs))

cnt = 0

for data in index.generate_formulas(size):
    cnt += 1

    outputs = list(solver.solve(data["s"], inputs))

    db_inputs = "|".join(map(lambda x: ("%016x" % int(str(x), base=16)), inputs))
    db_outputs = "|".join(map(lambda x: "%016x" % int(hex(x).rstrip("L"), base=16), outputs))
    operators = list(data["ops"])
    operators.sort()
    operators = "_".join(operators)
    assert len(outputs)

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
