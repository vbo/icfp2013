import argparse
import itertools
from multiprocessing import Process, Condition, active_children

from solution import submitter
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
        slave = Process(target=submitter.submit_in_sandbox, args=(problem, True, cond))
        cond.acquire()
        slave.start()

        print "MASTER: waiting for process to exhaust its variants."
        cond.wait(300)
        cond.release()

        if slave.is_alive():
            print "MASTER: worker tried hard but no success so far. Letting him stay for a while."

    while active_children():
        children = active_children()
        print "PROCESSES LEFT:", children
        for c in children:
            c.join(timeout=60)
