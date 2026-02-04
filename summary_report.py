import os
from datetime import datetime

INCIDENT_FILE = "incident_log.txt"
SUMMARY_FILE = "executive_summary.txt"

def generate_summary(stats):
    net_inc = 0
    sys_inc = 0

    if os.path.isfile(INCIDENT_FILE):
        with open(INCIDENT_FILE) as f:
            for line in f:
                if "NETWORK" in line:
                    net_inc += 1
                if "SYSTEM" in line:
                    sys_inc += 1

    report = f"""
EXECUTIVE SUMMARY
=================
Generated At        : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Monitoring Duration : {stats['duration']}

System Health Final : {stats['final_health']}

Average CPU Usage   : {stats['avg_cpu']:.2f} %
Average RAM Usage   : {stats['avg_ram']:.2f} %
Average Disk Usage  : {stats['avg_disk']:.2f} %

Network Incidents   : {net_inc}
System Incidents    : {sys_inc}

Overall Conclusion:
{"Sistem stabil dan layak digunakan." if net_inc + sys_inc < 3 else "Sistem mengalami beberapa gangguan."}
"""

    with open(SUMMARY_FILE, "w") as f:
        f.write(report.strip())

    return "Executive summary berhasil dibuat"