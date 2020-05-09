import tkinter as tk
import tkinter.ttk as ttk

class VariableInputs(tk.Frame):
    
    def __init__(self, master = None, treeview = None, **kw):
        super().__init__(master, **kw)

        self.__initialize_sub_widgets()
    
    def __initialize_sub_widgets(self):
        
        #labelframe
        self.labelframe = tk.LabelFrame(self, text = "Variables", font = ("", 9, "bold"), padx = 10, pady = 10)

        input_frame = tk.Frame(self.labelframe)

        #submit button
        self.submit_button = tk.Button(self.labelframe, 
                                    text = "submit", 
                                    width = 15, 
                                    state = "disabled",
                                    command = self.__submit_button_clicked)

        #labels
        var_label = tk.Label(input_frame, text = "var:")
        value_label = tk.Label(input_frame, text = "value:")
        func_label = tk.Label(input_frame, text = "f(x):")

        #Entries and combobox
        self.var_entry = tk.Entry(input_frame)
        self.var_entry.bind("<KeyRelease>", self.__var_entry_key_pressed)

        self.value_entry = tk.Entry(input_frame)
        self.value_entry.bind("<KeyRelease>", self.__value_entry_key_pressed) 

        self.func_combobox = ttk.Combobox(input_frame, 
                                    values = ("MOVE", "ROTATE", "SAVE", "LOAD"),
                                    state = "readonly",
                                    width = 17)
        self.func_combobox.bind("<<ComboboxSelected>>", self.__func_combobox_picked)
        
        #Placement
        var_label.grid(column = 0, row = 0, pady = 5)
        func_label.grid(column = 0, row = 1, pady = 5)
        value_label.grid(column = 0, row = 2, pady = 5)

        self.var_entry.grid(column = 1, row = 0)
        self.func_combobox.grid(column = 1, row = 1)
        self.value_entry.grid(column = 1, row = 2)
        input_frame.grid(column = 0, row = 0, pady = 5)
        self.submit_button.grid(column = 0, row = 3)

        self.labelframe.pack()
    
    def __update_submit_button_state(self):
        
        if len(self.var_entry.get()) > 0 and len(self.value_entry.get()) > 0 and self.func_combobox.get() is not "":
            self.submit_button["state"] = "active"
        else:
            self.submit_button["state"] = "disabled"

    def __submit_button_clicked(self):

        treeview.insert_variable(self.var_entry.get(), self.func_combobox.get(), self.value_entry.get())
    
    def __func_combobox_picked(self, picked_args):

        self.__update_submit_button_state() 

    def __value_entry_key_pressed(self, keyinfo_args):

        self.__update_submit_button_state()
        
            

    def __var_entry_key_pressed(self, keyinfo_args):
        
        if len(self.var_entry.get()) > 0:
            self.var_entry.delete(1, tk.END)

        self.__update_submit_button_state()    

class VariablesTreeview(tk.Frame):
    
    def __init__(self, master = None, **kw):
        super().__init__(master, **kw)

        self.__initialize_sub_widgets()

    def __initialize_sub_widgets(self):
        
        self.treeview_frame = tk.Frame(self)
        #Treeview
        self.treeview = ttk.Treeview(self.treeview_frame, columns = ["var", "function", "value"], show = "headings")
        self.treeview.heading("var", text = "var")
        self.treeview.heading("function", text = "f(x)")
        self.treeview.heading("value", text = "value")

        #Buttons & frame
        self.buttons_frame = tk.Frame(self)
        self.delete_button = tk.Button(self.buttons_frame, text = "delete")
        self.edit_button = tk.Button(self.buttons_frame, text = "edit")
        
        #Placement
        self.treeview_frame.pack()
        self.treeview.pack(padx = 5, pady = 5)

        self.buttons_frame.pack(fill = "x", padx = 5, pady = 5)
        self.delete_button.grid(column = 0, row = 0)
        self.edit_button.grid(column = 2, row = 0, padx = 5)

    
    def insert_variable(self, var, func, value):

        self.treeview.insert("", tk.END, values = (var, func, value))
    



app = tk.Tk()

variables = VariableInputs(app)
variables.pack()
treeview = VariablesTreeview(app)
treeview.pack()

app.mainloop()