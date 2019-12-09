from lib.intcode import *
import logging

logging.disable(logging.CRITICAL)

def test_negative():
    # day 5, part 1, sample
    code = "1101,100,-1,4,0"
    prog = Program(code)
    prog.run()
    assert prog.read(4) == 99

def test_simple_input_output():
    # day 2, part 1
    code = "3,225,1,225,6,6,1100,1,238,225,104,0,1101,32,43,225,101,68,192,224,1001,224,-160,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1001,118,77,224,1001,224,-87,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,1102,5,19,225,1102,74,50,224,101,-3700,224,224,4,224,1002,223,8,223,1001,224,1,224,1,223,224,223,1102,89,18,225,1002,14,72,224,1001,224,-3096,224,4,224,102,8,223,223,101,5,224,224,1,223,224,223,1101,34,53,225,1102,54,10,225,1,113,61,224,101,-39,224,224,4,224,102,8,223,223,101,2,224,224,1,223,224,223,1101,31,61,224,101,-92,224,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,1102,75,18,225,102,48,87,224,101,-4272,224,224,4,224,102,8,223,223,1001,224,7,224,1,224,223,223,1101,23,92,225,2,165,218,224,101,-3675,224,224,4,224,1002,223,8,223,101,1,224,224,1,223,224,223,1102,8,49,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1107,226,226,224,1002,223,2,223,1005,224,329,1001,223,1,223,1007,677,226,224,1002,223,2,223,1006,224,344,1001,223,1,223,108,677,226,224,102,2,223,223,1006,224,359,1001,223,1,223,7,226,226,224,1002,223,2,223,1005,224,374,101,1,223,223,107,677,677,224,1002,223,2,223,1006,224,389,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,404,1001,223,1,223,1107,677,226,224,1002,223,2,223,1005,224,419,1001,223,1,223,108,226,226,224,102,2,223,223,1006,224,434,1001,223,1,223,1108,226,677,224,1002,223,2,223,1006,224,449,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,464,1001,223,1,223,107,226,226,224,102,2,223,223,1006,224,479,1001,223,1,223,1008,226,226,224,102,2,223,223,1005,224,494,101,1,223,223,7,677,226,224,1002,223,2,223,1005,224,509,101,1,223,223,8,226,677,224,1002,223,2,223,1006,224,524,1001,223,1,223,1007,226,226,224,1002,223,2,223,1006,224,539,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,554,101,1,223,223,1108,677,677,224,102,2,223,223,1006,224,569,101,1,223,223,1107,226,677,224,102,2,223,223,1005,224,584,1001,223,1,223,8,677,226,224,1002,223,2,223,1006,224,599,101,1,223,223,1008,677,226,224,102,2,223,223,1006,224,614,1001,223,1,223,7,226,677,224,1002,223,2,223,1005,224,629,101,1,223,223,107,226,677,224,102,2,223,223,1005,224,644,101,1,223,223,8,677,677,224,102,2,223,223,1005,224,659,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,674,101,1,223,223,4,223,99,226"
    prog = Program(code)
    output = prog.run(input=[1], output=ReturnSink())
    assert output == [0, 0, 0, 0, 0, 0, 0, 0, 0, 5821753]

def test_position_mode():
    # day 5, part 2, sample
    code = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"
    prog = Program(code)
    output = prog.run(input=[0], output=ReturnSink())
    assert output == [0]

    prog = Program(code)
    output = prog.run(input=[1], output=ReturnSink())
    assert output == [1]

def test_immediate_mode():
    # day 5, part 2, sample
    code = "3,3,1105,-1,9,1101,0,0,12,4,12,99,1"
    prog = Program(code)
    output = prog.run(input=[0], output=ReturnSink())
    assert output == [0]

    prog = Program(code)
    output = prog.run(input=[1], output=ReturnSink())
    assert output == [1]

def test_eight():
    # day 5, part 2, sample
    code = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
    prog = Program(code)
    output = prog.run(input=[7], output=ReturnSink())
    assert output == [999]

    prog = Program(code)
    output = prog.run(input=[8], output=ReturnSink())
    assert output == [1000]

    prog = Program(code)
    output = prog.run(input=[10], output=ReturnSink())
    assert output == [1001]

