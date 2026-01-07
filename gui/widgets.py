import tkinter as tk
from tkinter import ttk

from datetime import datetime as dt
from numpy.random import choice as nprc

from core.constants import READ_WRITE as RW
import gui.fields as f

class DFrame(tk.Frame):
    """
    Extension of tk.Frame with an optional debug mode, which randomises the colour within greyscale, for easy debugging frame structure.
    """
    DEBUG_MODE = True
    def __init__(self, master=None, debug_name:str|None= None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.__debug_name = debug_name
        if DFrame.DEBUG_MODE:
            self.config(background="#" + (self.__randhex() + self.__randhex()) * 3)
            self.bind("<Button-1>", self.__print_info)
        
    def __randhex(self) -> str:
        """
        Returns a random hex digit between A and F
        """
        return nprc(list("ABCDEF"))

    def __print_info(self, var):
        if self.__debug_name:
            print("This frame is " + self.__debug_name, end=" | ")
        else:
            print("No debug name provided for this frame, location: " + str(self), end=" | ")
        print("Owner class is " + str(self.__class__.__name__))

class BgButton(ttk.Button): # To delete?

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw) # type: ignore
        #self.config(background=master.)

class ScrollFrameOld(tk.Canvas): # TODO delete
    def __init__(self, master):
        super().__init__(master=master)
        self.__scrollbar = ttk.Scrollbar(self)
        self.__scrollbar.pack(side="right")

    @property # scrollbar getter
    def scrollbar(self):
        return self.__scrollbar
    # No setter as scrollbar shouldn't be changed

class VCombobox(ttk.Combobox): # TODO Delete
    """
    Slightly more advanced Combobox which can display multiple lists of things
    """
    def __init__(self, 
            parent, 
            on_select:callable = None, 
            values:list= [[],[]], # List containing two lists, one of pks, one of other str values
            default_index:int = 0, # Default index
            use_value_pairs:bool = True,
            **kwargs
            ):
        self.__pk_list:list = values[0] # List of the pks
        self.__value_list:list = values[1]
        self.__index:int = default_index
        self.__on_select = on_select
        self.__raw_list:list[str] # (Set later)
        self.__use_value_pairs:bool = use_value_pairs # If true, only shows the values and not the pks in the list

        # TODO Change to primary and secondary values not pk and value lists?

        super().__init__(parent, values=None, **kwargs)

        self.update_list(self.__pk_list, self.__value_list)

        if on_select:
            self.bind("<<ComboboxSelected>>", self.__value_selected)

    def __value_selected(self, val):
        """Called when a value is selected by the user from the list"""
        if self.get().strip() == "":
            print("Value is null in combobox")
            return
        print("The value given was", val)
        if self.current() == -1: 
            raise # TODO Maybe return not raise
        self.__index = self.current()

        self.__on_select((self.__index, self.__pk_list[self.__index]))


    def update_list(self, pks:list, values:list[str], default_index:int = 0):
        """Update the contents of the list"""
        
        print(pks)
        if self.__use_value_pairs:
            self.__raw_list = list((pks[i] + " - " + str(values[i])) for i in range(len(pks)))
        else:
            self.__raw_list = list((values[i]) for i in range(len(pks)))
        self.config(values=self.__raw_list)
        self.__pk_list = pks
        self.__value_list = values


    def __set_index(self, val:int):
        
        # Save original state and set state to normal because it won't let me insert when it's readonly
        original_state = self.state
        self.config(state="normal")

        self.__index = val
        self.delete(0, tk.END)
        self.insert(0, self.__raw_list[val])

        # Return state to how it was
        self.config(state=original_state)


    @property
    def value(self):
        return self.__pk_list[self.current()]

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, val:int):
        self.__set_index(val)

class DoubleCombobox(ttk.Combobox):
    """Combobox which displays different values to the stored ones"""

    def __init__(self, 
                 master, 
                 raw:list[str] = [], 
                 display:list[str] = [], 
                 default:int = 0, 
                 creation_call:bool = False, 
                 on_select = None,
                 **kwargs
    ):
        self.display = display
        self.raw = raw
        self.__on_select = on_select
        super().__init__(master, values=display, **kwargs)

        if self.__on_select:
            self.bind("<<ComboboxSelected>>", self.__get_and_call)

        self.set_value(default, creation_call)

    def __get_and_call(self, something):
        index = self.current()
        self.__call_on_select(index, self.raw[index])

    def __call_on_select(self, index, value):
        """Calls the on_select function, only if it exists"""
        if self.__on_select:
            self.__on_select(index, value)

    # No @property because with_call is needed
    def set_value(self, index, with_call=False):
        """Sets the value to an index"""
        self.delete(0, tk.END)
        self.insert(0, self.display[index])
        if with_call:
            self.__call_on_select(index, self.raw[index])
    
    def get_value(self):
        return self.get()
    
    def get_index(self):
        return self.current()


