'''
Core functions of the bookstore app
Autumn Hickinbotham - 11/25
'''

# Lib imports
import os
import sqlite3 as sqlite
import datetime as dt

#Class imports
from SQLManager import SQLManager

DEFAULT_PATH:str = "bookstore.sqlite"
TABLE_SQLS:list[list[str]] = [
    ["book", "isbn TEXT PRIMARY KEY, author INTEGER, title TEXT, date_published DATE, genre TEXT, price NUMBER"],
    ["author", "id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, surname TEXT, nationality TEXT"],
    ["customer", "id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, surname TEXT, phone TEXT, email TEXT"],
    ["invoice", "id INTEGER PRIMARY KEY AUTOINCREMENT, customer INTEGER, book INTEGER"]
]

base_path:str = DEFAULT_PATH
sm = SQLManager(base_path)

def rangecalc(value:int|float, max:int|float|None=None, min:int|float|None=None) -> bool:
    if min:
        if value < min:
            return False
    if max:
        if value > max:
            return False
    return True

def validate_str(inp:str,maxlen:int = -1, minlen:int = -1):
    """Returns """

    if not rangecalc(len(inp),max=maxlen,min=minlen):
        return False
    
    return True

def validate_int(inp:str|int, max:int|None = None, min:int|None = None):
    """Returns true if the inputted integer is valid according to the parameters
    `inp` = 
    `max`, `min` = Inclusive
    """
    try:
        int_inp = int(inp)
    except:
        return False
    if not rangecalc(int_inp,max=max,min=min):
        return False
    
    return True

def sanitise_date(date_string, form):
    try:
        date = dt.strptime(date_string, form)
        return date
    except:
        return False

def initialise_database() -> None:
    """Creates the sqlite database if it doesn't already exist, also creates files"""

    for table_sql in TABLE_SQLS: # Iterate through the table constant to initialise the tables
        sm.exe(f"CREATE TABLE IF NOT EXISTS {table_sql[0]} ({table_sql[1]})")

def add_book(
        isbn:str|None,
        author:str|None=None,
        title:str|None=None,
        date_published:dt.date|None=None,
        genre:str|None=None,
        price:float|None=None
        ):
    dict = kwargs
    sm.exe(f"INSERT INTO {"book"}")


initialise_database()