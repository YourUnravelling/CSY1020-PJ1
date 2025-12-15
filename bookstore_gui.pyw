'''
GUI for the bookstore app
Autumn Hickinbotham - 12/25
'''

# Lib imports
import bookstore_core as core
import tkinter as tk
from tkinter import ttk

# Class imports
from scrollable_external import ScrollFrame
from record_viewier import RecordViewer

ANIMAL_TABLE = [["id","name", "Test bool", "Bool 2"],["INTEGER","TEXT", "BOOL", "BOOL"]] #[["id","INTEGER"],["name","TEXT"]] TODO remove



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

w = tk.Tk()
w.iconphoto(True,tk.PhotoImage(file="icon.png"))
#s = ScrollFrame(w)


class EntryView(tk.Frame):
    def __init__(self, parent, exe):
        super().__init__(parent)
        self.__parent = parent
        self.__exe = exe

        self.__topbar = tk.Frame(self)
        self.__topbar.pack(fill="x", padx=5, pady=5)
        self.__content = tk.Frame(self, background="blue")
        self.__content.pack(expand=True, fill="both")

        self.__table_selector = ttk.Combobox(self.__topbar, state="readonly", values=["Books", "Customers", "Authors", "Invoices"])
        self.__table_selector.pack(side=tk.LEFT)

        self.__view_edit_button = tk.Button(self.__topbar, text="Viewing")
        self.__view_edit_button.pack(side="right")


        self.__sub_content = tk.Frame(self.__content, width=500)
        self.__sub_content.pack(fill="y", expand=True)
        self.pack(fill="both", expand=True)

        self.__viewer = RecordViewer("book", self.__sub_content, exe=self.__exe)
        self.__viewer.pack()


EntryView(w, core.sm.exe).pack()

def main():
    w.mainloop()

if __name__ == "__main__":
    main()

