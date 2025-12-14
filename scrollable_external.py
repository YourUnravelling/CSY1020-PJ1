"""
NOT MY CODE! From:
https://sqlpey.com/python/tkinter-implementing-scrollbars-for-frames/
"""

import tkinter as tk
#from tkinter import ttk

class AdvancedScrollableFrame(tk.Frame):
    """
    Encapsulates Frame scrolling using Canvas, requiring an .update() call 
    after content modification.
    """
    def __init__(self, parent, scrollbar_width=18):
        # Initialize the base Frame container (the 'parent' argument of this constructor)
        tk.Frame.__init__(self, parent)

        # Setup Scrollbar (vertical)
        self.scrollbar = tk.Scrollbar(self, width=scrollbar_width)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        # Setup Canvas
        self.canvas = tk.Canvas(self, yscrollcommand=self.scrollbar.set, background="#ffffff")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        # Create the internal frame that holds the content
        self.inner_frame = tk.Frame(self.canvas, background="#ffffff")
        
        # Create the window item linking the inner frame to the canvas
        self.window_item = self.canvas.create_window(0, 0, window=self.inner_frame, anchor=tk.NW)

        # Bind configuration to adjust window width and later refresh scroll region
        self.canvas.bind('<Button-1>', self.__adjust_canvas_width)
        
        # Use the inner frame's configuration to update the scroll region
        self.inner_frame.bind('<Configure>', self.refresh_scroll_region)

        self.bind("<Button-4>", "scroll_up")


    def __adjust_canvas_width(self, event):
        '''Ensures the internal frame spans the width of the canvas'''
        canvas_width = event.width
        self.canvas.itemconfig(self.window_item, width=canvas_width)

    def refresh_scroll_region(self, event=None):
        '''Calculates and sets the new scrollable area'''
        self.update_idletasks() # Crucial for accurate bounding box calculation
        bbox = self.canvas.bbox(self.window_item)
        if bbox:
             self.canvas.config(scrollregion=bbox)

    def update(self):
        '''Public method to force a refresh, mainly calls refresh_scroll_region'''
        self.refresh_scroll_region()
    
    def scroll_up(self):
        print("test")
        
    @property
    def content_parent(self):
        '''Property to easily access the frame where users should pack/grid widgets'''
        return self.inner_frame