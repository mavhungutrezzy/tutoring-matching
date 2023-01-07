import json
import unittest
import warnings

from server import server


class TestSwagger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def test_get_spec(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="unclosed file")
            response = self.client.get("/application/spec")
        self.assertEqual(response.status_code, 200)

    def test_swagger_is_not_empty(self):

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="unclosed file")
            response = self.client.get("/application/spec")
        response_json = json.loads(response.data.decode("utf-8"))
        self.assertTrue(response_json["paths"])
