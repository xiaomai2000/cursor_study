import os
import yaml
import logging
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker, scoped_session

class DBUtils:
    _engine = None
    _session_factory = None
    _session = None
    
    @staticmethod
    def get_db_config():
        env = os.getenv('APP_ENV', 'Non_Prod')
        with open("config.yaml", 'r', encoding='utf-8') as stream:
            config = yaml.safe_load(stream)
        db_config = config[env]['DB']
        return db_config

    @staticmethod
    def get_sqlalchemy_engine():
        if DBUtils._engine is None:
            db_config = DBUtils.get_db_config()
            connection_string = (
                f"mssql+pyodbc://@{db_config['SERVER']}\\{db_config['DATABASE_INSTANCE_NAME']},{db_config['PORT']}/{db_config['DATABASE']}"
                "?driver=ODBC Driver 17 for SQL Server"
                "&Trusted_Connection=yes"
            )
            DBUtils._engine = create_engine(connection_string)
            logging.info(f"Connection string being used: {DBUtils._engine.url}")
        return DBUtils._engine

    @classmethod
    def get_sqlalchemy_session(cls):
        if cls._session_factory is None:
            engine = cls.get_sqlalchemy_engine()
            cls._session_factory = sessionmaker(bind=engine)
            cls._session = scoped_session(cls._session_factory)
        return cls._session()

    @classmethod
    def close_sqlalchemy_session(cls, session):
        """Close and remove the provided SQLAlchemy session."""
        if session is not None:
            session.close()
        if cls._session is not None:
            cls._session.remove()  # Correctly use the scoped_session factory to remove the session

    @staticmethod
    def append_df_to_db_table(dataframe, table_name):
        session = DBUtils.get_sqlalchemy_session()
        dataframe.to_sql(table_name, con=session.bind, if_exists='append', index=False)
        session.commit()
        session.close()

    @staticmethod
    def overwrite_df_to_db_table(dataframe, table_name):
        session = DBUtils.get_sqlalchemy_session()
        engine = session.bind
        inspector = inspect(engine)

        # Check if the table exists
        if inspector.has_table(table_name):
            # Delete all records from the table
            session.execute(text(f"DELETE FROM {table_name}"))
            session.commit()
        
        # Append new data
        dataframe.to_sql(table_name, con=engine, if_exists='append', index=False)
        session.commit()
        session.close()

    @staticmethod
    def read_sql_statement_from_file(sql_file_path):
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            return file.read()

