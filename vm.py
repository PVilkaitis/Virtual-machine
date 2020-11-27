
def main():
    with open("C:/Users/pauli/Desktop/macupikcu/python/virtualMachine/dec.bin", 'rb') as file:
        bytearr = file.read()
    with open("C:/Users/pauli/Desktop/macupikcu/python/virtualMachine/my.txt", 'rb') as file:
        text = file.read()
    output = open("output.txt", "w")
    
    regs = [None] * 16
    memory = [None] * 256
    flag = 0
    fileEnd = False
    textCursor = 0
    binLength = len(bytearr)
    i = 0
    for byte in bytearr:
        memory[i] = str(hex(byte).replace("0x", "")) 
        if len(memory[i]) == 1:
            memory[i] = '0' + memory[i]
        i += 1
    
    i = 0
    while True:
        code = memory[i]
        const = memory[i+1]
        if code == None: break
        
        elif code == '01':
            regs, flag = INC(const, regs, flag)
        elif code == '02':
            regs, flag = DEC(const, regs, flag)
        elif code == '03':
            regs, flag = MOV(const, regs, flag)
        elif code == '04':
            regs = MOVC(const, regs)
        elif code == '05':
            regs, flag = LSL(const, regs, flag)
        elif code == '06':
            regs, flag = LSR(const, regs, flag)
        elif code =='07':
            i = JMP(const, i, binLength)
            continue
        elif code == '08':
            if flag == 1:
                i = JMP(const, i, binLength)
                continue
        elif code == '09':
            if flag == 0:
                i = JMP(const, i, binLength)
                continue
        elif code == '0a' and fileEnd == True:
            i = JMP(const, i, binLength)
            continue
        elif code == '0b':
            break
        elif code == '0c':
            regs, flag = ADD(const, regs, flag)
        elif code == '0d':
            regs, flag = SUB(const, regs, flag)
        elif code == '0e':
            regs, flag = XOR(const, regs, flag)
        elif code == '0f':
            regs, flag = OR(const, regs, flag)
        elif code == '10':
            regs, textCursor, fileEnd = IN(const, regs, textCursor, fileEnd, text)
        elif code == '11':
            OUT(const, regs, output)
        i += 2


def indexHandler(const):
    xreg = int(const, 16) & 15 #0000 1111bin = 15dec
    yreg = int(const, 16) >> 4
    ind = {
        'xreg':xreg,
        'yreg':yreg
    }
    return ind

def INC(const, regs, flag):
    index = indexHandler(const)
    if regs[index['xreg']] is None:
        regs[index['xreg']] = 1
    else:
        regs[index['xreg']] += 1
    if regs[index['xreg']] == 0:
        flag = 1
    else:
        flag = 0
    return regs, flag

def DEC(const, regs, flag):
    index = indexHandler(const)
    if regs[index['xreg']] is None:
        regs[index['xreg']] = -1
    else:
        regs[index['xreg']] -= 1
    if regs[index['xreg']] == 0:
        flag = 1
    else:
        flag = 0
    return regs, flag

def MOV(const, regs, flag):
    index = indexHandler(const)
    if regs[index['yreg']] is not None:
        copy = regs[index['yreg']]
        regs[index['xreg']] = copy
    if regs[index['xreg']] == 0:
        flag = 1
    else:
        flag = 0
    return regs, flag

def MOVC(const, regs):
    copy = int(const, 16)
    regs[0] = copy
    return regs

def LSL(const, regs, flag):
    index = indexHandler(const)
    if regs[index['xreg']] is not None:
        shift = regs[index['xreg']] << 1
        regs[index['xreg']] = shift
    if regs[index['xreg']] == 0:
        flag = 1
    else:
        flag = 0
    return regs, flag

def LSR(const, regs, flag):
    index = indexHandler(const)
    if regs[index['xreg']] is not None:
        shift = regs[index['xreg']] >> 1
        regs[index['xreg']] = shift
    if regs[index['xreg']] == 0:
        flag = 1
    else:
        flag = 0
    return regs, flag

def JMP(const, cursor, length):
    jump = int(const, 16)
    signed = jump if jump < (1 << 7) else jump - (1 << 8)
    if signed < 0:
        cursor += signed
    else:
        x = jump % length
        cursor += x
        if cursor > (length-1):
            cursor -= length
    return cursor

def ADD(const, regs, flag):
    index = indexHandler(const)
    if (regs[index['xreg']] is not None) and (regs[index['yreg']] is not None):
        regs[index['xreg']] += regs[index['yreg']]
    elif regs[index['yreg']] is not None:
        regs[index['xreg']] = regs[index['yreg']]
    if regs[index['xreg']] == 0:
        flag = 1
    else:
        flag = 0
    return regs, flag

def SUB(const, regs, flag):
    index = indexHandler(const)
    if (regs[index['xreg']] is not None) and (regs[index['yreg']] is not None):
        regs[index['xreg']] -= regs[index['yreg']]
    elif regs[index['yreg']] is not None:
        regs[index['xreg']] = 0 - regs[index['yreg']]
    if regs[index['xreg']] == 0:
        flag = 1
    else:
        flag = 0
    return regs, flag

def XOR(const, regs, flag):
    index = indexHandler(const)
    if (regs[index['xreg']] is not None) and (regs[index['yreg']] is not None):
        regs[index['xreg']] = regs[index['xreg']] ^ regs[index['yreg']]
    if regs[index['xreg']] == 0:
        flag = 1
    else:
        flag = 0
    return regs, flag

def OR(const, regs, flag):
    index = indexHandler(const)
    if (regs[index['xreg']] is not None) and (regs[index['yreg']] is not None):
        regs[index['xreg']] = regs[index['xreg']] | regs[index['yreg']] 
    if regs[index['xreg']] == 0:
        flag = 1
    else:
        flag = 0
    return regs, flag

def IN(const, regs, textCursor, fileEnd, text):
    xreg = int(const, 16)
    fileL = len(text)
    if textCursor < fileL:
        regs[xreg] = int(text[textCursor])
        textCursor += 1
        if textCursor == fileL:
            fileEnd = True
    return regs, textCursor, fileEnd

def OUT(const, regs, output):
    xreg = int(const, 16)
    char = chr(regs[xreg])
    output.write(char)
    return

main()