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
        Method to create the blank tables in the database.
        """
        #Create contacts table
        with self._db_conn:
            self._db_conn.execute('''CREATE TABLE  IF NOT EXISTS contacts
                            ( contact_id INTEGER PRIMARY KEY,
                            first_name TEXT,
                            last_name TEXT
                            )''')
            self._db_conn.commit()

            self._db_conn.execute('''CREATE TABLE IF NOT EXISTS address 
                            ( address_id INTEGER PRIMARY KEY, 
                            contact_id INTEGER, 
                            street TEXT, 
                            address_2 TEXT, 
                            address_3 TEXT, 
                            town TEXT, 
                            county TEXT, 
                            postcode TEXT, 
                            FOREIGN KEY(contact_id) REFERENCES contacts(contact_id) 
                            )''')

            self._db_conn.execute('''CREATE TABLE IF NOT EXISTS phone 
                            ( phone_id INTEGER PRIMARY KEY, 
                            contact_id INTEGER, 
                            phone_number TEXT, 
                            type TEXT, 
                            FOREIGN KEY(contact_id) REFERENCES contacts(contact_id)
                             )''')

            self._db_conn.execute('''CREATE TABLE IF NOT EXISTS email 
                            ( email_id INTEGER PRIMARY KEY, 
                            contact_id INTEGER, 
                            email_address TEXT, 
                            type TEXT, 
                            FOREIGN KEY(contact_id) REFERENCES contacts(contact_id)
                             )''')
            self._db_conn.commit()

    def table_exists(self, table_name):
        """
        Method to create check whether a table is in the database.
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
        Method to insert, update or remove a contact in the database.
        """
        cursor = self._db_conn.cursor()
        if action == 'insert':
            cursor.execute('''INSERT INTO contacts(first_name, last_name) VALUES(?,?)''', 
                    (contact['first_name'], contact['last_name']))
        self._db_conn.commit()

        return cursor.lastrowid

    def update_email(self, contact_id, email_details, action):
        """
        Method to insert, update or remove a contact in the database.
        """
        cursor = self._db_conn.cursor()
        if action == 'insert':
            cursor.execute('''INSERT INTO email(contact_id, email_address, type) VALUES(?,?,?)''', 
                    (contact_id, email_details['email_address'], email_details['type']))
        self._db_conn.commit()

        return cursor.lastrowid

    def update_address(self, contact_id, address_details, action):
        """
        Method to insert, update or remove a contact in the database.
        """
        pass
    
    def update_phone(self, contact_id, phone_details, action):
        """
        Method to insert, update or remove a contact in the database.
        """
        pass

    def get_contact_by_name(self, contact_name):
        """
        Method to return a contact from the database.
        """
        contact = None
        result = {}
        success = False

        cursor = self._db_conn.cursor()
        print(contact_name['first_name'], contact_name['last_name'])
        cursor.execute('''SELECT * FROM contacts WHERE first_name LIKE ? AND last_name LIKE ?''', 
            (contact_name['first_name'], contact_name['last_name']))
        
        rows = cursor.fetchall()

        num_rows = len(rows)
        result['rows'] = num_rows

        #If we just have one contact returned get the contact_id
        if num_rows == 1:
            contact = rows[0]
            success = True
        
        result['success'] = success
        result['contact'] = contact
        
        return result


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
        new_email = {}
        new_contact['first_name'] = 'Andy'
        new_contact['last_name'] = 'Stiller'
        new_email['email_address'] = 'email@somewhere.local'
        new_email['type'] = 'home'
        contact_id = addressbook.update_contact(new_contact,'insert')
        print(contact_id)
        print(addressbook.update_email(contact_id, new_email,'insert'))
        print(addressbook.get_contact_by_name(new_contact))

if __name__ == "__main__":
    main()