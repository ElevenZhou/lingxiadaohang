import paramiko

HOST = '106.55.106.28'
PORT = 22
USERNAME = 'ubuntu'
PASSWORD = 'Test2026.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)

# 检查SSH服务状态
print("=== 检查SSH服务状态 ===")
stdin, stdout, stderr = client.exec_command('sudo systemctl status sshd')
print(stdout.read().decode())
print(stderr.read().decode())

# 检查SSH端口
print("\n=== 检查SSH端口 ===")
stdin, stdout, stderr = client.exec_command('netstat -tuln | grep :22')
print(stdout.read().decode())

# 检查防火墙状态
print("\n=== 检查防火墙状态 ===")
stdin, stdout, stderr = client.exec_command('sudo ufw status')
print(stdout.read().decode())

client.close()
