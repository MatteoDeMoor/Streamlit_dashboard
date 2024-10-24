import os
import logging
import pyodbc
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
import pandas as pd
from BinaryParsers import BinaryBaqHelper, BinaryFcaHelper, BinarySjtHelper
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Retrieve the environment variables
ssh_hostname = os.getenv('SSH_HOSTNAME')
ssh_port = int(os.getenv('SSH_PORT', 22))
ssh_username = os.getenv('SSH_USERNAME')
ssh_username = os.getenv('SSH_USERNAME')
ssh_username = os.getenv('SSH_USERNAME')
ssh_password = os.getenv('SSH_PASSWORD')
sql_hostname = os.getenv('SQL_HOSTNAME', '127.0.0.1')
sql_port = int(os.getenv('SQL_PORT', 1433))
sql_database = os.getenv('SQL_DATABASE')
sql_username = os.getenv('SQL_USERNAME')
sql_password = os.getenv('SQL_PASSWORD')

# Check for missing environment variables
required_env_vars = [
    ssh_hostname, ssh_username, ssh_password,
    sql_database, sql_username, sql_password
]
if any(var is None for var in required_env_vars):
    logging.error("Missing required environment variables.")
    exit(1)

class DatabaseConnection:
    def __init__(self):
        self.tunnel = None
        self.connection = None

    def open_ssh_tunnel(self):
        """Open an SSH tunnel to the remote server."""
        self.tunnel = SSHTunnelForwarder(
            (ssh_hostname, ssh_port),
            ssh_username=ssh_username,
            ssh_password=ssh_password,
            remote_bind_address=(sql_hostname, sql_port),
            local_bind_address=('127.0.0.1', sql_port)
        )
        self.tunnel.start()
        logging.info("SSH tunnel established")

    def close_ssh_tunnel(self):
        """Close the SSH tunnel if it's open."""
        if self.tunnel:
            self.tunnel.close()
            logging.info("SSH tunnel closed")

    def open_sql_connection(self):
        """Open a connection to the SQL database."""
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER=127.0.0.1,{self.tunnel.local_bind_port};"
            f"DATABASE={sql_database};"
            f"UID={sql_username};"
            f"PWD={sql_password}"
        )

        try:
            self.connection = pyodbc.connect(connection_string)
            logging.info("SQL connection established")
        except Exception as e:
            logging.error(f"Error establishing SQL connection: {e}")
            return None

    def close_sql_connection(self):
        """Close the SQL connection if it's open."""
        if self.connection:
            self.connection.close()
            logging.info("SQL connection closed")

    def get_table_names(self):
        """Retrieve the names of the tables in the database."""
        if self.connection is None:
            logging.error("SQL connection is not established.")
            return []

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
            tables = cursor.fetchall()
            return [table[0] for table in tables]
        except Exception as e:
            logging.error(f"Error fetching table names: {e}")
            return []
        
    def fetch_rows(self, table_name):
        """Fetch rows from the specified table one by one."""
        if self.connection is None:
            logging.error("SQL connection is not established.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT Data FROM {table_name}")
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                yield row  # Yield each row one by one for further processing
        except Exception as e:
            logging.error(f"Error fetching rows from {table_name}: {e}")
    def parse_data_SJT(self,data):
        helper = BinarySjtHelper(bytes(data))

        persons_answers = []
        person_data = {}
        for item_index in range(1, helper.total_items + 1):
            try:
                parsed_item = helper.parse_item(item_index)
                if parsed_item is None:
                    break  # Termination condition
                print(parsed_item)
                # Updated key from 'QuestionIndex' to 'ItemIndex'
                situation_id = parsed_item.get('InstrumentClassId', f'Situation_{parsed_item["ItemIndex"]}')
                answer = parsed_item.get('TimeSpent', [np.nan])  # Expecting 3 answers per situation
                person_data[f"{situation_id}_TimeSpent"] = answer

            except Exception as e:
                logging.error(f"Error parsing candidate , item index {item_index}: {e}")

        if person_data:
            persons_answers.append(person_data)

        return persons_answers[0]
def main():
    db_connection = DatabaseConnection()
    try:
        db_connection.open_ssh_tunnel()
        db_connection.open_sql_connection()

        rows = db_connection.fetch_rows('CandidateResultSJT')
        time_spent_data = []
        for _ in range(4):
            parsed_data = db_connection.parse_data_SJT(next(rows)[0])
            time_spent_data.append(parsed_data)

    finally:
        db_connection.close_sql_connection()
        db_connection.close_ssh_tunnel()
    
if __name__ == "__main__":
    main()
