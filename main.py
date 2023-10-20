import paramiko
import os
from dotenv import load_dotenv, find_dotenv

class collector:
    def __init__(self, ssh_host, ssh_port, ssh_username, ssh_password):
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password

    def save_data_to_file(self, data, filename):
        with open(f'output/{filename}', 'w') as file:
            file.write(data)

    def connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.ssh_host, port=self.ssh_port, username=self.ssh_username, password=self.ssh_password)
        return client

    def execute_command(self, client, command):
            stdin, stdout, stderr = client.exec_command(command + '\n')
            output = stdout.read().decode('utf-8')
            return output


    def get_version(self):
        client = self.connect()
        output = self.execute_command(client, "show version")
        self.save_data_to_file(output, 'version.txt')
        print(f'\nВерсия коммутатора:\n{output}')
        client.close()

    def get_startup_config(self):
        client = self.connect()
        output = self.execute_command(client, "autocommand show startup-config")
        self.save_data_to_file(output, 'startup_config.txt')
        print(f'\nСтартовая конфигурация коммутатора:\n{output}')
        client.close()

    def get_running_config(self):
        client = self.connect()
        output = self.execute_command(client, "autocommand show running-config")
        self.save_data_to_file(output, 'current_config.txt')
        print(f'\nТекущая конфигурация коммутатора:\n{output}')
        client.close()

    def get_acl_info(self):
        client = self.connect()
        output = self.execute_command(client, "show ip access-list")
        self.save_data_to_file(output, 'ACL_info.txt')
        print(f'\nИнформация о списках контроля доступа (ACL):\n{output}')
        client.close()

    def get_interface_info(self):
        client = self.connect()
        output = self.execute_command(client, "show interfaces")
        self.save_data_to_file(output, 'interface_info.txt')
        print(f'\nИнформация об интерфейсах коммутатора:\n{output}')
        client.close()

    def main(self):
        self.get_version()
        self.get_startup_config()
        self.get_running_config()
        self.get_acl_info()
        self.get_interface_info()

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    ssh_host = os.environ.get("SSH_HOST")
    ssh_port = int(os.environ.get("SSH_PORT"))
    ssh_username = os.environ.get("SSH_USERNAME")
    ssh_password = os.environ.get("SSH_PASSWORD")

    collector = collector(ssh_host, ssh_port, ssh_username, ssh_password)
    collector.main()
