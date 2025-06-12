# backend/email_utils.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient_email, subject, body, sender_email, sender_password):
    """
    Sends a plain text email from Gmail.
    """
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return True
    except Exception as e:
        print("Email failed to send:", e)
        return False
