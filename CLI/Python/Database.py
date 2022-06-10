#!/bin/env python

import sys
import mariadb
import json

def forge_connection(host, user, password, database):
    try:
        return mariadb.connect(host=host, user=user, password=password, database=database)
    except mariadb.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

def send_command(connection ,command, commit=False):
    """
    Send a command to the database and return the result
    """
    try:
        cursor = connection.cursor()
        cursor.execute(command)
        return cursor.fetchall()
        if commit:
            connection.commit()
    except mariadb.Error as e:
        #@TODO: Handle errors and report appropriately.
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)

def print__data_as_dictionary(key: list,data: tuple):
    if len(key) != len(data):
        sys.stderr.write("Check the lenght of the key and data values")
        raise Exception("Error: print__data_as_dictionary takes key and data of equal length")

    for i in range(len(key)):
        print(key[i], data[i])

def show_permissions_on_database(connection, database):
    command = "SELECT * FROM mysql.db WHERE Db = '%s'" % database
    return send_command(connection, command)

def update_permissions_on_database(connection, database, user, host, permissions):
    command = "GRANT %s ON %s.* TO '%s'@'%s'" % (permissions, database, user, host)
    return send_command(connection, command)

def switch_database(connection, database):
    command = "USE %s" % database
    return send_command(connection, command)

def show_tables(connection):
    command = "SHOW TABLES"
    return send_command(connection, command)


def create_table(connection, table_name, columns_with_types):
    command = "CREATE TABLE %s (%s)" % (table_name, columns_with_types)
    return send_command(connection, command)

if __name__ == "__main__":
    connection = forge_connection("localhost", "dev", "1234", "test")
    connection.autocommit = False


