import paramiko

HOST = '106.55.106.28'
PORT = 22
USERNAME = 'ubuntu'
PASSWORD = 'Test2026.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)

# 修复Nginx配置（确保try_files格式正确）
nginx_config = '''server {
    listen 80;
    server_name nav.yumiai.art;
    
    root /home/ubuntu/lingxia_nav;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
'''

print("修复Nginx配置...")
# 使用不同的方法写入文件
stdin, stdout, stderr = client.exec_command('sudo bash -c "echo \'' + nginx_config + '\' > /etc/nginx/sites-available/nav"')
print(stdout.read().decode())
print(stderr.read().decode())

# 检查文件内容
print("\n检查配置文件内容...")
stdin, stdout, stderr = client.exec_command('cat /etc/nginx/sites-available/nav')
print(stdout.read().decode())

# 测试配置
print("\n测试Nginx配置...")
stdin, stdout, stderr = client.exec_command('sudo nginx -t')
print(stdout.read().decode())
print(stderr.read().decode())

# 重启Nginx
print("\n重启Nginx...")
stdin, stdout, stderr = client.exec_command('sudo systemctl restart nginx')
print(stdout.read().decode())

# 测试子域名访问
print("\n测试子域名访问...")
stdin, stdout, stderr = client.exec_command('curl -s -o /dev/null -w "%{http_code}" -H "Host: nav.yumiai.art" http://localhost/')
print("子域名访问状态码:", stdout.read().decode())

# 测试直接访问文件
print("\n测试直接访问index.html...")
stdin, stdout, stderr = client.exec_command('curl -s -o /dev/null -w "%{http_code}" -H "Host: nav.yumiai.art" http://localhost/index.html')
print("直接访问状态码:", stdout.read().decode())

client.close()
print("\n修复完成！")
