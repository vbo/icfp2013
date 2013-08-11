import argparse
import itertools
from multiprocessing import Process, Condition

from solution.submitter import submit
from solution.problems import original_problems
from solution import api


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--sizes", default=None, type=str)
    parser.add_argument("--train-amount", default=5, type=int, dest='train_amount')
    parser.add_argument("--train", action='store_true')

    args = parser.parse_args()

    sizes = map(int, args.sizes.split(",")) if args.sizes else None

    if args.train:
        if sizes:
            problems_to_solve = itertools.islice(itertools.imap(api.train, itertools.cycle(sizes)), args.train_amount)
        else:
            problems_to_solve = (api.train(6) for i in range(args.train_amount))
    else:
        if sizes:
            problems_to_solve = filter(lambda p: p['size'] in sizes, original_problems)
        else:
            problems_to_solve = original_problems

    cond = Condition()

    for problem in problems_to_solve:
        slave = Process(target=submit, args=(problem, True, cond))
        slave.start()
        # Give at least 3 seconds to solve a problem
        slave.join(timeout=3)

        if slave.is_alive():
            print "MASTER: waiting for process to exhaust its variants."
            cond.acquire()
            cond.wait(300)
            cond.release()
            print "MASTER: worker tried hard but no success so far. Letting him stay for a while."
