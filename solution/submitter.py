from itertools import izip

from . import db
from . import api
from . import solver
from . import util
from .problems import original_problems


api.request_delay = 3

class NotSolvedError(BaseException):
    def __init__(self, outputs, variants):
        super(BaseException, self).__init__()
        self.outputs = outputs
        self.variants = variants

class IndexNotFoundError(Exception):
    pass


def is_program_conform_to_data(program_text, inputs, outputs):
    for ideal_out, our_out in izip(outputs, solver.solve(program_text, inputs)):
        if ideal_out != our_out:
            return False
    return True

def load_inputs_from_index(size, operators):
    operators = "_".join(operators)
    inputs_hash = db.fetchone(
        "SELECT inputs from program WHERE size = %s and operators = %s",
        (size, operators))
    if not inputs_hash:
        raise IndexNotFoundError('There is no data in DB about this problem')
    serialized = db.fetchone(
        "SELECT inputs FROM inputs WHERE inputs_hash = %s",
        (inputs_hash,))
    if not serialized:
        raise IndexNotFoundError('There is no data in DB about this problem')
    return serialized.split('|'), inputs_hash

def load_variants_from_index(size, operators, inputs_hash, outputs_hash):
    operators = "_".join(operators)
    sql = "SELECT distinct code FROM program WHERE size=%s AND operators=%s AND inputs=%s AND outputs=%s"
    variants = [row[0] for row in db.query(sql, (size, operators, inputs_hash, outputs_hash))]
    print variants
    return variants

def submit(problem):
    operators = list(problem["operators"])
    operators.sort()
    inputs, inputs_hash = load_inputs_from_index(problem["size"], operators)

    result = api.eval(map(lambda x: '0x' + x, inputs), problem['id'])
    if result['status'] != 'ok':
        raise Exception('Eval error')

    readable_outputs = result['outputs']
    outputs_hash = util.get_int64_array_hash(map(lambda x: long(int(x, base=16)), readable_outputs))
    variants = load_variants_from_index(problem['size'], operators, inputs_hash, outputs_hash)

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
    raise NotSolvedError(readable_outputs, variants)


if __name__ == '__main__':
    if True:
        problem = api.train(6)
        submit(problem)
    else:
        group_id = int(raw_input())
        for problem in filter(lambda x: x['group_id'] == group_id, original_problems):
            try:
                submit(problem)
            except NotSolvedError as e:
                print "not solved"
                print e.outputs
                print "variants", e.variants
                #print "expected", problem['challenge']
            except api.AlreadySolvedException as e:
                print 'solved'
                pass
            print 'want another one?'
            raw_input()

