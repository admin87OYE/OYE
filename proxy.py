import sys
import socket
import threading


def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [recieve_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    recieve_first = sys.argv[5]
    if "True" in recieve_first:
        recieve_first = True
    else:
        recieve_first = False
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except:
        print("[-] Failed to listen on " + str(local_host) + ":" + str(local_port))
        print("[!] Check for other listening sockets or correct permissions.")
        sys.exit(0)
    print("[+] Listening on " + str(local_host) + ":" + str(local_port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        print("[+] Recieved incoming connection from " + str(addr[0]) + ":" + str(addr[1]))
        proxy_thread = threading.Thread(target=proxy_handler,
                                        args=(client_socket, remote_host, remote_port, recieve_first))
        proxy_thread.start()


def proxy_handler(client_socket, remote_host, remote_port, recieve_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    if recieve_first:
        remote_buffer = recieve_from(remote_socket)
        hexdump(remote_buffer)
        remote_buffer = response_handler(remote_buffer)
        if len(remote_buffer):
            print("[*] Sending " + str(len(remote_buffer)) + " to localhost...")
            client_socket.send(remote_buffer)
    while True:
        local_buffer = recieve_from(client_socket)
        if len(local_buffer):
            print("[+] Recieved " + str(len(local_buffer)) + " from localhost")
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[+] Sent to remote")
        remote_buffer = recieve_from(remote_socket)
        if len(remote_buffer):
            print("[+] Recieved " + str(len(remote_buffer)) + " from remote")
            hexdump(remote_buffer)
            client_socket.send(remote_buffer)
            print("[+] Sent to lacalhost")
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[!] No more data. Closing connections...")
            break


if __name__ == '__main__':
    main()

