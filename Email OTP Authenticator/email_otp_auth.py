import os
import random
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv("op.env")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def generate_otp(length=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def send_otp(to_email, otp):
    msg = EmailMessage()
    msg['Subject'] = "OTP Verification"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(f"Your OTP is: {otp}")

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

def main():
    to_mail = input('Enter your email: ')
    otp = generate_otp()

    send_otp(to_mail, otp)

    input_otp = input("Enter OTP: ")
    if input_otp == otp:
        print("OTP verified.")
    else:
        print("Invalid OTP.")

if __name__ == "__main__":
    main()
