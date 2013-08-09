class Int64(long):

    def __init__(self, x):
        if x > 0xFFFFFFFFFFFFFFFF:
            raise Exception('Input too large') 
        x %= 2 ** 64
        super(Int64, self).__init__(x)

    def __iter__(self):
        me = self
        for a in range(8):
            d = 2 ** 8
            yield me % d
            me >>= 8
