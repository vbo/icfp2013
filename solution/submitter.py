from itertools import izip

from . import db
from . import api
from . import solver
from . import util
from .problems import original_problems


api.request_delay = 1
use_output_index_only = False

class NotSolvedError(BaseException):
    def __init__(self, message, inputs, outputs, variants):
        super(BaseException, self).__init__()
        self.message = message
        self.inputs = inputs
        self.outputs = outputs
        self.variants = variants

    def __str__(self):
        return self.message

class IndexNotFoundError(Exception):
    pass


def is_program_conform_to_data(program_text, inputs, outputs):
    for ideal_out, our_out in izip(outputs, solver.solve(program_text, inputs)):
        if ideal_out != our_out:
            return False
    return True

def get_variants_count(variants):
    return len(variants)

def load_inputs_from_index(size, operators):
    operators = "_".join(operators)
    if use_output_index_only:
        inputs_hash = db.fetchone(
            "SELECT inputs from program WHERE operators = '*'")
    else:
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
    return map(lambda x: '0x' + str(x), serialized.split('|')), inputs_hash

def load_variants_from_index(size, operators, inputs_hash, outputs_hash):
    operators = "_".join(operators)
    if use_output_index_only:
        sql = "SELECT distinct code FROM program WHERE inputs=%s AND outputs=%s"
        variants = [row[0] for row in db.query(sql, (inputs_hash, outputs_hash))]
    else:
        sql = "SELECT distinct code FROM program WHERE size=%s AND operators=%s AND inputs=%s AND outputs=%s"
        variants = [row[0] for row in db.query(sql, (size, operators, inputs_hash, outputs_hash))]
    return variants

def submit(problem):
    operators = list(problem["operators"])
    operators.sort()
    inputs, inputs_hash = load_inputs_from_index(problem["size"], operators)

    result = api.eval(inputs, problem['id'])
    if result['status'] != 'ok':
        raise Exception('Eval error: ' + result["message"])

    readable_outputs = result['outputs']
    outputs_hash = util.get_int64_array_hash(map(lambda x: long(int(x, base=16)), readable_outputs))
    variants = load_variants_from_index(problem['size'], operators, inputs_hash, outputs_hash, use_output_index_only)

    new_inputs = []
    new_outputs = []

    guesses_used = 0
    comforming_variants = []
    for variant in variants:
        print 'Variant:', variant
        comforming_variants.append(variant)
        if not is_program_conform_to_data(variant, new_inputs, new_outputs):
            print "skipping variant because it doesn't work on new data"
            continue
        guesses_used += 1
        res = api.guess(problem['id'], variant)
        if res['status'] == 'win':
            print "solved from %d variants. %d guesses used. " % (get_variants_count(variants), guesses_used)
            print "answer is: ", variant
            return
        elif res['status'] == 'error':
            print "error returned:", res.get('message')
        else:
            #mismatch
            new_input, new_output, _my_bad_output = map(lambda x: int(x, base=16), res['values'])
            new_inputs.append(new_input)
            new_outputs.append(new_output)
    raise NotSolvedError("All variants failed! Guesses used: %d" % (guesses_used,), inputs, readable_outputs, comforming_variants)


if __name__ == '__main__':
    if True:
        problem = api.train(6)
        use_output_index_only=True
        submit(problem)
    else:
        inp = str(raw_input())
        group_ids = map(int, inp.split(" "))
        for group_id in group_ids:
            print "filter for group=%s" % (group_id,)
            for problem in filter(lambda x: x['group_id'] == group_id, original_problems):
                try:
                    print "Solving %s[group=%s]" % (problem['id'], group_id)
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

