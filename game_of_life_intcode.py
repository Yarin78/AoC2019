from goto import with_goto
from lib.intcode import *
from lib.intcode_decompile import *

class DecompiledProgram(DecompiledProgramBase):


    @with_goto
    def func0(self):
        # This instruction may get modified
        if self.mem[4]:
            goto .lbl_11
        self.mem[self.mem[7]] = self.mem[self.mem[5]] + self.mem[self.mem[6]]
        # This instruction may get modified
        # This instruction may get modified
        # This instruction may get modified
        label .lbl_11
        self.mem[6] = 317
        self.mem[7] = 3757
        self.mem[8] = self.mem[7]
        label .lbl_23
        self.mem[8] -= 1
        self.mem[9] = self.mem[8] + 3440
        self.mem[40] = self.mem[8]
        self.mem[42] = self.mem[9]
        self.mem[self.mem[42]] = self.mem[self.mem[40]]
        self.mem[10] = 1 if 317 == self.mem[8] else 0
        if not self.mem[10]:
            goto .lbl_23
        if self.mem[4]:
            goto .lbl_242
        # This instruction may get modified
        # This instruction may get modified
        # This instruction may get modified
        # This instruction may get modified
        # This instruction may get modified
        label .lbl_59
        self.mem[54] = self.mem[6] + 3440
        self.mem[55] = self.mem[7] + 3440
        self.mem[53] = 3440
        label .lbl_71
        self.mem[54] -= 1
        self.mem[55] -= 1
        self.mem[53] -= 1
        self.mem[56] = 0
        self.mem[92] = self.mem[54] - 81
        self.mem[57] = 1 if self.mem[self.mem[92]] == 79 else 0
        self.mem[56] += self.mem[57]
        self.mem[104] = self.mem[54] - 80
        self.mem[57] = 1 if self.mem[self.mem[104]] == 79 else 0
        self.mem[56] += self.mem[57]
        self.mem[116] = self.mem[54] - 79
        self.mem[57] = 1 if self.mem[self.mem[116]] == 79 else 0
        self.mem[56] += self.mem[57]
        self.mem[128] = self.mem[54] - 1
        self.mem[57] = 1 if self.mem[self.mem[128]] == 79 else 0
        self.mem[56] += self.mem[57]
        self.mem[140] = self.mem[54] + 1
        self.mem[57] = 1 if self.mem[self.mem[140]] == 79 else 0
        self.mem[56] += self.mem[57]
        self.mem[152] = self.mem[54] + 79
        self.mem[57] = 1 if self.mem[self.mem[152]] == 79 else 0
        self.mem[56] += self.mem[57]
        self.mem[164] = self.mem[54] + 80
        self.mem[57] = 1 if self.mem[self.mem[164]] == 79 else 0
        self.mem[56] += self.mem[57]
        self.mem[176] = self.mem[54] + 81
        self.mem[57] = 1 if self.mem[self.mem[176]] == 79 else 0
        self.mem[56] += self.mem[57]
        self.mem[5] = 1 if self.mem[56] == 3 else 0
        if self.mem[5]:
            goto .lbl_208
        self.mem[5] = 1 if self.mem[56] == 2 else 0
        if self.mem[5]:
            goto .lbl_219
        self.mem[204] = self.mem[55]
        self.mem[self.mem[204]] = 46
        if self.mem[4]:
            goto .lbl_231
        label .lbl_208
        self.mem[215] = self.mem[55]
        self.mem[self.mem[215]] = 79
        if self.mem[4]:
            goto .lbl_231
        label .lbl_219
        self.mem[228] = self.mem[54]
        self.mem[230] = self.mem[55]
        self.mem[self.mem[230]] = self.mem[self.mem[228]]
        label .lbl_231
        if self.mem[53]:
            goto .lbl_71
        if self.mem[4]:
            goto .lbl_242
        # This instruction may get modified
        # This instruction may get modified
        # This instruction may get modified
        label .lbl_242
        self.mem[239] = self.mem[7]
        self.mem[237] = 43
        label .lbl_250
        self.mem[237] -= 1
        self.mem[238] = 80
        label .lbl_258
        self.mem[238] -= 1
        self.output(self.mem[238])
        self.output(self.mem[237])
        self.mem[271] = self.mem[239]
        self.mem[5] = self.mem[self.mem[271]]
        self.mem[5] = 1 if self.mem[5] == 79 else 0
        self.output(self.mem[5])
        self.mem[239] += 1
        if self.mem[238]:
            goto .lbl_258
        if self.mem[237]:
            goto .lbl_250
        self.output(0)
        self.output(0)
        self.output(3)
        self.output(0)
        self.output(0)
        self.output(4)
        self.mem[5] = self.mem[6]
        self.mem[6] = self.mem[7]
        self.mem[7] = self.mem[5]
        if self.mem[4]:
            goto .lbl_59
        return

    funcs = {
      0: func0
    }

    code = [1005,4,11,0,1,0,0,0,0,0,0,1101,317,0,6,1101,317,3440,7,1001,7,0,8,1001,8,-1,8,1001,8,3440,9,1001,8,0,40,1001,9,0,42,1001,0,0,0,108,317,8,10,1006,10,23,1005,4,242,0,0,0,0,0,0,1001,6,3440,54,1001,7,3440,55,1101,3440,0,53,1001,54,-1,54,1001,55,-1,55,1001,53,-1,53,1101,0,0,56,1001,54,-81,92,1008,999999,79,57,1,57,56,56,1001,54,-80,104,1008,999999,79,57,1,57,56,56,1001,54,-79,116,1008,999999,79,57,1,57,56,56,1001,54,-1,128,1008,999999,79,57,1,57,56,56,1001,54,1,140,1008,999999,79,57,1,57,56,56,1001,54,79,152,1008,999999,79,57,1,57,56,56,1001,54,80,164,1008,999999,79,57,1,57,56,56,1001,54,81,176,1008,999999,79,57,1,57,56,56,1008,56,3,5,1005,5,208,1008,56,2,5,1005,5,219,1001,55,0,204,1101,46,0,999999,1005,4,231,1001,55,0,215,1101,79,0,999999,1005,4,231,1001,54,0,228,1001,55,0,230,1001,54,0,55,1005,53,71,1005,4,242,0,0,0,0,0,1001,7,0,239,1101,43,0,237,1001,237,-1,237,1101,80,0,238,1001,238,-1,238,4,238,4,237,1001,239,0,271,1001,0,0,5,1008,5,79,5,4,5,1001,239,1,239,1005,238,258,1005,237,250,104,0,104,0,104,3,104,0,104,0,104,4,1001,6,0,5,1001,7,0,6,1001,5,0,7,1005,4,59,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,46,46,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,46,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,46,46,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,46,46,79,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,46,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,46,46,46,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,79,46,46,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,79,79,79,79,46,46,46,46,46,46,46,46,46,46,79,79,46,46,79,79,46,79,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,79,79,46,79,79,79,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,79,79,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,79,79,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46
]


if __name__ == "__main__":
    from lib.util import *
    from lib.geo2d import *
    prog = DecompiledProgram()
    prog.init_io(Queue(), Queue())
    t = prog.start_async()
    map = defaultdict(int)
    while True:
        x = prog._output.get()
        y = prog._output.get()
        tile = prog._output.get()
        map[Point(x,y)] = tile
        if x == 0 and y == 0:
            print_array(gridify_sparse_map(map))
            print("\033[1;1H")
