import sqlite3 as sqlite
from pathlib import Path
from typing import Literal

class SQLManager():
    """
    Creates an object which can execute sql on an sqlite file.
    """
    def __init__(self, file_path:Path|str) -> None:
        self.__path = Path(file_path) # Private - Convert given path to a pathlib object
        self.__schema = self.__generate_full_schema()

    def exe(self, sql:str, args:tuple=(), ret: Literal["one", "desc", "all"]="one"):
        """
        Executes sql on the database at `__path`, returns a tuple of the returned value and cur.description, or the error if an sql error occurs.
        """
        try:
            with sqlite.connect(self.__path) as conn:
                cur = conn.cursor() # Create cursor object
                print("Executing:", sql, args)
                try:
                    cur.execute(sql, args) # Execute on cursor object
                except Exception as e:
                    print(e)
                if ret == "one":
                    return cur.fetchone()
                elif ret == "all":
                    return cur.fetchall()
                elif ret == "desc":
                    return cur.description
                # TODO change
        except sqlite.IntegrityError as error:
            print("There has been an error:", error)
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
        self.exe(f"UPDATE {table} SET ") # TODO

    def read(self, table:str, id, pk_column_name:str="id"):
        """Helper function to read a record"""
        
        self.exe(f"SELECT * FROM {table} WHERE {pk_column_name} == \"{id}\"")

    def format_dict_as_sql(self, inp:dict):
        """Returns a string of keys and ?s seperated by colons, seperated by commas, and a corresponding list of the values"""
        values = []
        formatted_string = ""
        for key in inp:
            formatted_string = formatted_string + "?, "
            values.append(inp[key])
        formatted_string = formatted_string[0: len(formatted_string) - 2] # Remove last comma # TODO replace with join()
        return formatted_string, tuple(values)

    def __generate_full_schema(self) -> dict:
        """
        Returns the full schema of every table in a dictionary
        """
        table_list = self.exe("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';", ret="all")
        schema = {}
        for table_tup in table_list: # type: ignore | Iterate through table names
            table = table_tup[0]
            schema[table] = self.__generate_table_schema(table)
        
        return schema
    
    def __generate_table_schema(self, table) -> list: # TODO delete as a small function and no longer public?
        """
        Returns the schema for a specified `table`
        """
        return self.exe(f"PRAGMA table_info('{table}')", ret="all") # type: ignore


    @property
    # Path getter
    def path(self):
        return self.__path

    @path.setter # Path setter
    def path(self, file_path):
        self.__path = Path(file_path)

    @property # Schema getter
    def schema(self):
        return self.__schema