from random import randint


class Int64(long):

    max = 18446744073709551615

    def __init__(self, x):
        if x > 0xFFFFFFFFFFFFFFFF:
            raise Exception('Input too large: %s' % x)
        x %= 2 ** 64
        super(Int64, self).__init__(x)

    def __iter__(self):
        me = self
        for a in range(8):
            d = 2 ** 8
            yield Int64(me % d)
            me >>= 8

    @classmethod
    def random(cls):
        return cls(randint(0, cls.max))


def generate_inputs(ninputs):
    for a in range(ninputs):
        r = Int64.random()
        rstr = str(hex(r)).rstrip("L")
        yield rstr
