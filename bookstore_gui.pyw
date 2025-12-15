'''
GUI for the bookstore app
Autumn Hickinbotham - 12/25
'''

import bookstore_core as core
import tkinter as tk
from tkinter import ttk
from scrollable_external import ScrollFrame

class ThemeManager():
    all_widgets:list

    def __init__(self, mode):
        self.__mode = mode
        ThemeManager.all_widgets.append(self)
    
    @property
    def mode(self):
        return self.__mode

class ScrollFrameOld(tk.Canvas):
    def __init__(self, master):
        super().__init__(master=master)
        self.__scrollbar = ttk.Scrollbar(self)
        self.__scrollbar.pack(side="right")

    @property # scrollbar getter
    def scrollbar(self):
        return self.__scrollbar
    # No setter as scrollbar shouldn't be changed


w = tk.Tk()
s = ScrollFrame(w)
s.pack()

for i in range(8):
    ttk.Button(s.viewPort, text="test").pack()


def main():
    w.mainloop()

if __name__ == "__main__":
    main()

