import tkinter as tk
import tkinter.ttk as ttk

class VariablesFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup frames
        self.label_frame = tk.LabelFrame(self, text = "Variables", font = ("", 9, "bold"))
        self.entry_frame = tk.Frame(self.label_frame)
        self.submit_frame = tk.Frame(self.label_frame)

        #Setup labels
        self.var_label = tk.Label(self.entry_frame, text = "var:")
        self.val_label = tk.Label(self.entry_frame, text = "value:")
        self.func_label = tk.Label(self.entry_frame, text = "f(x):")

        #Setup entries
        self.var_entry = tk.Entry(self.entry_frame)
        self.val_entry = tk.Entry(self.entry_frame)
        self.func_combobox = ttk.Combobox(self.entry_frame, 
                                            values = ["Move", "Rotate", "Save", "Load"], 
                                            state = "readonly",
                                            width = 17)
        #Setup submit button
        self.submit_button = tk.Button(self.submit_frame, text = "submit", width = 21)

        #Event bindings
        self.func_combobox.bind("<<ComboboxSelected>>", self.func_selection_event)
        self.var_entry.bind("<KeyRelease>", self.var_key_released_event)

        #Placement
        self.label_frame.pack(padx = 5, pady = 5)
        self.entry_frame.pack(padx = 5, pady = 5)
        self.submit_frame.pack()

        self.var_label.grid(column = 0, row = 0, sticky = tk.W)
        self.func_label.grid(column = 0, row = 1, sticky = tk.W)
        self.val_label.grid(column = 0, row = 2, sticky = tk.W)

        self.var_entry.grid(column = 1, row = 0, pady = 5)
        self.func_combobox.grid(column = 1, row = 1, pady = 5)
        self.val_entry.grid(column = 1, row = 2, pady = 5)

        self.submit_button.pack(pady = (0, 6))

    def var_key_released_event(self, args):
        '''
        Checks if entry has more than one char,
        if it has delete everything but the first char
        '''
        if len(self.var_entry.get()) > 1:
            self.var_entry.delete(1, tk.END)

    def func_selection_event(self, args):
        '''
        Checks whether LOAD or SAVE has been selected,
        if it has then disable the val_entry else enable it
        '''
        item = self.func_combobox.get()
        if item == "Save" or item == "Load":
            self.val_entry.delete(0, tk.END)
            self.val_entry["state"] = tk.DISABLED
        else:
            self.val_entry["state"] = tk.NORMAL
        



app = tk.Tk()

variables = VariablesFrame(app)
variables.pack()

app.mainloop()