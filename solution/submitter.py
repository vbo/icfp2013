import db
import api

api.request_delay = 5

class Submitter:
    def __init__(self, problem):
        sql = "SELECT inputs from program WHERE size = %s"
        cur = db.query(sql, (problem['size'], ))
        inputs = cur.fetchone()[0]
        operators = list(problem["operators"])
        operators.sort()
        operators = "_".join(operators)
        print operators
        print problem['size']
        result = api.eval(map(lambda x: '0x' + x, inputs.split('|')), problem['id'])
        if result['status'] != 'ok':
            raise Exception('Eval error')
        outputs = "|".join(map(lambda x: "%016x" % int(x, base=16), result['outputs']))
        sql = "SELECT code FROM program WHERE size=%s AND operators=%s AND outputs=%s";
        variants = [row[0] for row in db.query(sql, (problem['size'], operators, outputs))]
        for i, variant in enumerate(variants):
            res = api.guess(problem['id'], variant)
            if res['status'] == 'win':
                print "solved from %d variants. %d guesses used. " % (len(variants), i + 1)
                print "answer is: ", variant
                return

        print "not solved"
        print outputs
        print "variants", variants
        print "expected", problem['challenge']

problem = api.train(6)
submitter = Submitter(problem)
