from random import randint
from random import seed as set_seed


class Int64(long):

    max = 0xFFFFFFFFFFFFFFFF

    def __init__(self, x):
        if x > Int64.max:
            raise Exception('Input too large: %s' % x)
        # NOTE: This is redundant because 2 ** 64 > Int64.max and if a > b then b % a = b.
        # x %= 2 ** 64
        super(Int64, self).__init__(x)

    def __iter__(self):
        me = self
        for a in range(8):
            yield Int64(me & 0xFF)
            me >>= 8

    @classmethod
    def random(cls):
        return cls(randint(0, cls.max))

    def as_hex(self):
        return str(hex(self)).rstrip("L")

Int64.ZERO = Int64(0)
Int64.ONE = Int64(1)
Int64.MAX = Int64(Int64.max)


def generate_inputs(ninputs, seed=None):
    yield Int64.ZERO
    yield Int64.ONE
    yield Int64.MAX

    if seed is not None:
        set_seed(seed)

    for a in range(ninputs - 3):
        yield Int64.random()

