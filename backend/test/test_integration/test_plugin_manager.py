import unittest

from infracheck.Api import convert_test_input_json_to_dataclasses
from infracheck.PluginManager import PluginManager
from test import mock_data


class PluginManagerTest(unittest.TestCase):
    """
    E-1 - Plugin-Manager
    """

    def test_serialize_and_deserialize(self):
        """
        Launch a test with two plugins
        Check if both results are in the output object
        :return:
        """
        data = convert_test_input_json_to_dataclasses(mock_data.local_test_with_two_plugins)
        res = PluginManager().launch_tests(data)
        self.assertEqual(len(res.plugin_result), 2)
