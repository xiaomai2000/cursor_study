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
        env = os.getenv('APP_ENV', 'Non_Prod')
        with open("config.yaml", 'r', encoding='utf-8') as stream:  # Specify encoding here
            config = yaml.safe_load(stream)
        db_config = config[env]['DB']
        return db_config

    @classmethod
    def get_connection(cls):
        if cls._conn is None:
            db_config = cls.get_db_config()
            if os.getenv('APP_ENV') == "Unit_Test":
                database_path = db_config["DATABASE"]
                # 确保路径是有效的文件路径
                if not database_path or "://" in database_path:
                    raise ValueError(f"数据库路径({database_path})配置不正确")
                # 确保目录存在
                database_dir = os.path.dirname(database_path)
                if database_dir:
                    os.makedirs(database_dir, exist_ok=True)
                cls._conn = sqlite3.connect(database_path)
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
    def read_sql_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:  # Specify encoding here
            return file.read()

class SFTPUtils:
    @staticmethod
    def get_sftp_config():
        env = os.getenv('APP_ENV', 'Non_Prod')  # 默认为Non-Prod
        with open("config.yaml", 'r') as stream:
            config = yaml.safe_load(stream)
        sftp_config = config[env]['SFTP']
        return sftp_config

    @staticmethod
    def test_sftp_connection(env="Non_Prod"):
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



