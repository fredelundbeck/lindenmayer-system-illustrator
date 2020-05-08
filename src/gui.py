import tkinter as tk
import tkinter.ttk as ttk

class VariableInputs(tk.Frame):
    
    def __init__(self, master = None, **kw):
        super().__init__(master, **kw)

        self.__initialize_sub_widgets()
    
    def __initialize_sub_widgets(self):
        
        #labelframe
        self.labelframe = tk.LabelFrame(self, text = "Variables", font = ("", 9, "bold"), padx = 10, pady = 10)

        input_frame = tk.Frame(self.labelframe)

        #submit button
        submit_button = tk.Button(self.labelframe, text = "submit", width = 15, bg = "lightgray")

        #labels
        var_label = tk.Label(input_frame, text = "var:")
        value_label = tk.Label(input_frame, text = "value:")
        func_label = tk.Label(input_frame, text = "f(x):")

        #Entries and combobox
        self.var_entry = tk.Entry(input_frame)
        self.var_entry.bind("<Key>", self.__var_label_key_pressed)

        value_entry = tk.Entry(input_frame)    
        func_combobox = ttk.Combobox(input_frame, 
                                    values = ("MOVE", "ROTATE", "SAVE", "LOAD"),
                                    width = 17)
        
        #Placement
        var_label.grid(column = 0, row = 0, pady = 5)
        func_label.grid(column = 0, row = 1, pady = 5)
        value_label.grid(column = 0, row = 2, pady = 5)

        self.var_entry.grid(column = 1, row = 0)
        func_combobox.grid(column = 1, row = 1)
        value_entry.grid(column = 1, row = 2)
        
        input_frame.grid(column = 0, row = 0, pady = 5)

        submit_button.grid(column = 0, row = 3)

        self.labelframe.pack()
    
    def __var_label_key_pressed(self, keyinfo):
        
        if len(self.var_entry.get()) > 0:
            self.var_entry.delete(0, tk.END)    

class VariablesTreeview(tk.Frame):
    
    def __init__(self, master = None, **kw):
        super().__init__(master, **kw)

        self.__initialize_sub_widgets()

    def __initialize_sub_widgets(self):
        
        #Treeview
        self.treeview = ttk.Treeview(self, columns = ["var", "function", "value"], show = "headings")
        self.treeview.heading("var", text = "var")
        self.treeview.heading("function", text = "f(x)")
        self.treeview.heading("value", text = "value")
        
        #Placement
        self.treeview.pack()
    



app = tk.Tk()

variables = VariableInputs(app)
variables.pack()
treeview = VariablesTreeview(app)
treeview.pack()

app.mainloop()