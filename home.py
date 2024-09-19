import streamlit as st
import logging

from logging_config import setup_logging  # Import the logging setup
setup_logging()  # Initialize logging

# Initialize logger with the module name
logger = logging.getLogger(__name__)

class HomePage:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def display_title(self):
        self.logger.info("Displaying the home page title")
        st.title("Welcome to the Finance P&L Tool!")

def main():
    page = HomePage()
    page.display_title()

if __name__ == "__main__":
    main()