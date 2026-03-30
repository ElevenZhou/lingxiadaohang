import paramiko

HOST = '106.55.106.28'
PORT = 22
USERNAME = 'ubuntu'
PASSWORD = 'Test2026.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)

# 安装Nginx
print("安装Nginx...")
stdin, stdout, stderr = client.exec_command('sudo apt update && sudo apt install -y nginx')
print(stdout.read().decode())
print(stderr.read().decode())

# 创建Nginx配置文件
nginx_config = '''server {
    listen 80;
    server_name 106.55.106.28;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
'''

# 写入配置文件
print("\n创建Nginx配置...")
stdin, stdout, stderr = client.exec_command('sudo tee /etc/nginx/sites-available/lingxia_nav << EOF\n' + nginx_config + 'EOF')
print(stdout.read().decode())

# 启用站点
print("\n启用站点...")
stdin, stdout, stderr = client.exec_command('sudo ln -sf /etc/nginx/sites-available/lingxia_nav /etc/nginx/sites-enabled/')
stdin, stdout, stderr = client.exec_command('sudo rm -f /etc/nginx/sites-enabled/default')

# 测试配置
print("\n测试Nginx配置...")
stdin, stdout, stderr = client.exec_command('sudo nginx -t')
print(stdout.read().decode())
print(stderr.read().decode())

# 重启Nginx
print("\n重启Nginx...")
stdin, stdout, stderr = client.exec_command('sudo systemctl restart nginx')
print(stdout.read().decode())

# 检查状态
print("\n检查Nginx状态...")
stdin, stdout, stderr = client.exec_command('sudo systemctl status nginx | grep Active')
print(stdout.read().decode())

client.close()
print("\nNginx配置完成！")
print("现在可以通过 http://106.55.106.28 访问网站（无需端口号）")
