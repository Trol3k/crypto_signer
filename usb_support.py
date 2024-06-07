import threading
import time
import wmi
import pythoncom
from kivy.app import App
from kivy.clock import mainthread


class DiskChecker(threading.Thread):
    def __init__(self, screen_manager):
        super(DiskChecker, self).__init__()
        self.disk_caption = None
        self.daemon = True
        self.screen_manager = screen_manager
        self.app = App.get_running_app()

    def run(self):
        pythoncom.CoInitialize()
        c = wmi.WMI()
        while True:
            connected = False
            for disk in c.Win32_LogicalDisk():
                if disk.VolumeName == "KEY STORAGE":
                    connected = True
                    pin_screen = self.app.root.get_screen('pin')
                    pin_screen.disk = disk.Caption
                    break
            if connected:
                self.update_label("Device status: connected", connected)
            else:
                self.update_label("Device status: not connected", connected)
            time.sleep(1)

    @mainthread
    def update_label(self, text, status):
        for screen_name in ['main', 'signDocument', 'signatureVerification', 'encrypt', 'decrypt']:
            screen = self.screen_manager.get_screen(screen_name)
            if hasattr(screen, 'ids'):
                if 'connection_label' in screen.ids:
                    screen.ids.connection_label.text = text
                if screen_name == 'main' and 'sign_button' in screen.ids:
                    screen.ids.sign_button.disabled = not status

