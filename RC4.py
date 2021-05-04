import string

import idc

KEY_BYTES = [0xBA, 0xAA, 0xAA, 0xAA, 0xAD]  # Array with the key in bytes

PRINT_SET = set(string.printable)


def RC4(key_bytes, encrypted_bytes):
    S = list(range(256))
    j = 0
    result = []

    # KSA
    for i in range(256):
        j = (j + S[i] + key_bytes[i % len(key_bytes)]) % 256
        S[i], S[j] = S[j], S[i]

    # PRGA
    i = j = 0
    for byte in encrypted_bytes:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        result.append(chr(byte ^ S[(S[i] + S[j]) % 256]))

    return "".join(result)


def get_bytes(addr):
    i = 0
    bytes = []
    while get_wide_byte(addr) != 0:
        bytes.append(get_wide_byte(addr))
        addr += 1
        i += 1
        if i > 100:
            return None  # You shouldn't be reading here
    return bytes


def is_printable(string):
    return set(string).issubset(PRINT_SET)


ea = idc.next_head(0)
while ea != idaapi.BADADDR:
    if print_insn_mnem(ea) == "mov" and get_operand_type(ea, 1) == 5:
        offset = get_operand_value(ea, 1)
        encrypted_bytes = get_bytes(offset)
        if encrypted_bytes and len(encrypted_bytes) > 3:
            result = RC4(KEY_BYTES, encrypted_bytes)
            if is_printable(result):
                print(f'Decoded "{result}" with RC4 at: {hex(ea)}')
                idc.set_cmt(ea, f"RC4: {result}", 0)

    ea = next_head(ea)
