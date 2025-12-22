'''
GUI for the bookstore app
Autumn Hickinbotham - 12/25
'''

# Lib imports
import bookstore_core as core
import sys
import tkinter as tk
from tkinter import ttk

# Class imports
from scrollable_external import ScrollFrame
from record_viewier import RecordViewer
from resources import config as configuration
from widgets import DFrame, VCombobox

ANIMAL_TABLE = [["id","name", "Test bool", "Bool 2"],["INTEGER","TEXT", "BOOL", "BOOL"]] # TODO remove

class ThemeManager():
    all_widgets:list

    def __init__(self, mode):
        self.__mode = mode
        ThemeManager.all_widgets.append(self)
    
    @property
    def mode(self):
        return self.__mode

class ScrollFrameOld(tk.Canvas): # TODO delet/move to own file
    def __init__(self, master):
        super().__init__(master=master)
        self.__scrollbar = ttk.Scrollbar(self)
        self.__scrollbar.pack(side="right")

    @property # scrollbar getter
    def scrollbar(self):
        return self.__scrollbar
    # No setter as scrollbar shouldn't be changed

class EntryView(DFrame):
    def __init__(self, parent, sql_manager, config):
        super().__init__(parent)
        self.__parent = parent # Private, TODO maybe delete
        self.__sm = sql_manager # Private, Pointer to an SQLManager instance which executes sql

        self.__topbar = DFrame(self)
        self.__topbar.pack(fill="x", padx=5, pady=5)
        self.__content = DFrame(self)
        self.__content.pack(expand=True, fill="both")

        self.__table_selector = VCombobox(self.__topbar, state="normal", values=list(table for table in self.__sm.schema))#["Books", "Customers", "Authors", "Invoices"])
        self.__table_selector.pack(side=tk.LEFT)
        self.__table_selector.insert(0, config.default_table)
        self.__table_selector.config(state="readonly") # TODO Make setting?

        self.__view_edit_button = tk.Button(self.__topbar, text="Viewing")
        self.__view_edit_button.pack(side="right")


        self.__sub_content = DFrame(self.__content, width=400)

        self.__sub_content.pack(fill="y", expand=True)
        self.__sub_content.pack_propagate(False) # Ensure correct size
        self.pack(fill="both", expand=True)

        self.__viewer = RecordViewer(self, "book", self.__sub_content, sm=self.__sm)
        self.__viewer.pack(fill="x",)

        # Bind update table command from the table selector combobox
        self.__table_selector.bind('<<ComboboxSelected>>', lambda e: self.__viewer.set_table(self.__table_selector.get()), False)


w = tk.Tk()
w.iconphoto(True,tk.PhotoImage(file="resources/icon.png"))
w.minsize(width=600, height=300)

EntryView(w, core.sm, config=configuration.c).pack()

def main():
    w.mainloop()

if __name__ == "__main__":
    main()
    sys.exit()