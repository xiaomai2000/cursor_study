import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from db_util import DBUtils
import yaml






"""
def export_to_parquet(table_name, export_file_name=None):
    # 先读取环境变量
    env = os.getenv('APP_ENV', 'Non_Prod')
    print(f"Environment: {env}")

    # 然后获取数据库连接
    conn = DBUtils.get_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name}"
    print(f"Executing query: {query}")  # 打印查询语句以检查其正确性
    df = pd.read_sql(query, conn)
    cursor.close()

    # 读取配置文件，指定编码为 UTF-8
    with open("config.yaml", 'r', encoding='utf-8') as stream:
        config = yaml.safe_load(stream)
    default_path = config[env]['default_export_path']

    # 如果没有提供文件名，使用默认路径和表名
    if export_file_name is None:
        export_file_name = f"{default_path}{table_name}.parquet"
    elif not os.path.dirname(export_file_name):
        export_file_name = f"{default_path}{export_file_name}"

    #print(f"Config loaded: {config}")
    print(f"Default export path: {default_path}")
    print(f"Final export file name: {export_file_name}")


    return export_file_name

"""