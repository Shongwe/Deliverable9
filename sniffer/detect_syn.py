import joblib
import scapy.all as scapy
import numpy as np
import time
import os
import requests
import pandas as pd
import statistics
import logging
import subprocess

try:
    subprocess.run(["ip", "link", "set", "eth0", "promisc", "on"], check=True)
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("Promiscuous mode enabled on eth0.")
except Exception as e:
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.error(f"Failed to enable promiscuous mode: {e}")

if not os.path.exists("/sys/class/net/eth0"):
    logging.error("eth0 interface not found. Exiting.")
    exit(1)

try:
    model = joblib.load('model.pkl')
    logging.info("Sniffer started on eth0. Model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    exit(1)

flows = {}
FLOW_TIMEOUT = 5

def get_flow_key(pkt):
    ip = pkt[scapy.IP]
    tcp = pkt[scapy.TCP]
    return (ip.src, ip.dst, tcp.sport, tcp.dport, ip.proto)

def update_flow(pkt):
    key = get_flow_key(pkt)
    now = time.time()

    if key not in flows:
        flows[key] = {
            'start': now,
            'last': now,
            'fwd_lengths': [],
            'bwd_lengths': [],
            'fwd_win_bytes': [],
            'bwd_win_bytes': [],
            'fwd_count': 0,
            'bwd_count': 0,
            'bwd_psh_flags': 0,
            'iat_times': [],
            'last_pkt_time': None
        }
        logging.debug(f"New flow started: {key}")

    flow = flows[key]
    flow['last'] = now

    length = pkt[scapy.IP].len
    win = pkt[scapy.TCP].window
    src = pkt[scapy.IP].src

    if src == key[0]: 
        flow['fwd_lengths'].append(length)
        flow['fwd_win_bytes'].append(win)
        flow['fwd_count'] += 1
    else:  
        flow['bwd_lengths'].append(length)
        flow['bwd_win_bytes'].append(win)
        flow['bwd_count'] += 1
        if pkt[scapy.TCP].flags & 0x08:  
            flow['bwd_psh_flags'] += 1

    if flow['last_pkt_time']:
        flow['iat_times'].append(now - flow['last_pkt_time'])
    flow['last_pkt_time'] = now

def expire_flows():
    now = time.time()
    expired = [k for k, v in flows.items() if now - v['last'] > FLOW_TIMEOUT]
    for key in expired:
        flow = flows.pop(key)
        duration = flow['last'] - flow['start']
        total_pkts = flow['fwd_count'] + flow['bwd_count']
        total_bytes = sum(flow['fwd_lengths']) + sum(flow['bwd_lengths'])

        feat_values = {
            'Init_Win_bytes_forward': flow['fwd_win_bytes'][0] if flow['fwd_win_bytes'] else 0,
            'Packet Length Mean': statistics.mean(flow['fwd_lengths'] + flow['bwd_lengths']) if total_pkts > 0 else 0,
            'Bwd Packet Length Max': max(flow['bwd_lengths']) if flow['bwd_lengths'] else 0,
            'Bwd Packet Length Mean': statistics.mean(flow['bwd_lengths']) if flow['bwd_lengths'] else 0,
            'Fwd Packet Length Mean': statistics.mean(flow['fwd_lengths']) if flow['fwd_lengths'] else 0,
            'Fwd Packet Length Min': min(flow['fwd_lengths']) if flow['fwd_lengths'] else 0,
            'Fwd Packet Length Max': max(flow['fwd_lengths']) if flow['fwd_lengths'] else 0,
            'Fwd Packet Length Std': statistics.pstdev(flow['fwd_lengths']) if len(flow['fwd_lengths']) > 1 else 0,
            'Total Length of Fwd Packets': sum(flow['fwd_lengths']),
            'min_seg_size_forward': min(flow['fwd_lengths']) if flow['fwd_lengths'] else 0,
            'Down/Up Ratio': (flow['bwd_count'] / flow['fwd_count']) if flow['fwd_count'] > 0 else 0,
            'Bwd Packet Length Min': min(flow['bwd_lengths']) if flow['bwd_lengths'] else 0,
            'Flow Duration': duration,
            'Total Fwd Packets': flow['fwd_count'],
            'Flow Bytes/s': (total_bytes / duration) if duration > 0 else 0,
            'Bwd Packet Length Std': statistics.pstdev(flow['bwd_lengths']) if len(flow['bwd_lengths']) > 1 else 0,
            'Bwd Packets/s': (flow['bwd_count'] / duration) if duration > 0 else 0,
            'Bwd PSH Flags': flow['bwd_psh_flags'],
            'Bwd Avg Bytes/Bulk': (sum(flow['bwd_lengths']) / flow['bwd_count']) if flow['bwd_count'] > 0 else 0,
            'Fwd Avg Bytes/Bulk': (sum(flow['fwd_lengths']) / flow['fwd_count']) if flow['fwd_count'] > 0 else 0,
            'Bwd Avg Packets/Bulk': flow['bwd_count'],
            'Bwd Avg Bulk Rate': (flow['bwd_count'] / duration) if duration > 0 else 0,
            'Fwd Avg Bulk Rate': (flow['fwd_count'] / duration) if duration > 0 else 0,
            'Active Min': min(flow['iat_times']) if flow['iat_times'] else 0,
            'Bwd IAT Min': min(flow['iat_times']) if flow['iat_times'] else 0,
            'Active Std': statistics.pstdev(flow['iat_times']) if len(flow['iat_times']) > 1 else 0
        }

        try:
            df = pd.DataFrame([feat_values], columns=model.feature_names_in_)
            logging.debug(f"Extracted features for flow {key}: {feat_values}")
            pred = model.predict(df)
            label = 'SYN Flood' if pred[0] == 1 else 'Benign'
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(flow['last']))
            logging.info(f"[{label}] {timestamp} | Flow from {key[0]} to {key[1]} ({total_pkts} packets, duration {duration:.2f}s)")
            send_alert(label, key, flow)
        except Exception as e:
            logging.error(f"Failed to classify flow {key}: {e}")

def process(pkt):
    if pkt.haslayer(scapy.TCP) and pkt.haslayer(scapy.IP):
        update_flow(pkt)
        expire_flows()

def send_alert(label, key, flow):
    alert = {
        "device": f"flow-{key[0]}",
        "type": label,
        "packet_count": flow['fwd_count'] + flow['bwd_count'],
        "duration": round(flow['last'] - flow['start'], 2),
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(flow['last']))
    }
    try:
        response = requests.post("http://dashboard:5002/alert", json=alert)
        logging.info(f"Alert sent to dashboard: {response.status_code} | {alert}")
    except Exception as e:
        logging.error(f"Failed to send alert for flow {key}: {e}")

logging.info("Available interfaces: %s", scapy.get_if_list())
scapy.sniff(iface="eth0", prn=process, store=0)
