## 🔧 ¿Qué debes hacer ahora?


# Reemplaza:

* TU_TOKEN_AQUI pon el token de tu bot.

* 123456789 pon tu user_id de Telegram.

* tu_usuario por tu nombre de usuario en el servidor.

## Guarda el archivo:

* nano install_sshbot.sh

## Hazlo ejecutable y lánzalo:

chmod +x install_sshbot.sh
./install_sshbot.sh

✅ Qué hacer después
1.- Guarda este código como ssh_bot.py en tu servidor, en la ruta usada por tu script de instalación (/home/tu_usuario/sshbot/).

2.- Asegúrate de que el usuario especificado tenga permisos en sudoers para los comandos:
useradd, userdel, chpasswd, systemctl

3.- Reinicia el bot si ya tenías el servicio corriendo:
"""
sudo systemctl restart sshbot.service
"""
