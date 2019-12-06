from collections import defaultdict
from queue import Queue, Empty
import functools
import logging
import sys

logger = logging.getLogger(__name__)

UNSAFE_RW = True  # 4 times faster

# Behaviour when trying to read and there is nothing on the input
# Default is to pause the machine (and not update the IP)
CRASH_ON_EOF = False  # Raise exception if trying to read from input when there is no data
BLOCK_ON_EOF = False  # Block calling thread if trying to read from input when there is no data


# The parameters are called x, y, z
OPCODE_ADD = 1         # z = x + y
OPCODE_MUL = 2         # z = x * y
OPCODE_IN = 3          # x = <value from input>
OPCODE_OUT = 4         # <write x to output>
OPCODE_JUMP_TRUE = 5   # if x<>0 then jump y
OPCODE_JUMP_FALSE = 6  # if x=0 then jump y
OPCODE_LESS_THAN = 7   # z = x < y ? 1 : 0
OPCODE_EQUALS = 8      # z = x == y ? 1 : 0
OPCODE_HALT = 99

class Program(object):

    opcodes = {}

    def __init__(self, code, prog_id=0):
        self.factory_settings = list(map(lambda x: int(x), code.strip().split(',')))
        self.reset()
        if UNSAFE_RW:
            self.read = self.unsafe_read
            self.write = self.unsafe_write

        self.output = []
        self.prog_id = prog_id
        self.init_io(None, None)

    def reset(self):
        self.mem = self.factory_settings[:]
        self.ip = 0
        self.count = 0  # num instructions executed
        self.instr_count = [0]*len(self.mem)
        self.halted = False
        self.blocked_on_input = False

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

    def init_io(self, input=None, output=None):
        if input is None:
            self.input = StdinSource()
        elif isinstance(input, list):
            self.input = Queue()
            for x in input:
                self.input.put(x)
        else:
            self.input = input

        if output is None:
            self.output = StdoutSink()
        else:
            self.output = output

    def run(self, input=None, output=None, steps=0):
        self.init_io(input, output)
        if steps:
            while steps > 0 and self.step():
                pass
        else:
            while self.step():
                pass

        if isinstance(self.output, ReturnSink):
            return self.output.values

    def step(self):
        if self.halted:
            raise MachineHaltedException()
        if self.ip < 0 or self.ip >= len(self.mem):
            raise ProgramOutOfBoundsException()
        opcode = self.read(self.ip)
        param_mode = opcode // 100
        opcode %= 100
        if opcode not in self.opcodes:
            raise UnknownOpcodeException()
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
            logger.info('%2d %5d: Executing %s' % (self.prog_id, self.ip, self.decode(self.ip)))
        self.count += 1
        self.instr_count[self.ip] += 1
        default_new_ip = self.ip + length
        new_ip = instr(self, *params)
        self.ip = default_new_ip if new_ip is None else new_ip  # Must distinguish 0 and None
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

    # If an opcode returns a non-value, it's the value of the new IP
    # Otherwise the length of the opcode is added to the IP

    def opcode_add(self, x, y, z):
        self.write(z, x + y)

    def opcode_mul(self, x, y, z):
        self.write(z, x * y)

    def opcode_in(self, x):
        if BLOCK_ON_EOF:
            try:
                self.write(x, self.input.get())
                self.blocked_on_input = False
            except Empty:
                # If we have multiple queues as input, this can happen because
                # we have no good way of blocking.
                self.blocked_on_input = True
                return self.ip
        elif CRASH_ON_EOF:
            self.write(x, self.input.get_nowait())
            self.blocked_on_input = False
        else:
            try:
                value = self.input.get_nowait()
                logger.info('%2d        Read %d' % (self.prog_id, value))
                self.write(x, value)
                self.blocked_on_input = False
            except Empty:
                logger.info('%2d        Blocked' % (self.prog_id))
                self.blocked_on_input = True
                return self.ip

    def opcode_out(self, x):
        self.output.put(x)

    def opcode_jump_true(self, x, y):
        if x != 0:
            return y

    def opcode_jump_false(self, x, y):
        if x == 0:
            return y

    def opcode_less_than(self, x, y, z):
        self.write(z, 1 if x < y else 0)

    def opcode_equals(self, x, y, z):
        self.write(z, 1 if x == y else 0)

    def opcode_exit(self):
        self.halted = True
        return self.ip

    # (function, mnemonic, length, lvalue param)
    # If a function has a variable number of parameters, set length=1
    # and parse the params manually in the instruction
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


def wire_up_serial(programs, input, output):
    '''Connects multiple programs with each other in a sequence.'''
    pipes = [Queue() for _ in range(len(programs) - 1)]
    for i in range(len(programs)):
        programs[i].init_io(pipes[i-1] if i > 0 else input, pipes[i] if i < len(programs) - 1 else output)


def parallel_executor(programs):
    '''Executes one instruction at a time across all programs in round robin fashion,
    until they're all halted. Assumes the IO has already been setup.
    Returns the an array, one element per input program. If the output is a ReturnSink
    for a program, the corresponding element will contain that list, otherwise null.
    '''

    while True:
        all_halted = True
        all_blocked = True
        for prog in programs:
            if not prog.halted:
                prog.step()
                if not prog.blocked_on_input:
                    all_blocked = False
                all_halted = False
        if all_halted:
            break
        if all_blocked:
            raise MachineBlockedException()

    result = []
    for prog in programs:
        if isinstance(prog.output, ReturnSink):
            result.append(prog.output.values)
        else:
            result.append(None)
    return result

class MemoryOutOfBoundsException(Exception):
    '''Thrown when trying to read or write data outside of the given memory boundaries.'''
    pass

class MachineHaltedException(Exception):
    '''Thrown when trying to execute code while the machine is halted.'''
    pass

class MachineBlockedException(Exception):
    '''Thrown when trying to execute code and the machine is blocked on input.'''
    pass

class ProgramOutOfBoundsException(Exception):
    '''Tried to execute an instruction outside of the programs memory.'''
    pass

class UnknownOpcodeException(Exception):
    '''Tried to execute an unknown opcode.'''
    pass

class ReturnSink(object):
    def __init__(self):
        self.values = []

    def put(self, x):
        self.values.append(x)

class StdoutSink(object):
    def put(self, x):
        sys.stdout.write(str(x) + '\n')

class StdinSource(object):
    def get(self):
        s = sys.stdin.readline()
        if s == '':
            raise MachineBlockedException()
        return int(s)

    def get_nowait(self):
        s = sys.stdin.readline()
        if s == '':
            raise Empty()
        return int(s)

class JoinedSource(object):
    '''Gets input from multiple sources.'''
    def __init__(self, queues):
        self.queues = queues

    def get(self):
        # No good way of doing a blocking get here
        return self.get_nowait()

    def get_nowait(self):
        # Need multiprocessing queues here
        for q in self.queues:
            try:
                return q.get_nowait()
            except Empty:
                pass
        raise Empty()

class DuplicateSink(object):
    '''Sends the same output to multiple output sources.'''
    def __init__(self, queues):
        self.queues = queues

    def put(self, x):
        for q in self.queues:
            q.put(x)


if __name__ == "__main__":
    adder_code = "3,0,1001,0,1,0,4,0,99"
    prog = Program(adder_code)
    prog.run(input=StdinSource(), output=StdoutSink())
