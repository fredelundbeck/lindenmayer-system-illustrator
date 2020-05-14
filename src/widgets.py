import tkinter as tk
import tkinter.ttk as ttk

class ScrollableTreeview(ttk.Treeview):
    def __init__(self, master=None, orient = tk.VERTICAL, **kw):
        super().__init__(master=master, **kw)

        #Setup scrollbar
        self.scrollbar = ttk.Scrollbar(master, orient = orient, command = self.yview)

        #Configure scrollbar
        self.configure(yscrollcommand = self.scrollbar.set)

        #Placement
        self.scrollbar.grid(column = 1, row = 0, sticky = tk.NS)