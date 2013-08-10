from itertools import izip

from . import db
from . import api
from . import solver
from .problems import original_problems


api.request_delay = 3

def get_int64_array_hash(numbers):
    import hashlib
    keystr = "|".join(map(hex, numbers))
    return hashlib.md5(keystr).hexdigest()


def fetchone(query, params=None):
    cur = db.query(query, params)
    return cur.fetchone()[0]


def is_program_conform_to_data(program_text, inputs, outputs):
    for ideal_out, our_out in izip(outputs, solver.solve(program_text, inputs)):
        if ideal_out != our_out:
            return False
    return True


def submit(problem):
    operators = list(problem["operators"])
    operators.sort()
    operators = "_".join(operators)
    print operators
    print problem['size']

    inputs_hash = fetchone(
        "SELECT inputs from program WHERE size = %s and operators = %s",
         (problem['size'], operators))

    if not inputs_hash:
        raise Exception('There is no data in DB about this problem')

    inputs_readable = fetchone(
        "SELECT inputs FROM inputs WHERE inputs_hash = %s",
        (inputs_hash,))

    if not inputs_hash:
        raise Exception('There is no data in DB about this problem')

    result = api.eval(map(lambda x: '0x' + x, inputs_readable.split('|')), problem['id'])
    if result['status'] != 'ok':
        raise Exception('Eval error')

    readable_outputs = result['outputs']
    outputs_hash = get_int64_array_hash(map(lambda x: int(x, base=16), readable_outputs))

    sql = "SELECT code FROM program WHERE size=%s AND operators=%s AND inputs=%s AND outputs=%s";
    variants = [row[0] for row in db.query(sql, (problem['size'], operators, inputs_hash, outputs_hash))]

    new_inputs = []
    new_outputs = []

    for i, variant in enumerate(variants):

        if not is_program_conform_to_data(variant, new_inputs, new_outputs):
            print "skipping variant because it doesn't work on new data"
            continue

        res = api.guess(problem['id'], variant)
        if res['status'] == 'win':
            print "solved from %d variants. %d guesses used. " % (len(variants), i + 1)
            print "answer is: ", variant
            return
        elif res['status'] == 'error':
            print "error returned:", res.get('message')
        else:
            #mismatch
            new_input, new_output, _my_bad_output = map(lambda x: int(x, base=16), res['values'])
            new_inputs.append(new_input)
            new_outputs.append(new_output)


    print "not solved"
    print readable_outputs
    print "variants", variants
    #print "expected", problem['challenge']

if __name__ == '__main__':
    problem = api.train(6)
    submit(problem)
    import sys
    sys.exit()
    #if 0:
    group_id = int(raw_input())
    for problem in filter(lambda x: x['group_id'] == group_id, original_problems):
        try:
            submit(problem)
        except api.AlreadySolvedException as e:
            print 'solved'
            pass
        print 'want another one?'
        raw_input()

