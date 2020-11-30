import unittest
import uuid
from datetime import datetime

from infracheck.model.TestResult import TestResult
from infracheck.services.Persistence import Persistence


class PersistenceTest(unittest.TestCase):
    """
    I-4 - Persistenz von Daten
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.persistence = Persistence()
        cls.uuid = uuid.uuid4().hex

    def test_add_result_to_db(self):
        self.persistence.add_result(TestResult(self.uuid, "", "test_only", "", -1, -1, -1, "", datetime.now(), []))

    def test_get_result_from_db(self):
        res = self.persistence.Result.query.filter_by(id=self.uuid).first()
        self.assertTrue(res)
