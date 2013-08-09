import itertools

from ..operators import Operators


class TreeVar(int):

    def __repr__(self):
        return 'T(%d)' % self

    def __str__(self):
        return 'T(%d)' % self


class TreeLevelTemplate(object):

    def __init__(self, size, operator, treevars=None):
        self.operator = operator

        if treevars is None and self.operator != Operators.TERMINAL:
            raise ValueError('treevars may be null only with TERMINAL nodes')
        else:
            self.treevars = (treevars if isinstance(treevars, tuple) else
                             (treevars,) if isinstance(treevars, TreeVar) else
                             tuple(treevars) if treevars is not None else
                             None)
        self.size = size

    def __repr__(self):
        return (
            'Tree(%d): %s' % (self.size, (self.operator,) + self.treevars)
            if self.operator != Operators.TERMINAL
            else 'T(%d)' % self.size
        )

    def __hash__(self):
        return hash((TreeLevelTemplate, self.operator, self.treevars))


class TemplatedProgramTreeNode(object):

    def __init__(self, operator, args=None, size=None):
        self.operator = operator
        self.has_fold = operator == Operators.FOLD \
                        or ((args is not None) and any(a.has_fold for a in args))

        self.could_contain_fold_ids = False

        if args is not None:
            self.args = tuple(args)
        elif operator != Operators.TERMINAL:
            raise ValueError('args may be null only with TERMINAL nodes')
        else:
            self.args = None

        if operator == Operators.FOLD:
            self.traverse(self.set_fold_property_to_terminals)
            self.args[2].traverse(self.set_could_contain_fold_ids)

        self.size = size

    def values(self):
        if self.operator == Operators.TERMINAL:
            for terminal in Operators.TERMINALS:
                yield {'s': terminal, 'ops': []}
            if self.could_contain_fold_ids:
                yield {'s': Operators.ID2, 'ops': []}
                yield {'s': Operators.ID3, 'ops': []}
        elif self.operator == Operators.OP1:
            for op in Operators.UNARY:
                for value in self.args[0].values():
                    yield {
                        's': "(%s %s)" % (op, value['s']),
                        'ops': value['ops'] + [op]
                    }
        elif self.operator == Operators.OP2:
            for op in Operators.BINARY:
                for value in self.args[0].values():
                    for value2 in self.args[1].values():
                        yield {
                            's': "(%s %s %s)" % (op, value['s'], value2['s']),
                            'ops': value['ops'] + value2['ops'] + [op]
                        }
        elif self.operator == Operators.IF0:
            for value in self.args[0].values():
                for value2 in self.args[1].values():
                    for value3 in self.args[2].values():
                        yield {
                            's': "(if0 %s %s %s)" % (value['s'], value2['s'], value3['s']),
                            'ops': value['ops'] + value2['ops'] + value3['ops'] + ['if0']
                        }
        elif self.operator == Operators.FOLD:
            for value in self.args[0].values():
                for value2 in self.args[1].values():
                    for value3 in self.args[2].values():
                        yield {
                            's': "(fold %s %s (lambda (%s %s) %s))" % (
                                value['s'], value2['s'], Operators.ID2, Operators.ID3, value3['s']),
                            'ops': value['ops'] + value2['ops'] + value3['ops'] + ['fold']
                        }

    def __repr__(self):
        if self.operator != Operators.TERMINAL:
            return repr((self.operator,) + self.args)
        else:
            return repr(self.operator)

    def set_fold_property_to_terminals(self, node):
        if node.operator == Operators.TERMINAL:
            node.has_fold = True

    def set_could_contain_fold_ids(self, node):
        if node.operator == Operators.TERMINAL:
            node.could_contain_fold_ids = True

    def traverse(self, func):
        if self.args is None:
            return

        for arg in self.args:
            func(arg)
            arg.traverse(func)


def get_tree_templates(size):

    if size == 1:
        yield TreeLevelTemplate(size, Operators.TERMINAL)
        return

    yield TreeLevelTemplate(size, Operators.OP1, TreeVar(size - 1))

    for i in range(1, (size + 1) // 2):
        yield TreeLevelTemplate(size, Operators.OP2, (TreeVar(i), TreeVar(size - 1 - i)))

    if0_limit = size - 1

    for i in range(1, if0_limit - 1):
        for j in range(i + 1, if0_limit):
            yield TreeLevelTemplate(size, Operators.IF0, (TreeVar(i), TreeVar(j - i), TreeVar(if0_limit - j)))

    fold_limit = size - 2

    for i in range(1, fold_limit - 1):
        for j in range(i + 1, fold_limit):
            yield TreeLevelTemplate(size, Operators.FOLD, (TreeVar(i), TreeVar(j - i), TreeVar(fold_limit - j)))


def make_tree_index(size, tree_indexes):
    '''
    Use carefully:

    >>> idxs = {}
    >>> for n in range(1, 19): idxs[n] = list(make_tree_index(n, idxs))
    >>> [len(idxs[n]) for n in sorted(idxs.keys())]
    [1,
    1,
    2,
    4,
    11,
    20,
    51,
    125,
    342,
    875,
    2303,
    5846,
    15335,
    40089,
    107671,
    287163,
    774628,
    2073501]
    '''

    if size == 1:
        for t in get_tree_templates(size):
            yield TemplatedProgramTreeNode(t.operator, size=size)
        return

    if size - 1 not in tree_indexes:
        raise ValueError('Cannot build index for size %d without indexes for sizes 1..%d' % (size, size - 1))

    for tree_template in get_tree_templates(size):
        indexes = map(tree_indexes.get, tree_template.treevars)

        for subtrees_combination in itertools.product(*indexes):

            # NOTE Heuristic: Skip combination if it includes more than one FOLD
            numfolds = sum(map(lambda tree: int(tree.has_fold), subtrees_combination))
            if numfolds > 1 or numfolds == 1 and tree_template.operator == Operators.FOLD:
                continue

            yield TemplatedProgramTreeNode(tree_template.operator, args=subtrees_combination, size=size)

def get_index_size(size):
    idxs = {}
    for n in range(1, size):
        idxs[n] = list(make_tree_index(n, idxs))
    return idxs

def get_formulas_from_index(size):
    idxs = get_index_size(size)
    for level in idxs:
        idx = idxs[level]
        for template in idx:
            for formula in template.values():
                formula['ops'] = set(formula['ops'])
                if formula['s'][:5] == '(fold':
                    formula['ops'] = set(['tfold']) - set(['fold'])
                formula['s'] = '(lambda (' + Operators.ID + ') ' + formula['s'] + ')'
                formula['size'] = level + 1
                if (formula['size'] == size):
                    yield formula
