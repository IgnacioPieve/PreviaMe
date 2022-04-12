import io
import paramiko as paramiko
from config import credentials
from config import title

sc = credentials['server']
key = paramiko.RSAKey.from_private_key(io.StringIO(sc['private_key']))
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=sc['host'], username=sc['username'], pkey=key)


workdir_command = f'cd /home/ubuntu/{title}'
commands = ['git pull',
            'docker stop previame-container',
            'docker rm previame-container',
            'docker rmi previame',
            'docker build -t previame .',
            'docker run -d --name previame-container -p 8000:8000 previame']

print('Executing commands on server...')
for command in commands:
    print(f'\nCommand: {command}')
    (stdin, stdout, stderr) = ssh.exec_command(f'{workdir_command}; {command}')
    result = stderr.read().decode('utf-8')
    if result == '':
        print('Successfully executed command.')
    print(result)


ssh.close()