def test_diagnostics():
    # day 5, part 2
    code = "3,225,1,225,6,6,1100,1,238,225,104,0,1101,32,43,225,101,68,192,224,1001,224,-160,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1001,118,77,224,1001,224,-87,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,1102,5,19,225,1102,74,50,224,101,-3700,224,224,4,224,1002,223,8,223,1001,224,1,224,1,223,224,223,1102,89,18,225,1002,14,72,224,1001,224,-3096,224,4,224,102,8,223,223,101,5,224,224,1,223,224,223,1101,34,53,225,1102,54,10,225,1,113,61,224,101,-39,224,224,4,224,102,8,223,223,101,2,224,224,1,223,224,223,1101,31,61,224,101,-92,224,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,1102,75,18,225,102,48,87,224,101,-4272,224,224,4,224,102,8,223,223,1001,224,7,224,1,224,223,223,1101,23,92,225,2,165,218,224,101,-3675,224,224,4,224,1002,223,8,223,101,1,224,224,1,223,224,223,1102,8,49,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1107,226,226,224,1002,223,2,223,1005,224,329,1001,223,1,223,1007,677,226,224,1002,223,2,223,1006,224,344,1001,223,1,223,108,677,226,224,102,2,223,223,1006,224,359,1001,223,1,223,7,226,226,224,1002,223,2,223,1005,224,374,101,1,223,223,107,677,677,224,1002,223,2,223,1006,224,389,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,404,1001,223,1,223,1107,677,226,224,1002,223,2,223,1005,224,419,1001,223,1,223,108,226,226,224,102,2,223,223,1006,224,434,1001,223,1,223,1108,226,677,224,1002,223,2,223,1006,224,449,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,464,1001,223,1,223,107,226,226,224,102,2,223,223,1006,224,479,1001,223,1,223,1008,226,226,224,102,2,223,223,1005,224,494,101,1,223,223,7,677,226,224,1002,223,2,223,1005,224,509,101,1,223,223,8,226,677,224,1002,223,2,223,1006,224,524,1001,223,1,223,1007,226,226,224,1002,223,2,223,1006,224,539,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,554,101,1,223,223,1108,677,677,224,102,2,223,223,1006,224,569,101,1,223,223,1107,226,677,224,102,2,223,223,1005,224,584,1001,223,1,223,8,677,226,224,1002,223,2,223,1006,224,599,101,1,223,223,1008,677,226,224,102,2,223,223,1006,224,614,1001,223,1,223,7,226,677,224,1002,223,2,223,1005,224,629,101,1,223,223,107,226,677,224,102,2,223,223,1005,224,644,101,1,223,223,8,677,677,224,102,2,223,223,1005,224,659,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,674,101,1,223,223,4,223,99,226"
    prog = Program(code)
    output = prog.run(input=[5], output=ReturnSink())
    assert output == [11956381]

def test_adder():
    adder_code = "3,0,1001,0,1,0,4,0,99"
    prog = Program(adder_code)
    output = prog.run([5], output=ReturnSink())
    assert output == [6]

def test_sequence_pipe():
    adder_code = "3,0,1001,0,1,0,4,0,99"
    prog1 = Program(adder_code, 1)
    prog2 = Program(adder_code, 2)
    prog3 = Program(adder_code, 3)
    all_progs = [prog1, prog2, prog3]
    wire_up_serial(all_progs, [5], ReturnSink())
    result = parallel_executor(all_progs)
    assert result == [None, None, [8]]

def test_sequence_pipe_threaded():
    adder_code = "3,0,1001,0,1,0,4,0,99"
    prog1 = Program(adder_code, 1)
    prog2 = Program(adder_code, 2)
    prog3 = Program(adder_code, 3)
    all_progs = [prog1, prog2, prog3]
    wire_up_serial(all_progs, [5], ReturnSink())
    result = threaded_executor(all_progs)
    assert result == [None, None, [8]]

