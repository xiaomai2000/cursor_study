import unittest
from unittest.mock import patch
from batch_processor import process_data
from db_util import DBUtils

class TestProcessData(unittest.TestCase):

    def test_process_data_success(self):
        result = process_data()
        print(result)


if __name__ == '__main__':
    unittest.main()

