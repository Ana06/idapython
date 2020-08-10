# returns a string with the hexadecimal little endian representation of the parameters
def little_endian(num):
    return ' '.join([ f'0x{i:X}' for i in num.to_bytes(4, 'little')])


def print_register(register):
    addr = get_event_ea()
    register_value = get_reg_value(register)
    print(f'## At 0x{addr:X}, "{register}" is: {register_value}')


def print_byte(location):
    value = get_wide_byte(location)
    print(f'## At 0x{location:X}, BYTE: 0x{value:X}')


def print_dword(location):
    value = get_wide_dword(location)
    print(f'## At 0x{location:X}, DWORD: {little_endian(value)}')


print('Print functions loaded correctly')

