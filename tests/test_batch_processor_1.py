import unittest
from unittest.mock import patch, mock_open
import pandas as pd
from batch_processor import load_excel_meta, validate, run_batch
import os

# python -m unittest tests.test_batch_processor_



class TestBatchProcessor(unittest.TestCase):

    def test_load_excel_meta(self):
        # Mocking the open function to simulate reading from a file
        with patch("builtins.open", mock_open(read_data='{"test": {"prefix": "test", "suffix": "data", "start_row": 1, "fields": ["id", "name"], "target_db_table_name": "test_table"}}')):
            result = load_excel_meta()
            self.assertEqual(result, {"test": {"prefix": "test", "suffix": "data", "start_row": 1, "fields": ["id", "name"], "target_db_table_name": "test_table"}})

    def test_validate(self):
        data_df = pd.DataFrame({
            'id': [1, 2],
            'name': ['Alice', 'Bob']
        })
        result = validate(data_df, 'test.xlsx', ['id', 'name'])
        self.assertTrue(result)

    def test_validate_missing_fields(self):
        data_df = pd.DataFrame({
            'id': [1, 2]
        })
        with self.assertRaises(ValueError) as context:
            validate(data_df, 'test.xlsx', ['id', 'name'])
        self.assertIn('test.xlsx: Missing required fields: name', str(context.exception))


    def test_run_batch_real_file(self):
        excel_file_path = "./excelfiles/sbu_cost_map.xlsx"

        # Check if the file exists at the specified path
        self.assertTrue(os.path.exists(excel_file_path), f"Excel file does not exist at {excel_file_path}")

        result = run_batch(os.path.dirname(excel_file_path))
        self.assertTrue(result, "run_batch failed to process the existing file correctly")





if __name__ == '__main__':
    unittest.main()

