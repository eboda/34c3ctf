FROM ubuntu:17.10

RUN bash -c "debconf-set-selections <<< 'mysql-server mysql-server/root_password password FUCKmyL1f3AZiwqecq'"
RUN bash -c "debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password FUCKmyL1f3AZiwqecq'"

RUN apt-get -y update && apt-get -y install curl wget zip 

# apache & php & stuff
RUN apt-get -y install apache2 apt-transport-https curl wget zip php php-curl php-pclzip libapache2-mod-php mysql-server php-mysql p7zip-full vim-common cron

ENV WEBROOT /var/www/html
ENV MYSQL_USER=mysql
RUN rm /var/www/html/index.html

ADD mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf

ADD dump.sql /tmp/
RUN service mysql start; mysql -u root -pFUCKmyL1f3AZiwqecq < /tmp/dump.sql && rm /tmp/dump.sql

# challenge files and configs
RUN (crontab -l ; echo "*/5 * * * * rm -r /var/www/html/files/* ; touch /var/www/html/files/index.php";\
        echo "*/5 * * * * rm -r /tmp/* && touch /tmp/index.php") | crontab -
ADD 000-default.conf /etc/apache2/sites-enabled/000-default.conf
ADD webroot/ /var/www/html/
RUN touch /tmp/index.php
RUN useradd extract0r -m
ADD files/create_a_backup_of_my_supersecret_flag.sh /home/extract0r/
RUN chown -R www-data /var/www/html/files && \
    chown extract0r:extract0r /home/extract0r/create_a_backup_of_my_supersecret_flag.sh


CMD service mysql start; service cron start; echo 'INSERT INTO flag.flag VALUES("34C3_you_Extr4cted_the_unExtract0ble_plUs_you_knoW_s0me_SSRF");' | mysql -u root -pFUCKmyL1f3AZiwqecq; service apache2 start;  /bin/bash
