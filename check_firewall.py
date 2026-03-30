import paramiko

HOST = '106.55.106.28'
PORT = 22
USERNAME = 'ubuntu'
PASSWORD = 'Test2026.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)

# 检查防火墙状态
print("检查UFW防火墙...")
stdin, stdout, stderr = client.exec_command('sudo ufw status')
print(stdout.read().decode())
print(stderr.read().decode())

# 检查iptables
print("\n检查iptables...")
stdin, stdout, stderr = client.exec_command('sudo iptables -L -n | grep 8000')
print(stdout.read().decode())

# 检查安全组（如果是云服务器）
print("\n检查云服务器安全组...")
stdin, stdout, stderr = client.exec_command('curl -s http://169.254.169.254/latest/meta-data/security-groups 2>/dev/null || echo "不是AWS/阿里云ECS"')
print(stdout.read().decode())

# 测试本地访问
print("\n测试本地访问...")
stdin, stdout, stderr = client.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/')
print("HTTP状态码:", stdout.read().decode())

client.close()
