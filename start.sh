#!/bin/bash
cd /home/www/xiaomubiao_celery

source env/bin/activate

gunicorn -c gun.py manage:app
