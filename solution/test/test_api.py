import unittest

from .. import api, config


config.service_url = "http://robopoker.org/icfp/"
config.auth_token = "31337"


class ApiTestCase(unittest.TestCase):

    def test_train(self):
        result = api.train(20, "tfold")
        self.assertTrue("tfold" in result["operators"])
