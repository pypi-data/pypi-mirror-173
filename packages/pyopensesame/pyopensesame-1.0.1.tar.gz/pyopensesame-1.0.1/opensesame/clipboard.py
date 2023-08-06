try:
    import pyperclip
except ModuleNotFoundError:
    pyperclip=None
import tkinter
try:
    WIN = tkinter.Tk()
    WIN.withdraw()
    CAN=True
except:
    WIN=None
    CAN=False
def copy(text):
    if not CAN:
        raise NotImplementedError("pasting is not implemented on this device")
    if pyperclip:
        return pyperclip.copy(text)
    if WIN:
        return WIN.clipboard_append(text)

    
