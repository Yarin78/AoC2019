from goto import with_goto
from lib.intcode import *

class DecompiledProgram(Program):

    @with_goto
    def func12(self):
        #   12: ADD_BP #2664
        #   14: MUL #1, #0, (383)
        self.mem[383] = 0
        #   18: MUL #0, #1, (382)
        label .lbl_18
        self.mem[382] = 0
        #   22: MUL #1, (382), (BP+1)
        label .lbl_22
        q0 = self.mem[382]
        #   26: ADD (383), #0, (BP+2)
        q1 = self.mem[383]
        #   30: MUL #37, #1, (BP+0)
        #   34: JMPT #1, #578
        (q0, q1) = self.func578(q0, q1)
        #   37: OUT (382)
        self.output(self.mem[382])
        #   39: OUT (383)
        self.output(self.mem[383])
        #   41: OUT (BP+1)
        self.output(q0)
        #   43: ADD (382), #1, (382)
        self.mem[382] += 1
        #   47: LT (382), #44, (381)
        self.mem[381] = 1 if self.mem[382] < 44 else 0
        #   51: JMPT (381), #22
        if self.mem[381]:
            goto .lbl_22
        #   54: ADD (383), #1, (383)
        self.mem[383] += 1
        #   58: LT (383), #23, (381)
        self.mem[381] = 1 if self.mem[383] < 23 else 0
        #   62: JMPT (381), #18
        if self.mem[381]:
            goto .lbl_18
        #   65: JMPF (385), #69
        if not self.mem[385]:
            goto .lbl_69
        #   68: HALT 
        raise MachineHaltedException()
        #   69: OUT #-1
        label .lbl_69
        self.output(-1)
        #   71: OUT #0
        self.output(0)
        #   73: OUT (386)
        self.output(self.mem[386])
        #   75: IN (384)
        label .lbl_75
        self.mem[384] = self.input()
        #   77: LT (384), #0, (381)
        self.mem[381] = 1 if self.mem[384] < 0 else 0
        #   81: JMPT (381), #94
        if self.mem[381]:
            goto .lbl_94
        #   84: LT #0, (384), (381)
        self.mem[381] = 1 if 0 < self.mem[384] else 0
        #   88: JMPT (381), #108
        if self.mem[381]:
            goto .lbl_108
        #   91: JMPT #1, #161
        goto .lbl_161
        #   94: LT #1, (392), (381)
        label .lbl_94
        self.mem[381] = 1 if 1 < self.mem[392] else 0
        #   98: JMPF (381), #161
        if not self.mem[381]:
            goto .lbl_161
        #  101: MUL #-1, #1, (384)
        self.mem[384] = -1
        #  105: JMPT #1, #119
        goto .lbl_119
        #  108: LT (392), #42, (381)
        label .lbl_108
        self.mem[381] = 1 if self.mem[392] < 42 else 0
        #  112: JMPF (381), #161
        if not self.mem[381]:
            goto .lbl_161
        #  115: ADD #0, #1, (384)
        self.mem[384] = 1
        #  119: MUL #1, (392), (BP+1)
        label .lbl_119
        q0 = self.mem[392]
        #  123: MUL #21, #1, (BP+2)
        q1 = 21
        #  127: MUL #1, #0, (BP+3)
        q2 = 0
        #  131: MUL #138, #1, (BP+0)
        #  135: JMPT #1, #549
        (q0, q1, q2) = self.func549(q0, q1, q2)
        #  138: ADD (392), (384), (392)
        self.mem[392] += self.mem[384]
        #  142: ADD #0, (392), (BP+1)
        q0 = self.mem[392]
        #  146: MUL #21, #1, (BP+2)
        q1 = 21
        #  150: ADD #3, #0, (BP+3)
        q2 = 3
        #  154: ADD #0, #161, (BP+0)
        #  158: JMPF #0, #549
        (q0, q1, q2) = self.func549(q0, q1, q2)
        #  161: ADD #0, #0, (384)
        label .lbl_161
        self.mem[384] = 0
        #  165: ADD (388), (390), (BP+1)
        q0 = self.mem[388] + self.mem[390]
        #  169: MUL (389), #1, (BP+2)
        q1 = self.mem[389]
        #  173: MUL #180, #1, (BP+0)
        #  177: JMPF #0, #578
        (q0, q1) = self.func578(q0, q1)
        #  180: JMPF (BP+1), #213
        if not q0:
            goto .lbl_213
        #  183: EQ (BP+1), #2, (381)
        self.mem[381] = 1 if q0 == 2 else 0
        #  187: JMPF (381), #205
        if not self.mem[381]:
            goto .lbl_205
        #  190: ADD (388), (390), (BP+1)
        q0 = self.mem[388] + self.mem[390]
        #  194: MUL #1, (389), (BP+2)
        q1 = self.mem[389]
        #  198: ADD #0, #205, (BP+0)
        #  202: JMPT #1, #393
        (q0, q1) = self.func393(q0, q1)
        #  205: MUL (390), #-1, (390)
        label .lbl_205
        self.mem[390] = -self.mem[390]
        #  209: MUL #1, #1, (384)
        self.mem[384] = 1
        #  213: ADD (388), #0, (BP+1)
        label .lbl_213
        q0 = self.mem[388]
        #  217: ADD (389), (391), (BP+2)
        q1 = self.mem[389] + self.mem[391]
        #  221: MUL #1, #228, (BP+0)
        #  225: JMPF #0, #578
        (q0, q1) = self.func578(q0, q1)
        #  228: JMPF (BP+1), #261
        if not q0:
            goto .lbl_261
        #  231: EQ (BP+1), #2, (381)
        self.mem[381] = 1 if q0 == 2 else 0
        #  235: JMPF (381), #253
        if not self.mem[381]:
            goto .lbl_253
        #  238: MUL #1, (388), (BP+1)
        q0 = self.mem[388]
        #  242: ADD (389), (391), (BP+2)
        q1 = self.mem[389] + self.mem[391]
        #  246: ADD #253, #0, (BP+0)
        #  250: JMPT #1, #393
        (q0, q1) = self.func393(q0, q1)
        #  253: MUL (391), #-1, (391)
        label .lbl_253
        self.mem[391] = -self.mem[391]
        #  257: ADD #1, #0, (384)
        self.mem[384] = 1
        #  261: JMPT (384), #161
        label .lbl_261
        if self.mem[384]:
            goto .lbl_161
        #  264: ADD (388), (390), (BP+1)
        q0 = self.mem[388] + self.mem[390]
        #  268: ADD (389), (391), (BP+2)
        q1 = self.mem[389] + self.mem[391]
        #  272: ADD #0, #279, (BP+0)
        #  276: JMPT #1, #578
        (q0, q1) = self.func578(q0, q1)
        #  279: JMPF (BP+1), #316
        if not q0:
            goto .lbl_316
        #  282: EQ (BP+1), #2, (381)
        self.mem[381] = 1 if q0 == 2 else 0
        #  286: JMPF (381), #304
        if not self.mem[381]:
            goto .lbl_304
        #  289: ADD (388), (390), (BP+1)
        q0 = self.mem[388] + self.mem[390]
        #  293: ADD (389), (391), (BP+2)
        q1 = self.mem[389] + self.mem[391]
        #  297: ADD #0, #304, (BP+0)
        #  301: JMPF #0, #393
        (q0, q1) = self.func393(q0, q1)
        #  304: MUL (390), #-1, (390)
        label .lbl_304
        self.mem[390] = -self.mem[390]
        #  308: MUL (391), #-1, (391)
        self.mem[391] = -self.mem[391]
        #  312: ADD #0, #1, (384)
        self.mem[384] = 1
        #  316: JMPT (384), #161
        label .lbl_316
        if self.mem[384]:
            goto .lbl_161
        #  319: MUL #1, (388), (BP+1)
        q0 = self.mem[388]
        #  323: MUL (389), #1, (BP+2)
        q1 = self.mem[389]
        #  327: MUL #0, #1, (BP+3)
        q2 = 0
        #  331: ADD #0, #338, (BP+0)
        #  335: JMPF #0, #549
        (q0, q1, q2) = self.func549(q0, q1, q2)
        #  338: ADD (388), (390), (388)
        self.mem[388] += self.mem[390]
        #  342: ADD (389), (391), (389)
        self.mem[389] += self.mem[391]
        #  346: MUL (388), #1, (BP+1)
        q0 = self.mem[388]
        #  350: ADD (389), #0, (BP+2)
        q1 = self.mem[389]
        #  354: MUL #1, #4, (BP+3)
        q2 = 4
        #  358: MUL #365, #1, (BP+0)
        #  362: JMPT #1, #549
        (q0, q1, q2) = self.func549(q0, q1, q2)
        #  365: LT (389), #22, (381)
        self.mem[381] = 1 if self.mem[389] < 22 else 0
        #  369: JMPT (381), #75
        if self.mem[381]:
            goto .lbl_75
        #  372: OUT #-1
        self.output(-1)
        #  374: OUT #0
        self.output(0)
        #  376: OUT #0
        self.output(0)
        #  378: HALT 
        raise MachineHaltedException()

    @with_goto
    def func578(self, p0=0, p1=0):
        #  578: ADD_BP #3
        #  580: MUL (BP+-1), #44, (594)
        self.mem[594] = p1 * 44
        #  584: ADD (BP+-2), (594), (594)
        self.mem[594] += p0
        #  588: ADD #639, (594), (594)
        self.mem[594] += 639
        #  592: ADD #0, (0), (BP+-2)
        p0 = self.mem[self.mem[594]]
        #  596: ADD_BP #-3
        #  598: JMPF #0, (BP+0)
        return (p0, p1)

    @with_goto
    def func549(self, p0=0, p1=0, p2=0):
        #  549: ADD_BP #4
        #  551: MUL (BP+-2), #44, (566)
        self.mem[566] = p1 * 44
        #  555: ADD (BP+-3), (566), (566)
        self.mem[566] += p0
        #  559: ADD #639, (566), (566)
        self.mem[566] += 639
        #  563: ADD #0, (BP+-1), (0)
        self.mem[self.mem[566]] = p2
        #  567: OUT (BP+-3)
        self.output(p0)
        #  569: OUT (BP+-2)
        self.output(p1)
        #  571: OUT (BP+-1)
        self.output(p2)
        #  573: ADD_BP #-4
        #  575: JMPT #1, (BP+0)
        return (p0, p1, p2)

    @with_goto
    def func393(self, p0=0, p1=0):
        #  393: ADD_BP #3
        #  395: MUL #1, (BP+-2), (BP+1)
        q0 = p0
        #  399: MUL (BP+-1), #1, (BP+2)
        q1 = p1
        #  403: MUL #1, #0, (BP+3)
        q2 = 0
        #  407: ADD #0, #414, (BP+0)
        #  411: JMPF #0, #549
        (q0, q1, q2) = self.func549(q0, q1, q2)
        #  414: ADD (BP+-2), #0, (BP+1)
        q0 = p0
        #  418: MUL (BP+-1), #1, (BP+2)
        q1 = p1
        #  422: ADD #429, #0, (BP+0)
        #  426: JMPT #1, #601
        (q0, q1) = self.func601(q0, q1)
        #  429: ADD (BP+1), #0, (435)
        self.mem[435] = q0
        #  433: ADD (386), (0), (386)
        self.mem[386] += self.mem[self.mem[435]]
        #  437: OUT #-1
        self.output(-1)
        #  439: OUT #0
        self.output(0)
        #  441: OUT (386)
        self.output(self.mem[386])
        #  443: ADD (387), #-1, (387)
        self.mem[387] -= 1
        #  447: JMPT (387), #451
        if self.mem[387]:
            goto .lbl_451
        #  450: HALT 
        raise MachineHaltedException()
        #  451: ADD_BP #-3
        label .lbl_451
        #  453: JMPF #0, (BP+0)
        return (p0, p1)

    @with_goto
    def func601(self, p0=0, p1=0):
        #  601: ADD_BP #3
        #  603: MUL #23, (BP+-2), (BP+1)
        q0 = 23 * p0
        #  607: ADD (BP+1), (BP+-1), (BP+1)
        q0 += p1
        #  611: MUL #509, #1, (BP+2)
        q1 = 509
        #  615: MUL #150, #1, (BP+3)
        q2 = 150
        #  619: ADD #1012, #0, (BP+4)
        q3 = 1012
        #  623: MUL #630, #1, (BP+0)
        #  627: JMPF #0, #456
        (q0, q1, q2, q3, q4, q5, q6) = self.func456(q0, q1, q2, q3)
        #  630: ADD (BP+1), #1651, (BP+-2)
        p0 = q0 + 1651
        #  634: ADD_BP #-3
        #  636: JMPT #1, (BP+0)
        return (p0, p1)

    @with_goto
    def func456(self, p0=0, p1=0, p2=0, p3=0, p4=0, p5=0, p6=0):
        #  456: ADD_BP #8
        #  458: MUL (BP+-7), (BP+-6), (BP+-3)
        p4 = p0 * p1
        #  462: ADD (BP+-3), (BP+-5), (BP+-3)
        p4 += p2
        #  466: MUL (BP+-4), #64, (BP+-2)
        p5 = p3 * 64
        #  470: LT (BP+-3), (BP+-2), (381)
        self.mem[381] = 1 if p4 < p5 else 0
        #  474: JMPT (381), #492
        if self.mem[381]:
            goto .lbl_492
        #  477: MUL (BP+-2), #-1, (BP+-1)
        p6 = p5 * -1
        #  481: ADD (BP+-3), (BP+-1), (BP+-3)
        label .lbl_481
        p4 += p6
        #  485: LT (BP+-3), (BP+-2), (381)
        self.mem[381] = 1 if p4 < p5 else 0
        #  489: JMPF (381), #481
        if not self.mem[381]:
            goto .lbl_481
        #  492: MUL (BP+-4), #8, (BP+-2)
        label .lbl_492
        p5 = p3 * 8
        #  496: LT (BP+-3), (BP+-2), (381)
        self.mem[381] = 1 if p4 < p5 else 0
        #  500: JMPT (381), #518
        if self.mem[381]:
            goto .lbl_518
        #  503: MUL (BP+-2), #-1, (BP+-1)
        p6 = p5 * -1
        #  507: ADD (BP+-3), (BP+-1), (BP+-3)
        label .lbl_507
        p4 += p6
        #  511: LT (BP+-3), (BP+-2), (381)
        self.mem[381] = 1 if p4 < p5 else 0
        #  515: JMPF (381), #507
        if not self.mem[381]:
            goto .lbl_507
        #  518: LT (BP+-3), (BP+-4), (381)
        label .lbl_518
        self.mem[381] = 1 if p4 < p3 else 0
        #  522: JMPT (381), #540
        if self.mem[381]:
            goto .lbl_540
        #  525: MUL (BP+-4), #-1, (BP+-1)
        p6 = p3 * -1
        #  529: ADD (BP+-3), (BP+-1), (BP+-3)
        label .lbl_529
        p4 += p6
        #  533: LT (BP+-3), (BP+-4), (381)
        self.mem[381] = 1 if p4 < p3 else 0
        #  537: JMPF (381), #529
        if not self.mem[381]:
            goto .lbl_529
        #  540: MUL #1, (BP+-3), (BP+-7)
        label .lbl_540
        p0 = p4
        #  544: ADD_BP #-8
        #  546: JMPF #0, (BP+0)
        return (p0, p1, p2, p3, p4, p5, p6)
