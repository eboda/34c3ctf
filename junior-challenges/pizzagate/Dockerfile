FROM ubuntu:17.10

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install curl zip

RUN apt-get -y install python3 python3-pip
RUN bash -c "debconf-set-selections <<< 'mysql-server mysql-server/root_password password hwqfi3t873r1qwdhqu1'"
RUN bash -c "debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password hwqfi3t873r1qwdhqu1'"
RUN apt-get -y install mysql-server libmysqlclient-dev 

ENV DOCKER 1
ADD flag /flag
RUN useradd flagisinrootinthefileflag
RUN pip3 install django gunicorn mysqlclient requests lxml pyyaml


ADD mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf
ADD dump.sql /tmp/dump.sql
RUN service mysql start && \
    mysql -uroot -phwqfi3t873r1qwdhqu1 < /tmp/dump.sql && \
    rm /tmp/dump.sql

COPY app /app


RUN service mysql start && \
    cd /app && \
    python3 manage.py migrate && \
    python3 manage.py loaddata users && \
    python3 manage.py loaddata pizzas && \
    python3 manage.py loaddata illuminati

CMD service mysql start && \
    cd /app && \
    (gunicorn pizzagate.wsgi --bind 0.0.0.0:31337 & \
    /bin/bash -i)
