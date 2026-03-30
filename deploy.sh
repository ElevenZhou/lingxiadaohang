#!/bin/bash

# 创建网站目录
mkdir -p /home/ubuntu/lingxia_nav

# 上传文件
scp -r index.html data.json ubuntu@106.55.106.28:/home/ubuntu/lingxia_nav/

# 启动本地服务器
ssh ubuntu@106.55.106.28 'cd /home/ubuntu/lingxia_nav && python3 -m http.server 8000 &'

echo "部署完成！网站地址: http://106.55.106.28:8000"
