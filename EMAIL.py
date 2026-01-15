##myaccount.google.com\lesssecureapps

import smtplib
from email.message import EmailMessage
import os
import imghdr

sender_mail_id = 'testgroupproject15@gmail.com'
password = 'tkmneficyxmlqafc'

def send_mail(subject,send_to):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_mail_id
    msg['To'] = send_to
    msg.set_content("OTP for your secured login system")

    with open('image.jpg','rb') as m:

        file_data = m.read()
        file_type = imghdr.what(m.name)
        file_name = m.name

    msg.add_attachment(file_data, maintype = 'image', subtype = file_type, filename=subject + '.png')

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:

        smtp.login(sender_mail_id,password)
        smtp.send_message(msg)


