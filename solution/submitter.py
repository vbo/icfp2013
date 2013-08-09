import db
import api
from problems import original_problems

api.request_delay = 3

def submit(problem):
    operators = list(problem["operators"])
    operators.sort()
    operators = "_".join(operators)
    print operators
    print problem['size']

    sql = "SELECT inputs from program WHERE size = %s and operators = %s"
    cur = db.query(sql, (problem['size'], operators))
    inputs = cur.fetchone()[0]
    if not inputs:
        raise Exception('There is no data in DB about this problem')

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
    #print "expected", problem['challenge']

if __name__ == '__main__':
    #problem = api.train(6)
    #submit(problem)
    #exit()
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