def test_duplicate_joined_pipe():
    init_code = "3,0,1001,0,1,0,4,0,3,0,1001,0,2,0,4,0,99"  # out = <in>+1, out = <in>+2
    add_code = "3,0,3,1,1,0,1,2,4,2,99"  # out = <in>+<in>
    mul_code = "3,0,3,1,2,0,1,2,4,2,99"  # out = <in>*<in>
    prog1 = Program(init_code, 1)
    prog2 = Program(add_code, 2)
    prog3 = Program(mul_code, 3)
    prog4 = Program(mul_code, 4)
    pipe12 = Queue()
    pipe13 = Queue()
    pipe24 = Queue()
    pipe34 = Queue()

    a = 13
    b = 17

    prog1.init_io([a, b], DuplicateSink([pipe12, pipe13]))
    prog2.init_io(pipe12, pipe24)
    prog3.init_io(pipe13, pipe34)
    prog4.init_io(JoinedSource([pipe24, pipe34]), output=ReturnSink())
    result = parallel_executor([prog1, prog2, prog3, prog4])

    expected = ((a+1)+(b+2)) * ((a+1)*(b+2))
    assert next(r[0] for r in result if r) == expected

def test_long():
    # day 9 sample
    data = '1102,34915192,34915192,7,4,7,99,0'
    prog = Program(data)
    assert prog.run([], output=ReturnSink()) == [1219070632396864]

