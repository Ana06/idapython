import idaapi
import idc

# api resolution table starts at START and ends at END
# Run this script after the apis have been resolved
ea = START
while ea <= END:
    # same as create_data(ea, FF_DWORD, 4, ida_idaapi.BADADDR)
    op_offset(ea, 1, idaapi.REF_OFF32)
    addr = get_wide_dword(ea)
    name = get_name(addr)
    if name == "":
        print(f"ERROR at {hex(ea)}")
        ea += 1
        continue
    # IDA recognizes the function if we use Sleep instead of kernel32_Sleep
    func_name = name.split("_")[-1]
    # SN_FORCE = if the specified name is already present in the database, adds a numerical suffix instead of failing
    set_name(ea, func_name, idaapi.SN_FORCE)
    print(name)
    ea += 4
