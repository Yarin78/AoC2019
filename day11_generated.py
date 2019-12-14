from goto import with_goto
from lib.intcode import *

class DecompiledProgram(Program):

    @with_goto
    def func330(self):
        #  330: ADD_BP #652
        #  332: OUT #0
        self.output(0)
        #  334: OUT #1
        self.output(1)
        #  336: ADD #0, #937263411860, (BP+1)
        q0 = 937263411860
        #  340: MUL #347, #1, (BP+0)
        #  344: JMPT #1, #451
        (q0) = self.func451(q0)
        #  347: ADD #932440724376, #0, (BP+1)
        q0 = 932440724376
        #  351: MUL #1, #358, (BP+0)
        #  355: JMPT #1, #451
        (q0) = self.func451(q0)
        #  358: IN (10)
        self.mem[10] = self.input()
        #  360: OUT #0
        self.output(0)
        #  362: OUT #1
        self.output(1)
        #  364: IN (10)
        self.mem[10] = self.input()
        #  366: OUT #0
        self.output(0)
        #  368: OUT #0
        self.output(0)
        #  370: IN (10)
        self.mem[10] = self.input()
        #  372: OUT #0
        self.output(0)
        #  374: OUT #1
        self.output(1)
        #  376: IN (10)
        self.mem[10] = self.input()
        #  378: OUT #0
        self.output(0)
        #  380: OUT #1
        self.output(1)
        #  382: IN (10)
        self.mem[10] = self.input()
        #  384: OUT #0
        self.output(0)
        #  386: OUT #0
        self.output(0)
        #  388: IN (10)
        self.mem[10] = self.input()
        #  390: OUT #0
        self.output(0)
        #  392: OUT #1
        self.output(1)
        #  394: ADD #0, #29015167015, (BP+1)
        q0 = 29015167015
        #  398: ADD #0, #405, (BP+0)
        #  402: JMPF #0, #451
        (q0) = self.func451(q0)
        #  405: MUL #1, #3422723163, (BP+1)
        q0 = 3422723163
        #  409: ADD #0, #416, (BP+0)
        #  413: JMPF #0, #451
        (q0) = self.func451(q0)
        #  416: IN (10)
        self.mem[10] = self.input()
        #  418: OUT #0
        self.output(0)
        #  420: OUT #0
        self.output(0)
        #  422: IN (10)
        self.mem[10] = self.input()
        #  424: OUT #0
        self.output(0)
        #  426: OUT #0
        self.output(0)
        #  428: ADD #0, #868389376360, (BP+1)
        q0 = 868389376360
        #  432: ADD #0, #439, (BP+0)
        #  436: JMPT #1, #451
        (q0) = self.func451(q0)
        #  439: MUL #825544712960, #1, (BP+1)
        q0 = 825544712960
        #  443: MUL #1, #450, (BP+0)
        #  447: JMPF #0, #451
        (q0) = self.func451(q0)
        #  450: HALT
        self.halted = True
        return

    @with_goto
    def func451(self, p0=0):
        #  451: ADD_BP #2
        #  453: ADD (BP+-1), #0, (BP+1)
        q0 = p0
        #  457: ADD #0, #40, (BP+2)
        q1 = 40
        #  461: MUL #482, #1, (BP+3)
        q2 = 482
        #  465: MUL #1, #472, (BP+0)
        #  469: JMPF #0, #515
        (q0, q1, q2) = self.func515(q0, q1, q2)
        #  472: ADD_BP #-2
        #  474: JMPF #0, (BP+0)
        return (p0)

    @with_goto
    def func515(self, p0=0, p1=0, p2=0):
        #  515: ADD_BP #4
        #  517: ADD #0, (BP+-1), (514)
        self.mem[514] = p2
        #  521: LT (BP+-3), #0, (10)
        self.mem[10] = 1 if p0 < 0 else 0
        #  525: JMPF (10), #532
        if not self.mem[10]:
            goto .lbl_532
        #  528: MUL #1, #0, (BP+-3)
        p0 = 0
        #  532: ADD #0, (BP+-3), (BP+1)
        label .lbl_532
        q0 = p0
        #  536: MUL #1, (BP+-2), (BP+2)
        q1 = p1
        #  540: MUL #1, #1, (BP+3)
        q2 = 1
        #  544: ADD #551, #0, (BP+0)
        #  548: JMPF #0, #556
        (q0, q1, q2, q3) = self.func556(q0, q1, q2)
        #  551: ADD_BP #-4
        #  553: JMPT #1, (BP+0)
        return (p0, p1, p2)

    @with_goto
    def func556(self, p0=0, p1=0, p2=0, p3=0):
        #  556: ADD_BP #5
        #  558: LT (BP+-3), #1, (10)
        self.mem[10] = 1 if p1 < 1 else 0
        #  562: JMPF (10), #579
        if not self.mem[10]:
            goto .lbl_579
        #  565: LT (BP+-4), (BP+-2), (10)
        self.mem[10] = 1 if p0 < p2 else 0
        #  569: JMPF (10), #579
        if not self.mem[10]:
            goto .lbl_579
        #  572: MUL #1, (BP+-4), (BP+-4)
        #  576: JMPF #0, #647
        goto .lbl_647
        #  579: ADD (BP+-4), #0, (BP+1)
        label .lbl_579
        q0 = p0
        #  583: ADD (BP+-3), #-1, (BP+2)
        q1 = p1 - 1
        #  587: MUL (BP+-2), #2, (BP+3)
        q2 = p2 * 2
        #  591: MUL #1, #598, (BP+0)
        #  595: JMPF #0, #556
        (q0, q1, q2, q3) = self.func556(q0, q1, q2)
        #  598: ADD #0, (BP+1), (BP+-4)
        p0 = q0
        #  602: ADD #1, #0, (BP+-1)
        p3 = 1
        #  606: LT (BP+-4), (BP+-2), (10)
        self.mem[10] = 1 if p0 < p2 else 0
        #  610: JMPF (10), #617
        if not self.mem[10]:
            goto .lbl_617
        #  613: MUL #0, #1, (BP+-1)
        p3 = 0
        #  617: MUL (BP+-2), (BP+-1), (BP+-2)
        label .lbl_617
        p2 *= p3
        #  621: LT #0, (BP+-3), (10)
        self.mem[10] = 1 if 0 < p1 else 0
        #  625: JMPF (10), #639
        if not self.mem[10]:
            goto .lbl_639
        #  628: ADD (BP+-1), #0, (BP+1)
        q0 = p3
        #  632: MUL #639, #1, (BP+0)
        #  636: JMPT #1, (514)
        (q0) = self.func482(q0)
        #  639: MUL (BP+-2), #-1, (BP+-2)
        label .lbl_639
        p2 = -p2
        #  643: ADD (BP+-4), (BP+-2), (BP+-4)
        p0 += p2
        #  647: ADD_BP #-5
        label .lbl_647
        #  649: JMPT #1, (BP+0)
        return (p0, p1, p2, p3)

    @with_goto
    def func482(self, p0=0):
        #  482: ADD_BP #2
        #  484: IN (10)
        self.mem[10] = self.input()
        #  486: OUT (BP+-1)
        self.output(p0)
        #  488: ADD (477), #478, (493)
        self.mem[493] = self.mem[477] + 478
        #  492: OUT (0)
        #self.output(self.mem[0])
        self.output(self.mem[self.mem[493]])
        #  494: ADD (477), #1, (477)
        self.mem[477] += 1
        #  498: EQ #4, (477), (10)
        self.mem[10] = 1 if 4 == self.mem[477] else 0
        #  502: JMPF (10), #509
        if not self.mem[10]:
            goto .lbl_509
        #  505: ADD #0, #0, (477)
        self.mem[477] = 0
        #  509: ADD_BP #-2
        label .lbl_509
        #  511: JMPF #0, (BP+0)
        return (p0)
