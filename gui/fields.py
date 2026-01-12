"""
Field classes for the FieldsGrid widget
If not specified it's write, otherwise read.
"""

import tkinter as tk
from tkinter import ttk

from gui.widgets import DFrame
from core.constants import READ_WRITE as RW



class BaseField(DFrame):
    """
    A frame which has its w/r changed by mode()
    """
    def __init__(self, parent, index:int, updated_call = None, initial_mode: RW = "read"):
        super().__init__(parent)
        self._mode:RW = initial_mode # Protected
        self._value = None
        print("Field is being created")
    
    def mode(self, mode:RW):
        """
        Changes the mode to read or write
        """
        if mode in list(RW):
            self._mode = mode
        
        if mode == "read":
            self._read()
        elif mode == "write":
            self._write()
        else: raise

    def get_value(self):
        return self._value
        
    def set_value(self, val) -> None:
        """Sets the value both in the read widget and write widget
        Should be overwritten by children"""
        raise NotImplementedError

    def _read(self) -> None:
        """This method should be overwritten by children"""
        raise NotImplementedError

    def _write(self) -> None:
        """This method should be overwritten by children"""
        raise NotImplementedError

    def _call_callable(self, *args):
        """
        Calls the specified callable with the index as param
        Ignores all args
        """
        print("call callable")
        if self._updated_call:
            self._updated_call(self._index)


class Text(BaseField):
    """
    Viewer for the TEXT type, used in FieldsGrid
    """
    def __init__(self, parent, index:int, updated_call = None, initial_mode:RW="read", value = "ERROR"):
        super().__init__(parent, index, initial_mode=initial_mode)

        self.__readbox = ttk.Label(self, text=value, width=20)
        self.__writebox_var = tk.StringVar()
        self.__writebox = ttk.Entry(self, width=20, textvariable=self.__writebox_var)#, validate="focusout", validatecommand=self._call_callable)
        #self.__writebox.bind("<<Modified>>", self._call_callable)
        self.__writebox_var.trace_add("write", self._call_callable)
        self._index = index
        self.set_value(value)
        self._updated_call = updated_call
        print("setting value to ", value)

    def __call_call_callable(self, *args):
        pass

    def _read(self): # TODO make this a single function with literal
        self.__writebox.pack_forget()
        self.__readbox.pack(pady=5)

    def _write(self):
        self.__readbox.pack_forget()
        self.__writebox.pack(pady=3)
    
    def get_value(self):
        return self.__writebox.get()

    def set_value(self, val):
        self.__readbox.config(text=str(val))
        self.__writebox.delete(0, tk.END)
        self.__writebox.insert(0, str(val))
