import socket


def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 4765))
        s.listen()
        conn, addr = s.accept()
        conn.send('[+] Successfully connected to the server'.encode())

        cmd = conn.recv(8).decode('utf-8')
        if cmd == 'getlog':
            f = open('/sdcard/tosend.txt', 'r')
            l = f.read(1024)
            while l:
                conn.send(l.encode())
                l = f.read(1024)
            f.close()
            print("[+] Sent log")
        elif cmd == 'mailoff':
            print('[+] Mail turned off')
        elif cmd == 'mailon':
            print('[+] Mail turned on')

        conn.close()
        s.close()
        main()
    except:
        conn.close()
        s.close()
        main()


if __name__ == "__main__":
    main()
