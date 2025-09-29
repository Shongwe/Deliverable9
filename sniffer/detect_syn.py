from scapy.all import sniff, TCP, IP
from collections import Counter
import time, json, os, signal, sys

OUT = "/app/syn_counts.json"
counter = Counter()
window = 10  # seconds to aggregate
last_dump = time.time()

def dump_counts():
    global last_dump
    now = time.time()
    if now - last_dump >= window:
        with open(OUT, "w") as f:
            json.dump(counter, f, indent=2)
        last_dump = now
        print(f"[+] Dumped SYN counts at {time.strftime('%X')}")

def pkt_cb(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(IP):
        tcp = pkt.getlayer(TCP)
        ip = pkt.getlayer(IP)
        if tcp.flags & 0x02:  # SYN bit
            key = (ip.dst, tcp.dport)
            counter[key] += 1
            dump_counts()

def handle_exit(sig, frame):
    print("[!] Sniffer shutting down...")
    with open(OUT, "w") as f:
        json.dump(counter, f, indent=2)
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

print("[*] Starting SYN sniffer...")
sniff(prn=pkt_cb, store=False, filter="tcp", timeout=0)