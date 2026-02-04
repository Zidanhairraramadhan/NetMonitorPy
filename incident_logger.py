import os
from datetime import datetime

INCIDENT_FILE = "incident_log.txt"
_last_health = None
_last_network = None

# buat file jika belum ada
if not os.path.isfile(INCIDENT_FILE):
    with open(INCIDENT_FILE, "w") as f:
        f.write("=== Incident Log Initialized ===\n")



def log_incident(message):
    with open(INCIDENT_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")


def detect_incident(health_status, network_connected):
    global _last_health, _last_network
    incidents = []

    # Health incident
    if health_status == "CRITICAL" and _last_health != "CRITICAL":
        incidents.append("SYSTEM CRITICAL")

    if health_status == "HEALTHY" and _last_health in ["WARNING", "CRITICAL"]:
        incidents.append("SYSTEM RECOVERED (HEALTHY)")

    # Network incident
    if network_connected is False and _last_network is not False:
        incidents.append("NETWORK DISCONNECTED")

    if network_connected is True and _last_network is False:
        incidents.append("NETWORK RECONNECTED")

    _last_health = health_status
    _last_network = network_connected

    return incidents