import pandas as pd
import json
import yaml
from db_util import DBUtils
from sqlalchemy import create_engine, text
import os
import logging
from logging_config import setup_logging
import glob
setup_logging()


def load_excel_meta():
    with open('excel_meta.json', 'r') as file:
        meta_data = json.load(file)
    return meta_data

def validate(data_df, file_name, fields):
    # Check for missing fields and collect them
    missing_fields = [field for field in fields if field not in data_df.columns]
    if missing_fields:
        # Raise an exception with a message listing the missing fields
        logging.error(f"{file_name}: Missing required fields: {', '.join(missing_fields)}")
        raise ValueError(f"{file_name}: Missing required fields: {', '.join(missing_fields)}")
    return True

def run_batch(source_folder):
    logging.info(f"In run_batch({source_folder}).")
    meta_data = load_excel_meta()
    try:
        for key, value in meta_data.items():
            file_pattern = f"{source_folder}/{value['prefix']}*{value['suffix']}.xlsx"
            files = glob.glob(file_pattern)
            if not files:  # Check if the list is empty
                logging.error(f"No files found matching {file_pattern}")
                raise FileNotFoundError(f"No files found matching {file_pattern}")
            
            for file_path in files:
                data_df = pd.read_excel(file_path, skiprows=value['start_row'] - 1)
                if validate(data_df, key, value['fields']):
                    DBUtils.append_df_to_db_table(data_df, value["target_db_table_name"])
        return True
    except Exception as e:
        print(e)
        logging.error(e)
        return False

def approve_report():
    pass    
    # 其他逻辑...

def get_sql_query_list(query_name):
    with open('sql_queries.yaml', 'r') as file:
        queries = yaml.safe_load(file)
    return queries[query_name]['query']


def process_data():
    sql = get_sql_query_list('sum_sbu_cost_map_1')
    engine = DBUtils.get_sqlalchemy_engine()
    connection = engine.connect()
    transaction = connection.begin()
    try:
        logging.info(f"Going to execute SQL: {sql}")
        result_proxy = connection.execute(text(sql))
        result_set = result_proxy.fetchall()  # Fetch results immediately after execution

        # Convert result to DataFrame
        df = pd.DataFrame(result_set)
        df.columns = result_proxy.keys()  # Set the column names to match the result
        ##print(df)
        transaction.commit()
        return df
    except Exception as e:
        transaction.rollback()
        logging.error(f"Error executing SQL: {e}")
        print(f"Error executing SQL: {e}")
    finally:
        connection.close()


