#!/usr/bin/env python
import smtplib
import config

def SendEmail():
    sender = config.senderemailid
    receivers = [config.receiveremailid]
    yourname = "Sara Sjsu"
    recvname = "Professor sithu aung"
    sub = "Request an Appointment "
    message = "From: " + yourname + "\n"
    message = message + "To: " + recvname + "\n"
    message = message + "Subject: " + sub + "\n"
    message = message + config.body
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        username = config.senderemailid
        password = config.senderpassword
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(sender, receivers, message)
        server.quit()
        resp = "email to professor sithu successfully sent!"
    except  Exception:
        resp = "Error: unable to send email, please enter valid email address"
    return resp