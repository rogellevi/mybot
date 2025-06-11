import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# === CONFIGURA TU TOKEN Y USUARIOS AUTORIZADOS ===
TOKEN = "TU_TOKEN_AQUI"  # ← Reemplaza con el token de BotFather
AUTHORIZED_USERS = {123456789}  # ← Reemplaza con tu Telegram user_id (puedes añadir más separados por coma)

# === DECORADOR DE SEGURIDAD ===
def restricted(func):
    def wrapped(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in AUTHORIZED_USERS:
            update.message.reply_text("❌ No tienes permiso para usar este bot.")
            return
        return func(update, context, *args, **kwargs)
    return wrapped

# === COMANDOS ===
@restricted
def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Bot SSH avanzado activo. Usa /help para ver los comandos disponibles.")

@restricted
def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("""
🛠 Comandos disponibles:
/adduser <usuario> <contraseña> - Crear usuario SSH
/deluser <usuario> - Eliminar usuario SSH
/changepass <usuario> <nueva> - Cambiar contraseña
/listusers - Listar usuarios en /home
/sshstatus - Ver estado del servicio SSH
/restartssh - Reiniciar servicio SSH
/disk - Ver uso de disco en /home
/help - Mostrar esta ayuda
""")

@restricted
def add_user(update: Update, context: CallbackContext):
    try:
        user, password = context.args[0], context.args[1]
        subprocess.run(['sudo', 'useradd', '-m', '-s', '/bin/bash', user], check=True)
        subprocess.run(['sudo', 'chpasswd'], input=f"{user}:{password}".encode(), check=True)
        update.message.reply_text(f"✅ Usuario {user} creado.")
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

@restricted
def del_user(update: Update, context: CallbackContext):
    try:
        user = context.args[0]
        subprocess.run(['sudo', 'userdel', '-r', user], check=True)
        update.message.reply_text(f"✅ Usuario {user} eliminado.")
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

@restricted
def change_pass(update: Update, context: CallbackContext):
    try:
        user, password = context.args[0], context.args[1]
        subprocess.run(['sudo', 'chpasswd'], input=f"{user}:{password}".encode(), check=True)
        update.message.reply_text(f"🔐 Contraseña de {user} cambiada.")
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

@restricted
def list_users(update: Update, context: CallbackContext):
    try:
        users = subprocess.check_output("ls /home", shell=True).decode().split()
        update.message.reply_text("👥 Usuarios:\n" + "\n".join(users))
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

@restricted
def ssh_status(update: Update, context: CallbackContext):
    try:
        status = subprocess.check_output(['systemctl', 'is-active', 'ssh']).decode().strip()
        update.message.reply_text(f"🔌 Servicio SSH: {status}")
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

@restricted
def restart_ssh(update: Update, context: CallbackContext):
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', 'ssh'], check=True)
        update.message.reply_text("🔄 SSH reiniciado.")
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

@restricted
def disk_usage(update: Update, context: CallbackContext):
    try:
        usage = subprocess.check_output(['df', '-h', '/home']).decode()
        update.message.reply_text(f"💾 Uso de disco:\n{usage}")
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

# === INICIALIZACIÓN DEL BOT ===
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("adduser", add_user))
    dp.add_handler(CommandHandler("deluser", del_user))
    dp.add_handler(CommandHandler("changepass", change_pass))
    dp.add_handler(CommandHandler("listusers", list_users))
    dp.add_handler(CommandHandler("sshstatus", ssh_status))
    dp.add_handler(CommandHandler("restartssh", restart_ssh))
    dp.add_handler(CommandHandler("disk", disk_usage))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
