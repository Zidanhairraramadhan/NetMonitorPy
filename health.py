def evaluate_health(cpu, ram, disk):
    status = "Healthy"
    color = "green"

    if cpu > 85 or ram > 90 or disk > 90:
        status = "Critical"
        color = "red"
    elif cpu > 60 or ram > 70 or disk > 75:
        status = "Warning"
        color = "orange"

    return status, color