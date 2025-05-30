import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import os

user_email = os.environ['MY_EMAIL']
user_pass = os.environ['MY_PASS']
other_email = os.environ['RECEIVER_EMAIL']

def send_email_notification(subject, body, to_email):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = user_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(user_email, user_pass)  # App Password here
        smtp.send_message(msg)

# Step 1: Fetch and parse page
url = 'https://philnews.ph/pcso-lotto-result/swertres-result/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
page_text = soup.get_text()

# Step 2: Format today's and yesterday's dates (e.g., "May 30, 2025")
today_str = datetime.now().strftime('%B %d, %Y')
yesterday_str = (datetime.now() - timedelta(days=1)).strftime('%B %d, %Y')

# Step 3: Decide which table is today and which is yesterday
if today_str in page_text:
    print(f"✅ Found today's date in page: {today_str}")
    table_labels = ["Today's Results", "Yesterday's Results"]
elif yesterday_str in page_text:
    print(f"⚠️ Page is not updated yet. Most recent results are for {yesterday_str}")
    table_labels = ["Yesterday's Results", "Day Before Yesterday"]
else:
    print("❌ Could not find today's or yesterday's date in the page.")
    table_labels = ["Result #1", "Result #2"]

# Step 4: Find and label tables
tables = soup.find_all('table')

email_body = ''
for i, table in enumerate(tables):
    label = table_labels[i] if i < len(table_labels) else f"Result #{i+1}"
    section_header = f"\n📅 Swertres {label}\n" + "-" * 30 + "\n"
    print(section_header)
    email_body += section_header

    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all(['td', 'th'])
        if cells:
            cell_texts = [cell.get_text(strip=True) for cell in cells]
            if len(cell_texts) == 2:
                draw_time, result = cell_texts
                line = f"🕒 {draw_time}: 🎯 {result}\n"
            else:
                line = " | ".join(cell_texts) + "\n"
            print(line.strip())
            email_body += line

    email_body += "-" * 30 + "\n"


send_email_notification("📢 Swertres Lotto Update", email_body, other_email)
