import os
import fileinput
from re import sub, search
from solution.problems import original_problems

if __name__ == '__main__':
    folder = raw_input()
    os.chdir(folder)
    for f in os.listdir("."):
        if f.startswith("problem."):
            group_id = int(search(r'problem\.(\d+).*', f).group(1))
            print group_id
            ops = filter(lambda x: x['group_id'] == group_id, original_problems)
            if len(ops) == 0:
                continue
            ops = ops[0]['operators']
            ops.sort()
            operators = "_".join(ops)
            name = folder + '/' + f
            for i, line in enumerate(fileinput.input(name, inplace=True)):
                if i == 0:
                    print line
                else:
                    print sub(r"(^.*?')[1234567890a-z_]+('.*)$", r'\1' + operators + r'\2', line)
