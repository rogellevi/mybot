#!/bin/bash

# CONFIGURA ESTOS VALORES:
TOKEN="TU_TOKEN_AQUI"
AUTHORIZED_USER_ID="123456789"
BOT_USER="tu_usuario"
BOT_DIR="/home/$BOT_USER/sshbot"
SERVICE_FILE="/etc/systemd/system/sshbot.service"

# Instalar dependencias
sudo apt update
sudo apt install -y python3 python3-pip

# Instalar librería Telegram
pip3 install python-telegram-bot --quiet

# Crear directorio
mkdir -p "$BOT_DIR"
chown "$BOT_USER":"$BOT_USER" "$BOT_DIR"

# Crear script Python
cat > "$BOT_DIR/ssh_bot.py" <<EOL
# (Código Python completo aquí — lo puedes copiar desde mi mensaje anterior)
EOL

# Cambiar permisos
chown "$BOT_USER":"$BOT_USER" "$BOT_DIR/ssh_bot.py"
chmod +x "$BOT_DIR/ssh_bot.py"

# Configurar sudoers
USERADD=\$(which useradd)
USERDEL=\$(which userdel)
CHPASSWD=\$(which chpasswd)
SYSTEMCTL=\$(which systemctl)
echo "$BOT_USER ALL=(ALL) NOPASSWD: \$USERADD, \$USERDEL, \$CHPASSWD, \$SYSTEMCTL" | sudo tee /etc/sudoers.d/sshbot
sudo chmod 440 /etc/sudoers.d/sshbot

# Crear archivo systemd
sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Bot Telegram SSH Avanzado
After=network.target

[Service]
User=$BOT_USER
WorkingDirectory=$BOT_DIR
ExecStart=/usr/bin/python3 $BOT_DIR/ssh_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Activar servicio
sudo systemctl daemon-reload
sudo systemctl enable sshbot.service
sudo systemctl start sshbot.service

echo "✅ Bot instalado y ejecutándose."
echo "Usa /help en Telegram para ver comandos disponibles."
