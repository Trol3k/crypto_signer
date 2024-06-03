from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from usb_support import DiskChecker

from decrypt_screen import DecryptScreen
from encrypt_screen import EncryptScreen
from encryption import EncryptionManager


class MainScreen(Screen):
    pass


class SignatureVerificationScreen(Screen):
    pass


class SignDocumentScreen(Screen):
    pass


class CryptoSignerApp(App):
    def __init__(self, **kwargs):
        super(CryptoSignerApp, self).__init__(**kwargs)
        self.encryption_manager = EncryptionManager()
        self.sm = ScreenManager()

    def build(self):
        Builder.load_file('main_screen.kv')
        Builder.load_file('sign_document_screen.kv')
        Builder.load_file('signature_verification_screen.kv')
        Builder.load_file('encrypt_screen.kv')
        Builder.load_file('decrypt_screen.kv')

        main_screen = MainScreen(name='main')
        self.sm.add_widget(main_screen)

        sign_screen = SignDocumentScreen(name='signDocument')
        self.sm.add_widget(sign_screen)

        signature_screen = SignatureVerificationScreen(name='signatureVerification')
        self.sm.add_widget(signature_screen)

        encrypt_screen = EncryptScreen(self.encryption_manager, name='encrypt')
        self.sm.add_widget(encrypt_screen)

        decrypt_screen = DecryptScreen(self.encryption_manager, name='decrypt')
        self.sm.add_widget(decrypt_screen)

        disk_checker = DiskChecker(self.sm)
        disk_checker.start()

        return self.sm


if __name__ == '__main__':
    CryptoSignerApp().run()
