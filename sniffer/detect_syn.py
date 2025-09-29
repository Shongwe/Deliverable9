from scapy.all import sniff, TCP, IP
from collections import Counter
import time, json, os

OUT = "/app/syn_counts.json"
counter = Counter()
window = 10  # seconds to aggregate
last_dump = time.time()

def pkt_cb(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(IP):
        tcp = pkt.getlayer(TCP)
        ip = pkt.getlayer(IP)
        if tcp.flags & 0x02:  # SYN bit
            key = (ip.dst, tcp.dport)
            counter[key] += 1

sniff(prn=pkt_cb, store=False, filter="tcp", timeout=0)  # runs indefinitely

# note: this simple script counts SYNs per dest:port in memory.
# You can adapt to periodically write to disk or trigger alerts.
