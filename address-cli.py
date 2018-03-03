#!/usr/bin/env python
"""
Simplified address application application
This is the version just uses standard serialisation to text files
"""

import os, sys, getopt, json

FILE_PATH = "data/contacts.ab"

def list_addresses(filepath):
    path_exists = os.path.exists(filepath)
    loaded = True

    if path_exists:
        with open(filepath, 'r') as infile:
            contacts = json.load(infile)
            print(contacts)
    else:
        loaded = False

    return loaded

def find_address(filepath, contact):
    pass

def add_address(filepath):
    contact = {}
    print(filepath)

    fullname = input('Please enter the contact name: ')
    print(fullname)

    #if not fullname:
    contact['name'] = fullname
    contact['phone'] = str(input('Please enter their phone number: '))
    contact['address'] = input('Please enter their address: ')

    print(contact)
    with open(filepath, 'a') as outfile:
        print(outfile)
        json.dump(contact, outfile)


def remove_address(filepath, contact):
    pass

def help():
    cmd_help = 'address-cli.py -h -i <input file> -l -a -r -f <contact to find>"'
    print(cmd_help)

def process_options(argv, inputfile):
    action = ''
    contact = ''
    options = {}

    try:
        opts, args = getopt.getopt(argv,"hi:larf:",["help","ifile=","list","add","remove","find="])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            print(inputfile)
        elif opt in ("-l", "--list"):
            action = 'list'
        elif opt in ("-a", "--add"):
            action = 'add'
        elif opt in ("-r", "--remove"):
            action = 'remove'
        elif opt in ("-f", "--find"):
            action = 'find'
            contact = arg

    options['filepath'] = inputfile
    options['action'] = action
    options['contact'] = contact
    return options

def main(argv):
    options = process_options(argv, FILE_PATH)
    print(options['action'])
    print(options['filepath'])
    print(options['contact'])

    #Process the actions
    if options['action'] == 'list':
        list_addresses(options['filepath'])
    elif options['action'] == 'add':
        add_address(options['filepath'])
    elif options['action'] == 'remove':
        remove_address(options['filepath'], options['contact'])
    elif options['find'] == 'find':
        find_address(options['filepath'], options['contact'])
if __name__ == "__main__":
   main(sys.argv[1:])