from collections import defaultdict
import functools
import logging

logger = logging.getLogger(__name__)

UNSAFE_RW = True  # 4 times faster

OPCODE_ADD = 1   # add (x), (y), (z)  =>  (z) = (x) + (y)
OPCODE_MUL = 2   # mul (x), (y), (z)  =>  (z) = (x) * (y)
OPCODE_EXIT = 99

class Program(object):

    opcodes = {}

    def __init__(self, code):
        self.factory_settings = list(map(lambda x: int(x), code.strip().split(',')))
        self.reset()
        if UNSAFE_RW:
            self.read = self.unsafe_read
            self.write = self.unsafe_write

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
        (instr, mnemonic, length) = self.opcodes[opcode]
        if logger.isEnabledFor(logging.INFO):
            logger.info('Executing %s' % mnemonic.format(*self.mem[self.ip+1:self.ip+length]))
        self.count += 1
        self.instr_count[self.ip] += 1
        self.ip += 1
        instr(self)
        return not self.halted

    def show(self, addr):
        try:
            while addr < len(self.mem):
                opcode = self.mem[addr]
                if opcode in self.opcodes:
                    (instr, mnemonic, length) = self.opcodes[opcode]
                    line = '%5d %s' % (addr, mnemonic.format(*self.mem[addr+1:addr+length]))
                    if self.instr_count[addr]:
                        line = '%-30s [%d]' % (line, self.instr_count[addr])
                    print(line)
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

    def opcode_add(self):
        x = self.read(self.ip)
        y = self.read(self.ip+1)
        z = self.read(self.ip+2)
        self.ip += 3
        self.write(z, self.read(x)+self.read(y))

    def opcode_mul(self):
        x = self.read(self.ip)
        y = self.read(self.ip+1)
        z = self.read(self.ip+2)
        self.ip += 3
        self.write(z, self.read(x)*self.read(y))

    def opcode_exit(self):
        self.halted = True

    opcodes = {
        OPCODE_ADD: (opcode_add, 'ADD ({}), ({}), ({})', 4),
        OPCODE_MUL: (opcode_mul, 'MUL ({}), ({}), ({})', 4),
        OPCODE_EXIT: (opcode_exit, 'EXIT', 1),
    }


class MemoryOutOfBoundsException(Exception):
    '''Thrown when trying to read or write data outside of the given memory boundaries.'''
    pass

class MachineHaltedException(Exception):
    '''Thrown when trying to execute code while the machine is halted.'''
    pass

