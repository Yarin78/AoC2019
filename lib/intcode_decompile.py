import logging
import itertools
from queue import Queue
from lib.intcode import *

MODE_POSITION = 0
MODE_IMMEDIATE = 1
MODE_RELATIVE = 2

MAX_FRAME_SIZE = 15

# addr -> [bool-array] with possible outcomes of a jump condition check
OVERRIDE_JUMP_CONDITIONS = {}
# addr -> addr   overriding target address of jump if it can't be determined correctly
OVERRIDE_TARGET_ADDRESS = {}
#OVERRIDE_TARGET_ADDRESS = {636: 482}  # day 11

LOCAL_VARIABLES = {}   # set of mem addresses that is only access within a function
GLOBAL_VARIABLES = {}  # set of mem addresses that may be accessed from anywhere


class Node:
    addr = 0   # The address in memory where this node starts
    addr_len = 0  # The number of consecutive bytes this node consumes; may include multiple opcodes
    instr = None  # Instructions at this node
    children = None # Possible next nodes
    parents = None # Possible previous nodes

    def __init__(self, addr, decompiler, func):
        self.addr = addr
        self.decompiler = decompiler
        self.func = func
        (opcode, params, modes) = decompiler.decode(addr)
        self.instr = [(opcode, params, modes)]
        self.addr_len = len(params) + 1
        self.children = []
        self.parents = []
        self.variables_assigned = set()  # variables guaranteed to be assigned

    def get_param_str(self, param_modes):
        param_str = []
        for (param, mode) in param_modes:
            if mode == MODE_POSITION:
                param_str.append(self.decompiler.mem_address(param))
            elif mode == MODE_RELATIVE:
                param_str.append(self._local_var_name(param))
            else:
                param_str.append(str(param))
        return param_str

    def generate_code(self, next_node):
        '''Generates the code for this node.
        next_node is the next node to have code generated.'''
        codes = []
        ip = self.addr
        for j in range(len(self.instr)):
            (opcode, params, modes) = self.instr[j]
            param_str = self.get_param_str(zip(params, modes))
            is_return_addr = (0, MODE_RELATIVE) in zip(params, modes)

            if opcode in [OPCODE_ADD, OPCODE_MUL]:
                if is_return_addr:
                    # Don't generate any code for read/writing the return address
                    code = ''
                else:
                    fv = fixed_value(opcode, params, modes)
                    if fv is not None:
                        code = '%s = %d' % (param_str[2], fv)
                    else:
                        code = self._add_mul_code(opcode, param_str, modes)
            elif opcode == OPCODE_IN:
                code = '%s = self.input()' % param_str[0]
            elif opcode == OPCODE_OUT:
                code = 'self.output(%s)' % param_str[0]
            elif opcode == OPCODE_LESS_THAN:
                code = '%s = 1 if %s < %s else 0' % (param_str[2], param_str[0], param_str[1])
            elif opcode == OPCODE_EQUALS:
                code = '%s = 1 if %s == %s else 0' % (param_str[2], param_str[0], param_str[1])
            elif opcode == OPCODE_ADD_BP:
                code = ''
            elif opcode == OPCODE_HALT:
                code = 'self.halted = True'
            elif opcode in [OPCODE_JUMP_TRUE, OPCODE_JUMP_FALSE]:
                if j != len(self.instr) - 1:
                    # Can happen if a jump can never be evaluated to true
                    code = ''
                elif len(self.children) < 2:
                    # No branch, the jump will be taken care of elsewhere
                    code = ''
                    if ip in self.func.func_calls:
                        (target_addr, _) = self.func.func_calls[ip]
                        if target_addr is None:
                            code = '<unknown call>'
                        else:
                            # If we call a function with frame_size 5 (4 parameters/local vars),
                            # all of them may not have been set.
                            num_params_set = len(list(itertools.takewhile(
                                lambda x: self._local_var_name(x) in self.variables_assigned,
                                range(1, 20))))
                            code = self.decompiler.functions[target_addr].call_instr(num_params_set)
                else:
                    if ip in self.func.func_calls:
                        logging.warning('Conditional function calls not supported (%d)' % ip)
                    condition = param_str[0]
                    if opcode == OPCODE_JUMP_FALSE:
                        condition = 'not %s' % condition
                    code = [
                        'if %s:' % condition,
                        '    goto .lbl_%d' % self.children[1].addr
                    ]
            else:
                assert False
            if isinstance(code, list):
                codes.extend(code)
            else:
                codes.append(code)

            ip += 1 + len(params)

        if len(self.children) == 0:
            codes.append(self.func.return_statement())
        elif self.children[0].addr != next_node.addr:
            codes.append('goto .lbl_%d' % self.children[0].addr)

        return codes

    def get_target_variable(self):
        # Gets the variable that gets assigned a value in this node, if any
        for j in range(len(self.instr)):  # Should only be one instruction in here that can write to sth
            (opcode, params, modes) = self.instr[j]
            param_str = self.get_param_str(zip(params, modes))
            if opcode in [OPCODE_ADD, OPCODE_MUL, OPCODE_IN, OPCODE_LESS_THAN, OPCODE_EQUALS]:
                if param_str[-1] != 'RET_ADDR':
                    return param_str[-1]
        return None

    def _local_var_name(self, rel_addr):
        if rel_addr > 0:
            return 'q%d' % (rel_addr - 1)
        elif rel_addr < 0:
            return 'p%d' % (self.func.frame_size + rel_addr - 1)
        else:
            return 'RET_ADDR'

    def _add_mul_code(self, opcode, params, modes):
        sign = '+' if opcode == OPCODE_ADD else '*'
        if sign == '+' and params[1].startswith('-'):
            sign = '-'
            params[1] = params[1][1:]
        code = '%s = %s %s %s' % (params[2], params[0], sign, params[1])
        if (opcode == OPCODE_ADD and params[0] == '0') or (opcode == OPCODE_MUL and params[0] == '1'):
            if params[2] == params[1]:
                code = ''
            else:
                code = '%s = %s' % (params[2], params[1])
        elif (opcode == OPCODE_ADD and params[1] == '0') or (opcode == OPCODE_MUL and params[1] == '1'):
            if params[2] == params[0]:
                code = ''
            else:
                code = '%s = %s' % (params[2], params[0])
        elif params[2] == params[1]:
            if sign == '*' and params[0] == '-1':
                code = '%s = -%s' % (params[2], params[2])
            else:
                code = '%s %s= %s' % (params[2], sign, params[0])
        elif params[2] == params[0]:
            if sign == '*' and params[1] == '-1':
                code = '%s = -%s' % (params[2], params[2])
            else:
                code = '%s %s= %s' % (params[2], sign, params[1])
        return code


