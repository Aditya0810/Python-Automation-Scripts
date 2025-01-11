import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import schedule
import time
import json
import os
import reportlab


def send_email(receiver_email, subject, body):

    sender_email = 'adityayadav0810@gmail.com'
    sender_password = 'zfzw rygo tsqt epzx'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, receiver_email, message.as_string())

def generate_invoice(tutor_name, amount):
    today = datetime.date.today()
    due_date = today + datetime.timedelta(days=14)

    invoice_body = f"Dear {tutor_name},\n\n"\
                   f"This is a cash invoice for tutoring services provided.\n"\
                   f"Amount: ${amount}\n"\
                   f"Due Date: {due_date}\n\n"\
                   f"Thank you for your services!\n\n"\
                   f"Best regards,\n"\
                   f"Your Employer"

    return invoice_body

def main():
    receiver_name = input("Enter the employer's name: ")
    amount = float(input("Enter the total amount: "))
    receiver_email = input("Enter the email address you want to send it to: ")

    subject = "Cash Invoice for Tutoring Services"
    invoice_body = generate_invoice(receiver_name, amount)

    send_email(receiver_email, subject, invoice_body)

    print(f"Email sent to {receiver_name} at {receiver_email} with the cash invoice.")

def check_fortnight():
    last_sent_date_filename = 'last_sent_date.json'

    if os.path.exists(last_sent_date_filename):
        with open(last_sent_date_filename, 'r') as file:
            last_sent_date = datetime.datetime.strptime(json.load(file), '%Y-%m-%d').date()
    else:
        last_sent_date = datetime.date.today()

    today = datetime.date.today()
    days_passed = (today - last_sent_date).days

    if days_passed >= 14:
        main()
        with open(last_sent_date_filename, 'w') as file:
            json.dump(today.strftime('%Y-%m-%d'), file)

if __name__ == "__main__":
    schedule.every().day.at("12:00").do(check_fortnight)

    while True:
        schedule.run_pending()
        time.sleep(1)


