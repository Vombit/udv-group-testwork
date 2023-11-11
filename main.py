import os
import paramiko
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def save_data_to_file(data, filename):
    with open(f'output/{filename}', 'w') as file:
        file.write(data)

def connect(ssh_host, ssh_port, ssh_username, ssh_password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(self.ssh_host, port=self.ssh_port, username=self.ssh_username, password=self.ssh_password)
    return client


class Collection:
    def __init__(self, client):
        self.connect = client

    def execute_command(self, client, command):
        stdin, stdout, stderr = client.exec_command(command + '\n')
        output = stdout.read().decode('utf-8')
        return output

    def get_version(self):
        output = self.execute_command(self.connect, "show version")
        save_data_to_file(output, 'version.txt')
        print(f'\nВерсия коммутатора:\n{output}')

    def get_startup_config(self):
        output = self.execute_command(self.connect, "autocommand show startup-config")
        save_data_to_file(output, 'startup_config.txt')
        print(f'\nСтартовая конфигурация коммутатора:\n{output}')

    def get_running_config(self):
        output = self.execute_command(self.connect, "autocommand show running-config")
        save_data_to_file(output, 'current_config.txt')
        print(f'\nТекущая конфигурация коммутатора:\n{output}')

    def get_acl_info(self):
        output = self.execute_command(self.connect, "show ip access-list")
        save_data_to_file(output, 'ACL_info.txt')
        print(f'\nИнформация о списках контроля доступа (ACL):\n{output}')

    def get_interface_info(self):
        output = self.execute_command(self.connect, "show interfaces")
        save_data_to_file(output, 'interface_info.txt')
        print(f'\nИнформация об интерфейсах коммутатора:\n{output}')



if __name__ == "__main__":
    ssh_host = os.environ.get("SSH_HOST")
    ssh_port = int(os.environ.get("SSH_PORT"))
    ssh_username = os.environ.get("SSH_USERNAME")
    ssh_password = os.environ.get("SSH_PASSWORD")
    
    connect = connect(ssh_host, ssh_port, ssh_username, ssh_password)
    
    collector = Collection(connect)
    collector.get_version()
    collector.get_startup_config()
    collector.get_running_config()
    collector.get_acl_info()
    collector.get_interface_info()

    connect.close()