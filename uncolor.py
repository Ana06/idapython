import idaapi
import idautils
import idc

ea = idc.next_head(0)
while ea != idaapi.BADADDR:
    idc.set_color(ea, idc.CIC_ITEM, 0xFFFFFF)
    ea = idc.next_head(ea)

