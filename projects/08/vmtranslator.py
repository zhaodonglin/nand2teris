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

def generate_pop_for_static(val):
    global cur_file_name
    print 'current file name', cur_file_name
    codes = ['@' + cur_file_name +'.'+ val,
            'D=A',
            '@SP',
            'M=M-1',
            'A=M',
            'D=D+M',
            'A=D-M',
            'M=D-A'
            ]
    return codes

def POP(words):
    print 'pop',words
    segment = words[0]
    val = words[1]
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
        codes = generate_pop_for_static(val)
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

def generate_push_for_static(val):
    global cur_file_name
    print 'current file name', cur_file_name
    codes = ['@' + cur_file_name +'.'+ val,
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1'
            ]
    return codes

def PUSH(words):
    print words
    segment = words[0]
    val = words[1]
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
        codes = generate_push_for_static(val)

    print codes
    return codes

def LABEL(words):
    print words
    label= FUNCTION.current_function + '$' + words[0]
    codes = ['('+ label +')']
    return codes

def IF_GOTO(words):
    label = FUNCTION.current_function + '$' + words[0]
    codes = ['@SP','M=M-1','A=M','D=M', '@'+label, 'D;JNE']
    return codes

def GOTO(words):
    label = FUNCTION.current_function + '$' + words[0]
    codes = ['@'+label, '0;JMP']
    return codes

def FUNCTION(words):
    FUNCTION.current_function = words[0]
    local_variable_number = int(words[1])
    codes = ['(' + FUNCTION.current_function + ')']
    for i in range(local_variable_number):
        codes = codes + ['@'+str(i), 'D=A', '@LCL', 'A=M+D', 'M=0', '@SP','A=M', 'M=0', '@SP', 'M=M+1']
    return codes

def RETURN(words):
    codes =[]
    codes = codes + [ '@LCL', 'D=M', '@R13', 'M=D']# endframe = LCL
    codes = codes + [ '@5', 'D=A', '@R13', 'A=M-D', 'D=M', '@R14', 'M=D'] # retAddr = *(endframe - 5)
    codes = codes + POP(['argument', '0'])  # *ARG=POP()
    codes = codes + ['@ARG', 'D=M+1', '@SP', 'M=D'] # SP=ARG + 1
    codes = codes + ['@1', 'D=A', '@R13', 'A=M-D', 'D=M', '@THAT', 'M=D'] #THAT = *(endframe - 1)
    codes = codes + ['@2', 'D=A', '@R13', 'A=M-D', 'D=M', '@THIS', 'M=D'] #THIS = *(endframe - 2)
    codes = codes + ['@3', 'D=A', '@R13', 'A=M-D', 'D=M', '@ARG', 'M=D'] #ARG = *(endframe - 3)
    codes = codes + ['@4', 'D=A', '@R13', 'A=M-D', 'D=M', '@LCL', 'M=D'] #LCL = *(endframe - 4)
    codes = codes + ['@R14', 'A=M', '0;JMP']# goto RET
    return codes

def CALL(words):
    CALL.current_call = CALL.current_call + 1
    function_name = words[0]
    argument_number = int(words[1])
    return_label='ret-address' + str(CALL.current_call)
    codes = []
    codes = codes + ['@'+return_label, 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'] # push return-address
    codes = codes + ['@LCL', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'] #push LCL
    codes = codes + ['@ARG', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'] #push ARG
    codes = codes + ['@THIS', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'] #push THIS
    codes = codes + ['@THAT', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'] #push THAT
    offset = argument_number + 5
    codes = codes + ['@SP', 'D=M', '@'+str(offset), 'D=D-A', '@ARG', 'M=D']#ARG=sp-n-5
    codes = codes + ['@SP', 'D=M', '@LCL', 'M=D'] # LCL = SP
    codes = codes + ['@'+function_name, '0;JMP'] # goto f
    codes = codes + ['('+ return_label +')'] # return-address
    return codes

def parse(line):
    words = line.split()
    print 'parse', words
    command_type = words[0]
    codes = []
    print command_type, command_type.upper()

    codes = codes + eval(command_type.upper().replace('-', '_'))(words[1:])
    print codes
    return codes

EQ.label_count = 0
LT.label_count = 0
GT.label_count = 0
FUNCTION.current_function = 'null'
CALL.current_call = 0

def read_lines_from_path(path):
    lines = []
    vm_files = []
    file_lines_dict={}
    if os.path.isfile(path):
        with open(path) as f:
            lines = f.readlines()
            last_word = path.split('/')[-1]
            file_lines_dict[last_word.split('.')[0]] = lines
    elif os.path.isdir(path):
        print path
        files = os.listdir(path)
        for file in files:
            if file.split("/")[-1] == 'Sys.vm':
                with open(path + '/' + file) as f:
                    lines = f.readlines()
                    file_name = path + '/' + file
                    file_lines_dict[file.split('.')[0]] = lines
        for file in files:
            print file, os.path.splitext(file)[-1], file.split("/")[-1]
            if (os.path.splitext(file)[-1] == '.vm') and (not (file.split("/")[-1] == 'Sys.vm')):
                file_name = path + '/' + file
                with open(file_name) as f:
                    lines = f.readlines()
                    file_lines_dict[file.split('.')[0]] = lines
    return file_lines_dict

cur_file_name = ''

def parse_lines(file_name, lines):
    global cur_file_name
    codes=[]
    cur_file_name = file_name
    print 'parse_lines', cur_file_name
    for line in lines:
        sub_strs = line.split("//")
        words = list(sub_strs[0].strip())
        if len(words) == 0:
            continue
        print 'words', words
        codes = codes + (parse("".join(words)))
    return codes

def generate_asm_file_name(path):
    asm_file_prefix = path.split("/")[-1].split(".")[0]
    if os.path.isfile(path):
        parent_dir = os.path.abspath(path + "/../")
    else:
        parent_dir = path
    asm_file_name = parent_dir + "/" + asm_file_prefix + ".asm"
    return asm_file_name

if __name__ == "__main__":
    path = sys.argv[1]
    codes = []
    codes = ['@256', 'D=A', '@SP', 'M=D']   # need to comment out for prevoius two testcase
    codes = codes + CALL(['Sys.init', '0']) # need to comment out for prevoius two testcase

    file_lines_dict = read_lines_from_path(path)
    for file_name, lines in file_lines_dict.items():
        print 'main', file_name, lines
        codes = codes + parse_lines(file_name, lines)

    asm_file = generate_asm_file_name(path)
    print codes
    print asm_file
    f = open(asm_file, "w")
    for code in codes:
        f.write(code + "\n")
    f.close()
