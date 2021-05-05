"""It needs to be copied into the user directory, which you can get with `get_user_idadir()`, so that it is executed at the end of IDAPython’s initialization.
   It imports `color.py`, `nop.py` and `p.py`, defines an `init()` method and registers the `Ctrl+Enter` hotkey to it."""

import sys

import ida_kernwin
import ida_loader
import idaapi

# I like to store my idapython scripts on the Desktop
sys.path.insert(1, r"C:\Users\user\Desktop\idapython")

import color
import nop
import p
import decode


def init():
    """It colors the database, loads capa explorer (running its analysis) and reactivate the `IDA View-A` view.
    Call this method after IDA initial autoanalysis has been finished."""
    color.apply()
    ida_loader.load_and_run_plugin("capa_explorer", 1)  # 1 = analyze
    widget = idaapi.find_widget("IDA View-A")
    if widget:
        idaapi.activate_widget(widget, True)
    print("ANA: Initialization finished")


ida_kernwin.add_hotkey("Ctrl+Enter", init)
print("ANA: Registered 'Ctrl+Enter' hotkey to  init()")
