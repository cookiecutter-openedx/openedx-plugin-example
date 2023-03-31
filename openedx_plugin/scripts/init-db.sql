DROP USER IF EXISTS `mp_user`@`localhost`;
DROP DATABASE IF EXISTS `openedx_plugin_example`;

CREATE USER `mp_user`@`localhost` IDENTIFIED BY 'mp';
CREATE DATABASE `openedx_plugin_example`;
GRANT ALL PRIVILEGES ON `openedx_plugin_example`.* TO "mp_user"@"localhost";
FLUSH PRIVILEGES;
