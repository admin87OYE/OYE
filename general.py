import os
import textwrap


# Makes a separate directory for every website
def create_project_dir(directory):
    if not os.path.exists(directory):
        #  print('Creating project ' + directory + '.')
        os.makedirs(directory)


# Create queue and crawled files
def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


# Creates a new file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


# Append an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data)


# Delete contents of a file
def delete_file_contents(path):
    with open(path, 'w'):
        pass


# Read a file and convert it to a set
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Converts a set to a file
def set_to_file(links, file):
    delete_file_contents(file)
    for link in sorted(links):
        append_to_file(file, link)


# Returns MAC as string from bytes (ie AA:BB:CC:DD:EE:FF)
def get_mac_addr(mac_raw):
    byte_str = map('{:02x}'.format, mac_raw)
    mac_addr = ':'.join(byte_str).upper()
    return mac_addr


# Formats multi-line data
def format_multi_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size -= 1
    return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])
