'''
Core functions of the bookstore app
Autumn Hickinbotham - 11/25
'''

import os
import sqlite3 as sqlite

DEFAULT_PATH:str = "bookstore.sqlite"

base_path:str = DEFAULT_PATH

def rangecalc(value:int|float,max:int|float|None=None,min:int|float|None=None) -> bool:
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


def initialise_database() -> void:
    """Creates the sqlite database if it doesn't already exist, also creates all existing files"""

    with conn() as c:
        c.execute("CREATE TABLE IF NOT EXISTS book")

    

def conn() -> sqlite.Connection:
    return sqlite.connect(base_path)

def exe(sql:str):
    """Executes sql in the database"""
    with conn() as c:
        cur = c.cursor
        cur.execute(sql)


initialise_database()