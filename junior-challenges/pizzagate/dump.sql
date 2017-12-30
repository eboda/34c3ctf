CREATE DATABASE  IF NOT EXISTS `pizzagate` CHARACTER SET UTF8;

CREATE USER django@localhost IDENTIFIED BY 'yolofcfoobarbazkshia';

GRANT ALL PRIVILEGES ON pizzagate.* TO django@localhost;

FLUSH PRIVILEGES;

