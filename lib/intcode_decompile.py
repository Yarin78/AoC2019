import logging
from queue import Queue
from lib.intcode import *

MODE_POSITION = 0
MODE_IMMEDIATE = 1
MODE_RELATIVE = 2

# addr -> [bool-array] with possible outcomes of a jump condition check
OVERRIDE_JUMP_CONDITIONS = {}
# addr -> addr   overriding target address of jump if it can't be determined correctly
OVERRIDE_TARGET_ADDRESS = {636: 482}

'''Represents a proper function in intcode. The start address is the unique identifier.'''
class Function:

    def __init__(self, id, length):
        self.id = id
        self.length = length


def extract_funcions(prog, *ip):
    '''Detects all functions reachable from the given addresses.
    Returns a List[Function]'''

    funcs = {}  # start_addr -> Function
    addr_func = {}  # addr -> function id

    funcq = Queue()  # queue of address of all function starts
    for addr in ip:
        funcq.put(addr)
    while not funcq.empty():  # processing a function
        start_ip = funcq.get()
        if start_ip in funcs:
            continue  # Already done this function

        if start_ip in addr_func:
            logging.warning('Tried to start extracting function at %d but that address is already covered by function at %d' % (start_ip, addr_func[start_ip]))
            continue

        logging.info('Function %d' % start_ip)
        func_addr = set()  # all addresses that are part of this function
        ret_addr = {}  # ret_addr[x] = y  => the return address y was set at x
        ipq = Queue()  # queue of addresses reachable within the current function
        ipq.put(start_ip)
        while not ipq.empty():
            ip = ipq.get()
            if ip < 0 or ip > prog.last_addr():
                logging.warning('Trying to read outside memory at %d' % ip)
                continue
            if ip in func_addr:
                # This is ok, can be a loop or something
                continue
            if ip in addr_func:
                # This is not ok; what was thought to be two functions are intermingled
                logging.warning('Function %d reached address %d, which is included in function %d' % (start_ip, ip, all_addr[ip]))

            (opcode, params, modes) = decode(prog, ip)
            opcode_len = 1 + len(params)

            if opcode not in prog.opcodes:
                logging.warning('Unknown opcode at %d' % ip)
                continue

            # Mark the memory of this instruction as belonging to this function
            for i in range(opcode_len):
                if ip + i in func_addr:
                    # Overlapping opcodes - this is weird
                    logging.warning('Part of opcode at %d was already covered in this function' % (ip + i))
                elif ip + i in addr_func:
                    # This is odd, should have been caught earlier
                    logging.warning('Part of opcode at %d was covered by function %d' % (ip+i, addr_func[ip+i]))
                    continue
                func_addr.add(ip + i)

            if opcode in [OPCODE_JUMP_TRUE, OPCODE_JUMP_FALSE]:
                jump_type = 'jump'
                # If a hard return address was written to (BP) the previous instruction,
                # then this is probably a call, not a jump
                if ip-4 in ret_addr:
                    jump_type = 'call'
                poss = possible_jump_conditions(prog, ip, jump_type)
                s = 'Possible' if len(poss) == 2 else 'Mandatory'
                for v in poss:
                    if v:
                        # The jump/call/return may happen
                        if modes[1] == MODE_RELATIVE and params[1] == 0:
                            # Return statement
                            logging.info('%s return at %d' % (s, ip))
                        else:
                            target = None
                            if ip in OVERRIDE_TARGET_ADDRESS:
                                target = OVERRIDE_TARGET_ADDRESS[ip]
                                logging.info('%s %s to %d from %d (target override)' % (s, jump_type, target, ip))
                            elif modes[1] == MODE_IMMEDIATE:
                                target = params[1]
                                logging.info('%s %s to %d from %d' % (s, jump_type, target, ip))

                            if target is not None:
                                if jump_type == 'jump':
                                    ipq.put(target)
                                else:
                                    funcq.put(target)
                                    ipq.put(ret_addr[ip-4])

                            elif modes[1] == MODE_RELATIVE:
                                # !?
                                logging.warning('Target address of %s at %d was relative but not a return statement; more investigation needed' % (jump_type, ip))
                            else:
                                logging.warning('Target address of %s at %d not known; more investigation needed' % (jump_type, ip))

                    else:
                        # The jump may not happen
                        ipq.put(ip + opcode_len)
            elif opcode != OPCODE_HALT:
                fv = fixed_value(prog, ip)
                if fv is not None and modes[2] == MODE_RELATIVE and params[2] == 0:
                    logging.info('At %d, set return address to %d' % (ip, fv))
                    if fv != ip+7:
                        # Warn if we don't have the pattern
                        # X: <set return address to X+7>
                        # X+4: <call somewhere>
                        # X+7: <continue here after return>
                        logging.warning('Return address is not the expected one')
                    ret_addr[ip] = fv

                ipq.put(ip + opcode_len)


        # Verify function is continuous and sane
        # Otherwise something is fishy and will break later on
        func_len = max(func_addr) - min(func_addr) + 1
        if min(func_addr) != start_ip:
            logging.warning('Function %d reached earlier byte at %d' % (start_ip, min(func_addr)))
        else:
            if func_len != len(func_addr):
                logging.warning('Function %d covered range [%d,%d] but only %d bytes reached.' % (start_ip, min(func_addr), max(func_addr), len(func_addr)))
            else:
                logging.info('Successfully identified function [%d,%d]' % (start_ip, max(func_addr)))
            funcs[start_ip] = Function(start_ip, func_len)
            for addr in func_addr:
                addr_func[addr] = start_ip

    return funcs


