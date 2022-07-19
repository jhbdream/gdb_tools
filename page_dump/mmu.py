import gdb

def lookup_types(*types):
    for type_str in types:
        try:
            return gdb.lookup_type(type_str)
        except Exception as e:
            exc = e
    raise exc

uint64 = lookup_types('unsigned long long', 'ulong', 'u64', 'uint64')
uint   = lookup_types('unsigned int', 'uint', 'u32', 'uint32')
ushort = lookup_types('unsigned short', 'ushort', 'u16', 'uint16')
uchar  = lookup_types('unsigned char', 'ubyte', 'u8', 'uint8')

def read_reg(register):
    val = gdb.selected_frame().read_register(register)
    val = val.cast(uint64)
    return int(val)

def extract(value, s, e):
    return extract_no_shift(value, s, e) >> s

def extract_no_shift(value, s, e):
    mask = ((1<<(e + 1))-1) & ~((1<<s) - 1)
    return (value & mask)

SV_MODE = {
    0: "OFF",
    8: "SV39",
    9: "SV48",
}

class Page(gdb.Command):
    def __init__(self):
        super(Page, self).__init__("page", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE, True)
        print("init page command!")

    def invoke(self, arg, from_tty):
        print("start exec page command...")

        satp = read_reg("satp")
        
        addr = extract(satp, 0, 43) << 12
        mode = extract(satp, 60, 63)

        print("MMU Mode:" + SV_MODE.get(mode, "unknown"))
        print("pgdir addr: [0x%x]" % addr)

        print("end exec page command!")

Page()
