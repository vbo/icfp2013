import unittest, re, sys
from ..tools import build_formula_index
from .. import api, config

ex_train = config.example_train

api.request_delay = 5

class SolutionTestRange(unittest.TestCase):

    tree_index_root = './tree_index'




# skip to not DDoS game server
#SolutionTestRange.__test__ = False
