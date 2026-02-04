import tkinter as tk
import time
from PIL import ImageGrab
from datetime import datetime
from monitor import get_network_speed, check_connection, log_network, reset_log, init_network_log
from system_monitor import get_cpu_usage, get_ram_usage, get_disk_usage
from health import evaluate_health
from incident_logger import detect_incident, log_incident
from summary_report import generate_summary

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def __init__(self, root):
    self.root = root
    init_network_log()

class NetHealthMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NetHealth Monitor")
        self.root.geometry("860x640")

        self.running = True
        self.start_time = time.time()
        self.cpu_h, self.ram_h, self.disk_h = [], [], []
        self.final_health = "UNKNOWN"

        self.status = tk.Label(root, text="Network: Checking", font=("Arial", 12, "bold"))
        self.status.pack()

        self.cpu = tk.Label(root, text="CPU: 0%")
        self.cpu.pack()
        self.ram = tk.Label(root, text="RAM: 0%")
        self.ram.pack()
        self.disk = tk.Label(root, text="Disk: 0%")
        self.disk.pack()

        self.health = tk.Label(root, text="System Health: -", font=("Arial", 13, "bold"))
        self.health.pack()

        self.incident = tk.Label(root, text="Last Incident: -", fg="red")
        self.incident.pack()

        self.down = tk.Label(root, text="Download: 0 KB/s")
        self.down.pack()
        self.up = tk.Label(root, text="Upload: 0 KB/s")
        self.up.pack()

        self.download_data, self.upload_data = [], []
        self.fig = Figure(figsize=(7, 3))
        self.ax = self.fig.add_subplot(111)
        self.line_d, = self.ax.plot([], [])
        self.line_u, = self.ax.plot([], [])
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        btn = tk.Frame(root)
        btn.pack()

        tk.Button(btn, text="Start", width=12, command=self.start).grid(row=0, column=0)
        tk.Button(btn, text="Stop", width=12, command=self.stop).grid(row=0, column=1)
        tk.Button(btn, text="Reset", width=12, command=self.reset).grid(row=0, column=2)
        tk.Button(btn, text="Executive Summary", width=16, command=self.summary).grid(row=0, column=3)
        tk.Button(btn, text="Screenshot", width=12, command=self.screenshot).grid(row=0, column=4)


        self.update()

    def update(self):
        if not self.running:
            return

        cpu = get_cpu_usage()
        ram = get_ram_usage()
        disk = get_disk_usage()

        self.cpu.config(text=f"CPU: {cpu:.1f}%")
        self.ram.config(text=f"RAM: {ram:.1f}%")
        self.disk.config(text=f"Disk: {disk:.1f}%")

        self.cpu_h.append(cpu)
        self.ram_h.append(ram)
        self.disk_h.append(disk)

        h, color = evaluate_health(cpu, ram, disk)
        self.final_health = h
        self.health.config(text=f"System Health: {h}", fg=color)

        connected = check_connection()
        if connected:
            self.status.config(text="Network: Connected", fg="green")
            up, down = get_network_speed()
            dk, uk = down / 1024, up / 1024
            self.down.config(text=f"Download: {dk:.2f} KB/s")
            self.up.config(text=f"Upload: {uk:.2f} KB/s")
            self.download_data.append(dk)
            self.upload_data.append(uk)
            log_network("Connected", dk, uk)
        else:
            self.status.config(text="Network: Disconnected", fg="red")
            log_network("Disconnected", 0, 0)

        incidents = detect_incident(h, connected)
        for i in incidents:
            log_incident(i)
            self.incident.config(text=f"Last Incident: {i}")

        self.ax.clear()
        self.ax.plot(self.download_data[-25:], label="Download")
        self.ax.plot(self.upload_data[-25:], label="Upload")
        self.ax.legend()
        self.canvas.draw()

        self.root.after(1500, self.update)

    def stop(self):
        self.running = False
    def start(self):
     if not self.running:
        self.running = True
        self.update()


    def reset(self):
        reset_log()
        self.download_data.clear()
        self.upload_data.clear()
        self.cpu_h.clear()
        self.ram_h.clear()
        self.disk_h.clear()
        self.start_time = time.time()
        self.running = True
        self.update()

    def summary(self):
        duration = int(time.time() - self.start_time)
        stats = {
            "duration": f"{duration//60} menit {duration%60} detik",
            "avg_cpu": sum(self.cpu_h)/len(self.cpu_h),
            "avg_ram": sum(self.ram_h)/len(self.ram_h),
            "avg_disk": sum(self.disk_h)/len(self.disk_h),
            "final_health": self.final_health
        }
        self.incident.config(text=generate_summary(stats))

    def screenshot(self):
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{now}.png"
        img = ImageGrab.grab()
        img.save(filename)
        self.incident.config(text=f"Screenshot saved: {filename}")
