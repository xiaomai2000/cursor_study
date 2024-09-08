
# python -m unittest tests.test_sqlite3_case1


import unittest
import os
from utils import DBUtils

class TestSQLite3Case1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set environment for testing
        os.environ['APP_ENV'] = 'Unit_Test'

    def test_get_db_config(self):
        """Test the database configuration retrieval."""
        config = DBUtils.get_db_config()
        self.assertIsNotNone(config)
        self.assertIn('DATABASE', config)

    def test_get_connection(self):
        """Test the database connection."""
        conn = DBUtils.get_connection()
        self.assertIsNotNone(conn)

    def test_close_connection(self):
        """Test closing the database connection."""
        DBUtils.get_connection()  # Ensure connection is open
        DBUtils.close_connection()
        self.assertIsNone(DBUtils._conn)

    @classmethod
    def tearDownClass(cls):
        # Clean up environment
        DBUtils.close_connection()
        del os.environ['APP_ENV']

if __name__ == '__main__':
    unittest.main()