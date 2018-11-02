from werkzeug import datastructures


def build_multiple_select(
        table: str, parameters: tuple, resolve: datastructures.MultiDict):
    sql_statement = f'SELECT * FROM {table}'

    # the following line is for preventing IDE from "unexpected eol" warning
    sql_statement += ' WHERE '
    multiple_parameters = False
    at_least_one_argument = False
    for json_key in parameters:
        argument = resolve.get(json_key)
        if argument is not None:
            at_least_one_argument = True
            equal_operator = '=' if argument.isdigit() else 'LIKE'
            if multiple_parameters:
                sql_statement += ' AND '
            sql_statement += f'{json_key} {equal_operator} {argument}'
            multiple_parameters = True

    if at_least_one_argument:
        return sql_statement
    else:
        return None
