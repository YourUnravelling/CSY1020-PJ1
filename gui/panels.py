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
from gui.widgets import DFrame, TreeviewTable, HideShowFrame
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

        cats = core.config.category_contents
        for category in cats:
            category_frame = HideShowFrame(self, label=category[0])
            

            for tablename in category[1]:
                this_button = ttk.Button(category_frame.content, text=tablename, width=30)
                this_button.configure(command=lambda table=tablename, this_button=this_button: self.__table_button_clicked(table, this_button))
                this_button.pack(pady=3, padx=5, ipady=3)
            
            if not category[1]:
                ttk.Label(category_frame.content, text="No tables in this category").pack(pady=3, padx=5, ipady=3)


            category_frame.pack(fill="x", ipady=5)

        
    def __table_button_clicked(self, table:str, button):
        button.config(state = "disabled")
        if self.__last_clicked_button:
            self.__last_clicked_button.config(state = "enabled")
        self.__last_clicked_button = button
        self._call_binds({"table":table})


class RecordSelectTree(bp.BindablePanel):
    
    def __init__(self, master, update_function):
        super().__init__(master, core, update_function, debug_name="RecordSelectTree")

        self.__filtering:bool = False

        self.__treeview = TreeviewTable(self, self.__record_selected)

        self.__top_bar = DFrame(self, debug_name="Record select top bar")
        
        self.__add_record = ttk.Button(self.__top_bar, text="Add", command=self.__add_button_pressed)
        self.__dupe_record = ttk.Button(self.__top_bar, text="Duplicate")
        self.__remove_record = ttk.Button(self.__top_bar, text="Delete")
        
        self.__search_field = DFrame(self.__top_bar)
        self.__search_column_selector = ttk.Combobox(self.__search_field) # type: ignore
        self.__search_column_selector["state"] = "readonly"
        self.__search_column_selector.bind(sequence="<<ComboboxSelected>>", func=self.__search_column_selectors_updated) # type: ignore

        self.__search_type_selector = ttk.Combobox(self.__search_field, width=8) # type: ignore
        self.__search_type_selector["state"] = "readonly"
        self.__search_type_selector.bind(sequence="<<ComboboxSelected>>", func=self.__search_column_selectors_updated) # type: ignore
        self.__search_type_selector["values"] = ["contains", "is", "starts", "ends"]

        self.__searchbar_var = tk.StringVar()
        self.__searchbar_var.set("")
        self.__searchbar = ttk.Entry(self.__search_field, textvariable=self.__searchbar_var)
        self.__searchbar_var.trace_add("write", self.__searchbar_updated)

        self.__search_button = ttk.Button(self.__search_field, text="Search", command=self.__filter)
        self.__discard_search_button = ttk.Button(self.__search_field, text="Reset search", command=self.__remove_filter)

        PADXVAL = 5

        self.__add_record            .pack(padx=PADXVAL, side="left")
        self.__dupe_record           .pack(padx=PADXVAL, side="left")
        self.__remove_record         .pack(padx=PADXVAL, side="left")
        #self.__search_button         .pack(padx=PADXVAL, side="right") # No search button, because it dynamically updates
        self.__search_column_selector.pack(padx=PADXVAL, side="left")
        self.__search_type_selector  .pack(padx=PADXVAL, side="left")
        self.__searchbar             .pack(padx=PADXVAL, side="left", expand=True, fill="x")
        self.__discard_search_button .pack(padx=PADXVAL, side="left")
        self.__search_field          .pack(padx=PADXVAL, side="left", expand=True, fill="x")
        
        #self.__search_column_selector.insert(0, "Any field")
        
        self.__discard_search_button["state"] = "disabled"


    def __add_button_pressed(self):
        self._core.sm.add(self._object["table"], None)

    def __search_column_selectors_updated(self, v):
        self.__filter()

    def __searchbar_updated(self, a, b, c):
        self.__filter()
    
    
    def __filter(self):

        # No strip here to allow precise filtering, for example the user might want to search "we" without bringing up "ewes", so they search " we "
        filter_column = self.__search_column_selector.get()
        filter_type = self.__search_type_selector.get()
        filter_str = self.__searchbar.get() 
        print("[RecordSelectTree] searching", filter_column, filter_str)

        if not filter_str:
            if self.__filtering:
                self.__filtering = False
                self.__remove_filter()
        else:
            self.__filtering = True
            self.__load_table_data(filters=[(filter_column, filter_str, filter_type)])
            self.__discard_search_button["state"] = "enabled"

    def __remove_filter(self):
        self.__filtering = False
        self.__searchbar.delete(0, tk.END)
        self.__load_table_data()
        self.__discard_search_button["state"] = "disabled"


    def __load_table_data(self, filters:list[tuple[str, str, str]]|None = None):
        """
        Sets the table data by getting it with an sql query. Filters according to filters
        """
        table = self._object["table"]
        table_data = self._core.sm.read_full(table, filters)


        self.__treeview.set_table_data(table_data)


    def _set_object_spesific(self, updated_objects:set[str] = set()) -> None:
        if not self.__treeview.winfo_ismapped(): # If treeview is not visible, pack it and the top bar
            self.__top_bar.pack(fill="x", ipady=5)
            self.__treeview.pack(fill="both", expand=True, padx=5, pady=5)
            
        if not "table" in updated_objects:
            pass # TODO If table is not updated, only refresh the objects in the table and not the whole thing
            # Maybe another condition for if the primary key updates? Maybe not needed
        #else:
        #    self.__surpress_next_signal = True

        table = self._object["table"]

        # Get a headings list
        headings_raw = list(t[1] for t in self._core.sm.schema[table])

        self.__treeview.set_headings(
                table,
                headings_raw,
                headings_raw
                )
        self.__search_column_selector["values"] = headings_raw

        # Set the value in the combobox (need to enable then disable because tkinter sucks)
        self.__search_column_selector["state"] = "enabled"
        self.__search_column_selector.delete(0, tk.END)
        self.__search_column_selector.insert(0, headings_raw[0])
        self.__search_column_selector["state"] = "readonly"

        self.__search_type_selector["state"] = "enabled"
        self.__search_type_selector.delete(0, tk.END)
        self.__search_type_selector.insert(0, "contains")
        self.__search_type_selector["state"] = "readonly"

        self.__load_table_data()
        
        # Call binds as null when a new table is loaded
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
        self.__foreigns_frame.pack(padx=5, pady=0, fill="x")

        self.__foreigns:list = [] # List of pointers to the foreign showhide frames, used to delete them when new ones are to be made.

        self.__to_null_record()
        self.__to_saved()

    def __create_references(self):

        for item in self.__foreigns:
            item.pack_forget()
        self.__foreigns.clear()

        table_references:list[tuple[str,str]] = [] # (tablename, referencing column in the other table, referenced column in this table)

        
        for table in core.sm.schema:
            if not table[1] == self._object["table"]: # If the table isnt the current one
                if True: # If the table has a reference to this one
                    table_references.append((table[1], "the column that is referencing it"))
        
        for i in range(4): # TODO Replace with list of references
            this = HideShowFrame(self.__foreigns_frame, label="test " + str(i))
            
            tree = TreeviewTable(this.content, None)
            tree.pack(padx=15)
            tree.set_headings("null", 
                           ["ID", "Animal", "Date", "Height", "Weight"], 
                           ["ID", "Animal", "Date", "Height", "Weight"], 
                           )
            tree.set_table_data([
                            ["46", "1", "2025-12-12", "45.4", "22.2"],
                            ["32", "2", "2025-12-1", "45.1", "23.9"]
                        ])
            self.__foreigns.append(this)
            this.pack(pady=5, padx=10, fill="x")



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
            pass # TODO

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

        self._core.sm.write_record_dict(self._object["table"], self._object["record"], modified_values)
        self.__to_saved()
        self._broadcast_object_update(self._object)

    def __set_table(self, table:str):
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

    def __set_record(self, pk:str): # TODO make priv
        """Sets the current displayed record to pk"""

        #record_values = core.sm.read(self._object["table"], pk, self._core.config.pk_defaults[self._object["table"]])
        record_values = core.sm.read(self._object["table"], pk, self._core.sm.schema[self._object["table"]][0][1])#.pk_defaults[self._object["table"]])
        self.__fields.set_values(record_values)

        self.__create_references()

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
                self.__set_table(self._object["table"])
                self.__set_record(self._object["record"])
            elif "record" in updated_objects:
                self.__set_record(self._object["record"])

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