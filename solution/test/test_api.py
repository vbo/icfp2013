import unittest
from nose.exc import SkipTest
from nose.plugins.attrib import attr
from .. import api, config


ex_train = config.example_train


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        api.auto_retry = False
        api.request_delay = 3

    def test_connection(self):
        base_url = "http://robopoker.org/icfp/train"
        api.call_url = lambda x: base_url + "?sleep=40"
        api.timeout = 1
        with self.assertRaises(api.Timeout):
            result = api.train()
        api.call_url = api.default_call_url
        api.auto_retry = api.default_auto_retry
        api.timeout = api.default_timeout

    def test_train(self):
        result = api.train(20, "tfold")
        self.assertEquals(result["size"], 20)

    def test_eval(self):
        with self.assertRaises(api.AlreadySolvedException) as ex:
            result = api.eval([1], ex_train["id"])
        problem = api.train(3)
        result = api.eval([1], None, problem["challenge"])
        self.assertEquals(result["status"], "ok")

    def test_guess(self):
        with self.assertRaises(api.AlreadySolvedException) as ex:
            api.guess(ex_train["id"], ex_train["challenge"])
        problem = api.train(3)
        result = api.guess(problem["id"], '(lambda (x) (plus x 1))')
        self.assertEquals(result["status"], "mismatch")
        self.assertEquals(len(result["values"]), 3)
        result = api.guess(problem["id"], problem["challenge"])
        self.assertEquals(result["status"], "win")
