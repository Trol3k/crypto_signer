from Cryptodome.PublicKey import RSA
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.app import App


class PinScreen(Screen):
    pin_input_1 = ObjectProperty(None)
    pin_input_2 = ObjectProperty(None)
    pin_input_3 = ObjectProperty(None)
    pin_input_4 = ObjectProperty(None)
    font_size = 60

    def __init__(self, **kw):
        super().__init__(**kw)
        self.disk = None

    def on_enter(self, *args):
        self.pin_input_1.focus = True

    def move_focus(self, current_input, next_input):
        if len(current_input.text) == 1:
            next_input.focus = True

    def check_pin(self):
        pin = self.pin_input_1.text + self.pin_input_2.text + self.pin_input_3.text + self.pin_input_4.text

        try:
            private_key = RSA.import_key(open(self.disk + '\private.pem').read(), pin)

            app = App.get_running_app()
            sign_screen = app.root.get_screen('signDocument')
            sign_screen.private_key = private_key
            app.root.current = 'signDocument'
        except:
            content = BoxLayout(orientation='vertical')
            content.add_widget(Label(text='Invalid PIN'))
            close_button = Button(text='Close', size_hint=(None, None), size=(100, 50))
            content.add_widget(close_button)

            popup = Popup(title='Error', content=content, size_hint=(None, None), size=(400, 200))
            close_button.bind(on_press=popup.dismiss)

            popup.open()
