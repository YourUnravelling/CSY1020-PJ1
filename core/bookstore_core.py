'''
Core functions of the bookstore app, as well as some helper functions
'''

# Lib imports
import os
import sqlite3 as sqlite
import datetime as dt
import pickle as pik
from pathlib import Path

#Class imports
from core.SQLManager import SQLManager

from config import config as configuration

VERSION:str = "Generalised RMS Development"

DEFAULT_PATH:Path = Path("database.sqlite")

base_path:Path = DEFAULT_PATH
sm = SQLManager(base_path)
config = configuration.c

def rangecalc(value:int|float, max:int|float|None=None, min:int|float|None=None) -> bool:
    """
    Helper function, returns True if `value` is between `max` and `min`
    Max and min can be null to have no limit.
    """
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

def sanitise_string(string):
    """Returns false if the string is invalid, otherwise sanitises it and returns"""

def sanitise_date(date_string, form):
    
    try:
        date = dt.datetime.strptime(date_string, form)
        return date
    except:
        return False

def get_setting(setting:str|None=None):
    """
    Returns the value of a specified `setting`
    Leave `setting` blank to return the whole settings dictionary
    """
    settings_dict:dict = pik.load(open("settings.pk","rb"))

    if setting:
        if setting in settings_dict:
            return settings_dict[setting]
        else:
            raise
    else:
        return settings_dict

def add_book(
        ISBN:str|None,
        author:str|None=None,
        title:str|None=None,
        date_published:dt.date|None=None,
        genre:str|None=None,
        price:float|None=None
        ):
    sm.add("book",{
            "isbn": ISBN,
            "author": author,
            "title": title,
            "date_published": date_published,
            "genre": genre,
            "price": price,
    })

#add_book("3232", "me", "title", dt.datetime.strptime("05/05/2005",r"%d/%m/%Y"), "bad genre", 5000.0)