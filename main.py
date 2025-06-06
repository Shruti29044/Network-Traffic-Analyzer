# Install required packages
!pip install -q pyshark matplotlib
!apt update && apt install -y tshark
# ⬇️ Install TShark (required by PyShark)
!apt update && apt install -y tshark
!pip install -q pyshark matplotlib


# === Imports ===
import pyshark
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import os
from google.colab import files
import nest_asyncio
nest_asyncio.apply()

# === Step 1: Upload pcap file ===
print("📂 Please upload your .pcap file")
uploaded = files.upload()

# Assume the user uploaded a .pcap file
pcap_file = list(uploaded.keys())[0]
if not os.path.exists(pcap_file):
    raise FileNotFoundError(f"❌ File not found: {pcap_file}. Please upload it using the upload button.")

# === Step 2: Analyze pcap using PyShark (async-safe) ===
print("🔍 Analyzing packets...")
cap = pyshark.FileCapture(pcap_file, display_filter='ip')

# === Step 3: Extract and store traffic data ===
conn = sqlite3.connect("traffic_data.db")
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS traffic (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        src_ip TEXT,
        dst_ip TEXT,
        protocol TEXT
    )
''')

ip_filter = set()
time_series = {}

packet_limit = 200  # Cap analysis to avoid Colab crashes
count = 0

for pkt in cap:
    try:
        ts = str(datetime.fromtimestamp(float(pkt.sniff_timestamp)))
        src = pkt.ip.src
        dst = pkt.ip.dst
        proto = pkt.transport_layer or "N/A"

        cur.execute('INSERT INTO traffic (timestamp, src_ip, dst_ip, protocol) VALUES (?, ?, ?, ?)',
                    (ts, src, dst, proto))

        hour = ts[:13]  # e.g., '2024-06-01 14'
        time_series[hour] = time_series.get(hour, 0) + 1
        ip_filter.add(src)
        ip_filter.add(dst)

        count += 1
        if count >= packet_limit:
            break
    except Exception:
        continue

conn.commit()
cap.close()

# === Step 4: Show unique IPs seen ===
print(f"🧠 Unique IPs Detected: {len(ip_filter)}")
print(", ".join(list(ip_filter)[:5]), "..." if len(ip_filter) > 5 else "")

# === Step 5: Plot time-series traffic ===
plt.figure(figsize=(10, 5))
sorted_times = sorted(time_series.items())
x = [t[0] for t in sorted_times]
y = [t[1] for t in sorted_times]
plt.plot(x, y, marker='o')
plt.xticks(rotation=45)
plt.xlabel("Time (hour)")
plt.ylabel("Packets")
plt.title("📊 Network Traffic Over Time")
plt.tight_layout()
plt.grid(True)
plt.show()

# === Step 6: Sample SQL query output ===
print("\n📋 Top 5 Protocol Counts:")
for row in cur.execute("SELECT protocol, COUNT(*) FROM traffic GROUP BY protocol ORDER BY COUNT(*) DESC LIMIT 5"):
    print(f"{row[0]}: {row[1]} packets")

conn.close()
