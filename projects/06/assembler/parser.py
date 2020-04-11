import symbols
import code

def first_pass(filename):
	instruction_number = 0
	parsed_lines=[]
	with open(filename, 'r') as f:
		for line in f.readlines():
			sub_strs=line.split("//")
			words = list(sub_strs[0].strip())
			if len(words)==0:
				continue
			else:
				parsed_lines.append(''.join(words))
				if words[0] == '@':
					instruction_number = instruction_number + 1
				elif words[0] == '(':
					label = ''.join(words[1:-1])
					symbols.addEntry(label, instruction_number)
				else:
					instruction_number = instruction_number + 1
	print symbols.printEntry()
	return parsed_lines


def second_pass(parsed_lines):
	compile_lines = []
	var_mem_pos = 16

	for line in parsed_lines:
		words = list(line.strip())
		if words[0] == '(':
			continue
		# A instruction
		elif words[0] == '@':
			symbol = ''.join(words[1:])
			if symbol.isdigit():
				address = symbol
			elif symbols.contains(symbol):
				address = symbols.GetAddress(symbol)
			else:
				address = var_mem_pos
				symbols.addEntry(symbol, var_mem_pos)
				var_mem_pos = var_mem_pos + 1
			compiled_ins = code.fill(address)
			print symbol, address, compiled_ins
			compile_lines.append(compiled_ins)
		# C Instruction
		else:
			sub_words = line.strip().split(";")
			if len(sub_words) == 1:
				jmp = 'null'
			else:
				jmp = sub_words[1]
			dest_and_cmp = sub_words[0].split('=')
			if len(dest_and_cmp) == 1:
				dest = 'null'
				comp = dest_and_cmp[0]
			else:
				dest = dest_and_cmp[0]
				comp = dest_and_cmp[1]
			print dest, comp, jmp
			compiled_ins = '111' +  code.cmp(comp) + code.dest(dest) + code.jmp(jmp)
			print compiled_ins
			compile_lines.append(compiled_ins)
	return compile_lines







