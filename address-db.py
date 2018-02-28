#!/usr/bin/env python3
"""
Address application database module
This is the module that accesses the address book database for the main apllication.
"""
import sqlite3


DATABASE_PATH = "data/addressbook.db"

def createdb(conn):
    """
    Function to create the blank tables in the dabase.
    con is a connection to a Sqlite database
    """
    curs = conn.cursor()

    #Create Address table
    curs.execute('''CREATE TABLE address IF NOT EXISTS
             (first_name TEXT, 
             last_name TEXT, 
             phone TEXT, 
             email TEXT,
             address TEXT
             )''')
    # Save (commit) the changes
    conn.commit()

def table_exists(conn, table_name):
    curs = conn.cursor()

    #Create Address table
    curs.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='?';'''),table_name
    return curs.rowcount

def main():
    """
    Entry point for testing if the file is run on it's own.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    createdb(conn)
    conn.close

if __name__ == "__main__":
    main()