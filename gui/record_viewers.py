"""Record viewer classes

Unlike the table_viewers, these frames aren't self contained and need to have a link to core
"""
import tkinter as tk
from tkinter import ttk

from gui.widgets import DFrame, FeildsGrid

class BaseRecordViewer():
    pass


class DefaultRecordViewer(DFrame):
    def __init__(self, parent, core):
        self.__core = core
        self.__table = ""

        super().__init__(parent, debug_name="Default record viewer")

        # Private, Highest bar, for the controls
        self.__top_bar = DFrame(self, debug_name="Top bar") 
        self.__top_bar.pack(anchor="n", fill="x", expand=False, padx=10, pady=10)
        #self.__top_bar.columnconfigure(1, weight=2)
        
        # Private
        self.__delete = ttk.Button(self.__top_bar, text="Delete")
        self.__delete.pack(side="right")#grid(row=1, column=3)

        self.__edit = ttk.Button(self.__top_bar, text="Edit")
        self.__edit.pack(side="right")

        # Frame for record info, possibly scrolling
        self.__record_frame = DFrame(self, debug_name="Record frame")
        self.__record_frame.pack()

        self.__no_record_text = ttk.Label(self.__record_frame, text="No record selected", justify="center")
        self.__no_record_text.pack(pady=50)



        # Private, Frame for the feilds and image if it's present
        self.__feilds_img_grid = DFrame(self.__record_frame, debug_name="Feilds img grid")
        self.__feilds_img_grid.pack()

        self.__feilds = FeildsGrid(self.__feilds_img_grid)
        self.__feilds.grid(column=0, row=0)

        # Image
        if False:
            pass

        self.__foreigns_frame = DFrame(self, debug_name="Foreigns frame")
        self.__foreigns_frame.pack()

    def set_table(self, table:str):
        """Sets the types of the feilds"""
        self.__table = table

        column_types = list(col[2] for col in self.__core.sm.schema[table])
        default_values = self.__core.config.default_values[table]
        column_names = list(col[0] for col in self.__core.sm.schema[table])

        self.__feilds.set_feilds(column_types, default_values, column_names)

    def set_record(self, pk:str):
        """Sets the current displayed record to pk"""

        record_values = self.__core.sm.read(self.__table, pk, "isbn") #TODO generalise isbn
        self.__feilds.set_values(record_values)