def test_relbase():
    # day 9 part 1
    data = '1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1102,1,3,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,0,493,1024,1102,1,38,1015,1101,20,0,1011,1101,0,509,1026,1101,0,32,1018,1101,0,333,1022,1102,1,0,1020,1101,326,0,1023,1101,0,33,1010,1101,21,0,1016,1101,25,0,1004,1102,28,1,1008,1102,1,506,1027,1102,488,1,1025,1101,0,27,1013,1101,1,0,1021,1101,0,34,1019,1101,607,0,1028,1102,1,23,1003,1102,26,1,1007,1102,29,1,1009,1101,31,0,1000,1102,37,1,1012,1101,30,0,1005,1101,602,0,1029,1101,36,0,1002,1102,1,22,1001,1102,1,35,1014,1102,24,1,1006,1102,39,1,1017,109,4,21102,40,1,6,1008,1010,40,63,1005,63,203,4,187,1106,0,207,1001,64,1,64,1002,64,2,64,109,13,1206,3,221,4,213,1106,0,225,1001,64,1,64,1002,64,2,64,109,-5,1208,-9,22,63,1005,63,241,1106,0,247,4,231,1001,64,1,64,1002,64,2,64,109,-5,21107,41,40,3,1005,1010,263,1106,0,269,4,253,1001,64,1,64,1002,64,2,64,109,-1,1202,3,1,63,1008,63,29,63,1005,63,295,4,275,1001,64,1,64,1106,0,295,1002,64,2,64,109,16,21108,42,42,-8,1005,1014,313,4,301,1105,1,317,1001,64,1,64,1002,64,2,64,109,-4,2105,1,5,1001,64,1,64,1105,1,335,4,323,1002,64,2,64,109,-5,1207,-4,28,63,1005,63,355,1001,64,1,64,1105,1,357,4,341,1002,64,2,64,109,2,21102,43,1,-1,1008,1014,45,63,1005,63,377,1106,0,383,4,363,1001,64,1,64,1002,64,2,64,109,-10,1208,-3,36,63,1005,63,401,4,389,1106,0,405,1001,64,1,64,1002,64,2,64,109,6,21107,44,45,1,1005,1012,423,4,411,1105,1,427,1001,64,1,64,1002,64,2,64,109,4,21101,45,0,3,1008,1018,45,63,1005,63,453,4,433,1001,64,1,64,1105,1,453,1002,64,2,64,109,-23,2101,0,10,63,1008,63,36,63,1005,63,475,4,459,1106,0,479,1001,64,1,64,1002,64,2,64,109,26,2105,1,6,4,485,1105,1,497,1001,64,1,64,1002,64,2,64,109,4,2106,0,5,1105,1,515,4,503,1001,64,1,64,1002,64,2,64,109,-25,1201,10,0,63,1008,63,26,63,1005,63,537,4,521,1105,1,541,1001,64,1,64,1002,64,2,64,109,18,21101,46,0,-1,1008,1014,43,63,1005,63,565,1001,64,1,64,1106,0,567,4,547,1002,64,2,64,109,-6,1201,-4,0,63,1008,63,33,63,1005,63,587,1105,1,593,4,573,1001,64,1,64,1002,64,2,64,109,22,2106,0,-3,4,599,1105,1,611,1001,64,1,64,1002,64,2,64,109,-28,2102,1,-2,63,1008,63,22,63,1005,63,633,4,617,1105,1,637,1001,64,1,64,1002,64,2,64,109,-1,21108,47,44,9,1005,1011,653,1105,1,659,4,643,1001,64,1,64,1002,64,2,64,109,10,2107,24,-8,63,1005,63,681,4,665,1001,64,1,64,1105,1,681,1002,64,2,64,109,-11,2107,31,4,63,1005,63,697,1106,0,703,4,687,1001,64,1,64,1002,64,2,64,109,8,2101,0,-8,63,1008,63,23,63,1005,63,727,1001,64,1,64,1105,1,729,4,709,1002,64,2,64,109,-16,2108,21,10,63,1005,63,749,1001,64,1,64,1106,0,751,4,735,1002,64,2,64,109,17,2108,36,-8,63,1005,63,769,4,757,1105,1,773,1001,64,1,64,1002,64,2,64,109,-10,1207,1,23,63,1005,63,791,4,779,1105,1,795,1001,64,1,64,1002,64,2,64,109,-3,2102,1,6,63,1008,63,22,63,1005,63,815,1106,0,821,4,801,1001,64,1,64,1002,64,2,64,109,16,1205,7,837,1001,64,1,64,1105,1,839,4,827,1002,64,2,64,109,-5,1202,0,1,63,1008,63,30,63,1005,63,863,1001,64,1,64,1106,0,865,4,845,1002,64,2,64,109,4,1205,9,883,4,871,1001,64,1,64,1106,0,883,1002,64,2,64,109,16,1206,-7,899,1001,64,1,64,1106,0,901,4,889,4,64,99,21102,1,27,1,21101,915,0,0,1105,1,922,21201,1,47633,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21102,942,1,0,1105,1,922,22102,1,1,-1,21201,-2,-3,1,21101,957,0,0,1106,0,922,22201,1,-1,-2,1105,1,968,22101,0,-2,-2,109,-3,2106,0,0'

    prog = Program(data)
    assert prog.run([1], output=ReturnSink()) == [3345854957]

