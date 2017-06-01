import socket
import subprocess
from sys import platform


def scan(port=''):
    addr = get_local_addr()
    if port == '':
        cmd = subprocess.Popen('nmap -sP ' + addr + '/24')
        nmap = cmd.communicate()[0].decode('utf-8')
    else:
        nmap = subprocess.Popen('nmap -sP ')


def get_local_addr():
    if platform == 'linux' or platform == 'linux2':
        terminal = subprocess.Popen('ifconfig wlan0', stdout=subprocess.PIPE)
        ifconfig = terminal.communicate()[0].decode('utf-8')

        ip_address = ifconfig.split("inet addr:", 1)[1].split("Bcast:", 1)[0].strip()
        return ip_address
    elif platform == 'win32':
        cmd = subprocess.Popen('ipconfig', stdout=subprocess.PIPE)
        ipconfig = cmd.communicate()[0].decode('utf-8')

        ip_address =\
            ipconfig.split('Wi-Fi', 1)[1].split('IPv4 Address. . . . . . . . . . . :', 1)[1].split('\n', 1)[0].strip()
        return ip_address
    elif platform == 'darwin':
        print("[-] Lan scan failed!")
        print("[!] OS X not yet supported")
    else:
        print("[-] Lan scan failed!")
        print("[!] Unsupported operating system")


if __name__ == '__main__':
    scan()
