"""
Contains the SQLManager class
"""
import sqlite3 as sqlite
from pathlib import Path
from typing import Literal

class SQLManager():
    """
    An object which can execute sql on an sqlite file.
    """
    def __init__(self, file_path:Path|str) -> None:
        self.__path = Path(file_path) # Private - Convert given path to a pathlib object
        self.__schema = self.__generate_full_schema() # Private - Schema of the database

    def exe(self, sql:str, args:tuple|None=None, ret: Literal["one", "desc", "all"]="one"):
        """
        Executes sql on the database at `__path`, returns a tuple of the returned value and cur.description, or the error if an sql error occurs.
        """
        try:
            with sqlite.connect(self.__path) as conn:
                cur = conn.cursor() # Create cursor object
                
                try:
                    if args:
                        cur.execute(sql, args) # Execute on cursor object
                    else:
                        cur.execute(sql)
                    print("Executed:", sql, args)
                except Exception as e:
                    print(f"FAILED TO EXECUTE: {sql}, {args}", e)
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
    
    def add(self, table:str, values:dict|None = None):
        """Helper function to add a record to a table"""
        
        if values:
            formatted = self.format_dict_as_comma_list(values)
            self.exe(f"INSERT INTO {table} VALUES({formatted[0]})", formatted[1])
        else:
            self.exe(f"INSERT INTO {table} DEFAULT VALUES")

    def delete(self, table:str, id):
        """Helper function to delete a record."""
        primary_key = self.schema[table][0][1]
        self.exe(f"DELETE FROM {table} WHERE ({primary_key}=?)", (id,))
    
    def update(self, table:str, values:dict) -> None:
        """Helper function to ammend a record"""
        
        formatted = self.format_dict_as_comma_list(values)
        self.exe(f"UPDATE {table} SET ") # TODO

    def read(self, table:str, id, pk_column_name:str|None=None):
        """Helper function to read a record"""
        if not pk_column_name:
            pk_column_name = self.schema[table][0][1] # Set to first column TODO Change to config? but that'll be a circ import
        
        return self.exe(f"SELECT * FROM {table} WHERE {pk_column_name} == ?", (id,))

    def read_full(self, table:str, 
                filters:list[tuple[str, str|int|float, Literal["in", "is", "starts", "ends"]]]|None = None, # list[tuple[columnname:str, value:variant, ]]
                sort:tuple[str, bool]|None = None 
                ) -> list:
        """Returns a full list of records from a table"""

        sort_str:str = ""
        if sort:
            sort_str = f"ORDER BY {sort[0]} {["ASC", "DESC"][sort[1]]}"
        
        filt_str:str = ""
        filt_list = []
        if filters:
            filt_dict = {}

            for filt in filters:
                wildcards = { # TODO make param
                        "contains": ("%", "%"), 
                        "is": ("", ""),
                        "starts": ("", "%"),
                        "ends": ("%", ""),
                        }[filt[2]]

                column_to_filter = filt[0]
                filt_dict[filt[0]] = wildcards[0] + str(filt[1]) + wildcards[1]
            format_result = self.format_dict_as_key_comma_list(filt_dict, sep="LIKE")

            filt_str = "WHERE " + format_result[0]

            filt_list = format_result[1]#list(filt[1] for filt in filters)
        print("reading full", filt_str, filt_list)
        
        #if not filters: # If no filters are specified
            # Search
        #    return self.exe(f"SELECT * FROM {table} {sort_str}", filt_list, "all") # type: ignore


        return self.exe(f"SELECT * FROM {table} {filt_str}", (filt_list), "all") # type: ignore

    def write_record_list(self, table, pk, values:list|tuple):
        """Writes to a record specified by pk, with a list of values"""
        this_table_list_of_cols = list(self.schema[table][i][1] for i in range(len(self.schema[table])))
        
        assert len(this_table_list_of_cols) == len(values)

        colvals_dict:dict = dict()
        for i in range(len(values)):
            colvals_dict[this_table_list_of_cols[i]] = values[i]
        
        self.write_record_dict(table, pk, colvals_dict)

    def write_record_dict(self, table, pk, values:dict):
        formatted:tuple = self.format_dict_as_key_comma_list(values)
        # Create a tuple with all the values in dictionary order, then whatever the pk is at the end, and put it into function
        self.exe(f"UPDATE {table} SET {formatted[0]} WHERE {self.schema[table][0][1]} = ?", (formatted[1]+(pk,)))

    def write_field_index(self, table:str, record_pk, index:int, value):
        """
        Writes a single field in a record, field specified by an index
        """
        # Get field name at the index
        field = self.schema[table][index][1]

        self.write_field(table, record_pk, field, value)

    def write_field(self, table:str, record_pk, field:str, value):
        """
        Writes a single field in a record, field specified by field name
        """
        self.exe(f"UPDATE {table} SET {field} = ? WHERE {self.schema[table][0][1]} = ?", (value, record_pk))

    def format_dict_as_key_comma_list(self, inp:dict, sep="="):
        """Returns a string of keys and ?s seperated by equals, seperated by commas, and a corresponding list of the values"""
        values = []
        formatted_string = ""
        for key in inp:
            formatted_string = formatted_string + key + f" {sep} ?, "
            values.append(inp[key])
        formatted_string = formatted_string[0: len(formatted_string) - 2] # Remove last comma # TODO replace with join()
        return formatted_string, tuple(values)

    def format_dict_as_comma_list(self, inp:dict):
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