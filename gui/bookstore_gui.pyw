'''
GUI for the bookstore app
Autumn Hickinbotham - 12/25
'''

# Lib imports
import core.bookstore_core as core
import sys
import tkinter as tk
from tkinter import ttk

# Class imports
from external.scrollable_external import ScrollFrame
from record_viewier import RecordViewer
#from resources import config as configuration
from widgets import DFrame, DoubleCombobox

ANIMAL_TABLE = [["id","name", "Test bool", "Bool 2"],["INTEGER","TEXT", "BOOL", "BOOL"]] # TODO remove

class DBViewer(DFrame):
    def __init__(self, parent, core):
        super().__init__(parent)
        self.__parent = parent # Private, TODO maybe delete
        self.__sm = core.sm # Private, Pointer to an SQLManager instance which executes sql
        self.__core = core
        self.__config = core.config

        self.__topbar = DFrame(self)
        self.__topbar.pack(fill="x", padx=5, pady=5)
        self.__content = DFrame(self)
        self.__content.pack(expand=True, fill="both")

        tables_list = list(table for table in self.__sm.schema)
        self.__table_selector = DoubleCombobox(self.__topbar, 
                state="normal", 
                on_select= self.__table_selected,
                raw= tables_list, 
                display= list(table.capitalize() for table in tables_list), 
                default= tables_list.index(self.__core.config.default_table),
                creation_call = True)

        self.__table_selector.pack(side=tk.LEFT)

        self.__view_edit_button = tk.Button(self.__topbar, text="Viewing")
        self.__view_edit_button.pack(side="right")

        self.pack(fill="both", expand=True)

        self.__viewer = RecordViewer(self, self.__content, "book")
        self.__viewer.pack(fill="both",expand=True)


    def set_table(self, table):
        """Sets the table"""
        self.__table_selected(table)

    def __table_selected(self, index, tablename):
        self.__viewer.set_table(tablename)

    @property
    def sm(self):
        return self.__sm
    
    @property
    def core(self):
        return self.__core


w = tk.Tk()
w.iconphoto(True,tk.PhotoImage(file="resources/icon.png"))
w.minsize(width=600, height=300)

DBViewer(w, core).pack()

def main():
    w.mainloop()

if __name__ == "__main__":
    main()
    sys.exit()