import paramiko

HOST = '106.55.106.28'
PORT = 22
USERNAME = 'ubuntu'
PASSWORD = 'Test2026.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)

# 修复Nginx配置
nginx_config = '''
server {
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
stdin, stdout, stderr = client.exec_command('sudo tee /etc/nginx/sites-available/nav << EOF\n' + nginx_config + 'EOF')
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

# 测试本地访问
print("\n测试本地访问...")
stdin, stdout, stderr = client.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost/')
print("本地访问状态码:", stdout.read().decode())

# 测试子域名访问
print("\n测试子域名访问...")
stdin, stdout, stderr = client.exec_command('curl -s -o /dev/null -w "%{http_code}" -H "Host: nav.yumiai.art" http://localhost/')
print("子域名访问状态码:", stdout.read().decode())

client.close()
print("\n修复完成！")
print("现在可以通过 http://nav.yumiai.art 访问网站")
