def not_(x):
    return ~x & 0xFFFFFFFFFFFFFFFF

def and_(x, y):
    return x & y

def or_(x, y):
    return x | y

def xor(x, y):
    return x ^ y

def plus(x, y):
    return (x + y) & 0xFFFFFFFFFFFFFFFF

def shl1(x):
    return x << 1 & 0xFFFFFFFFFFFFFFFF

def shr1(x):
    return x >> 1

def shr4(x):
    return x >> 4

def shr16(x):
    return x >> 16

