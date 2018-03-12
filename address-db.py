#!/usr/bin/env python3
"""
Address application database module
This is the module that accesses the address book database for the main apllication.
"""
import os
import sqlite3

DATABASE_PATH = "data/addressbook.db"

class AddressDatabase(object):
    """
    The AddressDatabase Class handles creating, acessing a writing to the address sqlite database
    """
    def __init__(self, db_path = DATABASE_PATH):
        self._db_conn = None
        self._db_path = db_path

    def __enter__(self):
        self.open_db()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db_conn.close

    def open_db(self):
        """
        Method to open the database and create it if required 
        """
        path_exists = os.path.exists(self._db_path)

        self._db_conn = sqlite3.connect(self._db_path)

        #if the path didn't exist then we've created a new database file
        if not path_exists:
            self.createdb()

    def createdb(self):
        """
        Method to create the blank tables in the dabase.
        """
        #Create contacts table
        with self._db_conn:
            self._db_conn.execute('''CREATE TABLE  IF NOT EXISTS contacts
                            ( contact_id INTEGER PRIMARY KEY,
                            first_name TEXT,
                            last_name TEXT, 
                            phone TEXT, 
                            email TEXT,
                            address TEXT
                            )''')

    def table_exists(self, table_name):
        """
        Method to create check whether a table is in the dabase.
        """
        cursor = self._db_conn.cursor()
        exists = False

        #Check for the table
        cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='?';'''),table_name

        if cursor.rowcount > 0:
            exists = True

        return exists

    def update_contact(self, contact, action):
        """
        Method to insert, update or remove a contact in the dabase.
        """
        cursor = self._db_conn.cursor()
        if action == 'insert':
            cursor.execute('''INSERT INTO contacts(first_name, last_name, phone, email, address) VALUES(?,?,?,?,?)''', 
                    (contact['first_name'], contact['last_name'], contact['phone'], contact['email'], contact['address']))
        self._db_conn.commit()

    def update_email(self, contact_id, email_details):
        """
        Method to insert, update or remove a contact in the dabase.
        """
        pass

    def update_address(self, contact_id, address_details):
        """
        Method to insert, update or remove a contact in the dabase.
        """
        pass
    
    def update_phone(self, contact_id, phone_details):
        """
        Method to insert, update or remove a contact in the dabase.
        """
        pass

    def get_contact(self, contact_name):
        """
        Method to insert, update or remove a contact in the dabase.
        """
        pass

    @property
    def addressbook(self):
        """ Property to return the the full addressbook as list of contacts
        """
        pass
    
def main():
    """
    Entry point for testing if the file is run on it's own.
    """
    with AddressDatabase() as addressbook:
        if addressbook.table_exists('contacts'):
            print('Contacts table exists')
        
        new_contact = {}
        new_contact['first_name'] = 'Andy'
        new_contact['last_name'] = 'Stiller'
        new_contact['phone'] = '0'
        new_contact['email'] = 'email'
        new_contact['address'] = 'Here'
        addressbook.update_contact(new_contact,'insert')

if __name__ == "__main__":
    main()