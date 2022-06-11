#!/bin/env python

import sys
import mariadb

def forge_connection(host: str, user: str, password: str, database: str):
    """
    Create a connection to a database.

    Args:
        host: Hostname.
        user: Username.
        password: Password.
        database: Database name.
    """

    try:
        return mariadb.connect(host=host, user=user, password=password, database=database)
    except mariadb.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

def send_command(connection ,command: str, commit=False, fetch=True|int):
    """
    Send a command to the database and return the result

    Args:
        connection: Connection to the database.
        command: Command to send to the database.
        commit: Whether to commit the changes. Default is False.
        fetch: Number of rows to fetch. Default is True, which means to fetch all rows.

    Returns:
        tuple: Executes the command and fetches the result.
    """

    try:
        cursor = connection.cursor()
        cursor.execute(command)
        if commit:
            connection.commit()
        if fetch:
            return cursor.fetchall()
        else:
            return cursor.fetchmany(fetch)
    except mariadb.Error as e:
        #@TODO: Handle errors and report appropriately.
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

def print__data_as_dictionary(key: list,data: tuple):
    """
    Print data as a dictionary.

    Args:
        key: List of keys to use as keys in the dictionary.
        data: Tuple of data to use as values in the dictionary.
    """

    if len(key) != len(data):
        sys.stderr.write("Check the lenght of the key and data values")
        raise Exception("Error: print__data_as_dictionary takes key and data of equal length")

    for i in range(len(key)):
        print(key[i], data[i])

def show_permissions_on_database(connection, database: str):
    """
    Show the permissions on a database.

    Args:
        database: Name of the database to show the permissions on.
    """
    command = "SELECT * FROM mysql.db WHERE Db = '%s'" % database
    return send_command(connection, command)

def update_permissions_on_database(connection, database: str, user: str, host: str, permissions: str):
    """
    Update the permissions on a database.

    Args:
        database: Name of the database to update the permissions on.
        user: Username.
        host: Hostname.
        permissions: New permissions.
    """

    command = "GRANT %s ON %s.* TO '%s'@'%s'" % (permissions, database, user, host)
    return send_command(connection, command)

def switch_database(connection, database: str):
    """
    Switch to a different database.
    
    Args:
        database: Name of the database to switch to.
    """
    command = "USE %s" % database
    return send_command(connection, command)

def show_tables(connection):
    """
    Show all tables in the database.
    """
    command = "SHOW TABLES"
    return send_command(connection, command)

def get_columns_and_types(connection, table_name: str):
    """
    Get the columns and types of a table.

    Args:
        table_name: Name of the table to get the columns and types from.
    """
    command = "DESCRIBE %s" % table_name
    return send_command(connection, command)

def create_table(connection, table_name: str, columns_with_types: dict):
    """
    Create a table.

    Args:
        table_name: Name of the table to create.
        columns_with_types: Dictionary of columns and their types.
    """
    command = "CREATE TABLE %s (%s)" % (table_name, columns_with_types)
    return send_command(connection, command)

def insert_data(connection, table_name: str, **kwargs):
    """
    Insert data into a table.

    Args:
        table_name: Name of the table to insert data into.
        **kwargs: Keyword arguments. The key is the column name and the value is the data to insert.
    """
    command = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, ", ".join(kwargs.keys()), ", ".join(["'%s'" % kwargs[key] for key in kwargs.keys()]))
    return send_command(connection, command)

def get_data(connection, table_name: str, *data):
    """
    Get data from a table.

    Args:
        table_name: Name of the table to get data from.
        *data: Data to get from the table.
    """
    command = "SELECT %s FROM %s" % (", ".join(data), table_name)
    return send_command(connection, command)

def get_table_creation_script(connection, table_name: str):
    """
    Returns the creation script for a table.

    Args:
        table_name: Name of the table to show the creation script for.
    """
    command = "SHOW CREATE TABLE %s" % table_name
    return send_command(connection, command)

def join_table(connection, left: str, right: str, join_type: str, conditions: str):
    """
    Join two tables.

    Args:
        left: Name of the left table.
        right: Name of the right table.
        join_type: Type of join. Valid values are: INNER, LEFT, RIGHT, CROSS.
        conditions: Conditions to join on.
    """
    command = "SELECT * FROM %s %s JOIN %s ON %s" % (left, join_type, right, conditions)
    return send_command(connection, command)

def get_foreign_keys(connection, table_name: str):
    """
    Get the foreign keys for a table.

    Args:
        table_name: Name of the table to get the foreign keys for.
    """
    command = "SELECT * FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_NAME = '%s' AND REFERENCED_TABLE_NAME IS NOT NULL" % table_name
    return send_command(connection, command)


