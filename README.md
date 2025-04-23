# 🛡️ Ethical Keylogger for macOS

A Python-based ethical keylogger built for **parental control**, **system monitoring**, and **educational purposes**. It collects keystrokes, system information, screenshots, and audio — all zipped and emailed securely.

> ⚠️ This tool is intended for **ethical** use only. Do not deploy without user consent. Always comply with local laws and regulations.

---

## ✨ Features

- ✅ Keystroke logging (`pynput`)
- 🖥️ System info capture (`platform`, `psutil`)
- 📸 Screenshot snapshots (`Pillow`)
- 🎙️ Audio recording (`sounddevice`)
- 📦 Auto zips all data
- 📧 Sends logs via email

---

## 📁 Output

After running, it collects the following:

- `keystroke_log.txt`
- `system_info.txt`
- `screenshot_*.png`
- `audio.wav`
- ✅ All compressed to `logs.zip`

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/PratikNath/ethical-keylogger.git
cd ethical-keylogger


**2. Set up Python environment (recommended)**

python3 -m venv keyenv
source keyenv/bin/activate
pip install -r requirements.txt

**3. Configure email**
In emailer.py, set:

EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
RECIPIENT = "recipient_email@gmail.com"

✅ Use App Passwords for Gmail.

**4.▶️ Run the Logger**

python logger.py

Runs for 2 minutes, records audio (120s), captures 10 screenshots, then emails everything.

