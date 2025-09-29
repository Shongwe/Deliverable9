# GothamDataset2025: A Reproducible Large-Scale IoT Network Dataset for Intrusion Detection and Security Research

The dataset simulates a large-scale IoT network using the Gotham testbed, offering a realistic environment for network security research. It includes normal traffic generated with protocols such as MQTT, CoAP, and RTSP, alongside diverse attack scenarios, including port scanning, brute force, and DoS. This enables researchers to study the complexities of security mechanisms tailored to large-scale IoT networks.

The dataset includes several cybersecurity attacks: DoS, Remote Command Execution, Ingress Tool Transfer, Reporting, Telnet Brute Forcing, Network Scanning, Periodic C&C Communication, Remote Code Execution, and CoAP Amplification Attack. It is a multi-class dataset, where each row represents a network packet and contains 23 features along with a label field.

The dataset is fully extensible and reproducible as it relies on the open-source Gotham testbed, making it adaptable to emerging threats. Researchers can replicate experiments, integrate new IoT devices, and expand attack scenarios over time under consistent conditions. Furthermore, the processing and labelling pipeline is shared on GitHub to provide clear and reusable tools for dataset creation.


## Dataset Structure
The dataset is organised into a hierarchical structure to support scalability and facilitate distributed learning and decentralised analysis.

```
    ├── raw/
    │   ├── benign/
    │   │   ├── air-quality-1.pcap
    │   │   ├── building-monitor-1.pcap
    │   │   ├── ...
    │   │   ├── ...
    │   │   └── city-power-1.pcap
    │   │
    │   ├── malicious/
    │   │   ├── coap-amplification/
    │   │   ├── merlin/
    │   │   ├── mirai-dos/
    │   │   ├── mirai-infection/
    │   │   ├── network-scanning/
    │   │
    │   └── metadata/
    │       ├── metadata-coap-amplificator.json
    │       ├── metadata-network-scanning.json
    │       ├── metadata-merlin.json
    │       ├── metadata-mirai-dos.json
    │       ├── metadata-mirai-infection.json
    │       └── metadata-normal.json
    │
    ├── processed/
    │       ├── air-quality-1.csv
    │       ├── building-monitor-1.csv
    │       ├── ...
    │       ├── ...
    │       └── city-power-1.csv
    │
    └── README.md
```

### Subfolders and Files

-	**Raw Data**: This folder contains the original PCAP files of network traces collected using tcpdump. Each PCAP file corresponds to the network traffic for a specific IoT device during a given scenario. Subfolders are categorised by scenario:
    -	`Benign`: Contains PCAP files representing normal traffic.
    -	`Malicious`: Contains PCAP files categorised by attack type (e.g., Mirai DoS, CoAP amplification).
    -   `Metadata`: contains files used for labelling the network traffic. The metadata provides contextual information, such as device IP addresses, timestamps, and scenario descriptions, ensuring accurate and reproducible labelling.

-	**Processed Data**: This folder contains CSV files derived from the Raw Data. Each CSV file includes feature vectors extracted from network packets, converting unstructured packet data into a structured format ready for machine learning or statistical analysis.


## Use Cases


Researchers can leverage this dataset to develop various cybersecurity systems such as intrusion detection sytems, malware detection, privacy-preservation, adversarial machine learning, etc... 


## Contact

For more information, questions, or support, please contact:
- Name: Othmane Belarbi
- Affiliation: Cardiff University, School of Computer Science & Informatics
- Email: BelarbiO@cardiff.ac.uk

---
Thank you for using this dataset. Your feedback and contributions are welcome to improve its quality and extensibility.

