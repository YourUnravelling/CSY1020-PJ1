import sqlite3 as sqlite
from os import path

class SQLManager():
    """
    Creates an object which can execute sql on an sqlite file.
    """
    def __init__(self, file_path:str) -> None:
        self.__path = path.abspath(file_path) # Private - Convert given path to an absolute path

    def exe(self, sql, *args):
        with sqlite.connect(self.__path) as conn:
            cur = conn.cursor() # Create cursor object
            cur.execute(sql, *args) # Execute on cursor object
    
    @property
    # Path getter
    def path(self):
        return self.__path

    @path.setter # Path setter
    def path(self, file_path):
        self.__path = path.abspath(file_path)