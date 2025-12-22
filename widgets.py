import tkinter as tk
from tkinter import ttk

from numpy.random import choice as nprc

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

class VCombobox(ttk.Combobox):
    """
    Slightly more advanced Combobox which can display multiple lists of things
    """
    def __init__(self, 
            parent, 
            on_select:callable = None, 
            values:list=[list], # List containing two lists, one of pks, one of other str values
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

        print("I am being created!")

        super().__init__(parent, values=None, **kwargs)

        self.update_list(self.__pk_list, self.__value_list)

        if on_select:
            self.bind("<<ComboboxSelected>>", self.__value_selected)

    def __value_selected(self, val):
        """Called when a value is selected by the user from the list"""
        print("The value given was", val)
        if self.current() == -1: 
            raise # TODO Maybe return not raise
        self.__index = self.current()

        self.__on_select((self.__index, self.__pk_list[self.__index]))


    def update_list(self, pks:list, values:list[str], default_index:int = 0):
        """Update the contents of the list"""
        
        print(pks)
        if self.__use_value_pairs:
            self.__raw_list = list((pks[i] + " - " + values[i]) for i in range(len(pks)))
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
    def index(self):
        return self.__index

    @index.setter
    def index(self, val:int):
        self.__set_index(val)



