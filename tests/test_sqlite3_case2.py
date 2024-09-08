# python -m unittest tests.test_sqlite3_case2

import unittest
import os
import sqlite3
import pandas as pd
from utils import DBUtils
# 假设 etl_util.py 在同一目录下
import etl_util

class TestSQLite3Case2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 设置环境变量以使用 SQLite
        os.environ['APP_ENV'] = 'Unit_Test'
        cls.conn = DBUtils.get_connection()
        cls.cursor = cls.conn.cursor()
        # 创建表
        cls.cursor.execute("DROP TABLE IF EXISTS test1")
        cls.cursor.execute("""
            CREATE TABLE test1 (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                amount REAL
            )
        """)
        cls.conn.commit()

    def test_insert_and_query(self):
        # 创建 DataFrame
        df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'age': [25, 30, 35, 40, 45],
            'amount': [100.0, 150.0, 200.0, 250.0, 300.0]
        })
        # 插入数据到 SQLite
        df.to_sql('test1', self.conn, if_exists='append', index=False)
        
        # 从 SQLite 读取数据
        df_read = pd.read_sql('SELECT * FROM test1', self.conn)
        
        # 比较 DataFrame
        pd.testing.assert_frame_equal(df, df_read)

        # 导出到 Parquet 文件
        etl_util.export_to_parquet("test1")

    @classmethod
    def tearDownClass(cls):
        cls.cursor.close()
        cls.conn.close()
        del os.environ['APP_ENV']

if __name__ == '__main__':
    unittest.main()