'''Represents a proper function in intcode. The start address is the unique identifier.'''
class Function:

    def __init__(self, decompiler, id, length, frame_size, func_calls):
        self.decompiler = decompiler
        self.id = id
        self.length = length
        self.frame_size = frame_size
        self.func_calls = func_calls  # addr -> (target addr, return addr)
        self.nodes = None

    def name(self):
        return 'func%d' % self.id

    def call_instr(self, num_params_set):
        if self.frame_size > MAX_FRAME_SIZE:
            return 'self.%s()' % self.name()
        call_params = ', '.join(['q%d' % x for x in range(min(num_params_set, self.frame_size - 1))])
        ret_params = ', '.join(['q%d' % x for x in range(self.frame_size - 1)])
        return '(%s) = self.%s(%s)' % (ret_params, self.name(), call_params)

    def definition(self):
        if self.frame_size > MAX_FRAME_SIZE:
            return 'def %s(self):' % (self.name())
        params = ', '.join(['p%d=0' % x for x in range(self.frame_size - 1)])
        return 'def %s(self, %s):' % (self.name(), params)

    def return_statement(self):
        if self.frame_size > MAX_FRAME_SIZE:
            return 'return'
        params = ', '.join(['p%d' % x for x in range(self.frame_size - 1)])
        return 'return (%s)' % params

    def required_labels(self, node_order):
        # Stupid way of figuring out what labels are needed, should improve this
        labels = set()
        for i in range(len(node_order)):
            next_node = node_order[i+1] if i+1 < len(node_order) else None
            for child in node_order[i].children:
                if child != next_node:
                    labels.add(child.addr)
        return labels

    def generate_code(self, include_mnemonic=True):
        '''Generates code for this functino.'''
        lines = []

        if self.nodes is None:
            logging.warning('No nodes for function %s' % self.name())
            return lines
        lines.append('    @with_goto')
        lines.append('    %s' % self.definition())

        node_order = list(self.nodes.values())

        labels = self.required_labels(node_order)

        for i in range(len(node_order)):
            node = node_order[i]
            next_node = node_order[i+1] if i+1 < len(node_order) else None
            if include_mnemonic:
                (mnemonic, _) = self.decompiler.prog.decode(node.addr)
                lines.append('        # %4d: %s' % (node.addr, mnemonic))
                #lines.append('        # %s' % str(node.variables_assigned))
            if node.addr in labels:
                lines.append('        label .lbl_%d' % node.addr)
            for line in node.generate_code(next_node):
                if line:
                    lines.append('        %s' % line)

        return lines

    def set_variable_assignments(self):
        '''Checks what variables are guaranteed to be assigned at different addresses.'''
        node_order = list(self.nodes.values())
        for node in node_order:
            va = None
            if node.parents:
                for parent in node.parents:
                    if parent.variables_assigned is not None:
                        if va is None:
                            va = parent.variables_assigned
                        else:
                            va = va.intersection(parent.variables_assigned)
            if va is None:
                va = set()
            var = node.get_target_variable()
            va = set(va)  # clone it
            if var is not None:
                va.add(var)
            node.variables_assigned = va
            #logging.warning('Setting va in %d to %s' % (node.addr, str(va)))


    def build_code_graph(self):
        '''Returns a graph with the code execution flow in a function.
        Each node in the created graph represents one opcode and has
        0, 1 or 2 "next addresses" within the same function.
        '''
        next_addr = {}  # addr -> [next_addr]

        ip = self.id

        # Process the instructions in order
        while ip < self.id + self.length:
            next_addr[ip] = []
            (opcode, params, modes) = self.decompiler.decode(ip)
            if ip in self.func_calls:
                jc = self.decompiler.possible_jump_conditions(ip, 'call')
                if True in jc:
                    next_addr[ip].append(self.func_calls[ip][1])  # The return address
                if False in jc:
                    # Conditional function calls; not sure we can have this
                    logging.warning('Conditional function call at %d' % ip)
                    next_addr[ip].append(ip+3)
            elif opcode in [OPCODE_JUMP_TRUE, OPCODE_JUMP_FALSE]:
                jc = self.decompiler.possible_jump_conditions(ip)
                if False in jc:
                    next_addr[ip].append(ip + 3)
                if True in jc:
                    if modes[1] == MODE_RELATIVE and params[1] == 0:
                        # Return statement, no more instructions in this function
                        pass
                    else:
                        target = self.decompiler.jump_target(ip)
                        if target is not None:
                            next_addr[ip].append(target)
                        else:
                            logging.warning('Unknown jump target at %d' % ip)
            elif opcode not in [OPCODE_HALT]:
                next_addr[ip].append(ip + 1 + len(params))

            ip += 1 + len(params)

        self.nodes = {}
        for ip, _ in next_addr.items():
            self.nodes[ip] = Node(ip, self.decompiler, self)

        for ip, addrs in next_addr.items():
            for addr in addrs:
                if addr not in self.nodes:
                    # Not good, weird code; hopefully doesn't happen
                    logging.warning('Jump from %d to address %d outside function' % (ip, addr))
                else:
                    self.nodes[ip].children.append(self.nodes[addr])
                    self.nodes[addr].parents.append(self.nodes[ip])


