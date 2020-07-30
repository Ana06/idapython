import idaapi
import idautils
import idc
import ida_lines

PARAMETERS = { }
ALL_PREFIX_WIDTH = 4
PREFIX_WIDTH = ALL_PREFIX_WIDTH - 2
PREFIX_PUSH = f' {">" * PREFIX_WIDTH} '
PREFIX_NUM_FORMAT = f' {PREFIX_WIDTH}d'
# colors are in GRB format
COLOR_CALL = 0x91FFC9
COLOR_PUSH = 0xFFCC99
COLOR_POP = 0xE1EAEA

def prefix_callback(ea, insn, lnnum, indent, line):
    instruction = idc.print_insn_mnem(ea)
    if instruction == 'call':
        return PREFIX_PUSH
    elif PARAMETERS.get(ea):
        return f' {format(PARAMETERS[ea], PREFIX_NUM_FORMAT)} '
    else:
        return ' ' * ALL_PREFIX_WIDTH


ea = idc.next_head(0)
while ea != idaapi.BADADDR:
    instruction = idc.print_insn_mnem(ea)
    if instruction == 'call':
        idc.set_color(ea, idc.CIC_ITEM, COLOR_CALL)
        addresses = idaapi.get_arg_addrs(ea)
        if addresses:
            PARAMETERS.update({ e: i+1 for i,e in enumerate(addresses)})
    elif instruction == 'push':
        idc.set_color(ea, idc.CIC_ITEM, COLOR_PUSH)
    elif instruction == 'pop':
        idc.set_color(ea, idc.CIC_ITEM, COLOR_POP)
    ea = idc.next_head(ea)

ida_lines.set_user_defined_prefix(ALL_PREFIX_WIDTH, prefix_callback)

