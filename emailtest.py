import os
import smtplib
from email.message import EmailMessage

user_email = os.environ['MY_EMAIL']
user_pass = os.environ['MY_PASS']
other_email = os.environ['RECEIVER_EMAIL']

msg = EmailMessage()
msg.set_content("Test email from GitHub Actions")
msg['Subject'] = "Test Email"
msg['From'] = user_email
msg['To'] = other_email

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(user_email, user_pass)
        smtp.send_message(msg)
    print("✅ Test email sent successfully")
except Exception as e:
    print(f"❌ Failed to send test email: {e}")
