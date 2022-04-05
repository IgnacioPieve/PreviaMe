import io
import paramiko as paramiko
from config import server_credentials as sc
from config import title

key = paramiko.RSAKey.from_private_key(io.StringIO(sc['private_key']))
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=sc['host'], username=sc['username'], pkey=key)

commands = [f'cd /home/ubuntu/{title}',
            'mkdir test',
            'pkill -9 python',
            'git pull',
            'pip3 install -r requirements.txt',
            'python3 main.py > /dev/null 2>&1 &']
commands = '; '.join(commands)

(stdin, stdout, stderr) = ssh.exec_command(commands)

ssh.close()
