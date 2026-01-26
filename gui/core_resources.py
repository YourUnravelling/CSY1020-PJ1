"""
Keeps icons and some other gui related resources in memory
"""
import tkinter as tk


icons:dict = {}


def initialise_icons():
    icons["open"] = tk.PhotoImage(file="core_resources/closed.png")
    icons["closed"] = tk.PhotoImage(file="core_resources/open.png")
