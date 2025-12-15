import tkinter as tk
from tkinter import ttk


class FeildsGrid(tk.Frame):
    """A frame containing all feilds of a record
    `parent` The parent widget
    `tablename` The table's name in the sql
    `key` The primary key of the column
    `schema` (Remove)
    `writemode` True if the frame should allow writing to the table.
    ADD `require_apply` If true, the changes are not applied until the apply() method is called.
    """
    def __init__(self, parent, tablename, key, schema, writing=False):
        super().__init__(parent)

        self.__read_widgets:list = []
        self.__write_widgets:list = []
        self.__writing:bool = writing # TODO Decide if this should even be a param, TODO decide if this should be "editing" and "viewing" instead

        names = schema[0]
        types = schema[1]

        for i in range(len(schema[0])):
            tk.Label(self, text=names[i]).grid(row=i, column=0)

            # Read widgets
            self.__read_widgets.append(tk.Label(self, text="VAL"))

            # 
            if types[i] == "INTEGER":
                self.__write_widgets.append(tk.Spinbox(self, text="VAL"))
            elif types[i] == "TEXT":
                self.__write_widgets.append(tk.Entry(self, text="VAL"))
            elif types[i] == "BOOL":
                self.__write_widgets.append(tk.Checkbutton(self))

        
        if writing:
            self.write()
        else:
            self.read()
    
    def read(self):
        for i,widget in enumerate(self.__write_widgets):
            widget.grid_forget()
        for i,widget in enumerate(self.__read_widgets):
            widget.grid(row=i,column=1)
        self.__writing = False
            

    def write(self):
        for i,widget in enumerate(self.__read_widgets):
            widget.grid_forget()
        for i,widget in enumerate(self.__write_widgets):
            widget.grid(row=i,column=1)
        self.__writing = True

    
    @property 
    def writing(self):
        return self.__writing
    
    @writing.setter
    def writing(self, val):
        self.__writing = val
        if val:
            self.write()
        else:
            self.read()

class RecordViewer(tk.Frame):
    """A frame which allows viewing of an sqlite table.
    `tablename` The name of the table to be viewed
    `parent` The parent of the frame
    `exe` Function which is called to query the database `(sql,*args)`

    """
    def __init__(self, tablename, parent, exe):
        super().__init__(parent)
        self.__tablename = tablename # Private, The name of the table 
        self.__parent = parent # Private
        self.__exe = exe # Private

        ANIMAL_TABLE = ANIMAL_TABLE = [["id","name", "Test bool", "Bool 2"],["INTEGER","TEXT", "BOOL", "BOOL"]]# TODO remove
        names = ANIMAL_TABLE[0]
        types = ANIMAL_TABLE[1]

        meta_feild_selector = ttk.Combobox(self, values=names, state="readonly")
        record_selector = ttk.Combobox(self)

        meta_feild_selector.pack()
        record_selector.pack()


        objects_frame = FeildsGrid(self,"animal",0,ANIMAL_TABLE, writing=True)
        
        objects_frame.pack()
    
    def display_new_record(self, id):
        """
        Displays a new record with the id as id
        """