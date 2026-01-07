import tkinter as tk
from tkinter import ttk

from gui.widgets import DFrame
from core.constants import READ_WRITE as RW



class BaseField(DFrame):
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


class Text(BaseField):
    """
    Viewer for the TEXT type, used in FieldsGrid
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

