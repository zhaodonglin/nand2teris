xml_str = []
type_table = ['int', 'char', 'boolean', 'Array']
statement_keyword = ['let', 'if', 'else', 'while', 'do', 'return']
operation_table = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
unary_operation = ['-', '~']
keywordConstant = ['true', 'false', 'null', 'this']
subroutine_names = []
var_names = []
class_names = ['Keyboard']

var_scope_table = ['field', 'static']
subroutine_type_table = ['constructor', 'function', 'method']

symbol_conversion_table = {
	'<' : '&lt;',
	'>' : '&gt;',
	'"' : '&quot;',
	'&' : '&amp;'
}

def append_to_xml(token_str, token_type):
	converted = symbol_conversion_table.get(token_str, None)
	if converted is not None:
		token_str = converted
	xml_str.append('<' + token_type +'> ' + token_str + ' <' + '/' + token_type + '>')

def parse_token(tokens, i, expected_token_str=None, expected_token_type=None):
	token_str, token_type = tokens[i]
	if expected_token_str and (token_str != expected_token_str and token_str not in expected_token_str):
		raise Exception("Compile error: expect " + token_str)
	if expected_token_type and (token_type != expected_token_type and token_type not in expected_token_type):
		raise Exception("Compile error: expect " + token_type)
	append_to_xml(token_str, token_type)
	return token_str, token_type, i + 1

def compile_engine(tokens):
	i = 0
	global xml_str
	xml_str=[]
	while i < len(tokens):
		i = compile_class(tokens, i)
	return xml_str

def compile_class(tokens, i):
	xml_str.append('<class>')
	_, _, i = parse_token(tokens, i, expected_token_str='class')
	token_str, _, i = parse_token(tokens, i, expected_token_type='identifier')
	type_table.append(token_str)
	class_names.append(token_str)
	_, _, i = parse_token(tokens, i, expected_token_str='{')
	token_str, token_type = tokens[i]
	if token_str not in var_scope_table and token_str not in subroutine_type_table:
		raise Exception('Compile error: expect var dec or subroutine dec')
	else:
		i = compile_class_var_dec(tokens, i)
		print 'vardec', i, tokens[i]
		i = compile_subroutine_dec(tokens, i)
		print 'subroutine dec', i, tokens[i]
	print i
	_, _, i =parse_token(tokens, i, expected_token_str='}')
	xml_str.append('</class>')
	return i

def compile_class_var_dec(tokens, i):
	token_str, token_type = tokens[i]
	if token_str not in var_scope_table:
		return i
	
	while token_str in var_scope_table:
		xml_str.append('<classVarDec>')
		_, _, i = parse_token(tokens, i)
		_, _, i = parse_token(tokens, i)
		var_name, _, i = parse_token(tokens, i, expected_token_type='identifier')
		var_names.append(var_name)
		token_str, token_type = tokens[i]
		while token_str == ',':
			_,_,i = parse_token(tokens,i)
			var_name, _, i = parse_token(tokens, i, expected_token_type='identifier')
			var_names.append(var_name)
			token_str, token_type = tokens[i]
		_,_,i = parse_token(tokens, i, expected_token_str=';')
		token_str, token_type = tokens[i]
		xml_str.append('</classVarDec>')
	return i

def compile_subroutine_dec(tokens, i):
	token_str, token_type = tokens[i]
	if token_str not in subroutine_type_table:
		return i
	while token_str in subroutine_type_table:
		xml_str.append('<subroutineDec>')
		_, _, i = parse_token(tokens, i)
		expected_type = type_table + ['void']
		print expected_type
		_, _, i = parse_token(tokens, i)
		sub_routine_name, _, i = parse_token(tokens, i, expected_token_type='identifier')
		subroutine_names.append(sub_routine_name)
		_, _, i = parse_token(tokens,i, '(')
		i = compile_parameter_list(tokens, i)
		_, _, i = parse_token(tokens, i, ')')
		i = compile_subroutine_body(tokens, i)
		xml_str.append('</subroutineDec>')
		token_str, token_type = tokens[i]
	return i

# ((type varname)(',' type varnmae)*)?
def compile_parameter_list(tokens, i):
	token_str, token_type = tokens[i]
	xml_str.append('<parameterList>')
	while token_str in type_table:
		_, _, i = parse_token(tokens, i)
		_, _, i = parse_token(tokens, i, expected_token_type='identifier')
		token_str, token_type = tokens[i]
		while token_str == ',':
			_, _, i = parse_token(tokens, i)
			_, _, i = parse_token(tokens, i)
			_, _, i = parse_token(tokens, i, expected_token_type='identifier')
			token_str, token_type = tokens[i]
	xml_str.append('</parameterList>')
	return i

def compile_statements(tokens,i):
	token_str, token_type = tokens[i]
	xml_str.append('<statements>')
	while token_str in statement_keyword:
		if token_str == 'let':
			i = compile_let(tokens, i)
		elif token_str == 'if':
			i = compile_if(tokens, i)
		elif token_str == 'while':
			i = compile_while(tokens, i)
		elif token_str == 'do':
			i = compile_do(tokens, i)
		elif token_str == 'return':
			i = compile_return(tokens, i)
		token_str, token_type = tokens[i]
	xml_str.append('</statements>')
	return i

def compile_var_dec(tokens, i):
	token_str, token_type = tokens[i]
	while token_str == 'var':
		xml_str.append('<varDec>')
		_, _, i = parse_token(tokens, i)
		_, _, i = parse_token(tokens, i)
		var_name, _, i = parse_token(tokens, i, expected_token_type='identifier')
		var_names.append(var_name)
		token_str, token_type = tokens[i]
		while token_str == ',':
			_,_,i = parse_token(tokens,i)
			print tokens[i]
			var_name, _, i = parse_token(tokens, i, expected_token_type='identifier')
			var_names.append(var_name)
			token_str, token_type = tokens[i]
		_,_,i = parse_token(tokens, i, expected_token_str=';')
		token_str, token_type = tokens[i]
		xml_str.append('</varDec>')
	return i

def compile_subroutine_body(tokens, i):
	xml_str.append('<subroutineBody>')
	_, _, i = parse_token(tokens, i, expected_token_str='{')
	print 'cur', i
	i = compile_var_dec(tokens, i)
	i = compile_statements(tokens, i)
	_, _, i = parse_token(tokens, i, expected_token_str='}')
	xml_str.append('</subroutineBody>')
	return i

def compile_let(tokens, i):
	print "enter into let"
	xml_str.append('<letStatement>')
	_, _, i = parse_token(tokens, i, expected_token_str='let')
	_, _, i = parse_token(tokens, i)
	token_str, token_type = tokens[i]
	if token_str == '[':
		_,_,i = parse_token(tokens, i)
		i = compile_expression(tokens, i)
		_, _, i = parse_token(tokens,i,expected_token_str = ']')
	token_str, token_type = tokens[i]
	_,_,i = parse_token(tokens, i, expected_token_str='=')
	i = compile_expression(tokens, i)
	_,_,i = parse_token(tokens, i,expected_token_str=';')
	xml_str.append('</letStatement>')
	return i

def compile_if(tokens, i):
	xml_str.append('<ifStatement>')
	_, _, i = parse_token(tokens, i, expected_token_str='if')
	_, _, i = parse_token(tokens, i, expected_token_str='(')
	i = compile_expression(tokens,i)
	_, _, i = parse_token(tokens, i , expected_token_str=')')
	_, _, i = parse_token(tokens, i, expected_token_str='{')
	i = compile_statements(tokens,i)
	_, _, i = parse_token(tokens, i, expected_token_str= '}')
	token_str, token_type = tokens[i]
	if token_str == 'else':
		_, _, i = parse_token(tokens,i)
		_, _, i = parse_token(tokens, i, expected_token_str='{')
		i = compile_statements(tokens,i)
		_, _, i = parse_token(tokens, i, expected_token_str= '}')
	xml_str.append('</ifStatement>')
	return i

def compile_while(tokens, i):
	xml_str.append('<whileStatement>')
	print "while debug", i, tokens[i]
	_, _, i = parse_token(tokens, i, expected_token_str='while')
	_, _, i = parse_token(tokens, i, expected_token_str='(')
	i = compile_expression(tokens,i)
	_, _, i = parse_token(tokens, i , expected_token_str=')')
	_, _, i = parse_token(tokens, i, expected_token_str='{')
	i = compile_statements(tokens,i)
	_, _, i = parse_token(tokens, i, expected_token_str= '}')
	xml_str.append('</whileStatement>')
	return i

def compile_do(tokens,i):
	xml_str.append('<doStatement>')
	_,_,i = parse_token(tokens, i, expected_token_str='do')
	i = compile_subroutine_call(tokens, i)
	_,_,i = parse_token(tokens, i, expected_token_str=';')
	xml_str.append('</doStatement>')
	return i

def compile_return(tokens,i):
	xml_str.append('<returnStatement>')
	_, _,i = parse_token(tokens, i, expected_token_str='return')
	token_str, token_type = tokens[i]
	if token_str != ';':
		i = compile_expression(tokens, i)
	_, _, i= parse_token(tokens, i, expected_token_str=';')
	xml_str.append('</returnStatement>')
	return i

# expression term(op term)*
def compile_expression(tokens, i):
	xml_str.append('<expression>')
	i = compile_term(tokens, i)
	token_str, token_type = tokens[i]
	# print "token_str", token_str, token_str in operation_table
	while token_str in operation_table:
		_, _, i = parse_token(tokens, i)
		# print "compile_expression", tokens[i]
		i = compile_term(tokens, i)
		token_str, token_type = tokens[i]
	xml_str.append('</expression>')
	return i

#term: integerConstant | stringConstant | keywordConstant |
# varName | varName '[' expression ']' | subrountineCall |
# '(' expression ')' | unaryOp term
def compile_term(tokens, i):
	xml_str.append('<term>')
	token_str, token_type = tokens[i]
	print token_str, token_type
	if token_str in keywordConstant or token_type in ['integerConstant', 'stringConstant']:
		_, _, i = parse_token(tokens,i)
		xml_str.append('</term>')
		return i
	elif token_type == 'identifier':
		#varname | varname['expression'] | subroutineCall
		token_str, _ = tokens[i + 1]
		if token_str == '(' or token_str == '.':
			i = compile_subroutine_call(tokens, i)
		else:
			_, _, i = parse_token(tokens,i)
			token_str, token_type = tokens[i]
			if token_str == '[':
				_,_, i = parse_token(tokens, i)
				i = compile_expression(tokens, i)
				_,_,i = parse_token(tokens, i, expected_token_str=']')
	elif token_str in unary_operation:
		_, _, i = parse_token(tokens, i, expected_token_str=unary_operation)
		i = compile_term(tokens,i)
	elif token_str == '(':
		token_str, token_type = tokens[i+2]
		if token_str == '.':
			i = compile_subroutine_call(tokens,i)
		else:
			_, _, i = parse_token(tokens, i)
			i = compile_expression(tokens, i)
			_, _, i = parse_token(tokens, i, ')')
	xml_str.append('</term>')
	return i

def compile_subroutine_call(tokens, i):
	token_str, token_type = tokens[i + 1]
	if token_str == '.':
		_,_,i = parse_token(tokens, i)
		_,_,i = parse_token(tokens, i, expected_token_str='.')

	_, _, i = parse_token(tokens, i)
	_,_,i = parse_token(tokens, i, expected_token_str='(')
	i = compile_expression_list(tokens,i)
	_,_,i = parse_token(tokens, i, expected_token_str=')')
	return i

def compile_expression_list(tokens, i):
	xml_str.append('<expressionList>')
	token_str, token_type = tokens[i]
	if token_str == ')':
		xml_str.append('</expressionList>')
		return i
	else:
		i = compile_expression(tokens,i)
		token_str, token_type = tokens[i]
		while token_str == ',':
			_, _, i = parse_token(tokens, i)
			i = compile_expression(tokens,i)
			token_str, token_type = tokens[i]
	xml_str.append('</expressionList>')
	return i















