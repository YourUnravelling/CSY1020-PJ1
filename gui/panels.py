"""
This file contains the many inbuilt panels
Naming convention:
Table/Record/Feild - Object
Selector/NA - If selector, allows the user to select one of the objects from parent object
Description - Description of the instance of the object
"""
import tkinter as tk
from tkinter import ttk

from core import bookstore_core as core
from gui.widgets import DFrame, TreeviewTable
from gui.fields_grid import FieldsGrid
import gui.base_panels as bp

class TableSelectButtons(bp.BindablePanel):

    def __init__(self, master):
        super().__init__(master, core, debug_name="TableSelectButtons")

    def _set_object_spesific(self, updated_objects:set[str]) -> None:
        """
        Just initialises the tables, doesn't read object param.
        """
        tables = core.sm.schema.keys()
        for table in tables:
            ttk.Button(self, text=table, width=30, command= lambda table=table: self.__table_button_clicked(table)).pack(pady=3, padx=5, ipady=3)
        
    def __table_button_clicked(self, table:str):
        self._call_binds({"table":table})


class RecordSelectTree(bp.BindablePanel):
    
    def __init__(self, master):
        super().__init__(master, core, debug_name="RecordSelectTree")

        self.__treeview = TreeviewTable(self, self.__record_selected)

        self.__top_bar = DFrame(self, debug_name="Record select top bar")
        self.__add_record = ttk.Button(self.__top_bar, text="Add")
        self.__remove_record = ttk.Button(self.__top_bar, text="Remove")
        for item in [self.__add_record, self.__remove_record]:
            item.pack(padx=5, side="left")


    def _set_object_spesific(self, updated_objects:set[str]) -> None:
        #self.__treeview.pack_forget()
        if not self.__treeview.winfo_ismapped(): # If widgets are not visible, pack it
            self.__top_bar.pack(fill="x", ipady=5)
            self.__treeview.pack(fill="both", expand=True, padx=5, pady=5)
            

        table = self._object["table"]
        headings_raw = list(t[1] for t in self._core.sm.schema[table])
        table_data = self._core.sm.read_full(table)
        self.__treeview.set_table(
                table,
                headings_raw,
                headings_raw,#self._core.config,
                table_data
                )

    def __record_selected(self, uid):
        """
        Called when the treeview selects a record
        """
        self._call_binds({
            "table": self._object["table"],
            "record": uid
        })


class RecordScroll(bp.BasePanel):
    def __init__(self, master, autosave= False):
        super().__init__(master, core, debug_name="RecordScroll")

        self.__autosave:bool = autosave

        self.__unsaved = False # TODO Set a different way?

        # Private, Highest bar, for the controls
        self.__top_bar = DFrame(self, debug_name="Top bar") 
        self.__top_bar.pack(anchor="n", fill="x", expand=False, padx=10, pady=10)
        #self.__top_bar.columnconfigure(1, weight=2)
        
        # Private
        self.__delete = ttk.Button(self.__top_bar, text="Delete")
        self.__delete.pack(side="right")#grid(row=1, column=3)

        self.__edit = ttk.Button(self.__top_bar, text="Edit", command=lambda: self.__feilds.set_mode({"read":"write", "write":"read"}[self.__feilds.get_mode_at(0)]))
        self.__edit.pack(side="right")

        self.__apply = ttk.Button(self.__top_bar, text="Apply", command=self.__apply_pressed)
        self.__apply.pack(side="left")

        # Frame for record info, possibly scrolling
        self.__record_frame = DFrame(self, debug_name="Record frame")
        self.__record_frame.pack()

        self.__no_record_text = ttk.Label(self.__record_frame, text="No record selected", justify="center")
        self.__add_no_record_text()


        # Private, Frame for the feilds and image if it's present
        self.__feilds_img_grid = DFrame(self.__record_frame, debug_name="Feilds img grid")
        self.__feilds_img_grid.pack()

        self.__feilds = FieldsGrid(self.__feilds_img_grid, updated_call=self.a_field_was_updated)
        self.__feilds.grid(column=0, row=0)

        # Image
        self.__imagevar = tk.PhotoImage(file="resources/sidebar_image.png") # TODO
        self.__image = ttk.Label(self.__feilds_img_grid, image=self.__imagevar)
        self.__image.grid(column=1, row=0)

        self.__foreigns_frame = DFrame(self, debug_name="Foreigns frame")
        self.__foreigns_frame.pack()

    def a_field_was_updated(self, index, value):
        print("A feild was pdated")
        if not self.__autosave:
            self.__to_unsaved()
        else:
            self._core.sm.write_field_index(self._object["table"], self._object["record"], index, value)
    
    def __apply_pressed(self):
        """
        Triggered when apply is pressed, saves the content of the fields to the record
        """
        self._core.sm.write_record_list(self._object["table"], self._object["record"], self.__feilds.values)

    def set_table(self, table:str):
        """Sets the types of the feilds"""

        column_types = list(col[2] for col in core.sm.schema[table])
        default_values = core.config.default_values[table] # This is called default values but really should just be values MAYBE DISREG
        column_names = list(col[1] for col in core.sm.schema[table])

        self.__feilds.set_feilds(column_types, default_values, column_names)

    def set_record(self, pk:str):
        """Sets the current displayed record to pk"""

        record_values = core.sm.read(self._object["table"], pk, self._core.config.pk_defaults[self._object["table"]])
        self.__feilds.set_values(record_values)

    def _set_object_spesific(self, updated_objects:set[str] = set()) -> None:

        # Case to get rid of the no record selected text
        try:
            if self._object["table"] == None or self._object["record"] == None:
                self.__add_no_record_text()
            else:
                self.__remove_no_record_text()
        except: pass

        if "table" in updated_objects: # TODO If table is not what it already was
            self.set_table(self._object["table"])
        if "record" in updated_objects:
            self.set_record(self._object["record"])

        self.__feilds.set_mode("read")
        print("Record scroll thingy is being updated!", self._object["table"],self._object["record"], updated_objects, self._object)

    def __add_no_record_text(self):
        self.__no_record_text.pack(pady=50)

    def __remove_no_record_text(self):
        self.__no_record_text.pack_forget()

    def __to_unsaved(self):
        self.__unsaved = True
        self.__apply["state"] = "enabled"

    def __to_saved(self):... # TODO Is this needed?