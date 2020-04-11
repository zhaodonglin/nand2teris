keywords = ['class', 'constructor', 'function', 'method' , 'field' , 'static' , 'var' , 'int',
'char' , 'boolean',  'void', 'true' , 'false' ,'null' ,'this' , 'let' , 'do' , 'if' , 'else' , 
'while' , 'return']

symbols = ['{' , '}' , '(' , ')' , '[' , ']' , '.' , ',' , ';' , '+' , '-' ,'*' , 
'/' , '&' , '|' , '<' , '>' , '=' , '~']

#integerConstant: a decimal number in the range 0 ... 32767
#StringConstant: '"' a sequence of Unicode characters,not including double quote or newline '"'
#identifier: a sequence of letters, digits, and underscore ( '_' ) not starting with a digit.
symbol_conversion_table = {
	'<' : '&lt;',
	'>' : '&gt;',
	'"' : '&quot;',
	'&' : '&amp;'
}

def compose_symbol(words, i, tokens):
	converted_word = symbol_conversion_table.get(words[i]) 
	if converted_word:
		tokens.append('<symbol> ' + converted_word + ' </symbol>')
	else:
		tokens.append('<symbol> ' + words[i] + ' </symbol>')
	return i + 1

def compose_digit(words, i, length, tokens):
	token_chars = []
	j = i
	while j < length and words[j].isdigit():
		token_chars.append(words[j])
		j = j + 1
	token = "".join(token_chars)
	token_str = '<integerConstant> ' + token + ' </integerConstant>'
	tokens.append(token_str)
	return j

def compose_identifier_or_keyword(words, i, length, tokens):
	token_chars = []
	j = i
	while j < length and words[j].isalpha() or words[j].isdigit() or words[j] == '_':
		token_chars.append(words[j])
		j = j + 1

	token = "".join(token_chars)
	if token in keywords:
		token_str = '<keyword> ' + token + ' </keyword>'
	else:
		token_str = '<identifier> ' + token + ' </identifier>'
	tokens.append(token_str)
	return j

def compose_string_constant(words, i, length, tokens):
	token_chars = []
	j = i + 1
	while j < length and words[j] != '"':
		token_chars.append(words[j])
		j = j + 1

	token = "".join(token_chars)
	token_str = '<stringConstant> ' + token + ' </stringConstant>'
	tokens.append(token_str)
	return j + 1

def skip_comment(words, i, length):
	global match_begin
	j = i
	while j < length:
		if words[j] == '*' and j+1 < length and words[j+1] == '/':
			match_begin = False
			break
		else:
			j = j + 1
	return j + 2

match_begin = False

def jack_tokenizer(line):
	global match_begin

	words = list(line)
	length = len(words)
	i = 0
	tokens = []
	print 'cur', line, length
	while i < length:
		if words[i] == ' ' or words[i] == '\r' or words[i] == '\n' or words[i] == '\t':
			i = i + 1
		elif words[i] == '/':
			if i + 1 < length:
				if words[i+1] == '/':
					return tokens
				elif words[i+1] == '*':
					match_begin = True
					i = skip_comment(words, i+2, length)
				else:
					i = compose_symbol(words, i, tokens)
		elif words[i] == '*':
			if match_begin:
				i = skip_comment(words, i+1, length)
			else:
				i = compose_symbol(words, i, tokens)
		elif words[i] in symbols:
			i = compose_symbol(words, i, tokens)
		elif words[i].isdigit():
			i = compose_digit(words, i, length, tokens)
		elif words[i].isalpha():
			i = compose_identifier_or_keyword(words, i, length, tokens)
		elif words[i] == '"':
			i = compose_string_constant(words, i, length, tokens)
	return tokens

print jack_tokenizer('/** Computes the average of a sequence of integers. */')

