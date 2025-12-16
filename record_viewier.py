import tkinter as tk
from tkinter import ttk
from numpy.random import choice as nprc
from typing import Literal
from constants import READ_WRITE as RW

class DFrame(tk.Frame):
    DEBUG_MODE = True
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        if DFrame.DEBUG_MODE:
            self.config(background="#" + (self.__randhex() + self.__randhex()) * 3)
        
    def __randhex(self) -> str:
        return nprc(list("ABCDEF"))#"0123456789ABCDEF"))

class RWController(DFrame):
    """
    A frame which has its w/r changed by mode()
    """
    def __init__(self, initial_mode: RW = "read"):
        super.__init__()
        self._mode:RW = initial_mode # Protected
        self._value = None
    
    def mode(self, mod:RW):
        """
        Changes the mode to read or write
        """
        if mode in ["read", "write"]:
            self._mode = mode
        else: raise
        if mode == "read":
            _read()
        elif mode == "write":
            _write()

    def set_value(value):
        """Sets the value both in the read widget and write widget
        Should be overwritten by children"""
        raise

    def _read():
        """
        This method should be overwritten by children"""
        pass

    def _write():
        """This method should be overwritten by children"""
        pass


class Text(RWController):
    """
    Viewer for the TEXT type, used in FeildsGrid
    """
    def __init__(self, initial_mode:RW="read", value = ""):
        DFrame.__init__(self)
        RWController.__init__(self, initial_mode=initial_mode)
        self.set_value(value)

        self.__readbox = ttk.Label(self, text=value)
        self.__writebox = ttk.Entry(self)
        self.set_value(value)

    def _read():
        self.__writebox.pack()
        self.__readbox.pack_forget()

    def _write():
        self.__readbox.pack()
        self.__writebox.pack_forget()

    def get_value():
        return self.__label.text

    def set_value(val):
        self.__label = ttk.Label(self, text=str(val))
        self.__writebox
        self.__writebox.insert(value)


class FeildsGrid(DFrame):
    """A frame containing all feilds of a record
    `parent` The parent widget
    `tablename` The table's name in the sql
    `key` The primary key of the column
    `schema` (Remove)
    `writemode` True if the frame should allow writing to the table.
    ADD `require_apply` If true, the changes are not applied until the apply() method is called.
    """
    def __init__(self, parent, tablename, key, schema, writing=False):
        super().__init__(parent)

        self.__read_widgets:list = []
        self.__write_widgets:list = []
        self.__writing:bool = writing # TODO Decide if this should even be a param, TODO decide if this should be "editing" and "viewing" instead

        names = schema[0]
        types = schema[1]

        for i in range(len(schema[0])):
            tk.Label(self, text=names[i]).grid(row=i, column=0, sticky="w")

            # Read widgets
            self.__read_widgets.append(tk.Label(self, text="VAL"))

            if types[i] == "INTEGER":
                widget = tk.Spinbox(self)
            elif types[i] == "TEXT":
                widget = tk.Entry(self)
            elif types[i] == "BOOL":
                widget = tk.Checkbutton(self)
            self.__write_widgets.append(widget)

        if writing:
            self.write()
        else:
            self.read()
    
    def read(self):
        for i,widget in enumerate(self.__write_widgets):
            widget.grid_forget()
        for i,widget in enumerate(self.__read_widgets):
            widget.grid(row=i,column=1, sticky="nsew")
        self.__writing = False
            

    def write(self):
        for i,widget in enumerate(self.__read_widgets):
            widget.grid_forget()
        for i,widget in enumerate(self.__write_widgets):
            widget.grid(row=i,column=1, sticky="nsew")
        self.__writing = True

    
    @property 
    def writing(self):
        return self.__writing
    
    @writing.setter
    def writing(self, val):
        self.__writing = val
        if val:
            self.write()
        else:
            self.read()

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

        ANIMAL_TABLE = ANIMAL_TABLE = [["id","name", "Test bool", "Bool 2"],["INTEGER","TEXT", "BOOL", "BOOL"]]# TODO remove
        names = ANIMAL_TABLE[0]
        types = ANIMAL_TABLE[1]

        self.__meta_bar = DFrame(self) # Highest bar, for the controls
        self.__meta_bar.pack(fill="x")
        self.__meta_bar.columnconfigure(1, weight=2)
        
        self.__meta_feild_selector = ttk.Combobox(self.__meta_bar, values=names, state="readonly")
        self.__meta_feild_selector.grid(row=0, column=0)
        
        self.__record_selector = ttk.Combobox(self.__meta_bar)
        self.__record_selector.grid(row=1, column=0)

        self.__rename = ttk.Button(self.__meta_bar, text="Rename")
        self.__delete = ttk.Button(self.__meta_bar, text="Delete")
        for i, item in enumerate([self.__rename, self.__delete]):
            item.grid(row=1, column=2+i)

        self.__feilds_img_grid = DFrame(self)
        self.__feilds_img_grid.pack()

        self.__feilds_frame = FeildsGrid(self.__feilds_img_grid,"animal", 0, ANIMAL_TABLE, writing=True)
        self.__feilds_frame.pack(side="left", fill="both", expand=True)

        if False:
            pass # Pack the image to self.__feilds_img_grid, only if the table has an image
        self.__foreigns_frame = DFrame(self)
        self.__foreigns_frame.pack(fill="both", expand=True)
        tk.Button(self.__foreigns_frame).pack()

    
    def display_new_record(self, id):
        """
        Displays a new record with the id as uid
        """