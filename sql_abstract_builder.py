from werkzeug import datastructures


def build_select_with_multiple_conditions(
        table: str, parameters: tuple, arguments: datastructures.MultiDict):
    """
    :param table: Table to build query for.
    :param parameters: aka table.colomns to iterate
    :param arguments: aka table.rows

    the final query is basically as follows:
        SELECT * FROM <table>
        WHERE <parameter> = <argument>
                           \
                       or LIKE in case of string comparison

    """
    sql_statement = f'SELECT * FROM {table}'
    # the following line is for preventing IDE from "unexpected eol" warning
    sql_statement += ' WHERE '
    multiple_parameters = False
    at_least_one_argument = False
    for key in parameters:
        argument = arguments.get(key)
        if argument is not None:
            at_least_one_argument = True
            equal_operator = '=' if argument.isdigit() else 'LIKE'
            if multiple_parameters:
                sql_statement += ' AND '
            sql_statement += f'{key} {equal_operator} {argument}'
            multiple_parameters = True

    if at_least_one_argument:
        return sql_statement
    else:
        return None


def build_insert(
        table: str, colomn_names: tuple, values: tuple, values_types: tuple):
    # todo implement, for reference see TicketHandler's lines 51-75
    sql_statement = f'INSERT INTO {table} ('

    for col_name in colomn_names:
        sql_statement += f'{col_name}, '
    sql_statement = sql_statement[:-1]

    sql_statement += ') VALUES ('

    assert len(values) == len(values_types)
    for i in range(0, len(values)):
        value = values[i]
        value_type = values_types[i]
        use_backslash = value_type == 'str'

        if use_backslash:
            sql_statement += f'\'{value}\', '
        else:
            sql_statement += f'{value}, '

    sql_statement = sql_statement[:-2]
    sql_statement += ')'

    return sql_statement


def __init__():
    # maybe set table name here?
    ...
