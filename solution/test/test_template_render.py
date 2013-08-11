import unittest
from nose.plugins.attrib import attr

from ..tools.build_formula_index import TemplatedProgramTreeNode, formula_to_string

class TemplateRenderTestCase(unittest.TestCase):

    @attr('fast')
    def test_fold_variables_without_fold(self):
        template_proto = ('op1', ('op1', ('if0', 'T', ('fold', 'T', 'T', 'T'), 'T')))
        template = TemplatedProgramTreeNode.fromtuple(template_proto)

        for formula in template.render(False):
            s = formula_to_string(formula)
            if ('id2' in s or 'id3' in s):
                self.assertTrue('fold' in s, 'Has folded ids BUT NO FOLD: "%s"' % formula)
