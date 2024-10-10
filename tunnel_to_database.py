import paramiko

# Define SSH connection parameters
hostname = 'vichogent.be'
port = 40239
username = 'vicuser'
password = 'NouRobTomJarMat5'
def connect_ssh():
    # Create an SSH client instance
    client = paramiko.SSHClient()

    # Automatically add the server's host key (use with caution, in real applications it is better to manually add known hosts)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the SSH server
        client.connect(hostname, port, username, password)

        # Execute a command on the remote server
        stdin, stdout, stderr = client.exec_command('ls -l')

        # Print the command output
        for line in stdout:
            print(line.strip())

        # Print any error messages
        for line in stderr:
            print(line.strip())

    finally:
        # Close the connection
        client.close()
