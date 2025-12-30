"""Record viewer classes"""
import tkinter as tk
from tkinter import ttk

from widgets import DFrame

from record_viewier import FeildsGrid


class BaseRecordViewer():
    pass


class DefaultRecordViewer():
    def __init__(self):

        # Private, Highest bar, for the controls
        self.__top_bar = DFrame(self) 
        self.__top_bar.pack(anchor="n", fill="x", expand=False, padx=10, pady=10)
        #self.__top_bar.columnconfigure(1, weight=2)
        
        # Private
        self.__delete = ttk.Button(self.__top_bar, text="Delete")
        self.__delete.pack(side="right")#grid(row=1, column=3)

        self.__edit = ttk.Button(self.__top_bar, text="Edit")
        self.__edit.pack(side="right")

        # Frame for record info, possibly scrolling
        self.__record_frame = DFrame(self.__viewer)
        self.__record_frame.pack()

        self.__no_record_text = ttk.Label(self.__record_frame, text="No record selected", justify="center")
        self.__no_record_text.pack(pady=50)



        # Private, Frame for the feilds and image if it's present
        self.__feilds_img_grid = DFrame(self.__record_frame)
        self.__feilds_img_grid.pack()

        self.__feilds = FeildsGrid(self.__feilds_img_grid)
        self.__feilds.grid(column=0, row=0)

        # Image
        if False:
            pass


    def set_schema():
        """Sets the """

    def set_record_values(self, values):
        self.__feilds.set_feilds(values)