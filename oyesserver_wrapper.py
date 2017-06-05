from OYE_S_Server import OyeSServer
import subprocess


def main():
    server = OyeSServer()
    server.main()


if __name__ == "__main__":
    while True:
        try:
            main()
            print("End of main")
        except:
            continue
