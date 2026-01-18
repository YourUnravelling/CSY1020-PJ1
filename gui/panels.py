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

# TODO When a panel that can set things sets something, it needs to send a signal out to ALL other panels that it's updated.
# TODO When a object changes, it needs to ask all the bindables if they have unsaved stuff, and then display a confirmation thingy if they do.


class TableSelectButtons(bp.BindablePanel):

    def __init__(self, master, update_function):
        self.__last_clicked_button = None
        super().__init__(master, core, update_function, debug_name="TableSelectButtons")

    def _set_object_spesific(self, updated_objects:set[str] = set()) -> None:
        """
        Just initialises the tables, doesn't read object param.
        """
        tables:list[str] = list(core.sm.schema.keys())
        tables.sort()
        for table in tables:
            this_button = ttk.Button(self, text=table, width=30)
            this_button.configure(command= lambda table=table, this_button=this_button: self.__table_button_clicked(table, this_button))
            this_button.pack(pady=3, padx=5, ipady=3)
        
    def __table_button_clicked(self, table:str, button):
        button.config(state = "disabled")
        if self.__last_clicked_button:
            self.__last_clicked_button.config(state = "enabled")
        self.__last_clicked_button = button
        self._call_binds({"table":table})


class RecordSelectTree(bp.BindablePanel):
    
    def __init__(self, master, update_function):
        super().__init__(master, core, update_function, debug_name="RecordSelectTree")

        self.__treeview = TreeviewTable(self, self.__record_selected)

        self.__top_bar = DFrame(self, debug_name="Record select top bar")
        
        self.__add_record = ttk.Button(self.__top_bar, text="Add")
        self.__dupe_record = ttk.Button(self.__top_bar, text="Duplicate")
        self.__remove_record = ttk.Button(self.__top_bar, text="Delete")
        
        self.__search_field = DFrame(self.__top_bar)
        self.__search_column_selector = ttk.Combobox(self.__search_field)
        self.__search_column_selector.pack(side="left")
        self.__searchbar = ttk.Entry(self.__search_field)
        self.__searchbar.pack(side="left", fill="x", expand=True)
        self.__search = ttk.Button(self.__search_field, text="Search")
        self.__search.pack(side="left")
        
        for item in [self.__add_record, self.__dupe_record, self.__remove_record]:
            item.pack(padx=5, side="left")
        
        self.__search_field.pack(side="left", padx=5, fill="x", expand=True)

        self.__search_column_selector.insert(0, "Any field")

        


    def _set_object_spesific(self, updated_objects:set[str] = set()) -> None:
        #self.__treeview.pack_forget()
        if not self.__treeview.winfo_ismapped(): # If widgets are not visible, pack it
            self.__top_bar.pack(fill="x", ipady=5)
            self.__treeview.pack(fill="both", expand=True, padx=5, pady=5)
            
        if not "table" in updated_objects:
            pass # TODO If table is not updated, only refresh the objects in the table and not the whole thing
            # Maybe another condition for if the primary key updates? Maybe not needed
        #else:
        #    self.__surpress_next_signal = True

        table = self._object["table"]
        headings_raw = list(t[1] for t in self._core.sm.schema[table])
        table_data = self._core.sm.read_full(table)
        self.__treeview.set_table(
                table,
                headings_raw,
                headings_raw,#self._core.config,
                table_data
                )
        self._call_binds({
            "table": None,
            "record": None
        })

    def __record_selected(self, uid):
        """
        Called when the treeview selects a record
        """
        #if self.__surpress_next_signal: # If this signal is to be surpressed
        #    self.__surpress_next_signal = False
        #    return

        print("[RecordSelectTree] Record was selected with id", uid)
        self._call_binds({
            "table": self._object["table"],
            "record": uid
        })


