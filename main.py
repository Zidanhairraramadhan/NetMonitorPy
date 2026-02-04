import tkinter as tk
from gui import NetHealthMonitorGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = NetHealthMonitorGUI(root)
    root.mainloop()