import tkinter as tk
from tkinter import ttk
from typing import Literal

from constants import READ_WRITE as RW
from widgets import DFrame, VCombobox
import table_viewers as TableViewers

class BaseFeild(DFrame):
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
        if mode in RW:
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


class Text(BaseFeild):
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
    # TODO Make this generaliseable to settings and stuff
    TYPE_CLASSES = { # Mapping of sqlite type strings to their corresponding display classes
        "TEXT" : Text,
        "REAL" : Text, # TODO
        "INTEGER" : Text, # TODO
        "DATE" : Text, # TODO
        "BLOB" : Text, # TODO
    }

    def __init__(self, 
                 owner, # Pointer to this widget's owner
                 parent, # The parent widget
                 sm, # Instance of SQLManager class
                 table:str, 
                 pk:int|str = 0, 
                 pk_column_name:str = "id",
                 mode:RW="read"):
        super().__init__(parent)

        self.owner = owner
        self.__widgets:list = []
        self.__mode:RW = mode # TODO Decide if this should even be a param, TODO decide if this should be "editing" and "viewing" instead

        this_record = sm.read(table, pk, pk_column_name=pk_column_name)
        try:
            for i, column_tuple in enumerate(sm.schema[table]): # Iterate over each column
                print(column_tuple, i)
                tk.Label(self, text=column_tuple[1]).grid(row=i, column=0, sticky="w")

                # Read widgets
                pointer_to_class = FeildsGrid.TYPE_CLASSES["TEXT"]
                
                type_class_instance = pointer_to_class(self, initial_mode=mode, value=this_record[i])
                self.__widgets.append(type_class_instance)
                self.__widgets[i].grid(row=i, column=1, sticky="w")
        except: pass
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
    def __init__(self, owner, parent, tablename):
        super().__init__(parent)
        self.owner = owner # Public, Pointer to this instance's owner
        self.__table:str = tablename # Private, The name of the current table 
        #self.__sm = sm # Private, Pointer to SQLManager class

        # Initialising subframes, private
        self.__records = DFrame(self)
        self.__viewer = DFrame(self)
        self.__records.pack(side="left", expand=True, fill="both")#grid(column=0, row=0, padx=10, pady=10, sticky="nesw")
        self.__viewer.pack(side="right", expand=True, fill="both")#grid(column=1, row=0, padx=10, pady=10, sticky="nesw")
        
        # -- Table viewer
        self.__record_viewier = TableViewers.TreeTableViewer(self.__records) # Todo generalise
        self.__record_viewier.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # -- Record viewer

        # Private, Highest bar, for the controls
        self.__top_bar = DFrame(self.__viewer) 
        self.__top_bar.pack(anchor="n", fill="x", expand=False, padx=10, pady=10)
        #self.__top_bar.columnconfigure(1, weight=2)
        
        # Private
        self.__delete = ttk.Button(self.__top_bar, text="Delete")
        self.__delete.pack(side="right")#grid(row=1, column=3)

        self.__edit = ttk.Button(self.__top_bar, text="Edit")
        self.__edit.pack(side="right")

        self.__no_record_text = ttk.Label(self.__viewer, text="No record selected", justify="center")
        self.__no_record_text.pack(pady=50)

        # Private, Frame for the feilds and image if it's present
        self.__feilds_img_grid = DFrame(self.__viewer)
        self.__feilds_img_grid.pack()

        self.set_table(tablename)

    def record_selected(value):
        self.display_record[value[1]]
    
    def set_table(self, new_table:str):
        """
        Changes the table being viewed
        """
        if not new_table.strip():
            # TODO Error message
            print("No tabel")
            return
        
        # TODO Validate that the table exists

        self.__table = new_table # Change table variable

        #columns = list((col[1]) for col in (self.owner.sm.schema[self.__table]))
        #   self.__pk_selector.update_list(columns, columns, self.owner.config.pk_defaults[self.__table])
        
        # Set record selector
        #pk_list = list(self.owner.sm.exe(f"SELECT {self.owner.config.pk_defaults[self.__table]} FROM {self.__table}"))
        #values_list = list(self.owner.sm.exe(f"SELECT {self.__pk_selector.value} FROM {self.__table}"))

        headings_raw:list[str] = list(head_sch[1] for head_sch in self.owner.sm.schema[self.__table])
        self.__record_viewier.set_table(
                table = self.__table,
                headings = headings_raw,
                headingsdisplay = list(h.capitalize() for h in headings_raw),
                table_data = self.owner.sm.read_full(self.__table)
        )


    def set_record(self, record_name:str):
        # Update record viewer

        try: # Delete the feilds frame (ignore if it doesn't exist yet)
            self.__feilds_frame.pack_forget()
            del self.__feilds_frame
        except: pass

        try: # Delete foreigns_frame (ignore if it doesnt exist)
            self.__foreigns_frame.pack_forget()
            del self.__foreigns_frame
        except: pass
        
        # TODO It needs to make a new feilds_frame when the table changes
        self.__feilds_frame = FeildsGrid(self, self.__feilds_img_grid, self.__sm, self.__table, pk=self.__pk_selector.value, pk_column_name=self.__record_selector.get())
        self.__feilds_frame.pack(side="left", fill="both", expand=True)

        if False:
            pass # Pack the image to self.__feilds_img_grid, only if the table has an image

        self.__foreigns_frame = DFrame(self)
        self.__foreigns_frame.pack(fill="both", expand=True)

        tk.Button(self.__foreigns_frame).pack() # TODO Placeholder

    def get_table(self):
        return self.__table

    def display_record(self, id): # TODO remove handled itself I think
        """
        Displays a new record with the id as uid
        """