from int64 import Int64 


def not_(x):
    return Int64(~x & 0xFFFFFFFFFFFFFFFF)

def and_(x, y):
    return Int64(x & y)

def or_(x, y):
    return Int64(x | y)

def xor(x, y):
    return Int64(x ^ y)

def plus(x, y):
    return Int64((x + y) & 0xFFFFFFFFFFFFFFFF)

def shl1(x):
    return Int64(x << 1 & 0xFFFFFFFFFFFFFFFF)

def shr1(x):
    return Int64(x >> 1)

def shr4(x):
    return Int64(x >> 4)

def shr16(x):
    return Int64(x >> 16)


renames = {
    "not": not_,
    "and": and_,
    "or": or_,
}

