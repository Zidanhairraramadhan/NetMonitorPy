import psutil
import time
import socket
import csv
from datetime import datetime
import os

LOG_FILE = "network_log.csv"
REPORT_FILE = "laporan_monitoring.txt"


def get_network_speed(interval=1):
    net1 = psutil.net_io_counters()
    time.sleep(interval)
    net2 = psutil.net_io_counters()

    upload = net2.bytes_sent - net1.bytes_sent
    download = net2.bytes_recv - net1.bytes_recv

    return upload, download


def check_connection(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False


def log_network(status, download_kb, upload_kb):
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "status",
                "download_kbps",
                "upload_kbps"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status,
            f"{download_kb:.2f}",
            f"{upload_kb:.2f}"
        ])


def export_report():
    if not os.path.isfile(LOG_FILE):
        return "Belum ada data monitoring."

    rows = []
    total_down = 0
    total_up = 0
    connected = 0
    disconnected = 0

    with open(LOG_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
            total_down += float(row["download_kbps"])
            total_up += float(row["upload_kbps"])
            if row["status"] == "Connected":
                connected += 1
            else:
                disconnected += 1

    if len(rows) == 0:
        return "Data kosong."

    start_time = rows[0]["timestamp"]
    end_time = rows[-1]["timestamp"]
    avg_down = total_down / len(rows)
    avg_up = total_up / len(rows)

    laporan = f"""
LAPORAN MONITORING JARINGAN
===========================

Waktu Mulai   : {start_time}
Waktu Selesai : {end_time}
Total Data    : {len(rows)} baris

Rata-rata Download : {avg_down:.2f} KB/s
Rata-rata Upload   : {avg_up:.2f} KB/s

Status Koneksi:
- Connected    : {connected} kali
- Disconnected : {disconnected} kali

Kesimpulan:
Jaringan berada dalam kondisi {"stabil" if disconnected < connected else "kurang stabil"}.
"""

    with open(REPORT_FILE, "w") as file:
        file.write(laporan.strip())

    # reset data agar test berikutnya fresh
    os.remove(LOG_FILE)

    return "Laporan berhasil diexport & data direset"
def reset_log():
    if os.path.isfile(LOG_FILE):
        os.remove(LOG_FILE)

def init_network_log():
    if not os.path.isfile(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "status", "download", "upload"])       
