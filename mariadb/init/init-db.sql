CREATE DATABASE IF NOT EXISTS web_db; 
CREATE USER 'web_user' IDENTIFIED BY 'web_user_password';
GRANT USAGE ON *.* TO 'web_user'@localhost IDENTIFIED BY 'web_user_password';
GRANT USAGE ON *.* TO 'web_user'@'%' IDENTIFIED BY 'web_user_password';
GRANT ALL privileges ON `web_db`.* TO 'web_user'@'%';
FLUSH PRIVILEGES;
