Network Traffic Analyzer 

This project analyzes .pcap files using Python, PyShark (a wrapper for TShark), and visualizes traffic trends over time. It also stores packet-level metadata in a SQLite database for simple querying — all inside a Google Colab notebook.

🚀 Features

✅ Upload and parse .pcap files

✅ Extract timestamp, IPs, and protocols from each packet

✅ Store parsed data in SQLite (traffic_data.db)

✅ Plot time-series of packet flow per hour

✅ List unique IPs and top-used protocols

✅ Handles limited packets to avoid Colab memory crashes

📦 Requirements

These are automatically installed in the notebook:

!apt update && apt install -y tshark     # TShark CLI (required by PyShark)
!pip install -q pyshark matplotlib       # Python libraries

📁 How It Works

Upload PCAP File: User uploads a packet capture file via Colab file picker.

TShark Analysis: pyshark.FileCapture extracts IP packets and metadata.

SQLite Storage: Stores each packet's timestamp, source IP, destination IP, and protocol.

IP Tracking: Tracks all unique IPs seen in the session.

Time-Series Plot: Generates a Matplotlib graph showing packet volume over time.

SQL Queries: Outputs top 5 protocols by packet count.

📊 Output Example

📂 Please upload your .pcap file

🧠 Unique IPs Detected: 48

Time-Series Plot: Packets per hour

Top Protocols:

TCP: 124 packets

UDP: 87 packets

ICMP: 3 packets

🛠 Technologies Used 

Python

PyShark

SQLite

Matplotlib

Google Colab

TShark (Wireshark backend)

🧪 Sample PCAP Files

If you don’t have one, you can find .pcap samples at:

Wireshark Sample Captures

(https://wiki.wireshark.org/SampleCaptures)

PacketLife.net Capture Library

⚠️ Notes

Only ~200 packets are processed per run to keep Colab stable.

TShark must be installed via apt or the notebook will fail.

The tool uses display_filter='ip' to focus on IP traffic.

⚠️ Challenges Faced

📦 Installing TShark in Colab

PyShark depends on the tshark binary, which is not preinstalled in Colab.

Required manual installation using !apt install -y tshark.

❌ TSharkNotFoundException

Even after installing, PyShark sometimes fails to find tshark due to PATH issues.

Needed to ensure TShark is accessible via system paths.

🧠 Event Loop RuntimeError

PyShark uses asyncio, which conflicts with Colab’s already-running event loop.

Required using nest_asyncio.apply() to allow async code execution in notebooks.

📁 FileNotFoundError for .pcap Upload

If a user forgets to upload a .pcap file or provides the wrong filename, the program fails.

Needed robust file existence checks and user instructions.

💥 Colab RAM Limits

Processing full .pcap files caused memory crashes due to Colab’s RAM limits.

Solved by limiting analysis to the first 200 packets (packet_limit = 200).

🧪 Parsing Errors

Not all packets contain complete IP or transport layer info.

Wrapped parsing code in try/except to skip malformed packets gracefully.

🔄 Packet Timing Resolution

pkt.sniff_timestamp sometimes threw errors if not casted properly.

Required conversion using float() and datetime.fromtimestamp().

📉 Matplotlib Plot Readability

Time-series plots had x-axis overlap or unreadable tick marks.

Resolved with rotation and layout adjustments.

🧬 Protocol Layer Access Issues

Some packets lacked transport_layer attributes (like ARP).

Needed default fallback to "N/A" if the attribute was missing.

🔎 SQL Query Consistency

Ensuring consistent schema and avoiding redundant inserts required table existence checks.





