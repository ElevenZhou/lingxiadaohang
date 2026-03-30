import paramiko

HOST = '106.55.106.28'
PORT = 22
USERNAME = 'ubuntu'
PASSWORD = 'Test2026.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)

# 检查进程
print("检查进程...")
stdin, stdout, stderr = client.exec_command('ps aux | grep python')
print(stdout.read().decode())

# 检查端口
print("\n检查端口...")
stdin, stdout, stderr = client.exec_command('netstat -tuln | grep 8000')
print(stdout.read().decode())

# 检查目录和文件
print("\n检查文件...")
stdin, stdout, stderr = client.exec_command('ls -la /home/ubuntu/lingxia_nav/')
print(stdout.read().decode())

# 检查日志
print("\n检查日志...")
stdin, stdout, stderr = client.exec_command('cat /home/ubuntu/lingxia_nav/server.log')
print(stdout.read().decode())

client.close()