class FieldsGrid(DFrame):
    """A frame allowing the editing of a list of various types

    """

    TYPE_CLASSES = { # Mapping of sqlite type strings to their corresponding display classes
            "TEXT" : Text,
            "NUMBER" : Text, # TODO
            "INTEGER" : Text, # TODO
            "DATE" : Text, # TODO
            "BLOB" : Text, # TODO
        }

    PY_TYPE_CLASSES = { # Mapping of python types to display classes
            str : Text,
            float : Text, # TODO
            int : Text, # TODO
            dt.date : Text, # TODO
            bool : Text, # TODO TODO CANGE TO blob
        }
    
    # TODO Maybe map the sql types to their python types, then python types to subclasses instead
    # TODO Add a "lock" system that locks one feild to the value of another until it's unlocked, eg Name and PreferredName stay the same by default

    def __init__(self, parent, mode:RW|list = "read"):
        super().__init__(parent)

        self.__labels:list = [] # Private, list of column name label widgets
        self.__widgets:list = [] # Private, list of value/feild __widgets
        self.__values:list # Private, keeps track of the values, updated when feilds are updated

        self.columnconfigure(index=1,pad=5)
    
    def set_feilds(self, feild_types, feild_defaults, feild_names):
        """Sets the feilds and sets them to defaults"""
        assert len(feild_defaults) == len(feild_types)

        # Ungrid all existing items in widgets and labels
        for i in range(len(self.__labels)):
            self.__labels[i].grid_forget()
            self.__widgets[i].grid_forget()


        self.__values = feild_defaults # Sent values list to defaults
        for i in range(len(feild_defaults)): # Iterate over each column
            
            # Column name label
            tk.Label(self, text=feild_names[i]).grid(row=i, column=0, sticky="w")

            # Create a pointer to the read/write widget matching the field type
            pointer_to_class = FeildsGrid.TYPE_CLASSES[feild_types[i]] # TODO To others except text

            type_class_instance = pointer_to_class(self, initial_mode="read", value=feild_defaults[i])
            self.__widgets.append(type_class_instance)
            self.__widgets[i].grid(row=i, column=1, sticky="w")
        
        # TODO Possibly in the future don't remove all widgets and replace them but change the existing ones and delete/add extras.

    def set_mode(self, mode:RW|list):
        """
        Sets the read/write mode of the widgets, either by accepting a mask list of read/write/None or a str literal.
        """

        if mode is list:
            assert len(mode) == len(self.__widgets)

            # Apply the modes in the list to each widget
            for i in range(len(mode)):
                if mode[i] in ("read", "write"): # Only change if the mode is read or write
                    self.__widgets[i].mode(mode[i])
        
        else: # If mode is a single str literal
            # Set each widget's mode to the value of the literal
            for widget in self.__widgets:
                widget.mode(mode)

        self.__mode = mode
         
    def value_updated(self, index, value):
        self.__values[index] = value

    def get_mode_at(self, index:int):
        """Gets the mode of a spesific widget at an index"""
        if self.__mode is list:
            return self.__mode[index]
        else:
            return self.__mode
    
    @property
    def values(self):
        return self.__values
    
    def set_values(self, values:list):
        for i in range(len(self.__widgets)):
            self.__widgets[i].set_value(values[i])


class TreeviewTable(ttk.Treeview):
    """
    A treeview that displays a table
    """
    WIDTH = 100
    MINWIDTH = 50

    def __init__(self, parent, on_select):
        #BaseTableViewer.__init__(self, parent)
        ttk.Treeview.__init__(self, parent)
        self.__on_select = on_select


    def set_table(self, table:str, headings:list[str], headingsdisplay:list[str], table_data:list[list]): # TODO Seperate into set_headings and set_data? 
        
        self.delete(*self.get_children())
        #ttk.Button(self, text="test").grid(column=1)

        headings_no_pk = headings[1:len(headings)]
        headings_display_no_pk = headingsdisplay[1:len(headingsdisplay)]

        self.config(columns=headings_no_pk, height=5)
        
        self.heading("#0", text= headingsdisplay[0])
        self.column("#0", minwidth= TreeviewTable.MINWIDTH, width= TreeviewTable.WIDTH)
        for i, heading in enumerate(headings): # TODO
            if i == 0: continue
            self.heading(headings[i], text= headingsdisplay[i])
            self.column(headings[i], minwidth= TreeviewTable.MINWIDTH, width= TreeviewTable.WIDTH)

        self.bind("<<TreeviewSelect>>", self.__record_selected)

        self.insert(parent="", index="end", iid="__null", text="null", values=[])
        for i, record in enumerate(table_data):
            self.insert(
                    parent = "",
                    index = "end",
                    iid = record[0],
                    text = record[0], 
                    values = record[1:len(record)]
            )

    def __record_selected(self, event) -> None:
        """Calls __on_select with the top record selected"""
        self.__on_select(self.selection()[0])