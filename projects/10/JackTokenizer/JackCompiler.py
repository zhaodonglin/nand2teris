#!/usr/bin/python
import sys
import os
import JackTokenizer 

def read_lines_from_path(path):
    lines = []
    vm_files = []
    file_lines_dict={}
    # abs_path = os.path.abspath(path)
    # print path, os.path.isfile(path), os.path.isdir(path), os.path.isfile(abs_path)
    if os.path.isfile(path):
        # print path
        with open(path) as f:
            lines = f.readlines()
            last_word = path.split('/')[-1]
            # print last_word
            file_lines_dict[last_word.split('.')[0]] = lines
    elif os.path.isdir(path):
        print path
        files = os.listdir(path)
        for file in files:
            print file, os.path.splitext(file)[-1], file.split("/")[-1]
            if os.path.splitext(file)[-1] == '.jack':
                file_name = path + '/' + file
                with open(file_name) as f:
                    lines = f.readlines()
                    file_lines_dict[file.split('.')[0]] = lines
    return file_lines_dict


def parse_lines(lines):
    tokens=[]
    for line in lines:
        print line
        tokens = tokens + JackTokenizer.jack_tokenizer(line)
    return tokens

def generate_token_file_name(path, file_name):
    if os.path.isfile(path):
        parent_dir = os.path.abspath(path + "/../")
    else:
        parent_dir = path
    token_file_name = parent_dir + "/" + file_name + '_Mine'+".xml"
    return token_file_name


if __name__ == "__main__":
    path = sys.argv[1]
    tokens = []
    print path
    file_lines_dict = read_lines_from_path(path)
    for file_name, lines in file_lines_dict.items():
        # print 'main', file_name, lines
        tokens = parse_lines(lines)
        token_file = generate_token_file_name(path, file_name)
        print token_file
        f = open(token_file, "w")
        f.write('<tokens>' + '\n')
        for token in tokens:
            f.write(token + "\n")
        f.write('</tokens>' + '\n')
        f.close()
