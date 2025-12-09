import sqlite3 as sqlite
from os import path

class SQLManager():
    """
    Creates an object which can execute sql on an sqlite file.
    """
    def __init__(self, file_path:str) -> None:
        self.__new_connection(file_path)

    def __new_connection(self, file_path):
        self.__close_connection()

        self.__path = path.abspath(file_path) # Private - Convert given path to an absolute path
        
        self.__connection = sqlite.connect(self.__path) # Private - Establish connection
        self.__cursor = self.__connection.cursor() # Private - Create cursor

    def __close_connection(self):
        try:
            self.__connection.close() # Make sure previous connection is closed
        except: # Ignore if there is no previous connection
            pass

    def exe(self, sql, *args):
        self.__cursor.execute(sql, *args)
    
    @property
    # Path getter
    def path(self):
        return self.__path

    @path.setter # Path setter
    def path(self, file_path):
        self.__new_connection(file_path)
    
    @path.deleter # Path deleter
    def path(self):
        self.__close_connection()
        del self.__connection

    @property
    # Cursor getter
    def cursor(self):
        return self.__cursor
    
    @cursor.setter # Cursor setter
    def cursor(self,val): # TODO Maybe delete this func
        self.__cursor = val

    # TODO add other getters and setters