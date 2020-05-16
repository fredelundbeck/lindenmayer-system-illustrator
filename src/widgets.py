'''
Holds special widgets used in the 
application.
'''

import tkinter as tk
import tkinter.ttk as ttk
import utilities as util

class ScrollableTreeviewFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup treeview
        self.treeview = ttk.Treeview(self)

        #Setup scrollbar
        self.scrollbar = tk.Scrollbar(
            self, 
            orient = tk.VERTICAL, 
            command = self.treeview.yview)

        #Configure scrollbar
        self.treeview.configure(yscrollcommand = self.scrollbar.set)
        
        #Configure column weights
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 0)

        #Placement
        self.treeview.grid(column = 0, row = 0, sticky = tk.EW)
        self.scrollbar.grid(column = 1, row = 0, sticky = tk.NS)

    def configure_treeview(self, **kw):
        self.treeview.configure(**kw)

    def modify_heading(self, column, **kw):
        self.treeview.heading(column, **kw)

    def modify_column(self, column, **kw):
        self.treeview.column(column, **kw)

    def insert_row(self, values):
        self.treeview.insert("", tk.END, values = values)

    def delete_row(self, row_item):
        self.treeview.delete(row_item)

    def clear_rows(self):
        for row in self.treeview.get_children():
            self.delete_row(row)
    
    def get_rows_values(self):
        rows = []
        for row in self.treeview.get_children():
            rows.append(self.treeview.item(row)["values"])
        return rows

class Entry(tk.Entry):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.configure(
            font = ("", 9), 
            relief = tk.FLAT,
            highlightthickness = 1,
            highlightbackground = "gray")
        

class NumberEntry(Entry):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.bind("<KeyRelease>", self.on_key_release_event, add = "+")

    def on_key_release_event(self, args):
        '''
        Checks if the value entry text can be converted to a number.
        If not it highlights the value entry background with red.
        '''
        value = self.get()
        if util.is_str_digit(value) or value == "":
            self["bg"] = "#FFFFFF"
        else:
            self["bg"] = "#FFAAAA"

