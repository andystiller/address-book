#!/usr/bin/env python3
"""
Simplified address application application
This is the version just uses standard serialisation to text files
"""

import os, sys, getopt, json

FILE_PATH = "data/contacts.json"

def open_addressbook(filepath):
    path_exists = os.path.exists(filepath)
    addressbook = None

    if path_exists:
        with open(filepath, 'r') as infile:
            addressbook = json.load(infile)
            print(addressbook)

    return addressbook

def list_addresses(filepath):
    addressbook = open_addressbook(filepath)
    print(addressbook)

def find_address(filepath, contact):
    pass

def add_address(filepath):
    new_contact = {}

    fullname = input('Please enter the contact name: ')
    print(fullname)

    # Have we got a name to add?
    if fullname:
        new_contact['name'] = fullname
        new_contact['phone'] = str(input('Please enter their phone number: '))
        new_contact['address'] = input('Please enter their address: ')

        # Try to open the current addressbook
        addressbook = open_addressbook(filepath)

        if addressbook is None:
            # If there was no addressbook create one
            print('Creating new address book')
            contacts = []
            addressbook = {'filetype':'Addressbook','application':'address-cli.py', 'contacts': contacts}

        print(new_contact)
        with open(filepath, 'w') as outfile:
            # Write the output file with the new contact
            print(outfile)
            addressbook['contacts'].append(new_contact)
            print(addressbook)
            json.dump(addressbook, outfile)


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

    if action == '':
        #If there are no actions display the help and quit the program
        help()
        sys.exit(2)

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
    elif options['action'] == 'find':
        find_address(options['filepath'], options['contact'])
        
if __name__ == "__main__":
   main(sys.argv[1:])