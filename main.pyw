"""
The main program that is run, imports all others.
"""

from gui import bookstore_gui as bsgui
from sys import exit

def main():
    bsgui.main()
    
if __name__ == "__main__":
    main()
    exit()