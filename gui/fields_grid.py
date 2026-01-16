"""
Fields grid widget, this needs to be in another file to widgets.py to avoid a circular import with DFrame and the field classes.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime as dt

from core.constants import READ_WRITE as RW
from gui.widgets import DFrame
import gui.fields as f



class FieldsGrid(DFrame):
    """A frame allowing the editing of a list of various types

    """

    TYPE_CLASSES = { # Mapping of sqlite type strings to their corresponding display classes
            "TEXT" : f.Text,
            "NUMBER" : f.Text, # TODO
            "INTEGER" : f.Text, # TODO
            "DATE" : f.Text, # TODO
            "BLOB" : f.Text, # TODO
        }

    PY_TYPE_CLASSES = { # Mapping of python types to display classes
            str : f.Text,
            float : f.Text, # TODO
            int : f.Text, # TODO
            dt.date : f.Text, # TODO
            bool : f.Text, # TODO TODO CANGE TO blob
        }
    
    # TODO Maybe map the sql types to their python types, then python types to subclasses instead
    # TODO Add a "lock" system that locks one feild to the value of another until it's unlocked, eg Name and PreferredName stay the same by default

    def __init__(self, parent, mode:RW|list = "read", updated_call = None):
        super().__init__(parent)

        self.__labels:list = [] # Private, list of column name label widgets
        self.__widgets:list = [] # Private, list of value/feild __widgets
        self.__values:list # Private, keeps track of the values, updated when feilds are updated
        self.__call_when_updated = updated_call # Private, callable called when any feild is updated, (index, value)

        self.columnconfigure(index=1,pad=5)
    
    def set_feilds(self, feild_types, feild_defaults, feild_names):
        """Sets the feilds and sets them to defaults"""
        print("Feildname: Feilds are being set to", feild_names, feild_defaults, feild_types)
        assert len(feild_defaults) == len(feild_types)

        # Ungrid all existing items in widgets and labels
        for i in range(len(self.__labels)):
            self.__labels[i].grid_forget()
            self.__widgets[i].grid_forget()
        self.__labels.clear()
        self.__widgets.clear()


        self.__values = feild_defaults # Sent values list to defaults
        for i in range(len(feild_defaults)): # Iterate over each column
            
            # Column name label
            tk.Label(self, text=feild_names[i]).grid(row=i, column=0, sticky="w")

            # Create a pointer to the read/write widget matching the field type
            pointer_to_class = FieldsGrid.TYPE_CLASSES[feild_types[i]] # TODO To others except text

            type_class_instance = pointer_to_class(self, i, updated_call=self.__value_written_to, value=feild_defaults[i])
            self.__widgets.append(type_class_instance)
            self.__widgets[i].grid(row=i, column=1, sticky="w")
        
        # TODO Possibly in the future don't remove all widgets and replace them but change the existing ones and delete/add extras.

    def __value_written_to(self, index):
        value = self.__widgets[index].get_value()
        #self.__values[index] = value

        if not self.__call_when_updated:
            return
        self.__call_when_updated(index, value)

    def set_mode(self, mode:RW|list):
        """
        Sets the read/write mode of the widgets, either by accepting a mask list of read/write/None or a str literal.
        This must be called to actually display the value widgets
        """
        if mode is list:
            assert len(mode) == len(self.__widgets)

            # Apply the modes in the list to each widget
            for i in range(len(mode)):
                if mode[i] in ("read", "write"): # Only change if the mode is read or write
                    self.__widgets[i].mode(mode[i])
                else:
                    print("Mode is not read or write", mode)
                    raise
        
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
        return list(wid.get_value() for wid in self.__widgets)
        return self.__values
    
    def set_values(self, values:list):

        if not len(self.__widgets) == len(values):
            print("Length is not the same", values)
            for item in self.__widgets:
                print(item)
            raise

        for i in range(len(self.__widgets)):
            self.__widgets[i].set_value(values[i])
