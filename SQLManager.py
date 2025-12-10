import sqlite3 as sqlite
from os import path

class SQLManager():
    """
    Creates an object which can execute sql on an sqlite file.
    """
    def __init__(self, file_path:str) -> None:
        self.__path = path.abspath(file_path) # Private - Convert given path to an absolute path

    def exe(self, sql, args=()):
        with sqlite.connect(self.__path) as conn:
            cur = conn.cursor() # Create cursor object
            cur.execute(sql, args) # Execute on cursor object
    
    def add_record(self, table:str, values:dict):
        """Helper function to add a record to a table"""
        
        formatted = self.format_dict_as_sql(values)
        self.exe(f"INSERT INTO book VALUES({formatted[0]})", formatted[1])

    def format_dict_as_sql(self, inp:dict):
        """Returns a string of keys and ?s seperated by colons, seperated by commas, and a corresponding list of the values"""
        values = []
        formatted_string = ""
        for key, value in inp.values():
            formatted_string = formatted_string + str(key) + ":?, "
            values.append(value)
        return formatted_string, tuple(values)

    @property
    # Path getter
    def path(self):
        return self.__path

    @path.setter # Path setter
    def path(self, file_path):
        self.__path = path.abspath(file_path)