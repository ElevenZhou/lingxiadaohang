import paramiko

HOST = '106.55.106.28'
PORT = 22
USERNAME = 'ubuntu'
PASSWORD = 'Test2026.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)

print("=== 1. 检查Nginx状态 ===")
stdin, stdout, stderr = client.exec_command('sudo systemctl status nginx')
print(stdout.read().decode())
print(stderr.read().decode())

print("\n=== 2. 检查Nginx配置 ===")
stdin, stdout, stderr = client.exec_command('sudo nginx -t')
print(stdout.read().decode())
print(stderr.read().decode())

print("\n=== 3. 检查站点配置 ===")
stdin, stdout, stderr = client.exec_command('cat /etc/nginx/sites-available/nav')
print(stdout.read().decode())

print("\n=== 4. 检查文件存在性 ===")
stdin, stdout, stderr = client.exec_command('ls -la /home/ubuntu/lingxia_nav/')
print(stdout.read().decode())

print("\n=== 5. 测试本地访问 ===")
stdin, stdout, stderr = client.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost/')
print("本地访问状态码:", stdout.read().decode())

print("\n=== 6. 检查端口 ===")
stdin, stdout, stderr = client.exec_command('netstat -tuln | grep :80')
print(stdout.read().decode())

print("\n=== 7. 检查防火墙 ===")
stdin, stdout, stderr = client.exec_command('sudo ufw status')
print(stdout.read().decode())

client.close()
