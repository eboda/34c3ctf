FROM ubuntu:17.10

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install curl zip

RUN apt-get -y install python3 python3-pip
RUN bash -c "debconf-set-selections <<< 'mysql-server mysql-server/root_password password hwqfi3t873r1qwdhqu1'"
RUN bash -c "debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password hwqfi3t873r1qwdhqu1'"
RUN apt-get -y install mysql-server libmysqlclient-dev 

ENV DOCKER 1

# install phantomjs
RUN apt-get -y install bzip2 libfreetype6 libfontconfig wget
ENV PHANTOMJS_VERSION 2.1.1
RUN mkdir -p /srv/var && \
    wget --local-encoding=UTF-8 --no-check-certificate -O /tmp/phantomjs-$PHANTOMJS_VERSION-linux-x86_64.tar.bz2 https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-$PHANTOMJS_VERSION-linux-x86_64.tar.bz2 && \
    tar -xjf /tmp/phantomjs-$PHANTOMJS_VERSION-linux-x86_64.tar.bz2 -C /tmp && \
    rm -f /tmp/phantomjs-$PHANTOMJS_VERSION-linux-x86_64.tar.bz2 && \
    mv /tmp/phantomjs-$PHANTOMJS_VERSION-linux-x86_64/ /srv/var/phantomjs && \
    ln -s /srv/var/phantomjs/bin/phantomjs /usr/bin/phantomjs

RUN pip3 install django gunicorn mysqlclient requests pyyaml 

RUN apt-get -y install nginx

COPY mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf
COPY dump.sql /tmp/dump.sql
RUN service mysql start && \
    mysql -uroot -phwqfi3t873r1qwdhqu1 < /tmp/dump.sql && \
    rm /tmp/dump.sql

COPY app /app
COPY scripts/run.sh /run.sh
COPY nginx/default /etc/nginx/sites-enabled/default
RUN chmod +x /run.sh


RUN service mysql start && \
    cd /app && \
    python3 manage.py migrate && \
    python3 manage.py loaddata admin

CMD service mysql start && \
    service nginx start && \
    cd /app && \
    (gunicorn quaker.wsgi --bind 0.0.0.0:80 & \
    /run.sh >> /tmp/adminvisit.log &  \
    /bin/bash -i)