def possible_jump_conditions(prog, ip, jump_type='jump'):
    '''Returns an array with bools if the jump can happen or not; true if it can happen,
    false if not. If it can't be determined for sure, returns [False, True].
    This can be overridden by setting OVERRIDE_JUMP_CONDITIONS.
    '''
    opcode = prog.read(ip)
    mode = (opcode // 100) % 10  # mode of the variable being checked
    opcode %= 100
    assert opcode in [OPCODE_JUMP_FALSE, OPCODE_JUMP_TRUE]
    if ip in OVERRIDE_JUMP_CONDITIONS:
        logging.info('%s at %d is overridden to %s' % (jump_type.capitalize(), ip, str(OVERRIDE_JUMP_CONDITIONS[ip])))
        return OVERRIDE_JUMP_CONDITIONS[ip]
    if mode != MODE_IMMEDIATE:
        logging.info('%s at %d is conditional' % (jump_type.capitalize(), ip))
        return [False, True]  # indirect addressing, we can't know for sure
    v = prog.read(ip+1)
    will_jump = (v != 0) == (opcode == OPCODE_JUMP_TRUE)
    logging.info('%s at %d will %s happen' % (jump_type.capitalize(), ip, 'always' if will_jump else 'never'))
    return [will_jump]

def fixed_value(prog, ip):
    '''If the MOV or MUL instruction at ip always writes a fixed integer, return that integer.
    Otherwise return None.'''
    opcode = prog.read(ip)
    p1 = prog.read(ip+1)
    p2 = prog.read(ip+2)
    modes = opcode // 100
    opcode %= 100
    m1 = modes % 10
    m2 = (modes // 10) % 10

    if opcode == OPCODE_MUL:
        if m1 == MODE_IMMEDIATE and p1 == 0:
            return 0
        if m2 == MODE_IMMEDIATE and p2 == 0:
            return 0
        if m1 == MODE_IMMEDIATE and m2 == MODE_IMMEDIATE:
            return p1 * p2
        return None
    elif opcode == OPCODE_ADD:
        if m1 == MODE_IMMEDIATE and m2 == MODE_IMMEDIATE:
            return p1 + p2
        return None
    else:
        return None


def decode(prog, ip):
    '''Returns a tuple (opcode, [p0, p1, ...], [mode0, mode1, ...])'''
    opcode = prog.read(ip)
    param_mode = opcode // 100
    opcode %= 100
    params = []
    param_modes = []
    if opcode in prog.opcodes:
        opcode_len = prog.opcodes[opcode][2]

        for i in range(1, opcode_len):
            x = prog.read(ip + i)
            param_modes.append(param_mode % 10)
            params.append(x)
            param_mode //= 10

    return (opcode, params, param_modes)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    code = '3,8,1005,8,330,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,102,1,8,29,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,51,1,1103,2,10,1006,0,94,1006,0,11,1,1106,13,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,87,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,109,2,1105,5,10,2,103,16,10,1,1103,12,10,2,105,2,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,146,1006,0,49,2,1,12,10,2,1006,6,10,1,1101,4,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,183,1,6,9,10,1006,0,32,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,213,2,1101,9,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,239,1006,0,47,1006,0,4,2,6,0,10,1006,0,58,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,274,2,1005,14,10,1006,0,17,1,104,20,10,1006,0,28,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1002,8,1,309,101,1,9,9,1007,9,928,10,1005,10,15,99,109,652,104,0,104,1,21101,0,937263411860,1,21102,347,1,0,1105,1,451,21101,932440724376,0,1,21102,1,358,0,1105,1,451,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,0,29015167015,1,21101,0,405,0,1106,0,451,21102,1,3422723163,1,21101,0,416,0,1106,0,451,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,868389376360,1,21101,0,439,0,1105,1,451,21102,825544712960,1,1,21102,1,450,0,1106,0,451,99,109,2,21201,-1,0,1,21101,0,40,2,21102,482,1,3,21102,1,472,0,1106,0,515,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,477,478,493,4,0,1001,477,1,477,108,4,477,10,1006,10,509,1101,0,0,477,109,-2,2106,0,0,0,109,4,2101,0,-1,514,1207,-3,0,10,1006,10,532,21102,1,0,-3,22101,0,-3,1,22102,1,-2,2,21102,1,1,3,21101,551,0,0,1106,0,556,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,579,2207,-4,-2,10,1006,10,579,22102,1,-4,-4,1106,0,647,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21102,1,598,0,1106,0,556,22101,0,1,-4,21101,1,0,-1,2207,-4,-2,10,1006,10,617,21102,0,1,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,639,21201,-1,0,1,21102,639,1,0,105,1,514,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0'
    prog = Program(code)
    functions = extract_funcions(prog, 0)
    for f in functions.values():
        print(f.id, f.id+f.length-1)
