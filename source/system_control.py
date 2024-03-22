import subprocess
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, Application

TOKEN = '6346647213:AAHDh3xyuERffn90khG8IRzTLlV2-6oJ1pY'

def remove_lines_with_value(file_path, value):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        with open(file_path, 'w') as file:
            for line in lines:
                if line.strip() != value:
                    file.write(line)
    except FileNotFoundError:
        print(f"File {file_path} not found")
    except IOError:
        print(f"Error reading or writing file '{file_path}")

async def set_command(update, context):
    global command
    command = ""
    await update.message.reply_text("Enter your command: ")

async def help_command(update, context):
    await update.message.reply_text("/help - List command \n/command - Remote to server\n/sayHi - Test for connection\n/blocked - Show blocked IP\n/unblock_all - Unblock all IP\n/unblock - Unblock an IP")

async def blocked_command(update, context):
    try:
        with open('blocked.txt', 'r') as f:
            f_content = f.read()
            if f_content == '':
                await update.message.reply_text('File is empty.')
            else:
                await update.message.reply_text(f_content)
    except FileNotFoundError:
        await update.message.reply_text("File 'blocked.txt' not found.")
    except IOError:
        await update.message.reply_text("Error reading file 'blocked.txt'.")

async def unblock_all_command(update, context):
    try:
        with open('blocked.txt', 'r') as f:
            lines = f.readlines()
            unique_addresses = set(lines)
            for line in unique_addresses:
                ipaddress = line.strip()
                command = f"echo 'kali' | sudo -S iptables -D INPUT -s {ipaddress} -j DROP"
                subprocess.check_output(command, shell=True)
        
        with open('blocked.txt', 'w') as f:
            f.write('')  # Clear the contents of the file
        
    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("Error reading file.")

async def say_hi(update, context):
    await update.message.reply_text('Connected to Server.')

async def handle_message(update, context):
    global command
    message = update.message.text
    if message.lower() == 'end':
        await update.message.reply_text("Command execution stopped.")
        command = ""
    else:
        try:
            if update.message.chat.id == 6530717979 and message != '':
                message = message.lower()
                if 'sudo' in message:
                    message.replace('sudo', '')
                    message = "echo 'kali' | sudo -S " + message
                    output = subprocess.check_output(message, shell=True)
                else:
                    output = subprocess.check_output(message, shell=True)
                if output is not None:
                    await update.message.reply_text(output.decode('utf-8'))
                else:
                    await update.message.reply_text("File empty.")
        except subprocess.CalledProcessError as e:
            await update.message.reply_text("Command execution failed: " + str(e))

async def unblock_command(update, context):
    # Extract the IP address from the command arguments
    if len(context.args) > 0:
        IP = context.args[0]
        try:
            command = f"echo 'kali' | sudo -S iptables -D INPUT -s {IP} -j DROP"
            subprocess.check_output(command, shell=True)
            remove_lines_with_value("blocked.txt", str(IP))
            await update.message.reply_text(f"Successfully unblocked IP: {IP}")
        except Exception as e:
            await update.message.reply_text(f"Failed to unblock IP: {IP}. Error: {str(e)}")
    else:
        await update.message.reply_text("Please provide an IP address to unblock.")

async def error(update, context):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    try:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler('command', set_command))
        app.add_handler(CommandHandler('help', help_command))
        app.add_handler(CommandHandler('sayHi', say_hi))
        app.add_handler(CommandHandler('blocked', blocked_command))
        app.add_handler(CommandHandler('unblock_all', unblock_all_command))
        app.add_handler(CommandHandler('unblock', unblock_command))
        app.add_handler(MessageHandler(filters.TEXT, handle_message))
        app.add_error_handler(error)
        app.run_polling(poll_interval=3)
    except:
        pass
