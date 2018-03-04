#!/usr/bin/env python3
"""
Simplified address application application
This is the version just uses standard serialisation to text files
"""

import os, sys, getopt, json

FILE_PATH = "data/contacts.json"

def open_addressbook(filepath):
    """
    Function to open the address book file specified
    Returns the addressbook or None
    """
    path_exists = os.path.exists(filepath)
    addressbook = None

    if path_exists:
        with open(filepath, 'r') as infile:
            addressbook = json.load(infile)

    return addressbook

def list_contacts(filepath):
    """
    Function to list contact details in the addressbook
    Returns 
    """
    addressbook = open_addressbook(filepath)
    
    if addressbook:
        for contact in addressbook['contacts']:
            print('Name: ' + contact['name'], 'Telephone: ' + contact['phone'], 'Address: ' + contact['address'], sep='\t', end='\n' )
    else:
        print('No address book found!')

def retrieve_contact(filepath, name):
    """
    Function to retirve specified contact details in the addressbook
    Returns a contact or None
    """
    contact_details = None
    addressbook = open_addressbook(filepath)
    print('Finding ', name)

    if addressbook:
        for contact in addressbook['contacts']:
            if contact['name'] == name:
                contact_details = contact
                break
    else:
        print('No address book found!')
    
    print('Name: ' + contact_details['name'], 'Telephone: ' + contact_details['phone'], 
        'Address: ' + contact_details['address'], sep='\t', end='\n' )
    return contact_details

def add_contact(filepath):
    """
    Function to add contact details to the addressbook
    It take user input and creates a contact that is added
    Returns 
    """
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
            addressbook['contacts'].append(new_contact)
            json.dump(addressbook, outfile)

def remove_contact(filepath, name):
    """
    Function to remove specified contact details from the addressbook
    Returns 
    """
    # Have we got a name to remove?
    if name:
        # Try to open the current addressbook and find the contact index
        addressbook = open_addressbook(filepath)
        contact = retrieve_contact(filepath, name)

        if contact:
            with open(filepath, 'w') as outfile:
                # If contact was found delete it
                addressbook['contacts'].remove(contact)
                json.dump(addressbook, outfile)
                print('Contact: ', contact, ' removed.\n')

def help():
    """
    Function to display the command line help
    Returns 
    """
    cmd_help = 'address-cli.py -h -i <input file> -l -a -r -f <contact to find>"'
    print(cmd_help)

def process_options(argv, inputfile):
    """
    Function to determine what option were spefied
    only the last action is used. Setting the file name always gets handled.
    Returns options that are selected including the last action, file path and contact name
    """
    action = ''
    contact = ''
    options = {}

    try:
        opts, args = getopt.getopt(argv,"hi:lar:f:",["help","ifile=","list","add","remove","find="])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-l", "--list"):
            action = 'list'
        elif opt in ("-a", "--add"):
            action = 'add'
        elif opt in ("-r", "--remove"):
            action = 'remove'
            contact = arg
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

    #Process the actions
    if options['action'] == 'list':
        list_contacts(options['filepath'])
    elif options['action'] == 'add':
        add_contact(options['filepath'])
    elif options['action'] == 'remove':
        remove_contact(options['filepath'], options['contact'])
    elif options['action'] == 'find':
        retrieve_contact(options['filepath'], options['contact'])
        
if __name__ == "__main__":
   main(sys.argv[1:])