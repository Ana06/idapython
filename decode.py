"""provides functions to decode strings."""

import idaapi
import idc
import idautils
import ida_bytes

def references(function_location, decoding_str):
    """decodes all decoded strings by a given function by applying decoding_str
       to every byte.
       decoding_str should contain encoded_byte, for example:
       decode.references(0x401000, "(encoded_byte ^ 0xA2) + 0x21")"""
    for xref in idautils.XrefsTo(function_location):
        ea = xref.frm
        # The function needs to be defined for get_arg_addrs to work
        args = idaapi.get_arg_addrs(ea)
        encoded = idc.get_operand_value(args[0], 0)
        decoded = idc.get_operand_value(args[1], 0)

        decoded_str = ""
        i = 0
        encoded_byte = ida_bytes.get_wide_byte(encoded)
        while encoded_byte != 0:
            decoded_byte = eval(decoding_str)
            decoded_str += chr(decoded_byte)
            ida_bytes.patch_byte(decoded + i, decoded_byte)
            i += 1
            encoded_byte = ida_bytes.get_wide_byte(encoded + i)

        ida_bytes.create_strlit(decoded, i, STRTYPE_C)
        idc.set_cmt(ea, f"Decoded: {decoded_str}", 0)
        print(f"##At {hex(ea)} decoded: {decoded_str}")


def decode_str(decoding_str):
    """decodes the current string pointer by applying decoding_str to every byte
       decoding_str should contain encoded_byte, for example:
       decode.string("(encoded_byte ^ 0xA2) + 0x21")"""
    encoded = get_screen_ea()

    decoded_str = ""
    i = 0
    encoded_byte = ida_bytes.get_wide_byte(encoded)
    while encoded_byte != 0:
        decoded_byte = eval(decoding_str)
        decoded_str += chr(decoded_byte)
        i += 1
        encoded_byte = ida_bytes.get_wide_byte(encoded + i)

    idc.set_cmt(encoded, f"Decoded: {decoded_str}", 1)
    print(f"##At {hex(encoded)} decoded: {decoded_str}")
