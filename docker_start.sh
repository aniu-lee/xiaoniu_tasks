#!/bin/bash
export C_FORCE_ROOT="true"
cd /home/www
pip3 install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt
if [ ! -d "migrations" ];then
python3 manage.py db init
python3 manage.py db migrate -m "init"
python3 manage.py db upgrade
fi
/etc/init.d/supervisor start