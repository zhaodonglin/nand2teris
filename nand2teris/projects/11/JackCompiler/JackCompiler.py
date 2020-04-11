#!/usr/bin/python
import re
import sys
import os
import JackTokenizer
import CompilationEngine


def read_lines_from_path(path):
    lines = []
    vm_files = []
    file_lines_dict = {}
    if os.path.isfile(path):
        with open(path) as f:
            lines = f.readlines()
            last_word = path.split("/")[-1]
            file_lines_dict[last_word.split(".")[0]] = lines
    elif os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            if os.path.splitext(file)[-1] == ".jack":
                file_name = path + "/" + file
                with open(file_name) as f:
                    lines = f.readlines()
                    file_lines_dict[file.split(".")[0]] = lines
    return file_lines_dict


def parse_lines(lines):
    tokens = []
    for line in lines:
        print line
        tokens = tokens + JackTokenizer.jack_tokenizer(line)
    return tokens


def generate_token_file_name(path, file_name):
    if os.path.isfile(path):
        parent_dir = os.path.abspath(path + "/../")
    else:
        parent_dir = path
    token_file_name = parent_dir + "/" + file_name + "_Mine" + ".xml"
    return token_file_name


if __name__ == "__main__":
    path = sys.argv[1]
    tokens = []
    file_lines_dict = read_lines_from_path(path)
    print file_lines_dict
    for file_name, lines in file_lines_dict.items():
        tokens = parse_lines(lines)
        print 'tokens', tokens
        vm_codes = CompilationEngine.compile_engine(file_name, tokens)
        vm_file = path + "/" + file_name + ".vm"
        f = open(vm_file, "w")
        for code in vm_codes:
            f.write(code + "\n")
        f.close()
