import tkinter as tk
from tkinter import ttk
from typing import Literal
#import typing
from datetime import datetime as dt

from constants import READ_WRITE as RW
from widgets import DFrame, VCombobox
import table_viewers as TableViewers
import record_viewers as RecordViewer

class RecordViewer(DFrame):
    """A frame which allows viewing of an sqlite table.
    `tablename` The name of the table to be viewed
    `parent` The parent of the frame
    `exe` Function which is called to query the database `(sql,*args)`

    """
    def __init__(self, owner, parent, tablename):
        super().__init__(parent)
        self.owner = owner # Public, Pointer to this instance's owner
        self.__table:str = tablename # Private, The name of the current table 
        #self.__sm = sm # Private, Pointer to SQLManager class

        # Initialising subframes, private
        self.__records = DFrame(self)
        self.__viewer = DFrame(self)
        self.__records.pack(side="left", expand=True, fill="both")#grid(column=0, row=0, padx=10, pady=10, sticky="nesw")
        self.__viewer.pack(side="right", expand=True, fill="both")#grid(column=1, row=0, padx=10, pady=10, sticky="nesw")
        
        # -- Table viewer
        self.__table_view = TableViewers.TreeTableViewer(self.__records, self.records_selected) # Todo generalise to different table viewers
        self.__table_view.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # -- Record viewer
        self.__record_view = RecordViewers.DefaultRecordViewer(self.__viewer)
        self.__record_view.pack()

        self.set_table(tablename)

    def records_selected(self, value):
        """
        Called when a record is selected in the table
        """
        self.__no_record_text.pack_forget()
        print("A record has been selected,", value)
        self.set_record(value)
    

    def set_table(self, new_table:str):
        """
        Changes the table being viewed
        """
        if not new_table.strip():
            # TODO Error message
            print("No tabel")
            return
        
        # TODO Validate that the table exists

        self.__table = new_table # Change table variable

        # Update the table view
        headings_raw:list[str] = list(head_sch[1] for head_sch in self.owner.sm.schema[self.__table])
        self.__table_view.set_table(
                table = self.__table,
                headings = headings_raw,
                headingsdisplay = list(h.capitalize() for h in headings_raw),
                table_data = self.owner.sm.read_full(self.__table)
        
        # Upadate the record view


        )


    def set_record(self, record_name:str):
        # Update record viewer

        try: # Delete the feilds frame (ignore if it doesn't exist yet)
            self.__feilds_frame.pack_forget()
            del self.__feilds_frame
        except: pass

        try: # Delete foreigns_frame (ignore if it doesnt exist)
            self.__foreigns_frame.pack_forget()
            del self.__foreigns_frame
        except: pass
        
        # TODO It needs to make a new feilds_frame when the table changes
        #self.__feilds_frame = FeildsGrid(self, self.__feilds_img_grid, self.owner.sm, self.__table, pk=self.owner.config.pk_defaults[self.__table], pk_column_name=record_name)
        #self.__feilds_frame.pack(side="top", fill="both", expand=True)

        if False:
            pass # Pack the image to self.__feilds_img_grid, only if the table has an image

        self.__foreigns_frame = DFrame(self)
        self.__foreigns_frame.pack(fill="both", expand=True)

        tk.Button(self.__foreigns_frame).pack() # TODO Placeholder

    def get_table(self):
        return self.__table

class FKCreator(): # 
    """
    Frame which displays a list of feilds, 
    """
    def __init__(self, 
                 columns, 
                 on_confirm, # Function which is called when the thingy is accepted.
    ):...
