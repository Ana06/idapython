"""It uses Appcall to decode strings calling a decoding routine. It searches
for all calls to the decoding routine.
Check https://hex-rays.com/blog/practical-appcall-examples"""

import idaapi, idc, ida_kernwin

def get_length_of_bytes(ea):
    length = 0
    while idc.get_wide_byte(ea + length) != 0:
        length += 1
    return length

def get_string(ea, length):
    return idc.get_strlit_contents(ea, length, STRTYPE_C).decode("utf-8")

decodingFunc = idc.get_name_ea_simple('decodingFunc')
for ref in CodeRefsTo(decodingFunc, True):
    print(hex(ref))
    params_addrs = idaapi.get_arg_addrs(ref)
    s_in = get_operand_value(params_addrs[0], 0)
    # If you don't want to decode in place, use:
    # s_out = Appcall.buffer(" ", length + 1)
    # s_out.value
    s_out = get_operand_value(params_addrs[1], 0)
    # The length is not always an immediate value
    length = get_operand_value(params_addrs[2], 0) or get_lenght_of_bytes(s_in)
    try:
        # decodingFunc needs to be defined as: decodingFunc(char *, char *, int)
        Appcall.decodingFunc(s_in, s_out, length);
        s_out_value = get_string(s_out, length)
        log_str = f"Decoded: {s_out_value}"
        print(f"{hex(ref)} Decoded: {s_out_value}")
        set_cmt(params_addrs[0], s_out_value, False)
        # Create string also renames the variable
        idc.create_strlit(s_out, s_out + length)

    except Exception as err:
        print (f"{hex(ref)} Exception:  {err}")
