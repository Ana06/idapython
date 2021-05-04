"""Provides a `nop()` method and registers the `Ctrl+N` hotkey to it."""

import ida_bytes
import ida_kernwin
import idaapi
import idc


def nop():
    """Nops-out the current instruction and advance the cursor to the next instruction."""
    ea = idaapi.get_screen_ea()
    num_bytes = idc.get_item_size(ea)
    for i in range(num_bytes):
        ida_bytes.patch_byte(ea, 0x90)
        ea += 1
    ida_kernwin.refresh_idaview_anyway()
    ida_kernwin.jumpto(ea)


ida_kernwin.add_hotkey("Ctrl+N", nop)
print("ANA nop: Registered 'Ctrl+N' hotkey to nop()")
