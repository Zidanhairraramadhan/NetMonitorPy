import psutil

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    ram = psutil.virtual_memory()
    return ram.percent

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.percent