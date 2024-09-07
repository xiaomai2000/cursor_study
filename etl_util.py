import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from utils import DBUtils

def export_to_parquet(table_name, export_file_name=None):
    conn = DBUtils.get_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    cursor.close()

    # 获取默认导出路径
    env = os.getenv('APP_ENV', 'Non-Prod')
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
    default_path = config[env]['default_export_path']

    # 如果没有提供文件名，使用默认路径和表名
    if export_file_name is None:
        export_file_name = f"{default_path}{table_name}.parquet"
    elif not os.path.dirname(export_file_name):
        export_file_name = f"{default_path}{export_file_name}"

    # 导出到Parquet文件
    table = pa.Table.from_pandas(df)
    pq.write_table(table, export_file_name)
    print(f"Data exported to {export_file_name}")

    return export_file_name