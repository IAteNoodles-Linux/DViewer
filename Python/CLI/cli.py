#!/bin/env pyhon

import sys
import argparse
import  Database

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


link = Database.forge_connection(args.user, args.password, args.hostname, args.database)

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
        print("show: Shows the connents.")
        print("Usage: show [database]|[table]|[column]")
        print("show database: Displays the list of databases.")
        print("show table: Displays the list of tables of the current database.")
        print("show table <database>: Displays the list of tables of the specified database.")
        print("show column: Displays the list of columns of the current table.")
        print("show column <table>: Displays the list of columns of the given table.")



def parse_command(response: str, *args):
    command = response.split(" ")
    try:
        if command[0] == "help":
            show_help(command[1])
    except IndexError:
        show_help(command[0])
    finally:
        return

    if command[0] == "status":
        status()
    elif command[0] == "show":
        if command[1] == "database":
            Database.show_databases(link)
        elif command[1] == "table":
            try:
                Database.show_tables(link, command[2])
            except IndexError:
                Database.show_tables(link)
        elif command[1] == "column":
            try:
                Database.show_columns(link, command[2])
            except IndexError:
                Database.show_columns(link, __current_table)
        

while (True):
    command = input("Enter a command: ")
    parse_command(command)
