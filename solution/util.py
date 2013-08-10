import hashlib


def get_int64_array_hash(numbers):
    keystr = "|".join(map(hex, numbers))
    return hashlib.md5(keystr).hexdigest()
