class Int64(long):

    def __init__(self, x):
        x %= 2 ** 64
        super(Int64, self).__init__(x)

    def __iter__(self):
        me = self
        for a in range(8):
            d = 2 ** 8
            yield me % d
            me >>= 8


def e_fold(e0, e1, lambda_):
    return reduce(lambda_, e0, e1)
