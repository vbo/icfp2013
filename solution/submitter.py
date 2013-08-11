import re
import time
import argparse
from itertools import izip

from . import api
from . import solver
from . import util
from .problems import original_problems


MAX_ALLOWED_SECONDS_PER_TASK = 310
api.request_delay = 1
use_output_index_only = True
poll_delay = 5

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

def load_inputs_from_index(size, operators, use_output_index_only=True):
    from . import db

    operators = "_".join(operators)
    if use_output_index_only:
        inputs_hash = 'cba118200cc674d696b08940b17a5301'
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
    from . import db

    operators = "_".join(operators)
    if use_output_index_only:
        sql = "SELECT DISTINCT code, id FROM program WHERE inputs=%s AND outputs=%s ORDER BY id"
        params = [inputs_hash, outputs_hash]
        variants = (row[0] for row in db.query(sql, tuple(params)))
    else:
        sql = "SELECT distinct code FROM program WHERE size=%s AND operators=%s AND inputs=%s AND outputs=%s"
        variants = (row[0] for row in db.query(sql, (size, operators, inputs_hash, outputs_hash)))
    return variants


def submit(problem, poll_storage=True, cond=None):


    operators = list(problem["operators"])
    operators.sort()
    inputs, inputs_hash = load_inputs_from_index(problem["size"], operators)

    submit_time = time.time()
    result = api.eval(inputs, problem['id'])
    if result['status'] != 'ok':
        print 'Eval error: ' + result["message"]
        return

    readable_outputs = result['outputs']
    outputs_hash = util.get_int64_array_hash(map(lambda x: long(int(x, base=16)), readable_outputs))

    guesses_used = 0
    new_inputs = []
    new_outputs = []
    comforming_variants = []
    is_first_iteration = True
    variants_tried = 0

    while True:
        variants = load_variants_from_index(problem['size'], operators, inputs_hash, outputs_hash)

        for variant in variants:
            variants_tried += 1

            if not is_program_conform_to_data(variant, new_inputs, new_outputs):
                continue
            comforming_variants.append(variant)
            guesses_used += 1
            res = api.guess(problem['id'], variant)
            if res['status'] == 'win':
                print "solved from (at least) %d variants. %d guesses used. " % (variants_tried, guesses_used)
                print "answer is: ", variant
            elif res['status'] == 'error':
                print "error returned:", res.get('message')
            else:
                #mismatch
                new_input, new_output, _my_bad_output = map(lambda x: int(x, base=16), res['values'])
                new_inputs.append(new_input)
                new_outputs.append(new_output)

        if not poll_storage:
            raise NotSolvedError("All variants failed! Guesses used: %d" % (guesses_used,), inputs, readable_outputs, comforming_variants)

        time_since_start = time.time() - submit_time
        if time_since_start > MAX_ALLOWED_SECONDS_PER_TASK:
            print 'We assume that task timed out. Giving up!'
            break
        else:
            if cond is not None and is_first_iteration:
                cond.notify()
                cond.release()

            is_first_iteration = False

            print "Not solvable after %s variants. Polling db for new knowledge" % (variants_tried)
            time.sleep(poll_delay)


def try_train():
    win = 0
    lose = 0
    while True:
        try:
            problem = api.train(11)
            problem = {u'challenge': u'(lambda (x_78425) (fold (shl1 x_78425) (not x_78425) (lambda (x_78426 x_78427) (if0 (shr4 (xor (shr16 x_78427) (plus (xor (xor (xor (shl1 (or (plus x_78426 (shr4 x_78427)) (shr16 x_78426))) x_78427) x_78427) x_78426) x_78427))) x_78426 x_78427))))', u'operators': [u'fold', u'if0', u'not', u'or', u'plus', u'shl1', u'shr16', u'shr4', u'xor'], u'id': u'FDDPUrzVIiCwpeM8k9iPcYHj', u'size': 30}
            print "We will solve problem:", problem
            submit(problem)
            win += 1
        except NotSolvedError as e:
            lose += 1
            print e
        print "win: %d from %d. lose: %d" % (win, win + lose, lose)


def submit_many(sizes=None, id=None, interactive=False, poll_storage=True):
    problems = None
    sizes = None

    if args.id:
        problems = [p for p in original_problems if p['id'] == args.id]
    elif args.interactive:
        sizes = map(int, raw_input().split(" "))
    else:
        sizes = map(int, args.sizes.split(","))

    if problems is None:
        problems = [p for p in original_problems if p['size'] in sizes]

    for problem in problems:
        submit_in_sandbox(problem, poll_storage=poll_storage)

    if args.interactive:
        print 'want another one?'
        raw_input()


def submit_in_sandbox(problem, poll_storage=True, cond=None):
    try:
        if cond is not None:
            cond.acquire()
        print "Solving %s[size=%s]" % (problem['id'], problem['size'])
        submit(problem, poll_storage=poll_storage, cond=cond)
    except NotSolvedError as e:
        print "not solved"
        print e.outputs
        print "variants", e.variants
        #print "expected", problem['challenge']
    except api.AlreadySolvedException as e:
        print 'was already solved'
        if cond:
            cond.notify()
    except api.RequestError as e:
        print 'Request error:', e
    except api.TaskGoneError as e:
        print "it's gone =("
    finally:
        if cond is not None:
            cond.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--prod", action='store_true')
    parser.add_argument("-i", '--interactive', action='store_true')
    parser.add_argument("--id", default=None, type=str)
    parser.add_argument("--sizes", default=None, type=str)

    args = parser.parse_args()

    if not args.prod:
        try_train()

    else:
        try:
            submit_many(args.sizes, args.id, args.interactive, False)
        except api.TaskGoneError:
            print "gone =("
