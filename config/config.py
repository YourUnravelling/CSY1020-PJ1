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

def to_pounds(input:float):
    strinp = str(input)
    if not "." in strinp:
        return "£" + strinp + ".00"
    else:
        whole, pence = strinp.split(".")
        if len(pence) == 1:
            pence = pence + "0"
        if len(pence) > 2:
            pence = pence[0:2]
        return "£" + whole + "." + pence

# TODO Move this to a class? And its own file?
def generate_invoice(core, object:dict):
    """Generates a formatted invoice in a new window, spesific to bookstore"""

    BOOKSTORE_NAME = "Clay brookstore"

    NORMAL_SHIPPING_PRICE = 3.5
    PRIORITY_SHIPPING_PRICE = 7.2

    VAT_MULTIPLIER = 0.20

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
    customer_full_name = f"{customer[1]} {customer[2]}"
    customer_email = customer[3]
    if not customer_email:
        customer_email = "No email provided"
    book_name = book[3]
    book_isbn = book[1]
    raw_book_price = book[6]

    delivery_ind = invoice[3]
    delivery_str:str
    delivery_price:float 
    if delivery_ind == 0: # No shipping
        delivery_str = "No shipping"
        delivery_price = 0.0
    elif delivery_ind == 1: # Normal
        delivery_str = "Normal shipping"
        delivery_price = NORMAL_SHIPPING_PRICE
    else: # Delivery ind is 2, priority
        delivery_str = "Priority shipping"
        delivery_price = PRIORITY_SHIPPING_PRICE
    
    no_vat_total = delivery_price + raw_book_price
    vat = no_vat_total * VAT_MULTIPLIER
    vat_total = no_vat_total + no_vat_total


    invoice_win = tk.Tk()
    invoice_win.geometry("650x800")
    invoice_win.resizable(False, False)

    invoice_frame = ttk.Frame(invoice_win, borderwidth=10, relief="sunken")
    invoice_frame.pack(padx=15, pady=15, expand=True, fill="both")

    tk.Label(invoice_frame, text="Invoice of purchase", font=("",16)).pack()
    tk.Label(invoice_frame, text=f"{BOOKSTORE_NAME} - {date}", font=("",16)).pack()
    tk.Label(invoice_frame, text=f"{customer_full_name} - {customer_email}", font=("",10)).pack()

    invoice_grid = tk.Frame(invoice_frame)
    invoice_grid.pack(pady=15, padx=50, expand=False, fill="x")
    invoice_grid.columnconfigure(1, weight=999)

    tk.Label(invoice_grid, text=f"{book_name} ({book_isbn})", font=("",10)).grid(column=0, row=0, sticky="w")
    tk.Label(invoice_grid, text=f"{to_pounds(raw_book_price)}", font=("",10)).grid(column=1, row=0, sticky="e")

    tk.Label(invoice_grid, text=f"{delivery_str}", font=("",10)).grid(column=0, row=1, sticky="w")
    tk.Label(invoice_grid, text=f"{to_pounds(delivery_price)}", font=("",10)).grid(column=1, row=1, sticky="e")

    ttk.Separator(invoice_grid).grid(column=0, row=2, sticky="nesw", pady=3, columnspan=2)

    tk.Label(invoice_grid, text=f"Total (before tax)", font=("",10)).grid(column=0, row=3, sticky="w")
    tk.Label(invoice_grid, text=f"{to_pounds(no_vat_total)}", font=("",10)).grid(column=1, row=3, sticky="e")

    tk.Label(invoice_grid, text="VAT", font=("",10)).grid(column=0, row=4, sticky="w")
    tk.Label(invoice_grid, text=to_pounds(vat), font=("",10)).grid(column=1, row=4, sticky="e")

    ttk.Separator(invoice_grid).grid(column=0, row=5, sticky="nesw", pady=3, columnspan=2)

    tk.Label(invoice_grid, text="Total (after tax)", font=("",10)).grid(column=0, row=6, sticky="w")
    tk.Label(invoice_grid, text= to_pounds(vat_total), font=("",10)).grid(column=1, row=6, sticky="e")

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