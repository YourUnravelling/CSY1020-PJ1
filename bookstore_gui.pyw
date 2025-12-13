'''
GUI for the bookstore app
Autumn Hickinbotham - 12/25
'''

import bookstore_core as core
import tkinter as tk

class ThemeManager():
    all_widgets:list

    def __init__(self, mode):
        self.__mode = mode
        ThemeManager.all_widgets.append(self)
    
    @property
    def mode(self):
        return self.__mode


w = tk.Tk()

def main():
    w.mainloop()

if __name__ == "__main__":
    main()

