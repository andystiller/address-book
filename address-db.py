#!/usr/bin/env python3

import sqlite3

def createdb(curs):
    """
    Function to create the blank tables in the dabase.
    curs is a cursor in a Sqlite database
    """

    #Create Address table
    curs.execute('''CREATE TABLE address
             (first text, 
             last text, 
             phone text, 
             email text,
             address text
             )''')