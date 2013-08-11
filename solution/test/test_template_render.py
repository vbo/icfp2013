import unittest
from nose.plugins.attrib import attr

from ..tools.build_formula_index import TemplatedProgramTreeNode, formula_to_string

class TemplateRenderTestCase(unittest.TestCase):

    @attr('fast')
    def test_fold_variables_without_fold(self):
        template_proto = ('if0', 'T', ('fold', 'T', 'T', 'T'), 'T')
        template = TemplatedProgramTreeNode.fromtuple(template_proto)

        for i, formula in enumerate(template.render(False)):
            s = formula_to_string(formula)
            if ('id2' in s or 'id3' in s):
                self.assertTrue('fold' in s, '[%d] Has folded ids BUT NO FOLD: "%s"' % (i, formula))
