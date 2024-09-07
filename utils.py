import os
import pyodbc
import paramiko
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import yaml
import sqlite3

class DBUtils:
    _conn = None  # 类属性，用于存储数据库连接

    @staticmethod
    def get_db_config():
        env = os.getenv('APP_ENV', 'Non-Prod')
        with open("config.yaml", 'r') as stream:
            config = yaml.safe_load(stream)
        db_config = config[env]['DB']
        return db_config

    @classmethod
    def get_connection(cls):
        if cls._conn is None:
            db_config = cls.get_db_config()
            if os.getenv('APP_ENV') == "Unit_Test":
                cls._conn = sqlite3.connect(db_config["DATABASE"])
            else:
                cls._conn = pyodbc.connect(
                    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                    f'SERVER={db_config["SERVER"]};'
                    f'DATABASE={db_config["DATABASE"]};'
                    'Trusted_Connection=yes;'
                )
        return cls._conn

    @classmethod
    def close_connection(cls):
        if cls._conn is not None:
            cls._conn.close()
            cls._conn = None

    @staticmethod
    def upload_to_sql(data, table_name):
        conn = DBUtils.get_connection()
        cursor = conn.cursor()
        # 进行数据上传操作
        cursor.close()

    @staticmethod
    def export_to_parquet(table_name, file_name):
        conn = DBUtils.get_connection()
        # 导出数据到Parquet文件的逻辑
        DBUtils.close_connection()  # 可以在适当的时候关闭连接

    @staticmethod
    def read_sql_file(file_path):
        with open(file_path, 'r') as file:
            return file.read()

class SFTPUtils:
    @staticmethod
    def get_sftp_config():
        env = os.getenv('APP_ENV', 'Non-Prod')  # 默认为Non-Prod
        with open("config.yaml", 'r') as stream:
            config = yaml.safe_load(stream)
        sftp_config = config[env]['SFTP']
        return sftp_config

    @staticmethod
    def test_sftp_connection(env="Non-Prod"):
        sftp_config = SFTPUtils.get_sftp_config(env)
        try:
            key = paramiko.RSAKey.from_private_key_file(sftp_config["PRIVATE_KEY_PATH"])
            transport = paramiko.Transport((sftp_config["HOST"], sftp_config["PORT"]))
            transport.connect(username=sftp_config["USERNAME"], pkey=key)
            sftp = paramiko.SFTPClient.from_transport(transport)
            print("SFTP connection successful.")
            sftp.close()
            transport.close()
            return True
        except Exception as e:
            print(f"Failed to connect to SFTP: {e}")
            return False

    @staticmethod
    def upload_file(local_path, remote_path):
        # SFTP上传文件逻辑
        pass





