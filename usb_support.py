import threading
import time
import wmi
import pythoncom
from kivy.clock import mainthread


class DiskChecker(threading.Thread):
    def __init__(self, screen_manager):
        super(DiskChecker, self).__init__()
        self.daemon = True
        self.screen_manager = screen_manager

    def run(self):
        pythoncom.CoInitialize()
        c = wmi.WMI()
        while True:
            connected = False
            for disk in c.Win32_LogicalDisk():
                if disk.VolumeName == "KEY STORAGE":
                    connected = True
                    break
            if connected:
                self.update_label("Device status: connected")
            else:
                self.update_label("Device status: not connected")
            time.sleep(1)

    @mainthread
    def update_label(self, text):
        for screen_name in ['main', 'signDocument', 'signatureVerification', 'encrypt', 'decrypt']:
            screen = self.screen_manager.get_screen(screen_name)
            if hasattr(screen, 'ids') and 'connection_label' in screen.ids:
                screen.ids.connection_label.text = text
