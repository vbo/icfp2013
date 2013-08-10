from random import randint


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


def generate_inputs(ninputs):
    yield Int64.ZERO
    yield Int64.ONE

    for a in range(ninputs - 2):
        yield Int64.random()
