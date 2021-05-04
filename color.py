"""Provides an `apply()` method to color and mark your database and a `clean()` method to undo it."""

import ida_auto
import ida_lines
import idaapi
import idautils
import idc

# colors are in GRB format
COLOR_CALL = 0xB2FFCB
COLOR_PUSH = 0xDCF4FF
COLOR_POP = 0xE1EAEA
ALL_PREFIX_WIDTH = 4
PREFIX_WIDTH = ALL_PREFIX_WIDTH - 2
PREFIX_PUSH = f' {">" * PREFIX_WIDTH} '
PREFIX_NUM_FORMAT = f" {PREFIX_WIDTH}d"
_PARAMETERS = {}


def _prefix_callback(ea, insn, lnnum, indent, line):
    instruction = idc.print_insn_mnem(ea)
    if instruction == "call":
        return PREFIX_PUSH
    elif _PARAMETERS.get(ea):
        return f" {format(_PARAMETERS[ea], PREFIX_NUM_FORMAT)} "
    else:
        return " " * ALL_PREFIX_WIDTH


def apply():
    """Provides an `apply()` method to color and mark your database and a `clean()` method to undo it.
    The `apply()` method colors `call`, `push` and `pop` instructions (sets background color).
    It also adds the prefix `>>` to`call` instructions and the number of argument to its parameters (only available if the function declaration is defined).
    This is useful to quickly identify function calls, their parameters and the calling convention."""
    ida_auto.auto_wait()
    ea = idc.next_head(0)
    while ea != idaapi.BADADDR:
        instruction = idc.print_insn_mnem(ea)
        if instruction == "call":
            idc.set_color(ea, idc.CIC_ITEM, COLOR_CALL)
            addresses = idaapi.get_arg_addrs(ea)
            if addresses:
                _PARAMETERS.update({e: i + 1 for i, e in enumerate(addresses)})
        elif instruction == "push":
            idc.set_color(ea, idc.CIC_ITEM, COLOR_PUSH)
        elif instruction == "pop":
            idc.set_color(ea, idc.CIC_ITEM, COLOR_POP)
        ea = idc.next_head(ea)

    ida_lines.set_user_defined_prefix(ALL_PREFIX_WIDTH, _prefix_callback)

    print("ANA color: Enjoy your colorful database!")


def clean():
    """Removes the background color of all the database.
    It can be used to remove the colors added by `apply()`, but it doesn't remove the prefixes."""
    ida_auto.auto_wait()
    ea = idc.next_head(0)
    while ea != idaapi.BADADDR:
        idc.set_color(ea, idc.CIC_ITEM, 0xFFFFFF)
        ea = idc.next_head(ea)

    print("ANA color: Enjoy your boring database")