class RecordScroll(bp.BasePanel):
    def __init__(self, master, update_function, autosave= False):
        super().__init__(master, core, update_function, debug_name="RecordScroll")

        self.__autosave:bool = autosave

        self.__unsaved = False # TODO Set a different way?

        # Private, Highest bar, for the controls
        self.__top_bar = DFrame(self, debug_name="Top bar") 
        self.__top_bar.pack(anchor="n", fill="x", expand=False, padx=10, pady=10)
        #self.__top_bar.columnconfigure(1, weight=2)
        
        # Private
        self.__delete = ttk.Button(self.__top_bar, text="Delete")
        self.__delete.pack(side="right")#grid(row=1, column=3)

        self.__edit = ttk.Button(self.__top_bar, text="Edit", command= self.__to_write)#self.__feilds.set_mode({"read":"write", "write":"read"}[self.__feilds.get_mode_at(0)]))

        self.__apply = ttk.Button(self.__top_bar, text="Apply", command=self.__apply_pressed, state="enabled")
        self.__cancel = ttk.Button(self.__top_bar, text="Cancel", command=self.__cancel_pressed, state="enabled") # TODO command

        # Frame for record info, possibly scrolling
        self.__record_frame = DFrame(self, debug_name="Record frame")

        self.__no_record_text = ttk.Label(self, text="No record selected", justify="center")
        


        # Private, Frame for the feilds and image if it's present
        self.__fields_img_grid = DFrame(self.__record_frame, debug_name="Feilds img grid")
        self.__fields_img_grid.pack()

        self.__fields = FieldsGrid(self.__fields_img_grid, updated_call=self.a_field_was_updated)
        self.__fields.grid(column=0, row=0, sticky="n")

        # Image
        self.__imagevar = tk.PhotoImage(file="resources/example_animal.png") # TODO
        self.__image = ttk.Label(self.__fields_img_grid, image=self.__imagevar)
        self.__image.grid(column=1, row=0)

        self.__foreigns_frame = DFrame(self.__record_frame, debug_name="Foreigns frame")
        self.__foreigns_frame.pack(padx=5, pady=0)

        # TODO THIS IS TEMPORARY ---------
        self.__first_one = DFrame(self.__foreigns_frame, debug_name="Example thingy frame")
        self.__first_one.pack(pady=5, padx=10, fill="x")
        ttk.Button(self.__first_one, text="AnimalMedicalRecords").pack(pady=5, padx=5, fill="x")

        self.__first_one_tree = TreeviewTable(self.__first_one, None)
        self.__first_one_tree.pack(padx=15)
        self.__first_one_tree.set_table("null", ["ID", "Animal", "Date", "Height", "Weight"], ["ID", "Animal", "Date", "Height", "Weight"], [
                                 ["46", "1", "2025-12-12", "45.4", "22.2"],
                                 ["32", "2", "2025-12-1", "45.1", "23.9"]
                                 ])
        
        for name in ["AnimalTransferHistory", "SponsorableAnimal"]:
            one = DFrame(self.__foreigns_frame)
            one.pack(pady=5, padx=10, fill="x")
            ttk.Button(one, text=name).pack(pady=0, padx=10, fill="x")



        # --------------------------------

        self.__to_null_record()
        self.__to_saved()

    def a_field_was_updated(self, index, value):
        if not self.__autosave:
            self.__to_unsaved()
        else:
            self._core.sm.write_field_index(self._object["table"], self._object["record"], index, value)
    
    def __cancel_pressed(self):
        """
        When the cancel button is pressed, just reverts the fieldgrid to the saved state
        """
        if self.__unsaved: # If it has been modified, we need to set the fields back to the db values
            pass

        self.__to_read()


    def __apply_pressed(self):
        """
        Triggered when apply is pressed, saves the content of the fields to the record
        """
        # Get all values of this record from the db, values currently in the grid, and column names in order
        saved_values:list = self._core.sm.read(self._object["table"], self._object["record"])
        unsaved_values:list = self.__fields.values
        field_names:list = list(column[1] for column in self._core.sm.schema[self._object["table"]])

        # Create a dictionary of all the values which are modified and what they are modified to
        modified_values:dict = {}
        for i, value in enumerate(unsaved_values):
            if value != saved_values[i]: # If value has been changed from the one in the db
                modified_values[field_names[i]] = value # Add the value to the dict with a key as col name

        #self._core.sm.write_record_list(self._object["table"], self._object["record"], self.__feilds.values)
        print(modified_values)
        self._core.sm.write_record_dict(self._object["table"], self._object["record"], modified_values)
        self.__to_saved()
        self._broadcast_object_update(self._object)

    def set_table(self, table:str):
        """Sets the types of the feilds"""
        try:
            column_types = list(col[2] for col in core.sm.schema[table])
            #default_values = core.config.default_values[table] # This is called default values but really should just be values MAYBE DISREG
            default_values = []
            for i in range(len(core.sm.schema[table])):
                default_values.append("")
            column_names = list(col[1] for col in core.sm.schema[table])
        except BaseException as error: print("There was an error setting the table in recordScroll",error, default_values)

        self.__fields.set_feilds(column_types, default_values, column_names)

    def set_record(self, pk:str):
        """Sets the current displayed record to pk"""

        #record_values = core.sm.read(self._object["table"], pk, self._core.config.pk_defaults[self._object["table"]])
        record_values = core.sm.read(self._object["table"], pk, self._core.sm.schema[self._object["table"]][0][1])#.pk_defaults[self._object["table"]])
        self.__fields.set_values(record_values)

    def _set_object_spesific(self, updated_objects:set[str] = set()) -> None:

        # Ensure object contains table and record TODO maybe add this to base function
        for sub_obj in ["table", "record"]:
            if not sub_obj in self._object:
                self._object[sub_obj] = None

        if self._object["table"] == None or self._object["record"] == None:
            print("[Recordscroll] part of object is null, setting to null", self._object)
            self.__to_null_record()
        else:
            if "table" in updated_objects: # TODO If table is not what it already was
                self.set_table(self._object["table"])
                self.set_record(self._object["record"])
            elif "record" in updated_objects:
                self.set_record(self._object["record"])

            self.__to_not_null_record()
        #except: self.__add_no_record_text()


        self.__fields.set_mode("read")
        self.__to_saved()
        print("[Recordscroll] object is being updated!", self._object["table"],self._object["record"], updated_objects, self._object)

    def __to_null_record(self):
        self.__no_record_text.pack(pady=50)
        self.__record_frame.pack_forget()
        #self.__fields.grid_forget()
        self.__fields.set_feilds([], [], [])

    def __to_not_null_record(self):
        print("[Recordscroll] To not null record", self._object)
        self.__record_frame.pack()
        self.__no_record_text.pack_forget()

    def __to_unsaved(self):
        self.__unsaved = True
        self.__apply["state"] = "normal"

    def __to_saved(self): # TODO Is this needed?
        self.__unsaved = False
        self.__apply["state"] = "disabled"
        self.__to_read()
    
    def __to_write(self):
        self.__edit.pack_forget()
        
        self.__apply.pack(side="left")
        self.__cancel.pack(side="left")

        self.__fields.set_mode("write")
        
    def __to_read(self):
        self.__edit.pack(side="left")
        
        self.__apply.pack_forget()
        self.__cancel.pack_forget()

        self.__fields.set_mode("read")
        
    

    # TODO __unsaved should be a set of field names which are unsaved
    # Apply should remove all from the set
    # Pressing apply should change them all individually, with a different case for the pk?
    # Maybe should just be smart and do them all seperate
    # ADD A CHECK THAT IT ACTUALLY CHANGED FOR VALIDATION, 
    # MAYBE EVEN COMPARE IT TO SAVED VALUE THIS EVERY TIME IT UPDATES!!!!

    # I'm going to change it so it just gets all the widget's values when apply is pressed and only changes them if they are different

    # TODO Check how the values in fields grid update