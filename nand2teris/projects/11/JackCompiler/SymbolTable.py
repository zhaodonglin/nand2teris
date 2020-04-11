class_symbol_table = {}
class_var_num_tbl = {"field": 0, "static": 0}

subroutine_symbol_table = {}
subroutine_var_num_tbl = {"local": 0, "argument": 0}


def add_to_class_symbol_table(var_name, var_type, var_kind):
    global class_symbol_table, class_var_num_tbl
    class_symbol_table[var_name] = (var_type, var_kind, class_var_num_tbl[var_kind])
    class_var_num_tbl[var_kind] = class_var_num_tbl[var_kind] + 1


def add_to_subroutine_symbol_table(var_name, var_type, var_kind):
    global subroutine_symbol_table, subroutine_var_num_tbl
    subroutine_symbol_table[var_name] = (
        var_type,
        var_kind,
        subroutine_var_num_tbl[var_kind],
    )
    subroutine_var_num_tbl[var_kind] = subroutine_var_num_tbl[var_kind] + 1


def get_var_by_name(var_name):
    var_info = subroutine_symbol_table.get(var_name, None)
    if var_info:
        var_type, var_kind, var_no = var_info
        return var_type, var_kind, str(var_no)
    var_info = class_symbol_table.get(var_name, None)
    if var_info:
        var_type, var_kind, var_no = var_info
        return var_type, var_kind, str(var_no)
    return None, None, None


def get_field_var_num():
    return class_var_num_tbl["field"]


def clear_class_symbol_table():
    global class_symbol_table, class_var_num_tbl
    class_symbol_table.clear()
    class_var_num_tbl = {"field": 0, "static": 0}


def clear_subroutine_symbol_table():
    global subroutine_var_num_tbl, subroutine_symbol_table
    subroutine_symbol_table.clear()
    print 'subroutine_symbol_table', subroutine_symbol_table
    subroutine_var_num_tbl = {"local": 0, "argument": 0}


def get_subroutine_local_num():
    print subroutine_var_num_tbl
    return subroutine_var_num_tbl['local']
