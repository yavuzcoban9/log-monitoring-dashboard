# send_email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ----- Mailtrap / SMTP AYARLARI -----
SMTP_SERVER = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 2525   # 2525 veya 587 önerilir (STARTTLS)
USERNAME = "0f6f3862f02331"   # Mailtrap kullanıcı adı (paneldeki)
EMAIL_PASSWORD = "41082633de7738"  # paneldeki tam şifreyi buraya koy

# Gönderen ve alıcı adresleri (Mailtrap inbox içinde göreceksin)
EMAIL_ADDRESS = "from@example.com"   # arbitrary (Mailtrap test inbox yakalar)
TO_EMAIL = "to@example.com"          # arbitrary (Mailtrap inbox yakalar)

def send_alert_email(message: str):
    """
    Mailtrap üzerinden test e-posta gönderir.
    message: e-posta gövdesine eklenecek metin.
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL
        msg["Subject"] = "🚨 Log Monitoring Uyarısı (Test - Mailtrap)"

        body = f"""Merhaba,

Sistem loglarında uyarı tespit edildi:

{message}

Bu bir test e-postasıdır (Mailtrap).
"""
        msg.attach(MIMEText(body, "plain"))

        # STARTTLS kullanan normal SMTP oturumu
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.ehlo()
        # STARTTLS (gerekirse)
        try:
            server.starttls()
            server.ehlo()
        except Exception:
            # bazı durumlarda STARTTLS isteğe bağlıdır, hata alınırsa devam ederiz
            pass

        # Mailtrap, kullanıcı adı + parola ile login ister
        server.login(USERNAME, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        server.quit()

        print("✅ Mailtrap üzerinden test e-postası gönderildi.")
    except Exception as e:
        print(f"❌ E-posta gönderilemedi: {e}")
