"""
Custom widgets
"""

import tkinter as tk
from tkinter import ttk

#from datetime import datetime as dt
from numpy.random import choice as nprc

from core.constants import READ_WRITE as RW

from gui.core_resources import icons


class DFrame(tk.Frame):
    """
    Extension of tk.Frame with an optional debug mode, which highlights on mouseover, for easy debugging frame structure.
    """
    DEBUG_PRINT = False
    DEBUG_SHOW  = False
    def __init__(self, master=None, debug_name:str|None= None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.__debug_name = debug_name
        self.__normal_bg_color = self.cget("background")

        if DFrame.DEBUG_PRINT:
            #self.config(background="#" + (self.__randhex() + self.__randhex()) * 3)
            self.bind("<Button-1>", self.__print_info)
        if DFrame.DEBUG_SHOW:
            self.bind("<Enter>", self.__hover)
            self.bind("<Leave>", self.__unhover)
        
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
    
    def __hover(self, var):
        randc = ""
        for i in range(6):
            randc = randc + self.__randhex()
        self.config(background="#" + randc )#"#00ffdd")

    def __unhover(self, var):
        self.config(background=self.__normal_bg_color)

class BgButton(ttk.Button): # TODO delete?

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw) # type: ignore
        #self.config(background=master.)

class HideShowFrame(DFrame):
    """Frame with a title that can be shown and hidden"""

    def __init__(self, master=None, debug_name: str | None = None, label:str = "No label", cnf={}, **kw):
        super().__init__(master, debug_name, cnf, **kw)

        self.__hidden = False

        # Creating the title bar
        wide_label_frame = DFrame(self) # Private, Frame holding category name 
        wide_label_frame.pack(fill="x")
        label_frame = DFrame(wide_label_frame) # Private, Frame holding category name 
        label_frame.pack()
        self.__image_label = tk.Label(label_frame)
        self.__image_label.pack(side="left")
        self.__label = tk.Label(label_frame, text=label)
        self.__label.pack(side="right")

        for item in [wide_label_frame, label_frame, self.__image_label, self.__label]:
            item.bind("<Button-1>", self.__toggle)

        self.__content = DFrame(self) # Private, Frame containing the actual content

        self.__hide()
    
    def __toggle(self, ignore = None):
        if self.__hidden:
            self.__show()
        else:
            self.__hide()
    
    def __hide(self): 
        self.__hidden = True
        self.__image_label.config(image=icons["closed"])
        self.__content.pack_forget()

    def __show(self):
        self.__hidden = False
        self.__image_label.config(image=icons["open"])
        self.__content.pack(fill="x")
    
    @property
    def hidden(self):
        return self.__hidden
    
    @hidden.setter
    def hidden(self, hidden:bool):
        if hidden:
            self.__hide()
        else:
            self.__show()
        
    @property
    def label(self):
        return self.__label.cget("text")
    
    @label.setter
    def label(self, text:str):
        self.__label.config(text=text)
    
    @property
    def content(self):
        return self.__content

    

class TreeviewTable(ttk.Treeview):
    """
    A treeview that displays a table
    """
    WIDTH = 10
    MINWIDTH = 50

    def __init__(self, parent, on_select):
        ttk.Treeview.__init__(self, parent)
        self.__on_select = on_select
        self.__current_selected_iid = None
        self.__surpress_calls:int = 0


    def set_headings(self, table:str, headings:list[str], headingsdisplay:list[str]):
        
        self.delete(*self.get_children())

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

    def set_table_data(self, table_data:list[list], keep_selected_item:bool = True):
        # Make note of previously selected item
        prev_selected_item = self.__current_selected_iid

        # Delete all records in the treeview
        self.delete(*self.get_children())

        for i, record in enumerate(table_data):
            self.insert(
                    parent = "",
                    index = "end",
                    iid = record[0],
                    text = record[0], 
                    values = record[1:len(record)]
            )
        try:
            if keep_selected_item and prev_selected_item:
                self.selection_add([prev_selected_item])
                #self.__surpress_calls = 0
                # TODO Make sure the method is NOT called to not trigger the other panel again, ABOVE LINE DID NOT WORK
            else:
                # reset the selected value to null
                self.__current_selected_iid = None
        except: pass
    
    def __record_selected(self, event) -> None:
        """Calls __on_select with the top record selected"""
        selection = self.selection()

        if not selection:
            print("[TreeViewTable] No selection")
            return
        if self.__current_selected_iid == selection[0]:
            print("[TreeViewTable] Not called bause the selected object is the same ACTUALLY IT WAS CALLED WEEEEEHHHHHHHH")
            #return

        self.__current_selected_iid = selection[0]

        # Surpresses call and moves surpression ticker down one if so.
        # TODO currently not used if fixing the updating when saving thing doesnt work
        if self.__surpress_calls > 0:
            self.__surpress_calls -= 1
            return
        
        try:
            self.__on_select(self.__current_selected_iid)
        except: pass
    
    @property
    def current_selected_iid(self):
        return self.__current_selected_iid