import logging
from logging_config import setup_logging
setup_logging()

# python -m unittest tests.test_sql_util_case1


import unittest
import os
from db_util import DBUtils 
import pandas as pd
from sqlalchemy import text, inspect

class TestSQLUtilCase1(unittest.TestCase): 
    @classmethod
    def setUpClass(cls):
        # Set environment for testing
        logging.info("Setting APP_ENV to Non_prod.")
        os.environ['APP_ENV'] = 'Non_Prod'

    def test_get_db_config(self):
        """Test the database configuration retrieval."""
        logging.info("Fetching DB configuration")
        config = DBUtils.get_db_config()
        self.assertIsNotNone(config)
        self.assertIn('DATABASE', config)
        logging.info("DB configuration fetched successfully")

    def test_get_connection(self):
        """Test the database connection using SQLAlchemy."""
        logging.info("Establishing database connection using SQLAlchemy")
        session = DBUtils.get_sqlalchemy_session() 
        self.assertIsNotNone(session)
        logging.info("Database connection established successfully using SQLAlchemy")

    def test_close_connection(self): 
        """Test closing the database connection using SQLAlchemy."""
        session = DBUtils.get_sqlalchemy_session() 
        DBUtils.close_sqlalchemy_session(session)
        logging.info("Database connection closed successfully using SQLAlchemy")

    def test_append_df_to_db_table(self):
        """Test appending a DataFrame to a database table."""
        # Create a sample DataFrame
        data = {'Column1': [1, 2], 'Column2': ['A', 'B']}
        dataframe = pd.DataFrame(data)

        # Specify the table name
        table_name = 'test_table'

        # Ensure the table is empty or does not exist before the test
        session = DBUtils.get_sqlalchemy_session()
        engine = session.bind
        inspector = inspect(engine)

        if inspector.has_table(table_name):
            session.execute(text(f"DELETE FROM {table_name}"))
            session.commit()

        # Append the DataFrame to the table
        DBUtils.append_df_to_db_table(dataframe, table_name)

        # Retrieve data from the table to verify insertion
        result = pd.read_sql_table(table_name, con=engine)
        session.close()

        # Check if the DataFrame was appended correctly
        pd.testing.assert_frame_equal(result, dataframe, check_dtype=False)

        logging.info("DataFrame appended to database table successfully.")

    @classmethod
    def tearDownClass(cls):
        # Clean up environment
        logging.info("Cleaning up environment.")
        del os.environ['APP_ENV']

if __name__ == '__main__':
    unittest.main()