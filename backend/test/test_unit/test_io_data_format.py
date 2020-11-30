import inspect
import unittest
from dataclasses import dataclass

from infracheck.model.TestInput import TestInput
from infracheck.model.TestResult import TestResult


class ValidIODataTest(unittest.TestCase):
    """
    I-1 - Aufbau der Eingabedaten
    I-2 - Aufbau der Ausgabedaten
    """

    def test_valid_input_data(self):
        data = TestInput
        self.assertTrue(type(data), dataclass)
        fields = data.__dataclass_fields__
        self.assertTrue(fields['description'], F"has a description attribute")
        self.assertTrue(fields['plugins'], F"has a plugins attribute")
        self.assertTrue(fields['label'], F"has a label attribute")

    def test_valid_output_data(self):
        data = TestResult
        self.assertTrue(type(data), dataclass)
        fields = data.__dataclass_fields__
        self.assertTrue(fields['id'], F"has a id attribute")
        self.assertTrue(fields['pdf_link'], F"has a pdf_link attribute")
        self.assertTrue(fields['label'], F"has a label attribute")
        self.assertTrue(fields['description'], F"has a description attribute")
        self.assertTrue(fields['success_count'], F"has a success_count attribute")
        self.assertTrue(fields['failure_count'], F"has a failure_count attribute")
        self.assertTrue(fields['total_count'], F"has a total_count attribute")
        self.assertTrue(fields['date'], F"has a date attribute")
        self.assertTrue(fields['message'], F"has a message attribute")
        self.assertTrue(fields['total_count'], F"has a total_count attribute")
        self.assertTrue(fields['plugin_result'], F"has a plugin_result attribute")
