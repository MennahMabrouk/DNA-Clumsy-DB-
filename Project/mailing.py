import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

GMAIL = "mennahtullahmabrouk@gmail.com"
GMAIL_USERNAME = "Mennahtullah Mabrouk"
GMAIL_PASSWORD = "zxyvjptscxwhkvuv"

def send_feedback_email(user_email, feedback_text):
    sender_email = GMAIL
    receiver_email = "mennahtullahmabrouk@gmail.com"
    subject = "Feedback from Helical Hues Haven"
    body = f"User Email: {user_email}\n\nFeedback:\n{feedback_text}"

    smtp_server = "smtp.gmail.com"
    smtp_port = 465

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    text_part = MIMEText(body, 'plain')
    message.attach(text_part)

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(GMAIL, GMAIL_PASSWORD)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return True
    except Exception as e:
        print(f"Error sending feedback: {e}")
        return False

