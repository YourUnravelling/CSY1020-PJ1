"""
All variables spesific to the database, including the schema, and functions
"""
# TODO Decide if this should be a class that is instanciated to defaultise var names, would make functions more complex?
# Or just a regular file with spesific var names

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from gui.widgets import DFrame
from core.config_class import ConfigClass
#import core.bookstore_core as core

# TODO Move this to a class? And its own file?
def generate_invoice(core, object:dict):
    """Generates a formatted invoice in a new window, spesific to bookstore"""

    BOOKSTORE_NAME = "Clay brookstore"

    invoice = core.sm.read("invoice", object["record"])
    customer = core.sm.read("customer", invoice[1])
    book = core.sm.read("book", invoice[2])

    if not customer or not book: # Error handling
        message = "Customer and book keys are invalid"
        if book:
            message = "Customer key is invalid"
        if customer:
            message = "Book key is invalid"
        
        messagebox.showerror("Cannot generate invoice", message=message)
        return


    date = "2/2/2026" # Wow I typed in the correct data by accident TODO Switch to proper date rooting from invoice



    invoice_win = tk.Tk()
    invoice_win.geometry("650x800")
    invoice_win.resizable(False, False)

    invoice_frame = ttk.Frame(invoice_win, borderwidth=10, relief="sunken")
    invoice_frame.pack(padx=15, pady=15, expand=True, fill="both")

    tk.Label(invoice_frame, text="Invoice of purchase", font=("",16)).pack()
    tk.Label(invoice_frame, text=f"{BOOKSTORE_NAME} - {date}", font=("",16)).pack()
    

    invoice_win.mainloop()



c = ConfigClass(
    default_settings={},
    table_custom_commands= {
        "invoice": {"Generate invoice": generate_invoice}
    },
    default_table="book",
    category_contents = [
        ("Tables", ["book", "author", "customer", "invoice"], True),
    ],
    window_name = "Bookstore Manager"
)