#!/bin/env pyhon

import sys
import argparse
import  Database as db

# A command line interface for accessing the APIs in the Database.py module.
# The user is prompted to enter a command and the corresponding function is called.

parser = argparse.ArgumentParser(description='A command line interface for accessing the APIs in the Database.py module.')

parser.add_argument('-u','--user', type=str, help='The user to connect to the database as.')
parser.add_argument('-p','--password', type=str, help='The password to connect to the database with.')
parser.add_argument('-host','--hostname', type=str, help='The host to connect to the database on.')
parser.add_argument('-d','--database', type=str, help='The database to connect to.')

# We parse the arguments.
args = parser.parse_args()

# We create a connection to the database.


Database = db(args.user, args.password, args.hostname, args.database)

# Still need to catch the exception if the connection fails.

# Greetings.

print("DViewer")

commands = ["help", "status", "show"]

def status():
    print("User: " + args.user)
    print("Host: " + args.hostname)
    print("Database: " + args.database)

def show_help(command: str):
    if command not in commands:
        print("Unknown command: " + command)
        return
    if command == "help":
        print("help: Show this help message.")
    elif command == "status":
        print("status: Show the status of the database connection.")
    elif command == "show":
        print("show") # Show the available commands. Needs color.
        print("Usage: show [database]|[table]|[column]")
        print("show database: Displays the list of databases.")
        print("show table: Displays the list of tables of the current database.")
        print("show table <database>: Displays the list of tables of the specified database.")
        print("show column: Displays the list of columns of the current table.")
        print("show column <table>: Displays the list of columns of the given table.")
        print("show column <database> <table>: Displays the list of columns of the given table in the given database.")
    elif command == "add": # Add a new table to the database.
        print("Usage: add <database> | <table> | <column>")
        print("add database <name>: Adds a new database.")
        print("add table <name> <columns>: Adds a new table to the current database.")
        print("add table <name> <database> <columns>: Adds a new table to the specified database.") #Need to think what if the database doesn't exist.
        print("add column <name> <description>: Adds a new column to the current table.")
        print("add column <name> <description> <table>: Adds a new column to the given table.")
        print("add column <name> <description> <database> <table>: Adds a new column to the given table in the given database.")


def parse_command(response: str):
    command = response.split(" ")
    try:
        if command[0] == "help":
            show_help(command[1])
    except IndexError:
        show_help(command[0])

    if command[0] == "status":
        status()
    elif command[0] == "show":
        if command[1] == "database":
            Database.show_databases()
        elif command[1] == "table":
            try:
                Database.show_tables(command[2])
            except IndexError:
                Database.show_tables()
        elif command[1] == "column":
            try:
                Database.show_columns(".".join(command[1:3]))
            except IndexError:
                try:
                    Database.show_columns(command[2])
                except IndexError:
                    Database.show_columns()
        else:
            print("Invalid usage of show. See help for more information.")
    elif command[0] == "add":
        if command[1] == "database":
            Database.add_database(command[2])
        elif command[1] == "table":
            try:
                Database.create_table(".".join(command[1:3]), command[4])
            except IndexError:
                Database.create_table(command[2], command[3])
        elif command[1] == "column":
            try:
                Database.add_column(command[2], command[3], ".".join(command[3:5]))
            except IndexError:
                try:
                    Database.add_column(command[2], command[3], command[4])
                except IndexError:
                    Database.add_column(command[2], command[3])
        else:
            print("Invalid usage of add. See help for more information.")
    else:
        print("Unknown command: " + command[0])
    return 

while (True):
    command = input("Enter a command: ")
    parse_command(command)
