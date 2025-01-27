import os
import smtplib
from datetime import datetime


def smtp_mail_it():
    try:
        from_address = os.getenv('EMAIL_USER')
        from_address_password = os.getenv('EMAIL_PASSWORD')
        to_list = ["recipient@example.com"]
        message = f"Received message from ({os.getlogin()}) @ Time: {datetime.now().strftime('%d/%m/%Y %H:%M')}"

        # Connect securely using SMTP with TLS
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade the connection to secure
        server.login(from_address, from_address_password)
        server.sendmail(from_address, to_list, message)
        server.quit()
    except:
        pass