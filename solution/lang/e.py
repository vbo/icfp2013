def fold(e0, e1, lambda_):
    return reduce2(lambda_, e0, e1)

def if0(e0, e1, e2):
    return e1 if e0 == 0 else e2

def reduce2(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        try:
            initializer = next(it)
        except StopIteration:
            raise TypeError('reduce() of empty sequence with no initial value')
    accum_value = initializer
    for x in it:
        accum_value = function(accum_value, x)
    return accum_value
