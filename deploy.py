import io
import paramiko as paramiko
from secure_config import server_credentials as sc
from config import title

key = paramiko.RSAKey.from_private_key(io.StringIO(sc['private_key']))
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=sc['host'], username=sc['username'], pkey=key)

commands = [f'cd /home/ubuntu/{title}',
            'pkill -9 python',
            'git pull',
            'python3 main.py']

for command in commands:
    ssh.exec_command(command)

ssh.close()
