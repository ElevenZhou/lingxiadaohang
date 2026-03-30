import paramiko

HOST = '106.55.106.28'
PORT = 22
USERNAME = 'ubuntu'
PASSWORD = 'Test2026.'

# 子域名设置
SUBDOMAIN = 'nav'
MAIN_DOMAIN = 'yumiai.art'
FULL_DOMAIN = f'{SUBDOMAIN}.{MAIN_DOMAIN}'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)

# 检查Nginx是否安装
print("检查Nginx状态...")
stdin, stdout, stderr = client.exec_command('sudo systemctl status nginx | grep Active')
nginx_status = stdout.read().decode().strip()
print(f"Nginx状态: {nginx_status}")

# 如果Nginx未安装，进行安装
if 'active (running)' not in nginx_status:
    print("安装Nginx...")
    stdin, stdout, stderr = client.exec_command('sudo apt update && sudo apt install -y nginx')
    print(stdout.read().decode())
    print(stderr.read().decode())

# 创建Nginx配置文件
nginx_config = f'''
server {{
    listen 80;
    server_name {FULL_DOMAIN};
    
    root /home/ubuntu/lingxia_nav;
    index index.html;
    
    location / {{
        try_files $uri $uri/ =404;
    }}
}}
'''

# 写入配置文件
print(f"\n创建子域名配置: {FULL_DOMAIN}...")
stdin, stdout, stderr = client.exec_command(f'sudo tee /etc/nginx/sites-available/{SUBDOMAIN} << EOF\n{nginx_config}EOF')
print(stdout.read().decode())

# 启用站点
print("\n启用站点...")
stdin, stdout, stderr = client.exec_command(f'sudo ln -sf /etc/nginx/sites-available/{SUBDOMAIN} /etc/nginx/sites-enabled/')

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

# 检查站点配置
print("\n检查站点配置...")
stdin, stdout, stderr = client.exec_command('ls -la /etc/nginx/sites-enabled/')
print(stdout.read().decode())

client.close()
print("\n子域名配置完成！")
print(f"现在可以通过 http://{FULL_DOMAIN} 访问网站")
print(f"请确保您的DNS已将 {FULL_DOMAIN} 指向服务器IP: 106.55.106.28")
