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
def show_connection():
    print("User: " + args.user)
    print("Host: " + args.hostname)
    print("Database: " + args.database)

commands = ["help", "status", "show"]

def show_help(command: str):
    if command not in commands:
        print("Unknown command: " + command)
        return False
    if command == "help":
        print("help: Show this help message.")
    elif command == "status":
        print("status: Show the status of the database connection.")
    elif command == "show":
        print("show: Shows the connents.")
        print("show database: Displays the list of databases.")
        print("show table: Displays the list of tables.")


def parse_command(command: str):
    command = command.split(" ")
    try:
        if command[0] == "help":
            show_help(command[1])

        

while (True):
    command = input("Enter a command: ")
    parse_command(command)
