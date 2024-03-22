import subprocess
import shlex

botToken = "6346647213:AAHDh3xyuERffn90khG8IRzTLlV2-6oJ1pY"
chatid = 6530717979

def send_message(ip):
    url = f"https://api.telegram.org/bot{botToken}/sendMessage"
    data = "Detected suspicious activity from IP address: " + ip
    command = f'curl -X POST "{url}" -d "chat_id={chatid}" -d "text={data}"'
    args = shlex.split(command)
    subprocess.run(args)