def test_boost():
    # day 9 part 2
    data = '1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1102,1,3,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,0,493,1024,1102,1,38,1015,1101,20,0,1011,1101,0,509,1026,1101,0,32,1018,1101,0,333,1022,1102,1,0,1020,1101,326,0,1023,1101,0,33,1010,1101,21,0,1016,1101,25,0,1004,1102,28,1,1008,1102,1,506,1027,1102,488,1,1025,1101,0,27,1013,1101,1,0,1021,1101,0,34,1019,1101,607,0,1028,1102,1,23,1003,1102,26,1,1007,1102,29,1,1009,1101,31,0,1000,1102,37,1,1012,1101,30,0,1005,1101,602,0,1029,1101,36,0,1002,1102,1,22,1001,1102,1,35,1014,1102,24,1,1006,1102,39,1,1017,109,4,21102,40,1,6,1008,1010,40,63,1005,63,203,4,187,1106,0,207,1001,64,1,64,1002,64,2,64,109,13,1206,3,221,4,213,1106,0,225,1001,64,1,64,1002,64,2,64,109,-5,1208,-9,22,63,1005,63,241,1106,0,247,4,231,1001,64,1,64,1002,64,2,64,109,-5,21107,41,40,3,1005,1010,263,1106,0,269,4,253,1001,64,1,64,1002,64,2,64,109,-1,1202,3,1,63,1008,63,29,63,1005,63,295,4,275,1001,64,1,64,1106,0,295,1002,64,2,64,109,16,21108,42,42,-8,1005,1014,313,4,301,1105,1,317,1001,64,1,64,1002,64,2,64,109,-4,2105,1,5,1001,64,1,64,1105,1,335,4,323,1002,64,2,64,109,-5,1207,-4,28,63,1005,63,355,1001,64,1,64,1105,1,357,4,341,1002,64,2,64,109,2,21102,43,1,-1,1008,1014,45,63,1005,63,377,1106,0,383,4,363,1001,64,1,64,1002,64,2,64,109,-10,1208,-3,36,63,1005,63,401,4,389,1106,0,405,1001,64,1,64,1002,64,2,64,109,6,21107,44,45,1,1005,1012,423,4,411,1105,1,427,1001,64,1,64,1002,64,2,64,109,4,21101,45,0,3,1008,1018,45,63,1005,63,453,4,433,1001,64,1,64,1105,1,453,1002,64,2,64,109,-23,2101,0,10,63,1008,63,36,63,1005,63,475,4,459,1106,0,479,1001,64,1,64,1002,64,2,64,109,26,2105,1,6,4,485,1105,1,497,1001,64,1,64,1002,64,2,64,109,4,2106,0,5,1105,1,515,4,503,1001,64,1,64,1002,64,2,64,109,-25,1201,10,0,63,1008,63,26,63,1005,63,537,4,521,1105,1,541,1001,64,1,64,1002,64,2,64,109,18,21101,46,0,-1,1008,1014,43,63,1005,63,565,1001,64,1,64,1106,0,567,4,547,1002,64,2,64,109,-6,1201,-4,0,63,1008,63,33,63,1005,63,587,1105,1,593,4,573,1001,64,1,64,1002,64,2,64,109,22,2106,0,-3,4,599,1105,1,611,1001,64,1,64,1002,64,2,64,109,-28,2102,1,-2,63,1008,63,22,63,1005,63,633,4,617,1105,1,637,1001,64,1,64,1002,64,2,64,109,-1,21108,47,44,9,1005,1011,653,1105,1,659,4,643,1001,64,1,64,1002,64,2,64,109,10,2107,24,-8,63,1005,63,681,4,665,1001,64,1,64,1105,1,681,1002,64,2,64,109,-11,2107,31,4,63,1005,63,697,1106,0,703,4,687,1001,64,1,64,1002,64,2,64,109,8,2101,0,-8,63,1008,63,23,63,1005,63,727,1001,64,1,64,1105,1,729,4,709,1002,64,2,64,109,-16,2108,21,10,63,1005,63,749,1001,64,1,64,1106,0,751,4,735,1002,64,2,64,109,17,2108,36,-8,63,1005,63,769,4,757,1105,1,773,1001,64,1,64,1002,64,2,64,109,-10,1207,1,23,63,1005,63,791,4,779,1105,1,795,1001,64,1,64,1002,64,2,64,109,-3,2102,1,6,63,1008,63,22,63,1005,63,815,1106,0,821,4,801,1001,64,1,64,1002,64,2,64,109,16,1205,7,837,1001,64,1,64,1105,1,839,4,827,1002,64,2,64,109,-5,1202,0,1,63,1008,63,30,63,1005,63,863,1001,64,1,64,1106,0,865,4,845,1002,64,2,64,109,4,1205,9,883,4,871,1001,64,1,64,1106,0,883,1002,64,2,64,109,16,1206,-7,899,1001,64,1,64,1106,0,901,4,889,4,64,99,21102,1,27,1,21101,915,0,0,1105,1,922,21201,1,47633,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21102,942,1,0,1105,1,922,22102,1,1,-1,21201,-2,-3,1,21101,957,0,0,1106,0,922,22201,1,-1,-2,1105,1,968,22101,0,-2,-2,109,-3,2106,0,0'

    prog = Program(data)
    assert prog.run([2], output=ReturnSink()) == [68938]
