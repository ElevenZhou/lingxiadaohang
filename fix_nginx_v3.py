import paramiko

HOST = '106.55.106.28'
PORT = 22
USERNAME = 'ubuntu'
PASSWORD = 'Test2026.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)

print("清理旧配置...")
client.exec_command('sudo rm /etc/nginx/sites-available/nav')

print("创建新配置...")
# 逐行写入配置
commands = [
    'sudo bash -c "echo \'server {\' > /etc/nginx/sites-available/nav"',
    'sudo bash -c "echo \'    listen 80;\' >> /etc/nginx/sites-available/nav"',
    'sudo bash -c "echo \'    server_name nav.yumiai.art;\' >> /etc/nginx/sites-available/nav"',
    'sudo bash -c "echo \'    \' >> /etc/nginx/sites-available/nav"',
    'sudo bash -c "echo \'    root /home/ubuntu/lingxia_nav;\' >> /etc/nginx/sites-available/nav"',
    'sudo bash -c "echo \'    index index.html;\' >> /etc/nginx/sites-available/nav"',
    'sudo bash -c "echo \'    \' >> /etc/nginx/sites-available/nav"',
    'sudo bash -c "echo \'    location / {\' >> /etc/nginx/sites-available/nav"',
    'sudo bash -c "echo \'        try_files $uri $uri/ =404;\' >> /etc/nginx/sites-available/nav"',
    'sudo bash -c "echo \'    }\' >> /etc/nginx/sites-available/nav"',
    'sudo bash -c "echo \'}\'> /etc/nginx/sites-available/nav"'
]

for cmd in commands:
    stdin, stdout, stderr = client.exec_command(cmd