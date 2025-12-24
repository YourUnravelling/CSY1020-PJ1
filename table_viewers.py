"""Table viewer classes"""
import tkinter as tk
from tkinter import ttk

from widgets import DFrame

class BaseTableViewer():
    def __init__(self, parent):
        raise NotImplementedError

    def set_table(self, table:str):
        raise NotImplementedError


class TreeTableViewer(BaseTableViewer, ttk.Treeview):
    WIDTH = 5
    MINWIDTH = 5

    def __init__(self, parent):
        #BaseTableViewer.__init__(self, parent)
        ttk.Treeview.__init__(self, parent)

    def set_table(self, table:str, headings:list[str], headingsdisplay:list[str], table_data:list[list]):
        
        headings_no_pk = headings[1:len(headings)]
        headings_display_no_pk = headingsdisplay[1:len(headingsdisplay)]

        self.config(columns=headings_no_pk, height=5)
        
        self.heading("#0", text= headingsdisplay[0])
        self.column("#0", minwidth= TreeTableViewer.MINWIDTH, width= TreeTableViewer.WIDTH)
        for i, heading in enumerate(headings): # TODO
            if i == 0: continue
            self.heading(headings[i], text= headingsdisplay[i])
            self.column(headings[i], minwidth= TreeTableViewer.MINWIDTH, width= TreeTableViewer.WIDTH)

        print(table_data)
        for i, record in enumerate(table_data):
            self.insert(
                    parent = "",
                    index = "end",
                    iid = record[0],
                    text = record[0], 
                    values = record[1:len(record)])
