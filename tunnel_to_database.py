import pyodbc
from sshtunnel import SSHTunnelForwarder
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now retrieve the variables
ssh_hostname = os.getenv('SSH_HOSTNAME')
ssh_port = int(os.getenv('SSH_PORT'))
ssh_username = os.getenv('SSH_USERNAME')
ssh_password = os.getenv('SSH_PASSWORD')
sql_hostname = os.getenv('SQL_HOSTNAME')
sql_port = int(os.getenv('SQL_PORT'))
sql_database = os.getenv('SQL_DATABASE')
sql_username = os.getenv('SQL_USERNAME')
sql_password = os.getenv('SQL_PASSWORD')

tunnel = None

def open_ssh_tunnel():
    global tunnel
    # Create an SSH tunnel
    tunnel = SSHTunnelForwarder(
        (ssh_hostname, ssh_port),
        ssh_username=ssh_username,
        ssh_password=ssh_password,
        remote_bind_address=('127.0.0.1', sql_port),  # Remote SQL Server address
        local_bind_address=('0.0.0.0', sql_port)  # Local port
    )
    tunnel.start()
    print("SSH tunnel established")

def close_ssh_tunnel():
    global tunnel
    if tunnel is not None:
        tunnel.close()
        print("SSH tunnel closed")

def open_sql_connection():
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={sql_hostname},{tunnel.local_bind_port};"
        f"DATABASE={sql_database};"
        f"UID={sql_username};"
        f"PWD={sql_password}"
    )

    try:
        # Establish the connection
        connection = pyodbc.connect(connection_string)
        print("SQL connection established")
        return connection

    except Exception as e:
        print(f"Error: {e}")
        return None

def close_sql_connection(connection):
    if connection is not None:
        connection.close()
        print("SQL connection closed")

def main():
    try:
        open_ssh_tunnel()

        connection = open_sql_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT @@VERSION;")

            # Fetch and print the results
            row = cursor.fetchone()
            while row:
                print(row[0])
                row = cursor.fetchone()

            close_sql_connection(connection)

    finally:
        close_ssh_tunnel()

if __name__ == "__main__":
    main()
