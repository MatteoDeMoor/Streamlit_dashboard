import paramiko
import pyodbc
from sshtunnel import SSHTunnelForwarder

# Define SSH connection parameters
ssh_hostname = 'vichogent.be'
ssh_port = 40239
ssh_username = 'vicuser'
ssh_password = 'NouRobTomJarMat5'

# Define MS SQL connection parameters
sql_hostname = '127.0.0.1'  # Localhost since we will use port forwarding
sql_port = 1433  # Default SQL Server port
sql_database = 'CandidateAssessmentDB'  # Replace with your database name
sql_username = 'DEP2_G05'  # SQL Server username
sql_password = 'NouRobTomJarMat5'  # SQL Server password

# Global variable for the SSH tunnel
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
