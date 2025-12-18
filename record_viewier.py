import tkinter as tk
from tkinter import ttk
from numpy.random import choice as nprc
from typing import Literal
from constants import READ_WRITE as RW

class DFrame(tk.Frame):
    """
    Extension of tk.Frame with an optional debug mode, which randomises the colour within greyscale, for easy debugging frame structure.
    """
    DEBUG_MODE = True
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        if DFrame.DEBUG_MODE:
            self.config(background="#" + (self.__randhex() + self.__randhex()) * 3)
        
    def __randhex(self) -> str:
        """
        Returns a random hex digit between A and F
        """
        return nprc(list("ABCDEF"))

class RWController(DFrame):
    """
    A frame which has its w/r changed by mode()
    """
    def __init__(self, parent, initial_mode: RW = "read"):
        super().__init__(parent)
        self._mode:RW = initial_mode # Protected
        self._value = None
    
    def mode(self, mode:RW):
        """
        Changes the mode to read or write
        """
        if mode in ["read", "write"]:
            self._mode = mode
        else: raise
        if mode == "read":
            self._read()
        elif mode == "write":
            self._write()

    def get_value(self):
        return self._value
        
    def set_value(self, val) -> None:
        """Sets the value both in the read widget and write widget
        Should be overwritten by children"""
        raise NotImplementedError

    def _read(self) -> None:
        """
        This method should be overwritten by children"""
        raise NotImplementedError

    def _write(self) -> None:
        """This method should be overwritten by children"""
        raise NotImplementedError


class Text(RWController):
    """
    Viewer for the TEXT type, used in FeildsGrid
    """
    def __init__(self, parent, initial_mode:RW="read", value = "ERROR"):
        super().__init__(parent, initial_mode=initial_mode)

        self.__readbox = ttk.Label(self, text=value)
        self.__writebox = ttk.Entry(self)
        self.set_value(value)

    def _read(self): # TODO make this a single function with literal
        self.__writebox.pack_forget()
        self.__readbox.pack()

    def _write(self):
        self.__readbox.pack_forget()
        self.__writebox.pack()
    
    def set_value(self, val):
        self.__readbox.config(text=str(val))
        self.__writebox.delete(0, tk.END)
        self.__writebox.insert(0, str(val))


class FeildsGrid(DFrame):
    """A frame containing all feilds of a record
    `parent` The parent widget
    `tablename` The table's name in the sql
    `key` The primary key of the column
    `schema` (Remove)
    `writemode` True if the frame should allow writing to the table.
    ADD `require_apply` If true, the changes are not applied until the apply() method is called.
    """
    TYPE_CLASSES = { # Mapping of sqlite type strings to their corresponding display classes
        "TEXT" : Text,
        "REAL" : Text, # TODO
        "INTEGER" : Text, # TODO
        "DATE" : Text, # TODO
        "BLOB" : Text, # TODO
    }

    def __init__(self, 
                 parent, # The parent widget
                 sm, # Instance of SQLManager class
                 table:str, 
                 pk:int|str = 0, 
                 pk_column_name:str = "id",
                 mode:RW="read"):
        super().__init__(parent)

        self.__widgets:list = []
        self.__mode:RW = mode # TODO Decide if this should even be a param, TODO decide if this should be "editing" and "viewing" instead

        this_record = sm.read

        for i, column_tuple in enumerate(sm.schema): # Iterate over each column
            print(column_tuple, i)
            tk.Label(self, text=column_tuple[1]).grid(row=i, column=0, sticky="w")

            # Read widgets
            pointer_to_class = FeildsGrid.TYPE_CLASSES["TEXT"]
            
            type_class_instance = pointer_to_class(self, initial_mode=mode, value=sm.read(table, pk, pk_column_name)) # TODO add pk_column_name
            self.__widgets.append(type_class_instance)
            self.__widgets[i].grid(row=i, column=1, sticky="w")

        self.set_mode(mode)
    
    def set_mode(self, mode:RW):
        for widget in self.__widgets:
            widget.mode(mode)
        self.__mode = mode
        
    @property 
    def mode(self):
        return self.__mode

class RecordViewer(DFrame):
    """A frame which allows viewing of an sqlite table.
    `tablename` The name of the table to be viewed
    `parent` The parent of the frame
    `exe` Function which is called to query the database `(sql,*args)`

    """
    def __init__(self, tablename, parent, sm):
        super().__init__(parent)
        self.current_table:str = tablename # Public, The name of the table 
        self.__parent = parent # Private
        self.__sm = sm # Private | Pointer to SQLManager class

        self.__meta_bar = DFrame(self) # Highest bar, for the controls
        self.__meta_bar.pack(fill="x")
        self.__meta_bar.columnconfigure(1, weight=2)
        
        self.__meta_feild_selector = ttk.Combobox(self.__meta_bar, values=list((col[1]) for col in (self.__sm.schema[self.current_table])), state="readonly", ) # type: ignore
        self.__meta_feild_selector.bind('<<ComboboxSelected>>', lambda e: self.display_new_table(), False) # Why the hell does adding and e fix the overload problem
        self.__meta_feild_selector.grid(row=0, column=0)

        
        self.__record_selector = ttk.Combobox(self.__meta_bar)
        self.__record_selector.grid(row=1, column=0)

        self.__rename = ttk.Button(self.__meta_bar, text="Rename")
        self.__delete = ttk.Button(self.__meta_bar, text="Delete")
        for i, item in enumerate([self.__rename, self.__delete]):
            item.grid(row=1, column=2+i)

        self.__feilds_img_grid = DFrame(self)
        self.__feilds_img_grid.pack()

        self.display_new_table()

        if False:
            pass # Pack the image to self.__feilds_img_grid, only if the table has an image
        self.__foreigns_frame = DFrame(self)
        self.__foreigns_frame.pack(fill="both", expand=True)
        tk.Button(self.__foreigns_frame).pack()

    
    def display_new_table(self):
        try:
            self.__feilds_frame.pack_forget()
            del self.__feilds_frame
        except:
            pass
        # TODO It needs to make a new feilds_frame when the table changes
        self.__feilds_frame = FeildsGrid(self.__feilds_img_grid, self.__sm, self.current_table, pk=self.__meta_feild_selector.get(), pk_column_name=self.__record_selector.get())
        self.__feilds_frame.pack(side="left", fill="both", expand=True)

    def display_new_record(self, id):
        """
        Displays a new record with the id as uid
        """