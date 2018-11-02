from werkzeug import datastructures


def build_multiple_select(
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
