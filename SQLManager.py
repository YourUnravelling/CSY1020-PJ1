import sqlite3 as sqlite
from pathlib import Path

class SQLManager():
    """
    Creates an object which can execute sql on an sqlite file.
    """
    def __init__(self, file_path:str) -> None:
        self.__path = Path(file_path) # Private - Convert given path to a pathlib object

    def exe(self, sql, args=()):
        """
        Executes sql on the database at `__path`
        """
        try:
            with sqlite.connect(self.__path) as conn:
                cur = conn.cursor() # Create cursor object
                print(sql, args)
                cur.execute(sql, args) # Execute on cursor object
                # TODO change
        except sqlite.IntegrityError as error:
            print(cur.fetchone())
            return error
    
    def add(self, table:str, values:dict):
        """Helper function to add a record to a table"""
        
        formatted = self.format_dict_as_sql(values)
        self.exe(f"INSERT INTO book VALUES({formatted[0]})", formatted[1])

    def delete(self, table:str, pk_row:str, pk_value_to_remove):
        """Helper function to delete a record."""
        self.exe(f"DELETE FROM {table} WHERE ({pk_row}={pk_value_to_remove})")
    
    def update(self, table:str, values:dict) -> None:
        """Helper function to ammend a record"""
        
        formatted = self.format_dict_as_sql(values)
        self.exe(f"UPDATE {table} SET ")


    def format_dict_as_sql(self, inp:dict):
        """Returns a string of keys and ?s seperated by colons, seperated by commas, and a corresponding list of the values"""
        values = []
        formatted_string = ""
        for key in inp:
            formatted_string = formatted_string + "?, "
            values.append(inp[key])
        formatted_string = formatted_string[0: len(formatted_string) - 2] # Remove last comma # TODO replace with join()
        return formatted_string, tuple(values)

    @property
    # Path getter
    def path(self):
        return self.__path

    @path.setter # Path setter
    def path(self, file_path):
        self.__path = Path(file_path)