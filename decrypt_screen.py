import os
from kivy.uix.screenmanager import Screen
from plyer import filechooser


class DecryptScreen(Screen):
    selected_file = None

    def __init__(self, encryption_manager, **kwargs):
        super().__init__(**kwargs)
        self.encryption_manager = encryption_manager

    def select_file(self):
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        if selection:
            self.selected_file = selection[0]
            self.ids.file_label.text = f"Selected file: {self.selected_file}"

    def decrypt_file(self):
        if not self.selected_file:
            return

        with open(self.selected_file, 'rb') as f:
            data = f.read()

        decrypted_data = self.encryption_manager.decrypt(data)

        file_path, file_extension = os.path.splitext(self.selected_file)
        decrypted_file_path = f"{file_path}_decrypted{file_extension}"
        with open(decrypted_file_path, 'wb') as f:
            f.write(decrypted_data)
