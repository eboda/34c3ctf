CREATE DATABASE  IF NOT EXISTS `quaker` CHARACTER SET UTF8;

CREATE USER django@localhost IDENTIFIED BY 'kneelbeforethealmightyshia';

GRANT ALL PRIVILEGES ON quaker.* TO django@localhost;

FLUSH PRIVILEGES;

