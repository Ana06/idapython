"""This code can be used in a conditional breakpoint at the of a decoding
routine (before restoring ebp) to output the decoded string."""

ebp = idc.get_reg_value('ebp')
string_addr = idc.get_wide_dword(ebp + 0xC)
length = idc.get_wide_dword(ebp + 0x10)
string = ida_bytes.get_strlit_contents(string_addr, length, STRTYPE_C)
print(f"Decoded: {string}")
