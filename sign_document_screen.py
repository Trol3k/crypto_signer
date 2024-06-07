import base64
import os
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from kivy.uix.screenmanager import Screen
from plyer import filechooser
from datetime import datetime
from lxml import etree


class SignDocumentScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.selected_file = None
        self.private_key = None

    def select_file(self):
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        if selection:
            self.selected_file = selection[0]
            self.ids.file_label.text = f"Selected file: {self.selected_file}"
            self.ids.sign_button.disabled = False

    def sign_document(self):
        if not self.selected_file:
            return

        with open(self.selected_file, 'rb') as f:
            data = f.read()

        file_size = os.path.getsize(self.selected_file)
        file_path = os.path.splitext(self.selected_file)[0]
        file_extension = os.path.splitext(self.selected_file)[1]
        file_modification_date = datetime.fromtimestamp(os.path.getmtime(self.selected_file)).isoformat()

        hash_obj = SHA256.new(data)
        encrypted_hash = pkcs1_15.new(self.private_key).sign(hash_obj)

        root = etree.Element("XAdES_Signature")

        file_info = etree.SubElement(root, "File_Info")
        etree.SubElement(file_info, "Size").text = str(file_size)
        etree.SubElement(file_info, "Extension").text = file_extension
        etree.SubElement(file_info, "Modification_Date").text = file_modification_date

        user_info = etree.SubElement(root, "User_Info")
        etree.SubElement(user_info, "Username").text = os.getlogin()

        etree.SubElement(root, "Encrypted_Hash").text = base64.b64encode(encrypted_hash).decode()

        timestamp = datetime.now().isoformat()
        etree.SubElement(root, "Timestamp").text = timestamp

        xml_str = etree.tostring(root, pretty_print=True, xml_declaration=True)

        xml_file_path = f"{file_path}_signature.xml"
        with open(xml_file_path, 'wb') as xml_file:
            xml_file.write(xml_str)

        return xml_file_path
