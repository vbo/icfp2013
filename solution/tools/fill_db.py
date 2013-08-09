import psycopg2
import build_formula_index
from ..lang.int64 import generate_inputs, Int64
from .. import solver


#a = '''"{"(lambda (id) (shr4 (shr1 (shr1 (shr16 0)))))","(lambda (id) (shr4 (shr16 (shr16 (shr1 1)))))","(lambda (id) (shr1 (shr16 (shr4 (shr1 1)))))","(lambda (id) (shr1 (shr1 (shr16 (shr4 1)))))","(lambda (id) (shr1 (shr1 (shr16 (shr4 0)))))","(lambda (id) (shr4 (shr16 (shr16 (shr1 0)))))","(lambda (id) (shr4 (shr16 (shr1 (shr4 1)))))","(lambda (id) (shr4 (shr16 (shr1 (shr4 0)))))","(lambda (id) (shr1 (shr16 (shr4 (shr16 1)))))","(lambda (id) (shr1 (shr4 (shr16 (shr1 0)))))","(lambda (id) (shr4 (shr16 (shr1 (shr16 1)))))","(lambda (id) (shr4 (shr16 (shr1 (shr16 0)))))","(lambda (id) (shr1 (shr4 (shr16 (shr1 1)))))","(lambda (id) (shr16 (shr16 (shr4 (shr1 0)))))","(lambda (id) (shr4 (shr1 (shr16 (shr4 1)))))","(lambda (id) (shr1 (shr4 (shr16 (shr16 0)))))","(lambda (id) (shr1 (shr4 (shr16 (shr16 1)))))","(lambda (id) (shr4 (shr16 (shr1 (shr1 1)))))","(lambda (id) (shr4 (shr1 (shr16 (shr4 0)))))","(lambda (id) (shr4 (shr4 (shr16 (shr1 1)))))","(lambda (id) (shr1 (shr4 (shr16 (shr4 0)))))","(lambda (id) (shr1 (shr16 (shr16 (shr4 1)))))","(lambda (id) (shr1 (shr4 (shr16 (shr4 1)))))","(lambda (id) (shr4 (shr1 (shr16 (shr16 1)))))","(lambda (id) (shr4 (shr16 (shr1 (shr1 0)))))","(lambda (id) (shr16 (shr4 (shr1 (shr16 1)))))","(lambda (id) (shr16 (shr4 (shr1 (shr4 0)))))","(lambda (id) (shr16 (shr4 (shr1 (shr4 1)))))","(lambda (id) (shr4 (shr4 (shr1 (shr16 0)))))","(lambda (id) (shr16 (shr4 (shr1 (shr16 0)))))","(lambda (id) (shr16 (shr4 (shr1 (shr1 1)))))","(lambda (id) (shr16 (shr4 (shr16 (shr1 0)))))","(lambda (id) (shr16 (shr4 (shr1 (shr1 0)))))","(lambda (id) (shr4 (shr4 (shr1 (shr16 1)))))","(lambda (id) (shr16 (shr4 (shr16 (shr1 1)))))","(lambda (id) (shr4 (shr1 (shr16 (shr16 0)))))","(lambda (id) (shr4 (shr1 (shr16 (shr1 1)))))","(lambda (id) (shr4 (shr1 (shr16 (shr1 0)))))","(lambda (id) (shr16 (shr4 (shr4 (shr1 0)))))","(lambda (id) (shr16 (shr4 (shr4 (shr1 1)))))","(lambda (id) (shr1 (shr16 (shr16 (shr4 0)))))","(lambda (id) (shr16 (shr16 (shr4 (shr1 1)))))","(lambda (id) (shr1 (shr16 (shr4 (shr4 1)))))","(lambda (id) (shr16 (shr1 (shr16 (shr4 1)))))","(lambda (id) (shr16 (shr16 (shr1 (shr4 0)))))","(lambda (id) (shr16 (shr1 (shr16 (shr4 0)))))","(lambda (id) (shr1 (shr16 (shr1 (shr4 0)))))","(lambda (id) (shr4 (shr1 (shr4 (shr16 1)))))","(lambda (id) (shr16 (shr1 (shr4 (shr4 0)))))","(lambda (id) (shr16 (shr1 (shr4 (shr1 1)))))","(lambda (id) (shr1 (shr16 (shr1 (shr4 1)))))","(lambda (id) (shr16 (shr1 (shr4 (shr4 1)))))","(lambda (id) (shr1 (shr1 (shr4 (shr16 1)))))","(lambda (id) (shr16 (shr1 (shr4 (shr16 0)))))","(lambda (id) (shr16 (shr1 (shr4 (shr16 1)))))","(lambda (id) (shr16 (shr1 (shr1 (shr4 1)))))","(lambda (id) (shr1 (shr4 (shr1 (shr16 0)))))","(lambda (id) (shr1 (shr4 (shr1 (shr16 1)))))","(lambda (id) (shr4 (shr1 (shr4 (shr16 0)))))","(lambda (id) (shr1 (shr4 (shr4 (shr16 0)))))","(lambda (id) (shr1 (shr1 (shr4 (shr16 0)))))","(lambda (id) (shr4 (shr16 (shr4 (shr1 1)))))","(lambda (id) (shr16 (shr1 (shr1 (shr4 0)))))","(lambda (id) (shr1 (shr16 (shr4 (shr4 0)))))","(lambda (id) (shr16 (shr16 (shr1 (shr4 1)))))","(lambda (id) (shr4 (shr4 (shr16 (shr1 0)))))","(lambda (id) (shr4 (shr16 (shr4 (shr1 0)))))","(lambda (id) (shr1 (shr4 (shr4 (shr16 1)))))","(lambda (id) (shr16 (shr1 (shr4 (shr1 0)))))","(lambda (id) (shr4 (shr1 (shr1 (shr16 1)))))","(lambda (id) (shr1 (shr16 (shr4 (shr1 0)))))","(lambda (id) (shr1 (shr16 (shr4 (shr16 0)))))"}"'''
#for x in a.split(','):
#    print x
#exit()
inputs = list(generate_inputs())

db = psycopg2.connect("dbname=icfp2013_01 user=vbo")
cur = db.cursor()
cnt = 0
for data in build_formula_index.get_formulas_from_index(5):
    cnt += 1
    outputs = list(solver.solve(data["s"], inputs))
    db_inputs = "|".join(map(lambda x: ("%016x" % int(str(x), base=16)), inputs))
    db_outputs = "|".join(map(lambda x: "%016x" % int(hex(x).rstrip("L"), base=16), outputs))
    operators = list(data["ops"])
    operators.sort()
    operators = "_".join(operators)
    assert len(outputs)
    cur.execute(
        "INSERT INTO program"
        "(size, operators, code, inputs, outputs)"
        "VALUES (%s, %s, %s, %s, %s)",
        (data["size"], operators, data["s"], db_inputs, db_outputs)
    )
    #for row in cur.fetchall():
    #    print row
db.commit()
print cnt



