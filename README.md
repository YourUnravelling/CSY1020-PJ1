A generalised SQLite editor, using the contents of the SQLite file and config.py

AS OF THE CURRENT BUILD, lots of things are hardcoded, for example, foreign key table names, external references, and the image.

Currently over 2000 lines of code


# Modules / folders
## config
Usecase-dependant files which define behaviour and database

## resources
Usecase-dependant files controlling non-source code files

## gui
All tkinter and other graphical elements

## core-resources
All images and other resources that 

## core
Non-graphical elements

## External
Code I did not write



# General notes

---

Each part of a window is a panel that calls core for info, and sends object update signals to the layout, as well as update signals to other panels which have their objects controlled by them.




TableSelector()



RecordSelector(table)
-> (table, record)


RecordViewer(table, record)
-> None



---

