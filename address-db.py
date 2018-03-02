#!/usr/bin/env python3
"""
Address application database module
This is the module that accesses the address book database for the main apllication.
"""
import os
import sqlite3

DATABASE_PATH = "data/addressbook.db"

class AddressDatabase(object):
    def __init__(self, db_path = DATABASE_PATH):
        self._db_conn = None
        self._db_path = db_path

    def __enter__(self):
        self.opendb()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db_conn.close

    def opendb(self):
        path_exists = os.path.exists(self._db_path)

        self._db_conn = sqlite3.connect(self._db_path)

        #if the path didn't exist then we've created a new database file
        if not path_exists:
            self.createdb()

    def createdb(self):
        """
        Method to create the blank tables in the dabase.
        """

        #Create Address table
        with self._db_conn:
            self._db_conn.execute('''CREATE TABLE  IF NOT EXISTS contacts
                            (full_name TEXT,  
                            phone TEXT, 
                            email TEXT,
                            address TEXT,
                            PRIMARY KEY (full_name)
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

    def insert(self, fullname, phone, email, address):
        cursor = self._db_conn.cursor()
        cursor.execute('''INSERT INTO contacts(full_name, phone, email, address)
                  VALUES(?,?,?,?)''', (fullname, phone, email, address))
        self._db_conn.commit()

def main():
    """
    Entry point for testing if the file is run on it's own.
    """
    with AddressDatabase() as addressbook:
        if addressbook.table_exists('contacts'):
            print('Contacts table exists')

        addressbook.insert('Andy Stiller', '0000', 'andys email', 'address')

if __name__ == "__main__":
    main()