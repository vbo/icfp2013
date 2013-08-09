def fold(e0, e1, lambda_):
    return reduce(lambda_, e0, e1)

def if0(e0, e1, e2):
    return e1 if e0 else e2
