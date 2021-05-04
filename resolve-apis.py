import idaapi
import idc

# api resolution table starts at START and ends at END
# Run this script after the apis have been resolved
ea = START
while ea < END:
    ea = idc.next_head(ea)
    addr = get_wide_dword(ea)
    name = get_name(addr)
    if name == "":
        print(f"ERROR at {hex(ea)}")
        break
    # IDA links the function if we use WinHttpQueryOption instead of winhttp_WinHttpQueryOption
    func_name = name.split("_")[1]
    set_name(ea, func_name, SN_CHECK)
    print(name)
