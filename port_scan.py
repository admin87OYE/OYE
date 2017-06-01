import socket
import sys
import time
import general
import tempfile


flag = 0
file_dir = tempfile.gettempdir() + '\\oye_port.txt'
general.write_file(file_dir, '')
host = '127.0.0.1'
ip = socket.gethostbyname(host)

start_port = 0
end_port = 1024


open_ports = []
common_ports = {

    '21': 'FTP',
    '22': 'SSH',
    '23': 'TELNET',
    '25': 'SMTP',
    '53': 'DNS',
    '69': 'TFTP',
    '80': 'HTTP',
    '109': 'POP2',
    '110': 'POP3',
    '123': 'NTP',
    '137': 'NETBIOS-NS',
    '138': 'NETBIOS-DGM',
    '139': 'NETBIOS-SSN',
    '143': 'IMAP',
    '156': 'SQL-SERVER',
    '389': 'LDAP',
    '443': 'HTTPS',
    '546': 'DHCP-CLIENT',
    '547': 'DHCP-SERVER',
    '995': 'POP3-SSL',
    '993': 'IMAP-SSL',
    '2086': 'WHM/CPANEL',
    '2087': 'WHM/CPANEL',
    '2082': 'CPANEL',
    '2083': 'CPANEL',
    '3306': 'MYSQL',
    '8443': 'PLESK',
    '10000': 'VIRTUALMIN/WEBMIN'
}

starting_time = time.time()


def check_port(host, port, result=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.07)
        r = sock.connect_ex((host, port))
        if r == 0:
            result = r
        sock.close()
    except:
        pass

    return result


def get_service(port):
    port = str(port)
    if port in common_ports:
        return common_ports[port]
    else:
        return 0


def start():
    try:
        if flag:
            for p in sorted(common_ports):
                sys.stdout.flush()
                p = int(p)
                response = check_port(host, p)
                if response == 0:
                    open_ports.append(p)
                    # if not p == end_port:
                    sys.stdout.write('\b' * len(str(p)))
        else:

            for p in range(start_port, end_port + 1):
                sys.stdout.flush()
                response = check_port(host, p)
                if response == 0:
                    open_ports.append(p)
                if not p == end_port:
                    sys.stdout.write('\b' * len(str(p)))

        general.append_to_file(file_dir, "Scanning completed at %s" % (time.strftime("%I:%M:%S %p")) + '\n')
        ending_time = time.time()
        total_time = ending_time - starting_time
        general.append_to_file(file_dir, "=" * 40 + '\n')
        general.append_to_file(file_dir, "\tScan Report: %s" % host + '\n')
        general.append_to_file(file_dir, "=" * 40 + '\n')
        if total_time <= 60:
            total_time = str(round(total_time, 2))
            general.append_to_file(file_dir, "Scan Took %s seconds" % total_time + '\n')

        else:
            total_time /= 60
            general.append_to_file(file_dir, "Scan Took %s Minutes" % total_time + '\n')

        if open_ports:
            general.append_to_file(file_dir, "Open Ports: " + '\n')
            for i in sorted(open_ports):
                service = get_service(i)
                if not service:
                    service = "Unknown service"
                    general.append_to_file(file_dir, "\t%s %s: Open" % (i, service) + '\n')

        else:
            general.append_to_file(file_dir, "Sorry, No open ports found.!!" + '\n')

    except:
        pass
