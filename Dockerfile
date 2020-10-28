FROM ubuntu:16.04
MAINTAINER aniulee@qq.com
RUN mkdir /home/www
COPY docker_start.sh /home/www
RUN apt-get update && apt-get install -y tzdata python3.5 python3-pip libmysqlclient-dev python3-dev supervisor
COPY docs/supervisors.conf /etc/supervisor/conf.d/supervisord.conf
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo "Asia/Shanghai" > /etc/timezone
CMD ["sh","/home/www/docker_start.sh"]
EXPOSE 80