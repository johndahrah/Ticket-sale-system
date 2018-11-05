from werkzeug import datastructures


def build_select_with_multiple_conditions(
        table: str, parameters: tuple, arguments: datastructures.MultiDict):
    """
    :param table:
        table to build query for
    :param parameters:
        represents table.columns to iterate
    :param arguments:
        represents table.rows to compare with
    :return
        'str' object containing sql query,
        or None in case of incorrect parameters

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


def build_insert_of_single_entry(
        table: str, column_names: tuple=None,
        values: tuple=None, returning_column: str=None):
    """
    :param table:
        table to build query for
    :param column_names:
        represents table.columns.
        in case of None, query fills the entire row
    :param values:
        values to insert in a new row.
        The type of values defines the use of the < ' > symbol,
        to specify a data type to be inserted.
        Therefore, it's a good idea to use an explicit cast of types,
        especially strings: str(string_data)
    :param returning_column:
        if not None, specifies the column.name to return
        after the statement will be executed
    :return: 'str' object containing sql query
    """
    sql_statement = f'INSERT INTO {table}'

    if column_names is not None:
        sql_statement += '('
        for col_name in column_names:
            sql_statement += f'{col_name}, '
        sql_statement = sql_statement[:-2]  # remove the trailing comma
        sql_statement += ')'

    sql_statement += ' VALUES ('

    for i in range(0, len(values)):
        value = values[i]

        if type(value) is str:
            sql_statement += f'\'{value}\', '
        else:
            sql_statement += f'{value}, '

    sql_statement = sql_statement[:-2]  # remove the trailing comma
    sql_statement += ')'

    if returning_column is not None:
        sql_statement += f' RETURNING {returning_column}'

    return sql_statement


def __init__():
    # maybe set table name here?
    ...
