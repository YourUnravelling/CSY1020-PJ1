import tkinter as tk
import tkinter.ttk as ttk

w = tk.Tk()
w.minsize(200,100)
grid = tk.Frame(padx=10,pady=10).grid(padx=10,pady=10)
tk.Button(grid,text="Normal").grid(column=0,row=0,padx=10,pady=10)
ttk.Button(grid,text="Themed").grid(column=1,row=0,padx=10,pady=10)

tk.Entry(grid).grid(column=0,row=1,padx=10,pady=10)
ttk.Entry(grid).grid(column=1,row=1,padx=10,pady=10)

tk.Label(grid,text="Normal").grid(column=0,row=2,padx=10,pady=10)
ttk.Label(grid,text="Themed").grid(column=1,row=2,padx=10,pady=10)

tk.Checkbutton(grid,text="Normal").grid(column=0,row=3,padx=10,pady=10)
ttk.Checkbutton(grid,text="Themed").grid(column=1,row=3,padx=10,pady=10)


ttk.Progressbar(value=50).grid(column=1,row=4,padx=10,pady=10)


#tk.Listbox(listvariable=["Test",""])
ttk.Combobox(grid,values=["Test1","Test2"],state="readonly").grid(column=1,row=5,padx=10,pady=10)

#tk.Listbox(grid,{"Test":"test"}).grid(column=0,row=6,padx=10,pady=10)

tk.Spinbox(grid).grid(column=0,row=7,padx=10,pady=10)
ttk.Spinbox(grid).grid(column=1,row=7,padx=10,pady=10)


ttk.Separator(grid).grid(column=1,row=8,padx=10,pady=10)

tk.Radiobutton(grid,text="Normal").grid(column=0,row=8,padx=10,pady=10)
ttk.Radiobutton(grid,text="Themed").grid(column=1,row=8,padx=10,pady=10)

v= (tk.StringVar(value="Test1"))
tk.Listbox(grid,listvariable=v).grid(column=0,row=9,padx=10,pady=10)


tree = ttk.Treeview(grid,columns=["Test"])
tree.grid(column=1,row=10,padx=10,pady=10)
tree.insert(parent="",index=0,iid="3",text="test")
tree.insert(parent="3",index=0,text="test2")
#tree.insert(parent="3",)

#nb = ttk.Notebook(grid).grid(column=1,row=8,padx=10,pady=10)
#ttk.Button(nb).grid(column=1,row=8,padx=10,pady=10)

#tk.Button(grid,text="Normal",background="pink",foreground="purple").grid(column=0,row=15,padx=10,pady=10)
#ttk.Button(grid,text="Themed").grid(column=1,row=15,padx=10,pady=10)


style = ttk.Style()
style.configure(".", background="black")

w.mainloop()