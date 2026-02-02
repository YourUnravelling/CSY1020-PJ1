'''
Main GUI/Layout file, mainloop
'''

# Lib imports
import core.bookstore_core as core
import sys
import tkinter as tk
from tkinter import ttk

# Class imports
from gui.widgets import DFrame, DoubleCombobox
from gui import panels
import gui.core_resources as cr

from config.config import c

class MainLayout(DFrame):
    """
    A mainlayout which has a table list, table view, and a fields grid.
    """
    # TODO Split this into a base class and a custom Layout class
    def __init__(self, master, core) -> None:
        super().__init__(master)
        self.__core = core # Private, pointer to core
        self.__panels:dict = {}



        self.__sidebar = DFrame(self, "sidebar")
        self.__sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.__sidebar_extra = DFrame(self.__sidebar, "sidebar extra")
        self.__sidebar_extra.pack(side=tk.BOTTOM, fill=tk.X, pady=3)
        self.__topbar = DFrame(self, "top bar")

        self.__right_sidebar = DFrame(self, "sidebar", width = 450)
        self.__right_sidebar.pack_propagate(False)
        self.__right_sidebar.pack(side="right", fill="y", ipadx=10, ipady=10)
        self.__content = DFrame(self, "content")
        self.__content.pack(expand=True, fill="both")

        self.__sidebar_image = tk.PhotoImage(file="resources/rms_fire.gif")
        tk.Label(self.__sidebar, text="test", image=self.__sidebar_image).pack()
        #tk.Label(self.__sidebar, text="Tables").pack()



        ttk.Label(self.__sidebar_extra, text=core.VERSION).pack(side="bottom",pady=3, padx=5)
        ttk.Button(self.__sidebar_extra, text="Log out", width=30, ).pack(side="bottom",pady=3, padx=5, ipady=3)
        ttk.Button(self.__sidebar_extra, text="Preferences", width=30, ).pack(side="bottom",pady=3, padx=5, ipady=3)

        self.__panels["table_select"] = panels.TableSelectButtons(self.__sidebar, self.update_panels)
        self.__panels["table_select"].pack(side="right", expand=True, fill="both")

        self.__panels["record_select"] = panels.RecordSelectTree(self.__content, self.update_panels)
        self.__panels["record_select"].pack(side="top", fill="both", expand=True)

        self.__record = panels.RecordScroll(self.__right_sidebar, self.update_panels)
        self.__record.pack(side="right", fill="y", expand=True)


        self.__panels["table_select"].add_bind(self.__panels["record_select"].set_object)
        self.__panels["record_select"].add_bind(self.__record.set_object)

        self.__panels["table_select"].set_object(object={}, force=True)
    
    def update_panels(self, updated_object:dict, caller_uid):
        print("[Layout] Updating all panels")
        for key in self.__panels:
            if not self.__panels[key].uid == caller_uid:
                self.__panels[key].signal_updated_object(updated_object, caller_uid)
            else:
                print("[MainLayout] A panel was not updated because it was the caller", caller_uid)


    @property
    def core(self):
        return self.__core

# Create window
w = tk.Tk()
w.iconphoto(True,tk.PhotoImage(file="resources/icon.png"))
w.minsize(width=1100, height=500)
w.title(c.window_name)

# Initialise the icons here because images need a window to be created
cr.initialise_icons()

MainLayout(w, core).pack(expand=True, fill="both")

def main():
    w.mainloop()