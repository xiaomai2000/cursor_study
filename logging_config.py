import logging
import os

def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    # Add 'class name' to the logging format
    logging.basicConfig(
        filename='logs/app_logs.log',
        filemode='a',
        format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s',  # Added [%(name)s] for class name
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )