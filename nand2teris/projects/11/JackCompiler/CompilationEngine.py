import SymbolTable

type_table = ["int", "char", "boolean", "Array"]
statement_keyword = ["let", "if", "else", "while", "do", "return"]
operation_table = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
unary_operation = ["-", "~"]
keywordConstant = ["true", "false", "null", "this"]

var_scope_table = ["field", "static"]
subroutine_type_table = ["constructor", "function", "method"]

cur_subroutine_name = ""
vm_codes = []
cur_label_table = {}
cur_subroutine_type = ""
cur_class_name = ''

def parse_token(tokens, i, expected_token_str=None, expected_token_type=None):
    token_str, token_type = tokens[i]
    if expected_token_str and (
        token_str != expected_token_str and token_str not in expected_token_str
    ):
        raise Exception(
            "Compile error: expect "
            + expected_token_str
            + " but current str is "
            + token_str
        )
    if expected_token_type and (
        token_type != expected_token_type and token_type not in expected_token_type
    ):
        raise Exception(
            "Compile error: expect "
            + expected_token_type
            + " but current str is "
            + token_type
        )
    return token_str, token_type, i + 1


def compile_engine(file_name, tokens):
    global vm_codes, cur_label_table
    vm_codes = []
    cur_label_table = {}
    
    i = 0
    while i < len(tokens):
        i = compile_class(tokens, i, file_name)

    return vm_codes


def compile_class(tokens, i, file_name):
    global type_table, cur_class_name
    SymbolTable.clear_class_symbol_table()
    _, _, i = parse_token(tokens, i, expected_token_str="class")
    class_name, _, i = parse_token(tokens, i, expected_token_type="identifier")
    type_table.append(class_name)
    cur_class_name = class_name
    _, _, i = parse_token(tokens, i, expected_token_str="{")
    token_str, token_type = tokens[i]
    if token_str not in var_scope_table and token_str not in subroutine_type_table:
        raise Exception("Compile error: expect var dec or subroutine dec")
    else:
        i = compile_class_var_dec(tokens, i)
        i = compile_subroutine_dec(tokens, i, class_name, file_name)
    _, _, i = parse_token(tokens, i, expected_token_str="}")
    return i


def compile_class_var_dec(tokens, i):
    token_str, token_type = tokens[i]
    if token_str not in var_scope_table:
        return i

    while token_str in var_scope_table:
        var_kind, _, i = parse_token(tokens, i)
        var_type, _, i = parse_token(tokens, i)
        var_name, _, i = parse_token(tokens, i, expected_token_type="identifier")
        SymbolTable.add_to_class_symbol_table(var_name, var_type, var_kind)
        token_str, token_type = tokens[i]
        while token_str == ",":
            _, _, i = parse_token(tokens, i)
            var_name, _, i = parse_token(tokens, i, expected_token_type="identifier")
            SymbolTable.add_to_class_symbol_table(var_name, var_type, var_kind)
            token_str, token_type = tokens[i]
        _, _, i = parse_token(tokens, i, expected_token_str=";")
        token_str, token_type = tokens[i]
    return i


def compile_subroutine_dec(tokens, i, class_name, file_name):
    global cur_subroutine_name, cur_subroutine_type, cur_label_table
    token_str, token_type = tokens[i]

    if token_str not in subroutine_type_table:
        return i

    while token_str in subroutine_type_table:
    	SymbolTable.clear_subroutine_symbol_table()
        cur_subroutine_type, _, i = parse_token(tokens, i)
        _, _, i = parse_token(tokens, i)
        cur_subroutine_name, _, i = parse_token(
            tokens, i, expected_token_type="identifier"
        )
        if cur_subroutine_type == "method":
            SymbolTable.add_to_subroutine_symbol_table("this", class_name, "argument")
        cur_label_table[cur_class_name + "$" + cur_subroutine_name] = 0
        _, _, i = parse_token(tokens, i, "(")
        i = compile_parameter_list(tokens, i)
        _, _, i = parse_token(tokens, i, ")")
        i = compile_subroutine_body(tokens, i, class_name, file_name)
        token_str, token_type = tokens[i]
    return i


# ((type varname)(',' type varnmae)*)?
def compile_parameter_list(tokens, i):
    token_str, token_type = tokens[i]
    while token_str in type_table:
        var_type, _, i = parse_token(tokens, i)
        var_name, _, i = parse_token(tokens, i, expected_token_type="identifier")
        SymbolTable.add_to_subroutine_symbol_table(var_name, var_type, "argument")
        token_str, token_type = tokens[i]
        while token_str == ",":
            _, _, i = parse_token(tokens, i)
            var_type, _, i = parse_token(tokens, i)
            var_name, _, i = parse_token(tokens, i, expected_token_type="identifier")
            SymbolTable.add_to_subroutine_symbol_table(var_name, var_type, "argument")
            token_str, token_type = tokens[i]
    return i


def compile_statements(tokens, i):
    token_str, token_type = tokens[i]
    while token_str in statement_keyword:
        if token_str == "let":
            i = compile_let(tokens, i)
        elif token_str == "if":
            i = compile_if(tokens, i)
        elif token_str == "while":
            i = compile_while(tokens, i)
        elif token_str == "do":
            i = compile_do(tokens, i)
        elif token_str == "return":
            i = compile_return(tokens, i)
        token_str, token_type = tokens[i]
    return i


def compile_var_dec(tokens, i):
    token_str, token_type = tokens[i]
    while token_str == "var":
        _, _, i = parse_token(tokens, i)
        var_type, _, i = parse_token(tokens, i)
        var_name, _, i = parse_token(tokens, i, expected_token_type="identifier")
        SymbolTable.add_to_subroutine_symbol_table(var_name, var_type, "local")

        token_str, token_type = tokens[i]
        while token_str == ",":
            _, _, i = parse_token(tokens, i)
            var_name, _, i = parse_token(tokens, i, expected_token_type="identifier")
            SymbolTable.add_to_subroutine_symbol_table(var_name, var_type, "local")
            token_str, token_type = tokens[i]
        _, _, i = parse_token(tokens, i, expected_token_str=";")
        token_str, token_type = tokens[i]
    return i


def compile_subroutine_body(tokens, i, class_name, file_name):
    _, _, i = parse_token(tokens, i, expected_token_str="{")
    i = compile_var_dec(tokens, i)
    subroutine_local_num = SymbolTable.get_subroutine_local_num()
    print 'sub_routine_local_num', subroutine_local_num, cur_subroutine_name, cur_subroutine_type
    vm_codes.append(
        "function "
        + file_name
        + "."
        + cur_subroutine_name
        + " "
        + str(subroutine_local_num)
    )

    if cur_subroutine_type == "method":
        # SymbolTable.add_to_subroutine_symbol_table("this", class_name, "argument")
        vm_codes.append("push argument 0")
        vm_codes.append("pop pointer 0")
    elif cur_subroutine_type == "constructor":
        field_num = SymbolTable.get_field_var_num()
        vm_codes.append("push constant " + str(field_num))
        vm_codes.append("call Memory.alloc 1")
        vm_codes.append("pop pointer 0")

    i = compile_statements(tokens, i)
    _, _, i = parse_token(tokens, i, expected_token_str="}")
    return i


def assign_value_to_var(var_name, is_arr_elem):
    global cur_subroutine_type
    if is_arr_elem:
    	vm_codes.append("pop temp 0")
        vm_codes.append("pop pointer 1")
        vm_codes.append("push temp 0")
        vm_codes.append("pop that 0")
        return
    var_type, var_kind, var_no = SymbolTable.get_var_by_name(var_name)
    if var_kind == "local":
        vm_codes.append("pop local " + var_no)
    elif var_kind == "argument":
        vm_codes.append("pop argument " + var_no)
    elif var_kind == "static":
        vm_codes.append("pop static " + var_no)
    elif var_kind == "field":
		vm_codes.append("pop this " + var_no)



def compile_let(tokens, i):
    _, _, i = parse_token(tokens, i, expected_token_str="let")
    var_name, _, i = parse_token(tokens, i)
    token_str, token_type = tokens[i]
    is_arr_elem = False
    if token_str == "[":
    	is_arr_elem = True
        # var_type, var_kind, var_no = SymbolTable.get_var_by_name(var_name)
        push_val_for_var(var_name)
        # vm_codes.append("push local " + var_no)
        _, _, i = parse_token(tokens, i)
        i = compile_expression(tokens, i)
        vm_codes.append("add")
        _, _, i = parse_token(tokens, i, expected_token_str="]")
    token_str, token_type = tokens[i]

    _, _, i = parse_token(tokens, i, expected_token_str="=")
    i = compile_expression(tokens, i)
    assign_value_to_var(var_name, is_arr_elem)
    _, _, i = parse_token(tokens, i, expected_token_str=";")

    return i


def get_label():
    global cur_label_table
    print cur_label_table
    label_prefix = cur_class_name + "$" + cur_subroutine_name
    label_suffix = cur_label_table[label_prefix]
    cur_label_table[label_prefix] = cur_label_table[label_prefix] + 1
    return label_prefix + str(label_suffix)


def compile_if(tokens, i):
    _, _, i = parse_token(tokens, i, expected_token_str="if")
    _, _, i = parse_token(tokens, i, expected_token_str="(")
    i = compile_expression(tokens, i)
    _, _, i = parse_token(tokens, i, expected_token_str=")")
    vm_codes.append("not")

    first_label = get_label()
    vm_codes.append("if-goto " + first_label)
    _, _, i = parse_token(tokens, i, expected_token_str="{")
    i = compile_statements(tokens, i)
    _, _, i = parse_token(tokens, i, expected_token_str="}")
    token_str, token_type = tokens[i]
    # cur_label_number  = cur_label_number + 1

    second_label = get_label()
    vm_codes.append("goto " + second_label)
    vm_codes.append("label " + first_label)
    if token_str == "else":
        _, _, i = parse_token(tokens, i)
        _, _, i = parse_token(tokens, i, expected_token_str="{")
        i = compile_statements(tokens, i)
        _, _, i = parse_token(tokens, i, expected_token_str="}")
    vm_codes.append("label " + second_label)
    return i


def compile_while(tokens, i):
    _, _, i = parse_token(tokens, i, expected_token_str="while")
    _, _, i = parse_token(tokens, i, expected_token_str="(")
    first_label = get_label()
    vm_codes.append("label " + first_label)
    i = compile_expression(tokens, i)
    vm_codes.append("not")
    _, _, i = parse_token(tokens, i, expected_token_str=")")
    _, _, i = parse_token(tokens, i, expected_token_str="{")
    second_label = get_label()
    vm_codes.append("if-goto " + second_label)
    i = compile_statements(tokens, i)
    vm_codes.append("goto " + first_label)
    vm_codes.append("label " + second_label)
    _, _, i = parse_token(tokens, i, expected_token_str="}")
    return i


def compile_do(tokens, i):
    _, _, i = parse_token(tokens, i, expected_token_str="do")
    i = compile_subroutine_call(tokens, i)
    _, _, i = parse_token(tokens, i, expected_token_str=";")
    vm_codes.append("pop temp 0")
    return i


def compile_return(tokens, i):
    _, _, i = parse_token(tokens, i, expected_token_str="return")
    token_str, token_type = tokens[i]
    if token_str != ";":
        i = compile_expression(tokens, i)
    else:
        vm_codes.append("push constant 0")
    _, _, i = parse_token(tokens, i, expected_token_str=";")
    vm_codes.append("return")
    return i


def compile_expression(tokens, i):
    operation_code_table = {
        "+": "add",
        "-": "sub",
        "*": "call Math.multiply 2",
        "/": "call Math.divide 2",
        "&": "and",
        "|": "or",
        "<": "lt",
        ">": "gt",
        "=": "eq",
    }
    i = compile_term(tokens, i)
    token_str, token_type = tokens[i]
    while token_str in operation_table:
        operation, _, i = parse_token(tokens, i)
        i = compile_term(tokens, i)
        vm_codes.append(operation_code_table[operation])
        token_str, token_type = tokens[i]
    return i


def push_val_for_keyword(constant_str):
    if constant_str == "this":
        vm_codes.append("push pointer 0")
    elif constant_str == "null":
        vm_codes.append("push constant 0")
    elif constant_str == "true":
        vm_codes.append("push constant 1")
        vm_codes.append("neg")
    elif constant_str == "false":
        vm_codes.append("push constant 0")


def push_val_for_var(var_name):
    # print 'var_name', var_name
    var_type, var_kind, var_no = SymbolTable.get_var_by_name(var_name)
    if var_kind == "local":
        vm_codes.append("push local " + var_no)
    elif var_kind == "argument":
        vm_codes.append("push argument " + var_no)
    elif var_kind == "field":
        # vm_codes.append("push argument 0")
        # vm_codes.append("pop pointer 0")
        vm_codes.append("push this " + var_no)
    elif var_kind == "static":
        vm_codes.append("push static " + var_no)


# term: integerConstant | stringConstant | keywordConstant |
# varName | varName '[' expression ']' | subrountineCall |
# '(' expression ')' | unaryOp term
def compile_term(tokens, i):
    token_str, token_type = tokens[i]
    if token_type == "integerConstant":
        constant_str, _, i = parse_token(tokens, i)
        vm_codes.append("push " + "constant " + constant_str)
        return i
    elif token_type == "stringConstant":
        constant_str, _, i = parse_token(tokens, i)
        str_length = len(constant_str)
        vm_codes.append("push constant " + str(str_length))
        vm_codes.append("call String.new 1")
        for c in list(constant_str):
            vm_codes.append("push constant " + str(ord(c)))
            vm_codes.append("call String.appendChar 2")
        return i
    elif token_type == "keyword":
        constant_str, _, i = parse_token(tokens, i)
        push_val_for_keyword(constant_str)
        return i
    elif token_type == "identifier":
        # varname | varname['expression'] | subroutineCall
        next_token_str, _ = tokens[i + 1]
        if next_token_str == "(" or next_token_str == ".":
            i = compile_subroutine_call(tokens, i)
        else:
            push_val_for_var(token_str)
            _, _, i = parse_token(tokens, i)
            token_str, token_type = tokens[i]
            if token_str == "[":
                _, _, i = parse_token(tokens, i)
                i = compile_expression(tokens, i)
                _, _, i = parse_token(tokens, i, expected_token_str="]")
                vm_codes.append("add")
                vm_codes.append('pop pointer 1')
                vm_codes.append('push that 0')
    elif token_type == "symbol":
        if token_str in unary_operation:
            _, _, i = parse_token(tokens, i, expected_token_str=unary_operation)
            i = compile_term(tokens, i)
            if token_str == '-':
            	vm_codes.append('neg')
            if token_str == '~':
            	vm_codes.append('not')
        elif token_str == "(":
            token_str, token_type = tokens[i + 2]
            if token_str == ".":
                i = compile_subroutine_call(tokens, i)
            else:
                _, _, i = parse_token(tokens, i)
                i = compile_expression(tokens, i)
                _, _, i = parse_token(tokens, i, ")")
    return i


def compile_subroutine_call(tokens, i):
    code = "call "
    token_str, token_type = tokens[i + 1]
    subroutine_argument_number = 0
    if token_str == ".":
        var_name, _, i = parse_token(tokens, i)
        var_type, var_kind, var_no = SymbolTable.get_var_by_name(var_name)
        if var_no and var_type and var_kind:
            if var_kind == 'field':
            	vm_codes.append('push this '+ var_no)
            	code = code + var_type + '.'
            	subroutine_argument_number = subroutine_argument_number + 1
            else:
                vm_codes.append("push " + var_kind + " " + var_no)
                code = code + var_type + '.'
                subroutine_argument_number = subroutine_argument_number + 1
        else:
            code = code + var_name + "."
        _, _, i = parse_token(tokens, i, expected_token_str=".")
    else:
    	subroutine_argument_number = subroutine_argument_number + 1
    	vm_codes.append('push pointer 0')
    	code = code + cur_class_name + '.'

    called_subroutine, _, i = parse_token(tokens, i)
    _, _, i = parse_token(tokens, i, expected_token_str="(")

    i, expression_num = compile_expression_list(tokens, i)
    subroutine_argument_number = subroutine_argument_number + expression_num
    code = code + called_subroutine + " " + str(subroutine_argument_number)
    vm_codes.append(code)

    _, _, i = parse_token(tokens, i, expected_token_str=")")
    return i


def compile_expression_list(tokens, i):
    expression_num = 0
    token_str, token_type = tokens[i]
    if token_str != ")":
        expression_num = expression_num + 1
        i = compile_expression(tokens, i)
        token_str, token_type = tokens[i]
        while token_str == ",":
            _, _, i = parse_token(tokens, i)
            expression_num = expression_num + 1
            i = compile_expression(tokens, i)
            token_str, token_type = tokens[i]
    return i, expression_num
