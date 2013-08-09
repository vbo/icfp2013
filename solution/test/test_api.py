import unittest
from nose.exc import SkipTest

from .. import api, config


ex_train = config.example_train

api.request_delay = 5

class ApiTestCase(unittest.TestCase):

    def test_train(self):
        result = api.train(20, "tfold")
        self.assertEquals(result["size"], 20)

    def test_eval(self):
        with self.assertRaises(api.RequestError) as ex:
            result = api.eval(ex_train["id"], ex_train["challenge"], [1])
            self.assertEquals(ex.code, 412)
        problem = api.train(3)
        result = api.eval(problem["id"], problem["challenge"], [1])
        self.assertEquals(result["status"], "ok")

    def test_guess(self):
        with self.assertRaises(api.RequestError) as ex:
            api.guess(ex_train["id"], ex_train["challenge"])
            self.assertEquals(ex.code, 412)
        problem = api.train(3)
        result = api.guess(problem["id"], '(lambda (x) (plus x 1))')
        self.assertEquals(result["status"], "mismatch")
        self.assertEquals(len(result["values"]), 3)
        result = api.guess(problem["id"], problem["challenge"])
        self.assertEquals(result["status"], "win")


# skip to not DDoS game server
ApiTestCase.__test__ = False
