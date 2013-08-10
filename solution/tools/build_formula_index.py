import itertools
import os

from ..operators import Operators, get_templated_operators


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


class TemplateRenderingState(object):

    def __init__(self, contain_fold_ids, allowed_ops=None):
        self.contain_fold_ids = contain_fold_ids
        self.allowed_ops = set(allowed_ops) if allowed_ops is not None else Operators.ALL_OPS
        self.allowed_unary = Operators.UNARY & self.allowed_ops
        self.allowed_binary = Operators.BINARY & self.allowed_ops

        self.is_if0_allowed = Operators.IF0 in self.allowed_ops
        self.is_fold_allowed = Operators.FOLD in self.allowed_ops


class TemplatedProgramTreeNode(object):

    def __init__(self, operator, args=None, size=None):
        self.operator = operator
        self.has_fold = operator == Operators.FOLD \
                        or ((args is not None) and any(a.has_fold for a in args))

        if args is not None:
            self.args = tuple(args)
        elif operator != Operators.TERMINAL:
            raise ValueError('args may be null only with TERMINAL nodes')
        else:
            self.args = None

        self.size = size

    def render(self, contain_fold_ids, allowed_ops=None):
        return self._render(TemplateRenderingState(contain_fold_ids, allowed_ops))

    def _render(self, state):
        if self.operator == Operators.TERMINAL:

            for terminal in Operators.TERMINALS:
                yield {'operator': terminal, 'ops': []}

            if state.contain_fold_ids:
                yield {'operator': Operators.ID2, 'ops': []}
                yield {'operator': Operators.ID3, 'ops': []}

        elif self.operator == Operators.OP1:
            for value in self.args[0]._render(state):
                for op in state.allowed_unary:
                    yield {
                        'operator': op,
                        'args': (value,),
                        'ops': value['ops'] + [op],
                    }

        elif self.operator == Operators.OP2:
            for value in self.args[0]._render(state):
                for value2 in self.args[1]._render(state):
                    for op in state.allowed_binary:
                        yield {
                            'operator': op,
                            'args': (value, value2),
                            'ops': value['ops'] + value2['ops'] + [op]
                        }

        elif self.operator == Operators.IF0 and state.is_if0_allowed:
            op = Operators.IF0

            for value in self.args[0]._render(state):
                for value2 in self.args[1]._render(state):
                    for value3 in self.args[2]._render(state):
                        yield {
                            'operator': op,
                            'args': (value, value2, value3),
                            'ops': [op] + value['ops'] + value2['ops'] + value3['ops'],
                        }

        elif self.operator == Operators.FOLD and state.is_fold_allowed:
            if state.contain_fold_ids:
                raise ValueError('Two folds in same tree is a BUG: %s' % self)

            op = Operators.FOLD

            for value in self.args[0]._render(state):
                for value2 in self.args[1]._render(state):

                    state.contain_fold_ids = True
                    for value3 in self.args[2]._render(state):
                        yield {
                            'operator': op,
                            'args': (value, value2, value3),
                            'ops': [op] + value['ops'] + value2['ops'] + value3['ops'],
                        }

                    state.contain_fold_ids = False

    def __repr__(self):
        if self.operator != Operators.TERMINAL:
            return repr((self.operator,) + self.args)
        else:
            return repr(self.operator)

    def traverse(self, func):
        if self.args is None:
            return

        for arg in self.args:
            func(arg)
            arg.traverse(func)

    def serialize(self):
        simple_repr = {
            'operator': self.operator,
            'has_fold': self.has_fold,
            'args': [arg.serialize() for arg in self.args] if self.args is not None else None,
            'size': self.size,
        }

        return simple_repr

    @staticmethod
    def deserialize(data):
        return TemplatedProgramTreeNode.deserialize_from_simple_repr(eval(data))

    @staticmethod
    def deserialize_from_simple_repr(simple_repr):
        args = map(TemplatedProgramTreeNode.deserialize_from_simple_repr,
                   simple_repr['args']) \
               if simple_repr['args'] is not None else None

        tree = TemplatedProgramTreeNode(
            simple_repr['operator'],
            args,
            simple_repr['size'])
        tree.has_fold = simple_repr['has_fold']
        return tree


