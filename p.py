"""Provides functions to print different formated data"""
import ida_bytes
import idc


def little_endian(num):
    """returns a string with the hexadecimal little endian representation of the parameter"""
    return " ".join([f"0x{i:X}" for i in num.to_bytes(4, "little")])


def register(register):
    """prints the given register value, useful for debugging"""
    addr = idc.get_event_ea()
    register_value = idc.get_reg_value(register)
    print(f'## At 0x{addr:X}, "{register}" is: {register_value}')


def byte(location):
    """prints the byte at the given location, useful for debugging"""
    value = ida_bytes.get_wide_byte(location)
    print(f"## At 0x{location:X}, BYTE: 0x{value:X}")


def dword(location):
    """prints the dword at the given location, useful for debugging"""
    value = ida_bytes.get_wide_dword(location)
    print(f"## At 0x{location:X}, DWORD: {little_endian(value)}")
