import sys
import os
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logging_config import setup_logging  # Import the logging setup
setup_logging()  # Initialize logging



import unittest
from db_util import DBUtils  # Updated import

class TestDBUtils(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDBUtils, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)  # Initialize logger

    def test_get_db_config(self):
        self.logger.info("Fetching DB configuration")  # Use class logger
        config = DBUtils.get_db_config()
        self.assertIsNotNone(config)  # Ensure the configuration is not None
        self.logger.info("DB configuration fetched successfully")

if __name__ == '__main__':
    unittest.main()


