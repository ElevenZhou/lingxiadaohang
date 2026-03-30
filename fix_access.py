import paramiko

HOST = '106.55.106.28'
PORT = 22
USERNAME = 'ubuntu'
PASSWORD = 'Test2026.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)

# 检查IP地址
print("检查IP地址...")
stdin, stdout, stderr = client.exec_command('ip addr show | grep inet')
print(stdout.read().decode())

# 检查路由
print("\n检查默认路由...")
stdin, stdout, stderr = client.exec_command('ip route | grep default')
print(stdout.read().decode())

# 检查监听地址
print("\n检查8000端口监听详情...")
stdin, stdout, stderr = client.exec_command('ss -tlnp | grep 8000')
print(stdout.read().decode())

# 尝试使用0.0.0.0重新启动服务器
print("\n停止现有服务器并重新启动...")
client.exec_command('pkill -f "python3 -m http.server 8000"')
import time
time.sleep(1)

# 使用0.0.0.0明确绑定到所有接口
stdin, stdout, stderr = client.exec_command('cd /home/ubuntu/lingxia_nav && nohup python3 -m http.server 8000 --bind 0.0.0.0 > server.log 2>&1 &')
time.sleep(2)

# 验证新进程
print("\n验证新进程...")
stdin, stdout, stderr = client.exec_command('ss -tlnp | grep 8000')
print(stdout.read().decode())

client.close()
print("\n已尝试重新绑定到0.0.0.0，请再次访问 http://106.55.106.28:8000")
