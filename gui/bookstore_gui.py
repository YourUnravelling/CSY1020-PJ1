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
#from record_viewier import RecordViewer
#from resources import config as configuration
from gui.widgets import DFrame, DoubleCombobox
from gui import panels

class MainLayout(DFrame):
    """
    TODO
    """
    def __init__(self, master, core) -> None:
        super().__init__(master)
        self.__core = core # Private, pointer to core
        self.__panels:dict = {}

        self.__sidebar = DFrame(self, "sidebar")
        self.__sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.__topbar = DFrame(self, "top bar")
        self.__topbar.pack(fill="x", padx=5, pady=5)
        self.__right_sidebar = DFrame(self, "sidebar")
        self.__right_sidebar.pack(side="right", fill="y")
        self.__content = DFrame(self, "content")
        self.__content.pack(expand=True, fill="both")

        self.__sidebar_image = tk.PhotoImage(file="resources/sidebar_image.png")
        tk.Label(self.__sidebar, text="test", image=self.__sidebar_image).pack()


        self.__panels["table_select"] = panels.TableSelectButtons(self.__sidebar, self.update_panels)
        self.__panels["table_select"].pack(side="right", expand=True, fill="y")

        self.__panels["record_select"] = panels.RecordSelectTree(self.__content, self.update_panels)
        self.__panels["record_select"].pack(side="top", fill="both", expand=True)

        self.__record = panels.RecordScroll(self.__right_sidebar, self.update_panels)
        self.__record.pack(side="right", fill="y", expand=True)





        self.__panels["table_select"].add_bind(self.__panels["record_select"].set_object)
        self.__panels["record_select"].add_bind(self.__record.set_object)

        self.__panels["table_select"].set_object(object={}, force=True)
    
    def update_panels(self, updated_object:dict, caller):
        for key in self.__panels:
            self.__panels[key].signal_updated_object(updated_object, caller)


    @property
    def core(self):
        return self.__core

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
w.minsize(width=1100, height=500)

#DBViewer(w, core).pack()
MainLayout(w, core).pack(expand=True, fill="both")

def main():
    w.mainloop()