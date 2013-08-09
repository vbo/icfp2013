from problems import original_problems
from operators import Operators

cnt = 0
for problem in original_problems:
    if problem["size"] < 8:
        continue
    ops = problem["operators"]
    if "if0" not in ops:
        continue
    cnt += 1
    print problem["id"], problem["operators"], problem["size"]
print cnt
