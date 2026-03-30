import paramiko
import os

# 服务器信息
HOST = '106.55.106.28'
PORT = 22
USERNAME = 'ubuntu'
PASSWORD = 'Test2026.'

# 本地文件路径
local_index = 'index.html'
local_data = 'data.json'

# 远程文件路径
remote_dir = '/home/ubuntu/lingxia_nav/'
remote_index = remote_dir + 'index.html'
remote_data = remote_dir + 'data.json'

print("开始部署灵虾导航站...")

# 创建SSH客户端
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 连接服务器
print(f"连接服务器: {HOST}")
client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)

# 创建目录
print("创建网站目录...")
stdin, stdout, stderr = client.exec_command(f'mkdir -p {remote_dir}')
stdout.read()

# 上传文件
print("上传文件...")
sftp = client.open_sftp()
sftp.put(local_index, remote_index)
sftp.put(local_data, remote_data)
sftp.close()

# 启动服务器
print("启动Web服务器...")
# 先停止可能存在的进程
client.exec_command('pkill -f "python3 -m http.server 8000"')
# 启动新服务器
client.exec_command(f'cd {remote_dir} && nohup python3 -m http.server 8000 > server.log 2>&1 &')

# 关闭连接
client.close()

print("部署完成！")
print(f"网站地址: http://{HOST}:8000")
