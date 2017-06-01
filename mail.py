import smtplib


def send(data='', from_addr='kitic.noob@gmail.com', to_addr='anijovanovic@gmail.com'):
    try:
        sender = from_addr
        receiver = to_addr
        password = 'anic99a3dam' if sender == 'kitic.noob@gmail.com' else ''
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, data)
        # server.sendmail(sender, 'zmajvukasin@gmail.com', data)
        server.close()
    except smtplib.SMTPException:
        pass
