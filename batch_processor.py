import pandas as pd
import json
import yaml
from utils import DBUtils, SFTPUtils, read_sql_file
from sqlalchemy import create_engine, text
from etl_util import export_to_parquet

def load_excel_meta():
    with open('excel_meta.json', 'r') as file:
        meta_data = json.load(file)
    return meta_data

def validate(data, fields):
    # 实现数据校验逻辑，确保所有必需字段都存在
    return all(field in data.columns for field in fields)

def run_batch(source_folder):
    meta_data = load_excel_meta()
    try:
        for key, value in meta_data.items():
            file_path = f"{source_folder}/{value['prefix']}*{value['suffix']}.xlsx"
            data = pd.read_excel(file_path, skiprows=value['start_row'] - 1)
            if validate(data, value['fields']):
                DBUtils.upload_to_sql(data, "landing_table")
        return True
    except Exception as e:
        print(e)
        return False

def approve_report():
    # 假设我们需要导出'target_table'到Parquet
    export_to_parquet("target_table")
    # 其他逻辑...

def process_data():
    sql = get_sql_query('process_data')
    conn = DBUtils.get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()

def get_sql_query(query_name):
    with open('sql_queries.yaml', 'r') as file:
        queries = yaml.safe_load(file)
    return queries[query_name]['query']