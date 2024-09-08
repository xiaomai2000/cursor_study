import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from utils import DBUtils  # Use absolute import

class TestDBUtils(unittest.TestCase):
    def test_get_db_config(self):
        config = DBUtils.get_db_config()
        self.assertIsNotNone(config)  # Ensure the configuration is not None

if __name__ == '__main__':
    unittest.main()


