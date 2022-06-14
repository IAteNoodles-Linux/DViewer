#!/bin/env python

import mariadb
import sys
# Variables

class SQL:
    """
    Class for working with SQL.
    """
    def __init__(self, user: str, password: str, host: str, database: str):
        """
        Create a connection to a database.

        Args:
            user: Username.
            password: Password.
            host: Hostname.
            database: Database name.
        """
        self.current_table = None
        try:
            self.connection = mariadb.connect(host=host, user=user, password=password, database=database)
        except mariadb.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))

    def send_command(self, command: str, commit=False, fetch=True):
        """
        Send a command to the database and return the result

        Args:
            self: Connection to the database.
            command: Command to send to the database.
            commit: Whether to commit the changes. Default is False.
            fetch: Number of rows to fetch. Default is True, which means to fetch all rows.

        Returns:
            tuple: Executes the command and fetches the result.
            False, if the command failed.
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(command)
            if commit:
                self.connection.commit()
            if fetch:
                return cursor.fetchall()
            else:
                return cursor.fetchmany(fetch)
        except mariadb.Error as e:
            #@TODO: Handle errors and report appropriately.
            print("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit(1)

    def show_databases(self):
        """
        Show all databases.
        """
        command = "SHOW DATABASES"
        return self.send_command(command)

    def add_database(self, database: str):
        """
        Add a database.

        Args:
            database: Name of the database to add.
        """
        command = "CREATE DATABASE %s" % database
        return self.send_command(command)

    def show_permissions_on_database(self, database: str):
        """
        Show the permissions on a database.

        Args:
            database: Name of the database to show the permissions on.
        """
        command = "SELECT * FROM mysql.db WHERE Db = '%s'" % database
        return self.send_command(command)

    def update_permissions_on_database(self, database: str, user: str, host: str, permissions: str):
        """
        Update the permissions on a database.

        Args:
            database: Name of the database to update the permissions on.
            user: Username.
            host: Hostname.
            permissions: New permissions.
        """

        command = "GRANT %s ON %s.* TO '%s'@'%s'" % (permissions, database, user, host)
        return self.send_command(command)

    def switch_database(self, database: str):
        """
        Switch to a different database.
        
        Args:
            database: Name of the database to switch to.
        """
        command = "USE %s" % database
        return self.send_command(command)

    def show_tables(self, *args):
        """
        Show all tables in the database.
        """
        if len(args) != 0:
            command = "SHOW TABLES FROM %s" % args[0]
        else:
            command = "SHOW TABLES"
        return self.send_command(command)

    def select_table(self, table_name: str):
        """
        Selects a table to work with.

        Args:
            table_name: Name of the table to select.
        """
        self.current_table = table_name

    def show_columns(self, *args):
        """
        Get the columns and types of a table.

        Args:
            table_name: Name of the table to get the columns and types from. If not specified, the current table is used.

        Returns:
            dict: Dictionary of columns and their attributes.
            {name: {column_type, is_nullable, key, default, extra}}

        """
        if len(args) == 0:
            command = "SHOW COLUMNS FROM %s" % self.current_table
        else:
            command = "DESCRIBE %s" % args[0]
        data = self.send_command(command)
        columns = {}
        for row in data:
            columns[row[0]] = {
                "column_type": row[1],
                "is_nullable": row[2],
                "key": row[3],
                "default": row[4],
                "extra": row[5]
            }
        return columns

    def create_table(self,  table_name: str, columns_with_types: dict):
        """
        Create a table.

        Args:
            table_name: Name of the table to create.
            columns_with_types: Dictionary of columns and their types.
        """
        command = "CREATE TABLE %s (%s)" % (table_name, ", ".join(["%s %s" % (key, columns_with_types[key]) for key in columns_with_types.keys()]))
        return self.send_command(command)

    def add_column(self, column_name: str, column_type: str, *args):
        """
        Add a column to a table.

        Args:
            column_name: Name of the column to add.
            column_type: Type of the column to add.
        """
        if len(args) == 0:
            table_name = self.current_table
        else:
            table_name = args[0]
        command = "ALTER TABLE %s ADD COLUMN %s %s" % (table_name, column_name, column_type)
        return self.send_command(command)

    def insert_data(self, *args, **kwargs):
        """
        Insert data into a table.

        Args:
            table_name: Name of the table to insert data into. If not specified, the current table is used.
            **kwargs: Keyword arguments. The key is the column name and the value is the data to insert.
        """
        if len(args) == 0:
            table_name = self.current_table
        else:
            table_name = args[0]
        command = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, ", ".join(kwargs.keys()), ", ".join(["'%s'" % kwargs[key] for key in kwargs.keys()]))
        return self.send_command(command)

    def get_data(self, *data):
        """
        Get data from a table.

        Args:
            table_name: Name of the table to get data from.
            columns: List of columns to get data from. If not specified, all columns are used.
        """
        if len(data) == 1:
            command = "SELECT * FROM %s" % data[0]
        else:
            command = "SELECT %s FROM %s" % (", ".join(data[1:]), data[0])
        return self.send_command(command)

    def get_table_creation_script(self, *args):
        """
        Returns the creation script for a table.

        Args:
            table_name: Name of the table to show the creation script for.
        """
        if len(args) == 0:
            command = "SHOW CREATE TABLE %s" % self.current_table
        else:
            command = "SHOW CREATE TABLE %s" % args[0]
        return self.send_command(command)

    def join_table(self, left: str, right: str, join_type: str, conditions: str):
        """
        Join two tables.

        Args:
            left: Name of the left table.
            right: Name of the right table.
            join_type: Type of join. Valid values are: INNER, LEFT, RIGHT, CROSS.
            conditions: Conditions to join on.
        """
        command = "SELECT * FROM %s %s JOIN %s ON %s" % (left, join_type, right, conditions)
        return self.send_command(command)

    def get_foreign_keys(self, *args):
        """
        Get the foreign keys for a table.

        Args:
            table_name: Name of the table to get the foreign keys for.
        """
        if len(args) == 0:
            command = "SELECT * FROM information_schema.key_column_usage WHERE REFERENCED_TABLE_NAME = '%s'" % self.current_table

        command = "SELECT * FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_NAME = '%s' AND REFERENCED_TABLE_NAME IS NOT NULL" % args[0]
        return self.send_command(command)

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

