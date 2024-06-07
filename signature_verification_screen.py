import base64
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from kivy.uix.screenmanager import Screen
from lxml import etree
from plyer import filechooser


class SignatureVerificationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file = None
        self.public_key_file = None
        self.signature_file = None

    def select_file(self):
        filechooser.open_file(on_selection=self.selected_file)

    def select_key(self):
        filechooser.open_file(on_selection=self.selected_key)

    def select_signature(self):
        filechooser.open_file(on_selection=self.selected_signature)

    def selected_file(self, selection):
        if selection:
            self.file = selection[0]
            self.ids.file_label.text = f"Selected file: {self.file}"

    def selected_key(self, selection):
        if selection:
            self.public_key_file = selection[0]
            self.ids.file_label.text = f"Selected key: {self.public_key_file}"

    def selected_signature(self, selection):
        if selection:
            self.signature_file = selection[0]
            self.ids.file_label.text = f"Selected signature: {self.signature_file}"

    def verify(self):

        secret_code = "Unguessable"
        key = RSA.import_key(open(self.public_key_file).read(), secret_code)
        public_key = key.public_key()

        with open(self.file, "rb") as f:
            data = f.read()

        file_hash = SHA256.new(data)

        tree = etree.parse(self.signature_file)
        root = tree.getroot()

        encrypted_hash = root.find('.//Encrypted_Hash')
        encrypted_hash_decoded = base64.b64decode(encrypted_hash.text)

        try:
            pkcs1_15.new(key).verify(file_hash, encrypted_hash_decoded)
            print("The signature is valid.")
        except (ValueError, TypeError):
            print("The signature is not valid.")
