#!/usr/bin/env python
import sys
import os

def ADD(_):
    return [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M+D",
        "M=D",
        "@SP",
        "M=M+1",
    ]

def SUB(_):
    return [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M-D",
        "M=D",
        "@SP",
        "M=M+1",
    ]

def NEG(_):
    return [
        "@SP",
        "M=M-1",
        "A=M",
        "D=-M",
        "M=D",
        "@SP",
        "M=M+1",
    ]

def NOT(_):
    return [
        "@SP",
        "M=M-1",
        "A=M",
        "D=!M",
        "M=D",
        "@SP",
        "M=M+1",
    ]

def AND(_):
    return [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M&D",
        "M=D",
        "@SP",
        "M=M+1",
    ]


def OR(_):
    return [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M|D",
        "M=D",
        "@SP",
        "M=M+1",
    ]

def EQ(_):
    EQ.label_count = EQ.label_count + 1
    codes = [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M-D",
        "@SP",
        "A=M",
        "M=0",
        "@EQ1",
        "D;JEQ",
        "@SP",
        "A=M",
        "M=1",
        "(EQ1)",
        "@SP",
        "A=M",
        "M=M-1",
        "@SP",
        "M=M+1",
    ]
    codes[11] = "@EQ" + str(EQ.label_count)
    codes[16] = "(EQ" + str(EQ.label_count) + ")"
    return codes


def LT(_):
    LT.label_count = LT.label_count + 1
    codes = [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M-D",
        "@SP",
        "A=M",
        "M=0",
        "@LT1",
        "D;JLT",
        "@SP",
        "A=M",
        "M=1",
        "(LT1)",
        "@SP",
        "A=M",
        "M=M-1",
        "@SP",
        "M=M+1",
    ]
    codes[11]='@LT'+str(LT.label_count)
    codes[16]='(LT'+str(LT.label_count)+')'
    return codes

def GT(_):
    GT.label_count = GT.label_count + 1
    codes = [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M-D",
        "@SP",
        "A=M",
        "M=0",
        "@GT1",
        "D;JGT",
        "@SP",
        "A=M",
        "M=1",
        "(GT1)",
        "@SP",
        "A=M",
        "M=M-1",
        "@SP",
        "M=M+1",
    ]
    codes[11]='@GT'+str(GT.label_count)
    codes[16]='(GT'+str(GT.label_count)+')'
    return codes


def generate_for_constant(val):
    codes = ["", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
    codes[0] = "@" + val
    return codes


def generate_pop(val, label):
    codes = ['',
            'D=A',
            '@LCL',
            'D=D+M',
            '@SP',
            'M=M-1',
            'A=M',
            'D=D+M',
            'A=D-M',
            'M=D-A'
            ]
    codes[0] = '@'+val
    codes[2] = '@'+label
    return codes

def generate_pop_for_temp(val, label):
    codes = ['',
            'D=A',
            '@LCL',
            'D=D+A',
            '@SP',
            'M=M-1',
            'A=M',
            'D=D+M',
            'A=D-M',
            'M=D-A'
            ]
    codes[0] = '@'+val
    codes[2] = '@'+label
    return codes

def POP(words):
    print 'pop',words
    segment = words[1]
    val = words[2]
    codes = []
    if segment == "local":
        codes = generate_pop(val, 'LCL')
    elif segment == 'argument':
        codes = generate_pop(val, 'ARG')
    elif segment == 'this':
        codes = generate_pop(val, 'THIS')
    elif segment == 'that':
        codes = generate_pop(val, 'THAT')
    elif segment == 'temp':
        codes = generate_pop_for_temp(val, '5')
    elif segment == 'pointer':
        if val == '0':
            codes = generate_pop_for_temp('0', 'THIS')
        else:
            codes = generate_pop_for_temp('0', 'THAT')
    elif segment == 'static':
        codes =generate_pop(val, 'STATIC')
    return codes

def generate_push(val, label):
    codes = ['@2',
            'D=A',
            '@LCL',
            'D=D+M',
            'A=D',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1'
            ]
    codes[0] = '@'+val
    codes[2] = '@'+label
    return codes

def generate_push_for_temp(val, label):
    codes = ['@2',
            'D=A',
            '@LCL',
            'D=D+A',
            'A=D',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1'
            ]
    codes[0] = '@'+val
    codes[2] = '@'+label
    return codes    

def PUSH(words):
    print words
    segment = words[1]
    val = words[2]
    codes = []
    if segment == "constant":
        codes = generate_for_constant(val)
    elif segment == "local":
        codes = generate_push(val, 'LCL')
    elif segment == 'that':
        codes = generate_push(val, 'THAT')
    elif segment == 'this':
        codes = generate_push(val, 'THIS')
    elif segment == 'argument':
        codes = generate_push(val, 'ARG')
    elif segment == 'temp':
        codes = generate_push_for_temp(val, '5')
    elif segment == 'pointer':
        if val == '0':
            codes = generate_push_for_temp('0', 'THIS')
        else:
            codes = generate_push_for_temp('0', 'THAT')
    elif segment == 'static':
        codes = generate_push(val, 'STATIC')

    print codes
    return codes

def LABEL(words):
    print words
    label= words[1]
    codes = ['('+ label +')']
    return codes

def IF_GOTO(words):
    label = words[1]
    codes = [ '@SP','D=M', '@'+label, 'D;JGT']
    return codes

def parse(line):
    words = line.split()
    print 'parse', words
    command_type = words[0]
    codes = []
    codes = codes + eval(command_type.upper())(words)
    print codes
    return codes

EQ.label_count = 0
LT.label_count = 0
GT.label_count = 0

if __name__ == "__main__":
    file_name = sys.argv[1]
    codes = []
    print file_name
    with open(file_name, "r") as f:
        for line in f.readlines():
            sub_strs = line.split("//")
            words = list(sub_strs[0].strip())
            if len(words) == 0:
                continue
            print words
            codes = codes + (parse("".join(words)))
    names = file_name.split("/")
    file_prefix = names[-1].split(".")
    file_path = os.path.abspath(file_name + "/../")
    print "absolute", file_path
    generated_file = file_path + "/" + file_prefix[0] + ".asm"
    print generated_file
    print codes
    f = open(generated_file, "w")
    for line in codes:
        f.write(line + "\n")
    f.close()