class Decompiler:

    prog = None
    functions = None  # addr -> Function

    def __init__(self, prog):
        self.prog = prog

    def decompile(self, start):
        # TODO: Pass in override options
        # TODO: Add something that finds potential function start points
        self.functions = self.extract_functions(start)
        for func in self.functions.values():
            func.build_code_graph()
            func.set_variable_assignments()

    def generate_code(self):
        lines = []
        lines.append('from goto import with_goto')
        lines.append('from lib.intcode import *')
        lines.append('')
        lines.append('class DecompiledProgram(Program):')
        #lines.append('')
        #lines.append('    def __init__(self, input, output):')
        #lines.append('        self.input = input')
        #lines.append('        self.output = output')
        for func in self.functions.values():
            lines.append('')
            lines.extend(func.generate_code())
        return lines

    def extract_functions(self, *ip):
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

            # Determine frame size
            (opcode, params, modes) = self.decode(start_ip)
            if opcode == OPCODE_ADD_BP and modes[0] == MODE_IMMEDIATE:
                frame_size = params[0]
            else:
                frame_size = 0

            logging.info('Function %d with frame size %d' % (start_ip, frame_size))

            func_addr = set()  # all addresses that are part of this function
            func_calls = {}  # func_calls[x] = (y, z)  => at addr x we're calling function at y and return to address z
            ret_addr = {}  # ret_addr[x] = y  => the return address y was set at x
            ipq = Queue()  # queue of addresses reachable within the current function
            ipq.put(start_ip)
            while not ipq.empty():
                ip = ipq.get()
                if ip < 0 or ip > self.prog.last_addr():
                    logging.warning('Trying to read outside memory at %d' % ip)
                    continue
                if ip in func_addr:
                    # This is ok, can be a loop or something
                    continue
                if ip in addr_func:
                    # This is not ok; what was thought to be two functions are intermingled
                    logging.warning('Function %d reached address %d, which is included in function %d' % (start_ip, ip, all_addr[ip]))

                (opcode, params, modes) = self.decode(ip)
                opcode_len = 1 + len(params)

                if opcode not in self.prog.opcodes:
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
                    poss = self.possible_jump_conditions(ip, jump_type)
                    s = 'Possible' if len(poss) == 2 else 'Mandatory'
                    for v in poss:
                        if v:
                            # The jump/call/return may happen
                            if modes[1] == MODE_RELATIVE and params[1] == 0:
                                # Return statement
                                logging.info('%s return at %d' % (s, ip))
                            else:
                                target = self.jump_target(ip, jump_type)
                                logging.info('%s %s to %s from %d' % (s, jump_type, str(target) if target is not None else '?', ip))

                                if target is not None:
                                    if jump_type == 'jump':
                                        ipq.put(target)
                                    else:
                                        func_calls[ip] = (target, ret_addr[ip-4])
                                        funcq.put(target)
                                        ipq.put(ret_addr[ip-4])

                                elif modes[1] == MODE_RELATIVE:
                                    # !?
                                    logging.warning('Target address of %s at %d was relative but not a return statement; more investigation needed' % (jump_type, ip))
                                else:
                                    logging.warning('Target address of %s at %d not known; more investigation needed' % (jump_type, ip))
                                    func_calls[ip] = (None, ret_addr[ip-4])


                        else:
                            # The jump may not happen
                            ipq.put(ip + opcode_len)
                elif opcode != OPCODE_HALT:
                    fv = self.fixed_value(ip)
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
                funcs[start_ip] = Function(self, start_ip, func_len, frame_size, func_calls)
                for addr in func_addr:
                    addr_func[addr] = start_ip

        return funcs

    def jump_target(self, ip, jump_type='jump'):
        '''Determines the jump target address at a given ip. Returns None if not possible to figure out.'''
        (_, params, modes) = self.decode(ip)
        target = None
        if ip in OVERRIDE_TARGET_ADDRESS:
            target = OVERRIDE_TARGET_ADDRESS[ip]
        elif modes[1] == MODE_IMMEDIATE:
            target = params[1]
        return target

    def possible_jump_conditions(self, ip, jump_type='jump'):
        '''Returns an array with bools if the jump can happen or not; true if it can happen,
        false if not. If it can't be determined for sure, returns [False, True].
        This can be overridden by setting OVERRIDE_JUMP_CONDITIONS.
        '''
        opcode = self.prog.read(ip)
        mode = (opcode // 100) % 10  # mode of the variable being checked
        opcode %= 100
        assert opcode in [OPCODE_JUMP_FALSE, OPCODE_JUMP_TRUE]
        if ip in OVERRIDE_JUMP_CONDITIONS:
            logging.info('%s at %d is overridden to %s' % (jump_type.capitalize(), ip, str(OVERRIDE_JUMP_CONDITIONS[ip])))
            return OVERRIDE_JUMP_CONDITIONS[ip]
        if mode != MODE_IMMEDIATE:
            logging.info('%s at %d is conditional' % (jump_type.capitalize(), ip))
            return [False, True]  # indirect addressing, we can't know for sure
        v = self.prog.read(ip+1)
        will_jump = (v != 0) == (opcode == OPCODE_JUMP_TRUE)
        logging.info('%s at %d will %s happen' % (jump_type.capitalize(), ip, 'always' if will_jump else 'never'))
        return [will_jump]

    def mem_address(self, addr):
        if addr in LOCAL_VARIABLES:
            return 'v%04d' % addr
        elif addr in GLOBAL_VARIABLES:
            return 'g%04d' % addr
        return 'self.mem[%d]' % addr

    def fixed_value(self, ip):
        '''If the MOV or MUL instruction at ip always writes a fixed integer, return that integer.
        Otherwise return None.'''
        opcode = self.prog.read(ip)
        p1 = self.prog.read(ip+1)
        p2 = self.prog.read(ip+2)
        modes = opcode // 100
        opcode %= 100
        m1 = modes % 10
        m2 = (modes // 10) % 10

        return fixed_value(opcode, [p1, p2], [m1, m2])

    def decode(self, ip):
        '''Returns a tuple (opcode, [p0, p1, ...], [mode0, mode1, ...])'''
        opcode = self.prog.read(ip)
        param_mode = opcode // 100
        opcode %= 100
        params = []
        param_modes = []
        if opcode in self.prog.opcodes:
            opcode_len = self.prog.opcodes[opcode][2]

            for i in range(1, opcode_len):
                x = self.prog.read(ip + i)
                param_modes.append(param_mode % 10)
                params.append(x)
                param_mode //= 10

        return (opcode, params, param_modes)

def fixed_value(opcode, p, m):
    if opcode == OPCODE_MUL:
        if m[0] == MODE_IMMEDIATE and p[0] == 0:
            return 0
        if m[1] == MODE_IMMEDIATE and p[1] == 0:
            return 0
        if m[0] == MODE_IMMEDIATE and m[1] == MODE_IMMEDIATE:
            return p[0] * p[1]
        return None
    elif opcode == OPCODE_ADD:
        if m[0] == MODE_IMMEDIATE and m[1] == MODE_IMMEDIATE:
            return p[0] + p[1]
        return None
    else:
        return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)

    #code = '3,8,1005,8,330,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,102,1,8,29,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,51,1,1103,2,10,1006,0,94,1006,0,11,1,1106,13,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,87,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,109,2,1105,5,10,2,103,16,10,1,1103,12,10,2,105,2,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,146,1006,0,49,2,1,12,10,2,1006,6,10,1,1101,4,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,183,1,6,9,10,1006,0,32,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,213,2,1101,9,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,239,1006,0,47,1006,0,4,2,6,0,10,1006,0,58,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,274,2,1005,14,10,1006,0,17,1,104,20,10,1006,0,28,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1002,8,1,309,101,1,9,9,1007,9,928,10,1005,10,15,99,109,652,104,0,104,1,21101,0,937263411860,1,21102,347,1,0,1105,1,451,21101,932440724376,0,1,21102,1,358,0,1105,1,451,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,0,29015167015,1,21101,0,405,0,1106,0,451,21102,1,3422723163,1,21101,0,416,0,1106,0,451,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,868389376360,1,21101,0,439,0,1105,1,451,21102,825544712960,1,1,21102,1,450,0,1106,0,451,99,109,2,21201,-1,0,1,21101,0,40,2,21102,482,1,3,21102,1,472,0,1106,0,515,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,477,478,493,4,0,1001,477,1,477,108,4,477,10,1006,10,509,1101,0,0,477,109,-2,2106,0,0,0,109,4,2101,0,-1,514,1207,-3,0,10,1006,10,532,21102,1,0,-3,22101,0,-3,1,22102,1,-2,2,21102,1,1,3,21101,551,0,0,1106,0,556,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,579,2207,-4,-2,10,1006,10,579,22102,1,-4,-4,1106,0,647,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21102,1,598,0,1106,0,556,22101,0,1,-4,21101,1,0,-1,2207,-4,-2,10,1006,10,617,21102,0,1,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,639,21201,-1,0,1,21102,639,1,0,105,1,514,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0'
    code = '1,380,379,385,1008,2663,704183,381,1005,381,12,99,109,2664,1102,1,0,383,1102,0,1,382,20102,1,382,1,21001,383,0,2,21102,37,1,0,1105,1,578,4,382,4,383,204,1,1001,382,1,382,1007,382,44,381,1005,381,22,1001,383,1,383,1007,383,23,381,1005,381,18,1006,385,69,99,104,-1,104,0,4,386,3,384,1007,384,0,381,1005,381,94,107,0,384,381,1005,381,108,1105,1,161,107,1,392,381,1006,381,161,1102,-1,1,384,1105,1,119,1007,392,42,381,1006,381,161,1101,0,1,384,20102,1,392,1,21102,21,1,2,21102,1,0,3,21102,138,1,0,1105,1,549,1,392,384,392,20101,0,392,1,21102,21,1,2,21101,3,0,3,21101,0,161,0,1106,0,549,1101,0,0,384,20001,388,390,1,21002,389,1,2,21102,180,1,0,1106,0,578,1206,1,213,1208,1,2,381,1006,381,205,20001,388,390,1,20102,1,389,2,21101,0,205,0,1105,1,393,1002,390,-1,390,1102,1,1,384,21001,388,0,1,20001,389,391,2,21102,1,228,0,1106,0,578,1206,1,261,1208,1,2,381,1006,381,253,20102,1,388,1,20001,389,391,2,21101,253,0,0,1105,1,393,1002,391,-1,391,1101,1,0,384,1005,384,161,20001,388,390,1,20001,389,391,2,21101,0,279,0,1105,1,578,1206,1,316,1208,1,2,381,1006,381,304,20001,388,390,1,20001,389,391,2,21101,0,304,0,1106,0,393,1002,390,-1,390,1002,391,-1,391,1101,0,1,384,1005,384,161,20102,1,388,1,21002,389,1,2,21102,0,1,3,21101,0,338,0,1106,0,549,1,388,390,388,1,389,391,389,21002,388,1,1,21001,389,0,2,21102,1,4,3,21102,365,1,0,1105,1,549,1007,389,22,381,1005,381,75,104,-1,104,0,104,0,99,0,1,0,0,0,0,0,0,414,20,18,1,1,22,109,3,22102,1,-2,1,21202,-1,1,2,21102,1,0,3,21101,0,414,0,1106,0,549,21201,-2,0,1,21202,-1,1,2,21101,429,0,0,1105,1,601,1201,1,0,435,1,386,0,386,104,-1,104,0,4,386,1001,387,-1,387,1005,387,451,99,109,-3,2106,0,0,109,8,22202,-7,-6,-3,22201,-3,-5,-3,21202,-4,64,-2,2207,-3,-2,381,1005,381,492,21202,-2,-1,-1,22201,-3,-1,-3,2207,-3,-2,381,1006,381,481,21202,-4,8,-2,2207,-3,-2,381,1005,381,518,21202,-2,-1,-1,22201,-3,-1,-3,2207,-3,-2,381,1006,381,507,2207,-3,-4,381,1005,381,540,21202,-4,-1,-1,22201,-3,-1,-3,2207,-3,-4,381,1006,381,529,22102,1,-3,-7,109,-8,2106,0,0,109,4,1202,-2,44,566,201,-3,566,566,101,639,566,566,2101,0,-1,0,204,-3,204,-2,204,-1,109,-4,2105,1,0,109,3,1202,-1,44,594,201,-2,594,594,101,639,594,594,20101,0,0,-2,109,-3,2106,0,0,109,3,22102,23,-2,1,22201,1,-1,1,21102,509,1,2,21102,150,1,3,21101,1012,0,4,21102,630,1,0,1106,0,456,21201,1,1651,-2,109,-3,2105,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,2,2,0,2,0,2,2,2,2,2,0,2,2,2,2,2,2,0,2,0,2,2,2,0,2,0,0,2,2,2,0,2,2,2,2,0,2,0,0,2,0,1,1,0,2,0,2,0,2,2,2,2,0,0,2,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,2,2,0,0,2,0,2,2,2,0,2,2,2,2,0,1,1,0,2,2,2,0,0,2,0,0,2,0,2,0,2,0,0,0,0,2,2,2,2,2,2,0,2,0,0,0,0,0,2,0,2,2,2,2,2,2,2,0,0,1,1,0,2,2,2,2,2,2,0,0,0,2,2,2,0,2,2,0,2,2,2,0,0,2,2,0,2,0,2,2,2,0,2,2,0,2,2,2,2,2,2,2,0,1,1,0,2,0,2,2,0,2,2,0,2,0,2,2,0,0,2,2,2,2,2,2,2,0,0,0,0,2,2,0,2,2,0,0,2,2,0,0,2,2,2,2,0,1,1,0,2,2,2,2,2,2,2,0,0,2,0,2,0,2,2,2,2,2,0,0,2,0,2,2,2,2,2,2,2,0,0,0,0,2,2,2,2,0,2,0,0,1,1,0,2,0,0,2,0,2,0,2,2,2,2,2,0,2,2,0,2,0,2,0,2,2,0,0,2,2,2,2,2,0,2,2,0,2,0,0,2,2,2,0,0,1,1,0,0,2,2,2,2,0,0,0,2,2,0,2,2,2,0,2,2,2,2,2,0,2,2,2,2,2,2,2,0,0,0,0,2,2,0,2,2,2,2,2,0,1,1,0,2,0,2,2,2,2,2,2,0,2,2,2,0,2,0,2,2,0,2,2,2,0,2,2,2,2,2,2,2,2,2,2,2,0,0,0,2,2,2,0,0,1,1,0,2,0,2,2,2,0,2,0,2,0,2,2,2,0,0,0,2,2,2,2,0,0,2,2,2,2,2,2,2,2,2,2,2,0,0,2,2,0,0,0,0,1,1,0,2,0,2,0,0,2,2,2,2,2,2,2,2,0,0,0,2,2,0,2,2,2,2,2,2,2,2,2,2,2,0,0,0,2,0,0,2,2,0,2,0,1,1,0,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,2,0,2,2,0,0,2,2,2,0,0,2,2,2,0,2,2,2,2,0,2,0,2,2,2,0,1,1,0,2,2,2,2,2,2,0,2,2,2,2,2,2,2,0,2,2,2,2,2,0,2,0,2,2,2,2,2,0,2,2,2,2,0,0,2,2,2,2,2,0,1,1,0,2,2,0,2,2,0,2,0,2,2,0,0,2,2,2,2,2,0,2,2,0,2,2,0,2,2,2,2,0,2,2,0,2,0,2,2,2,2,0,0,0,1,1,0,2,0,2,2,2,0,2,2,2,2,2,2,0,2,0,2,2,2,0,0,2,2,2,2,2,0,2,0,2,0,2,0,2,0,2,2,2,0,0,2,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,34,29,24,40,90,52,13,48,86,82,86,77,3,16,27,97,89,38,11,82,76,15,50,46,33,57,17,38,39,91,43,86,43,55,15,24,23,74,5,53,20,10,16,77,73,84,85,36,89,77,79,82,37,7,24,68,14,78,75,7,86,80,18,84,68,62,89,7,64,11,9,56,62,3,29,95,41,23,18,90,1,10,4,94,8,69,57,13,72,89,61,72,61,17,54,88,96,53,73,21,92,16,52,18,26,89,32,2,50,8,3,5,36,26,64,75,51,55,49,45,78,49,27,55,2,29,37,77,69,3,21,69,6,18,59,91,57,92,6,26,58,40,26,54,33,40,96,45,89,23,53,94,61,44,32,33,41,12,31,67,17,96,34,72,72,49,90,21,1,40,75,97,56,57,77,20,21,68,14,4,7,9,41,88,32,40,79,77,17,48,70,56,50,67,36,16,98,98,65,98,53,7,36,47,27,15,77,80,83,39,8,22,61,11,9,10,54,16,65,54,82,60,66,21,92,51,70,17,53,22,39,89,92,29,12,60,37,42,75,65,1,61,90,86,46,62,81,2,64,64,21,43,17,46,57,72,25,63,51,30,22,65,81,54,85,45,93,24,23,23,27,37,94,11,15,93,78,75,11,41,56,42,89,20,73,23,27,98,89,29,68,73,89,75,80,31,90,36,62,44,65,18,97,24,22,84,30,56,41,44,67,63,71,85,76,66,64,51,58,98,30,66,4,90,38,8,49,49,62,55,53,5,74,18,93,4,34,48,86,17,37,35,28,45,38,76,95,67,21,67,6,36,38,1,16,5,8,89,9,37,32,78,90,46,92,61,3,96,40,91,31,98,35,90,96,44,43,55,39,51,64,51,39,12,90,58,69,58,39,13,49,60,35,40,56,56,74,47,54,23,8,54,59,97,12,8,62,21,66,59,96,61,54,12,98,28,85,95,2,4,14,89,78,4,16,66,48,37,43,17,59,77,20,63,28,87,10,20,58,46,55,26,94,3,71,5,13,90,67,68,55,93,38,16,28,45,47,41,88,98,90,95,44,33,89,54,24,33,38,94,79,32,15,62,26,52,39,8,22,38,79,3,60,75,55,91,53,36,59,86,1,98,25,87,84,47,83,40,74,22,91,86,73,73,6,15,72,90,43,87,97,63,24,77,20,76,10,96,65,27,69,87,93,17,34,5,52,31,24,46,4,26,3,34,87,96,68,16,82,85,67,65,11,57,71,49,62,77,5,68,20,51,26,40,67,69,32,82,46,57,15,31,81,38,74,98,3,77,78,36,10,55,76,48,90,2,8,21,29,17,66,51,91,59,36,8,2,85,50,53,76,38,91,24,54,6,6,28,20,25,7,56,87,44,54,98,6,10,94,44,93,25,26,65,22,87,52,47,36,1,22,21,32,49,7,72,66,89,92,63,85,90,82,79,33,36,39,69,15,57,80,46,39,28,79,73,43,95,81,21,47,39,68,30,34,79,33,72,14,54,96,52,60,16,9,73,54,78,77,26,89,14,14,28,83,47,81,87,14,86,11,96,29,10,2,84,1,70,59,81,64,29,25,40,53,87,4,42,76,80,48,39,85,60,96,95,78,30,8,83,46,62,68,82,40,15,43,51,81,65,64,3,81,13,48,70,97,95,6,23,91,66,63,22,70,28,10,42,90,91,80,34,29,48,18,96,78,14,17,88,13,96,72,72,86,45,95,59,20,67,65,35,89,46,76,35,7,35,4,64,58,15,98,39,81,2,95,10,75,56,85,22,31,22,14,9,12,48,15,75,91,85,91,26,40,78,23,76,5,45,6,79,58,4,70,7,10,79,56,98,86,34,18,73,57,70,97,72,59,75,36,30,21,41,38,83,93,64,92,89,17,65,19,93,9,83,51,3,20,71,89,37,70,3,90,13,35,95,43,14,78,3,43,15,11,21,36,50,12,27,47,58,18,8,66,23,32,7,88,82,27,21,23,5,80,79,44,87,19,11,47,15,14,18,14,95,54,81,76,93,51,53,63,97,39,11,30,26,89,6,29,15,21,49,57,53,52,93,83,11,95,28,58,79,22,65,58,93,89,60,49,78,55,22,42,25,14,61,66,28,84,43,4,68,54,68,17,46,13,88,30,39,40,35,35,14,69,34,55,93,43,7,20,82,83,50,25,50,26,78,17,93,7,10,24,3,27,85,97,88,62,65,11,66,36,38,14,32,31,94,14,3,38,39,96,23,64,89,91,37,9,5,44,4,18,43,64,53,58,96,84,67,96,24,86,49,30,49,24,4,46,57,704183'
    prog = Program(code)
    decompiler = Decompiler(prog)
    #decompiler.decompile(330)  # day 11
    decompiler.decompile(12)  # day 13
    for line in decompiler.generate_code():
        print(line)
