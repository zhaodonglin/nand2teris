#!/usr/bin/python
import re
import sys
import os
import JackTokenizer 
import CompilationEngine

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
        tokens = parse_lines(lines)
        # print tokens
        xml_str = CompilationEngine.compile_engine(tokens)
        xml_file = path + '/'+ file_name + '_Compile'+ '.xml'
        print xml_file
        f = open(xml_file, "w")
        tab_num = 0
        prefix_tabs = []
        for xml in xml_str:
            print 'prefix', prefix_tabs
            # f.write(''.join(prefix_tabs) + xml + "\n")
            matched = re.match(r"(\<.*\>).*(\</.*\>)", xml)
            if not matched:
                need_remove = re.match(r"(\</.*\>)", xml)
                if need_remove:
                    prefix_tabs.remove('  ')
                    f.write(''.join(prefix_tabs) + xml + "\n")
                else:
                    f.write(''.join(prefix_tabs) + xml + "\n")
                    prefix_tabs.append('  ')
            else:
                f.write(''.join(prefix_tabs) + xml + "\n")
        f.close()



