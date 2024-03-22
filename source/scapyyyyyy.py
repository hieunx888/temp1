from scapy.all import *
from sqli_detect import *
from extract_POST_content import *
from extract_GET_content import *
from sqli_detect import detectSQLi
from xss_detect import detectXSS
from command_injection_detect import detectCommandInjection
from warning import send_message
import subprocess

IP_list = []
counter = []
payload_list = []

def write_to_File(ip):
	f = open("blocked.txt", 'a')
	f.write(ip)
	f.close()


def payloadCheck(ip_src, processData):
	if ip_src not in IP_list:
		IP_list.append(ip_src)
		counter.append(0)
		payload_list.append(processData)
	if ip_src in IP_list:
		position = IP_list.index(ip_src)
		counter[position] += 1
		payload_list[position].append(processData)
		print(counter[position])
		if counter[position] == 10:
			send_message(str(ip_src))
			write_to_File(ip_src + "\n")
			subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip_src, '-j', 'DROP'])
	print(IP_list, counter, payload_list)

def packet_handler(packet):
	if packet[TCP].dport == 80 and packet.haslayer(Raw):
		try:
			data = str((packet[Raw].load).decode('utf-8'))
			ip_src = str(packet[IP].src)
			if data[:4] == 'POST':
				try:
					print((packet[Raw].load).decode('utf-8'))
					processData = extract_input_fields(data)
					for value in processData:
						if detectSQLi(value):
							print("SQLi detected: " + value)
							payloadCheck(ip_src, processData)
						if detectXSS(value):
							payloadCheck(ip_src, processData)
							print("XSS detected: " + value)
						if detectCommandInjection(value):
							payloadCheck(ip_src, processData)
							print("Command Injection Detected: " + value)
				except:
					pass
			if data[:3] == 'GET':
				try:
					print((packet[Raw].load).decode('utf-8'))
					processData = extract_input_fields(data)
					for value in processData:
						if detectSQLi(value):
							print("SQLi detected: " + value)
							payloadCheck(ip_src, processData)
						if detectXSS(value):
							payloadCheck(ip_src, processData)
							print("XSS detected: " + value)
						if detectCommandInjection(value):
							payloadCheck(ip_src, processData)
							print("Command Injection Detected: " + value)
				except:
					pass
				pass
		except:
			pass

# Set the filter expression to capture HTTP traffic on port 80
filter_expr = "tcp port 80"

# Start capturing packets
sniff(filter=filter_expr, prn=packet_handler)
