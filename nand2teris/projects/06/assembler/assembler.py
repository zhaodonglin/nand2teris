#!/usr/bin/env python

import parser
import sys

if __name__ == "__main__":
	file_name = sys.argv[1]    
	parsed_lines = parser.first_pass(file_name)
	print parsed_lines
	compiled_lines=parser.second_pass(parsed_lines)
	names = file_name.split('/')
	file_prefix = names[-1].split('.')
	generated_file = './'+file_prefix[0] + '.hack'
	f = open(generated_file, "w")
	for line in compiled_lines:
		f.write(line+'\n')
	f.close()


