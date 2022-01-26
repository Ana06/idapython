ea = START
old_ea = ea
while ea < END:
    b = get_wide_byte(ea)
    if b == 0:
        create_strlit(old_ea, ea)
        old_ea = ea + 1
    elif b < 38 or b > 122:
        old_ea = ea + 1
    ea += 1