def get_tree_templates(size, allowed_ops=None):

    if size == 1:
        yield TreeLevelTemplate(size, Operators.TERMINAL)
        return

    if allowed_ops is None or Operators.OP1 in allowed_ops:
        yield TreeLevelTemplate(size, Operators.OP1, TreeVar(size - 1))

    # Since all binary operators are commutative, we don't need to generate half of possible combinations
    if allowed_ops is None or Operators.OP2 in allowed_ops:
        for i in range(1, (size + 1) // 2):
            yield TreeLevelTemplate(size, Operators.OP2, (TreeVar(i), TreeVar(size - 1 - i)))

    if allowed_ops is None or Operators.IF0 in allowed_ops:
        if0_limit = size - 1

        for i in range(1, if0_limit - 1):
            for j in range(i + 1, if0_limit):
                yield TreeLevelTemplate(size, Operators.IF0, (TreeVar(i), TreeVar(j - i), TreeVar(if0_limit - j)))

    if allowed_ops is None or Operators.FOLD in allowed_ops:
        fold_limit = size - 2

        for i in range(1, fold_limit - 1):
            for j in range(i + 1, fold_limit):
                yield TreeLevelTemplate(size, Operators.FOLD, (TreeVar(i), TreeVar(j - i), TreeVar(fold_limit - j)))


def expand_tree_templates(size, tree_indexes, allowed_ops=None):
    '''
    Use carefully:

    >>> idxs = {}
    >>> for n in range(1, 19): idxs[n] = list(expand_tree_templates(n, idxs))
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
        for t in get_tree_templates(size, allowed_ops):
            yield TemplatedProgramTreeNode(t.operator, size=size)
        return

    if size - 1 not in tree_indexes:
        raise ValueError('Cannot build index for size %d without indexes for sizes 1..%d' % (size, size - 1))

    for tree_template in get_tree_templates(size, allowed_ops=allowed_ops):
        indexes = map(tree_indexes.get, tree_template.treevars)

        for subtrees_combination in itertools.product(*indexes):

            # NOTE Heuristic: Skip combination if it includes more than one FOLD
            numfolds = sum(map(lambda tree: int(tree.has_fold), subtrees_combination))
            if numfolds > 1 or (numfolds == 1 and tree_template.operator == Operators.FOLD):
                continue

            yield TemplatedProgramTreeNode(tree_template.operator, args=subtrees_combination, size=size)

class TreeTemplatesIndex(object):

    def __init__(self, basedir, maxsize_to_keep_in_memory=16, allowed_ops=None):
        self.basedir = basedir

        if not os.path.isdir(basedir):
            os.makedirs(basedir)

        self.maxsize_to_keep_in_memory = maxsize_to_keep_in_memory
        self.inmemory_index = {}

        self.allowed_ops = set(allowed_ops) if allowed_ops is not None else None
        if allowed_ops is not None:
            self.allowed_ops_str = '_'.join(allowed_ops)

    def __contains__(self, size):
        return size in self.inmemory_index \
               or os.path.isfile(self.get_templates_filepath(size))

    def __getitem__(self, size):
        result = self.get(size)

        if result is None:
            raise IndexError("No index for size %d" % size)

    def get(self, size):
        if size in self.inmemory_index:
            return self.inmemory_index[size]

        if size <= self.maxsize_to_keep_in_memory:
            self.generate_templates(size)
            return self.inmemory_index[size]

        templates_file = self.get_templates_filepath(size)

        if os.path.isfile(templates_file):
            return itertools.imap(TemplatedProgramTreeNode.deserialize, open(templates_file, 'r'))

        return None

    def __setitem__(self, size, templates):
        if size <= self.maxsize_to_keep_in_memory:
            self.inmemory_index[size] = list(templates)
            return

        out_filename = self.get_templates_filepath(size)

        try:
            fp = open(out_filename, 'w')

            for t in templates:
                fp.write(repr(t.serialize()))
                fp.write('\n')
        except:
            if os.path.isfile(out_filename):
                os.remove(out_filename)
            raise
        finally:
            fp.close()

    def keys(self):
        return [
            int(template_entry.split('.')[1])
            for template_entry in os.listdir(self.basedir)
            if not template_entry.startswith('.')]

    def get_templates_filepath(self, size):
        if self.allowed_ops is None:
            filename = 'templates.%d.txt' % size
        else:
            filename = 'templates:%s.%d.txt' % (self.allowed_ops_str, size)
        return os.path.join(self.basedir, filename)

    def generate_templates(self, maxsize):
        for size in range(1, maxsize + 1):
            self[size] = expand_tree_templates(size, self, self.allowed_ops)

    def generate_missing_templates(self, maxsize):
        max_generated_level = max(self.keys() or [0])

        for size in range(max_generated_level + 1, maxsize + 1):
            print "GENERATING TEMPLATES FOR SIZE %d" % size
            self[size] = expand_tree_templates(size, self, self.allowed_ops)

    def generate_formulas(self, size, allowed_ops=None):

        templates_level = size - 1

        if allowed_ops is not None:
            allowed_ops = set(allowed_ops)

        if allowed_ops and Operators.TFOLD in allowed_ops:
            templates_level = templates_level - 3
            is_tfold = True
        else:
            is_tfold = False

        templates = self.get(templates_level)

        if templates is None:
            raise ValueError('Index for size %d was not built. You need to call index.generate_missing_templates(%d) first.' % (templates_level, templates_level))

        for template in templates:
            for formula in template.render(contain_fold_ids=is_tfold, allowed_ops=allowed_ops):
                ops = set(formula['ops'])


                if allowed_ops is not None:
                    if is_tfold:
                        ops.add(Operators.TFOLD)

                    # Do not yeld formula if it doesn't have ALL required operators
                    if ops.symmetric_difference(allowed_ops):
                        continue

                formula['ops'] = ops

                if is_tfold:
                    formula_str = '(lambda (%s) (fold %s 0 (lambda (%s %s) %s)))' % (
                        Operators.ID, Operators.ID, Operators.ID2, Operators.ID3, formula_to_string(formula))

                    formula = {
                        'operator': Operators.FOLD,
                        'ops': ops,
                        'args': (
                            {
                                'operator': Operators.ID,
                            },
                            {
                                'operator': Operators.ZERO,
                            },
                            {
                                'operator': Operators.ID2,
                            },
                            {
                                'operator': Operators.ID3,
                            },
                            formula,
                        ),
                    }
                else:
                    formula_str = '(lambda (%s) %s)' % (Operators.ID, formula_to_string(formula))

                formula['s'] = formula_str
                formula['size'] = size
                yield formula


class TreeIndexDispatcher(object):
    '''
    Distribution of problems grouped by allowed operators:
        (1, ('if0',)),
        (3, ('fold', 'if0', 'op2')),
        (5, ('op1',)),
        (6, ('op2',)),
        (7, ('fold', 'if0', 'op1')),
        (9, ('if0', 'op1')),
        (18, ('if0', 'op2')),
        (61, ('op1', 'op2')),
        (75, ('fold', 'op1', 'op2')),
        (288, ('fold', 'if0', 'op1', 'op2')),
        (698, ('if0', 'op1', 'op2'))
    '''
    existing_ops = [
        ('if0',),
        ('fold', 'if0', 'op2'),
        ('op1',),
        ('op2',),
        ('fold', 'if0', 'op1'),
        ('if0', 'op1'),
        ('if0', 'op2'),
        ('op1', 'op2'),
        ('fold', 'op1', 'op2'),
        #('fold', 'if0', 'op1', 'op2'),
        ('if0', 'op1', 'op2'),
    ]

    def __init__(self, basedir, maxsize_to_keep_in_memory=20):
        self.basedir = basedir
        self.maxsize_to_keep_in_memory = maxsize_to_keep_in_memory

        self.default_index = TreeTemplatesIndex(self.basedir, self.maxsize_to_keep_in_memory - 5)

        self.indexes = dict(
            (ops, TreeTemplatesIndex(self.basedir, self.maxsize_to_keep_in_memory, allowed_ops=ops))
             for ops in self.existing_ops)

    def get_index(self, allowed_ops):
        return self.default_index \
            if allowed_ops is None \
            else self.indexes.get(get_templated_operators(allowed_ops), self.default_index)


def formula_to_string(formula):
    '''
    :param formula:
        formula is a representation of \BV program with following attributes:
            "operator" - one of `Operators` fields, representing operator tag.
            "args" - tuple with subexpressions of the same form. Empty for terminals.
    :return:
        \BV program source code.
    '''
    op = formula['operator']
    args = formula.get('args')

    if op in Operators.UNARY:
        return '(%s %s)' % (op, formula_to_string(args[0]))
    elif op in Operators.BINARY:
        return '(%s %s %s)' % (op, formula_to_string(args[0]), formula_to_string(args[1]))
    elif op == Operators.IF0:
        return '(if0 %s %s %s)' % (
            formula_to_string(args[0]),
            formula_to_string(args[1]),
            formula_to_string(args[2]),
        )
    elif op == Operators.FOLD:
        return '(fold %s %s (lambda (%s %s) %s))' % (
            formula_to_string(args[0]),
            formula_to_string(args[1]),
            Operators.ID2,
            Operators.ID3,
            formula_to_string(args[2]),
        )
    else:
        # Assuming it is terminal
        return op
