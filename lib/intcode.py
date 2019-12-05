from collections import defaultdict
import functools
import logging

logger = logging.getLogger(__name__)

UNSAFE_RW = True  # 4 times faster

OPCODE_ADD = 1   # add (x), (y), (z)  =>  (z) = (x) + (y)
OPCODE_MUL = 2   # mul (x), (y), (z)  =>  (z) = (x) * (y)
OPCODE_IN = 3  # in (x)
OPCODE_OUT = 4  # out (x)
OPCODE_JUMP_TRUE = 5
OPCODE_JUMP_FALSE = 6
OPCODE_LESS_THAN = 7
OPCODE_EQUALS = 8
OPCODE_HALT = 99

class Program(object):

    opcodes = {}

    def __init__(self, code, input=None):
        self.factory_settings = list(map(lambda x: int(x), code.strip().split(',')))
        self.reset()
        if UNSAFE_RW:
            self.read = self.unsafe_read
            self.write = self.unsafe_write

        self.input = input
        self.input_pos = 0
        self.output = []

    def reset(self):
        self.mem = self.factory_settings[:]
        self.ip = 0
        self.count = 0  # num instructions executed
        self.instr_count = [0]*len(self.mem)
        self.halted = False

    def log_debug(self):
        logging.basicConfig(level=logging.DEBUG)

    def log_info(self):
        logging.basicConfig(level=logging.INFO)

    def log_warn(self):
        logging.basicConfig(level=logging.WARNING)

    def unsafe_read(self, addr):
        return self.mem[addr]

    def unsafe_write(self, addr, data):
        self.mem[addr] = data

    def read(self, addr):
        if addr < 0 or addr >= len(self.mem):
            raise MemoryOutOfBoundsException("Tried reading at mem address %d" % addr)
        data = self.mem[addr]
        logger.debug('Reading {} from [{}]'.format(data, addr))
        return data

    def write(self, addr, data):
        logger.debug('Writing {} to [{}]'.format(data, addr))
        if addr < 0 or addr >= len(self.mem):
            raise MemoryOutOfBoundsException("Tried writing at mem address %d" % addr)
        self.mem[addr] = data

    def run(self, steps=0):
        if steps:
            while steps > 0 and self.step():
                pass
        else:
            while self.step():
                pass

    def step(self):
        if self.halted:
            raise MachineHaltedException()
        opcode = self.read(self.ip)
        param_mode = opcode // 100
        opcode %= 100
        (instr, mnemonic, length, write_par) = self.opcodes[opcode]
        params = []
        for i in range(1, length):
            x = self.read(self.ip + i)
            if i == write_par:
                assert param_mode % 10 == 0
            elif param_mode % 10 == 0:
                x = self.read(x)
            param_mode //= 10
            params.append(x)

        if logger.isEnabledFor(logging.INFO):
            logger.info('%5d: Executing %s' % (self.ip, self.decode(self.ip)))
        self.count += 1
        self.instr_count[self.ip] += 1
        self.ip += length
        instr(self, *params)
        return not self.halted

    def decode(self, addr):
        # Converts instruction to mnemonic
        opcode = self.read(addr)
        param_mode = opcode // 100
        opcode %= 100
        if opcode not in self.opcodes:
            return 'DB %d' % opcode
        (instr, mnemonic, length, write_par) = self.opcodes[opcode]
        mnemonic += ' '
        for i in range(1, length):
            if i > 1:
                mnemonic += ', '
            x = self.read(addr + i)
            if param_mode % 10 == 0:
                mnemonic += '(%d)' % x
            else:
                mnemonic += '#%d' % x
            param_mode //= 10
        return mnemonic

    def show(self, addr):
        try:
            while addr < len(self.mem):
                opcode = self.mem[addr] % 100
                if opcode in self.opcodes:
                    line = '%5d %s' % (addr, self.decode(addr))
                    if self.instr_count[addr]:
                        line = '%-30s [%d]' % (line, self.instr_count[addr])
                    print(line)
                    (_, _, length, _) = self.opcodes[opcode]
                    addr += length
                else:
                    print('%5d DB %d' % (addr, opcode))
                    addr += 1
        except:
            pass

    def hotspots(self):
        # Might want to use show instead
        for i in range(len(self.instr_count)):
            if self.instr_count[i] > 0:
                print('%5d %15d' % (i, self.instr_count[i]))

    def opcode_add(self, x, y, z):
        self.write(z, x + y)

    def opcode_mul(self, x, y, z):
        self.write(z, x * y)

    def opcode_in(self, x):
        self.write(x, self.input[self.input_pos])
        self.input_pos += 1

    def opcode_out(self, x):
        self.output.append(x)

    def opcode_jump_true(self, x, y):
        if x != 0:
            self.ip = y

    def opcode_jump_false(self, x, y):
        if x == 0:
            self.ip = y

    def opcode_less_than(self, x, y, z):
        self.write(z, 1 if x < y else 0)

    def opcode_equals(self, x, y, z):
        self.write(z, 1 if x == y else 0)

    def opcode_exit(self):
        self.halted = True

    # (function, mnemonic, length, lvalue param)
    opcodes = {
        OPCODE_ADD: (opcode_add, 'ADD', 4, 3),
        OPCODE_MUL: (opcode_mul, 'MUL', 4, 3),
        OPCODE_IN: (opcode_in, 'IN', 2, 1),
        OPCODE_OUT: (opcode_out, 'OUT', 2, -1),
        OPCODE_HALT: (opcode_exit, 'HALT', 1, -1),
        OPCODE_JUMP_TRUE: (opcode_jump_true, 'JMPT', 3, -1),
        OPCODE_JUMP_FALSE: (opcode_jump_false, 'JMPF', 3, -1),
        OPCODE_LESS_THAN: (opcode_less_than, 'LT', 4, 3),
        OPCODE_EQUALS: (opcode_equals, 'EQ', 4, 3)
    }


class MemoryOutOfBoundsException(Exception):
    '''Thrown when trying to read or write data outside of the given memory boundaries.'''
    pass

class MachineHaltedException(Exception):
    '''Thrown when trying to execute code while the machine is halted.'''
    pass

