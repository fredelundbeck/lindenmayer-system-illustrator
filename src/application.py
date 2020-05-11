import tkinter as tk
import tkinter.ttk as ttk
import re as regex
import utilities as util

class VariablesFrame(tk.Frame):
    '''
    This frame holds the entries & submit button widgets for the variables list.
    '''
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
        self.submit_button = tk.Button(self.submit_frame, 
                                        text = "submit", 
                                        width = 21, state = tk.DISABLED,
                                        command = self.submit_button_clicked_event)

        #Event bindings
        self.func_combobox.bind("<<ComboboxSelected>>", self.func_selection_event)
        self.func_combobox.bind("<<ComboboxSelected>>", self.update_submit_button_state, add = "+")
        self.var_entry.bind("<KeyRelease>", self.var_key_released_event)
        self.var_entry.bind("<KeyRelease>", self.update_submit_button_state, add = "+")
        self.val_entry.bind("<KeyRelease>", self.val_key_released_event)
        self.val_entry.bind("<KeyRelease>", self.update_submit_button_state, add = "+")

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

    def set_instances(self, variable_treeview_frame, rules_frame):
        self.var_treeview_obj = variable_treeview_frame
        self.rules_frame_obj = rules_frame
    
    def var_key_released_event(self, args):
        '''
        Checks if entry has more than one char,
        if it has delete everything but the first char.
        '''
        if len(self.var_entry.get()) > 1:
            self.var_entry.delete(1, tk.END)

    def func_selection_event(self, args):
        '''
        Checks whether LOAD or SAVE has been selected,
        if it has then disable the val_entry else enable it.
        '''
        item = self.func_combobox.get()
        if item == "Save" or item == "Load":
            self.val_entry.delete(0, tk.END)
            self.val_entry["state"] = tk.DISABLED
        else:
            self.val_entry["state"] = tk.NORMAL
    
    def val_key_released_event(self, args):
        '''
        Checks if the value entry text can be converted to a number.
        If not it highlights the value entry background with red.
        '''
        value = self.val_entry.get()
        if util.isdigit(value) or value == "":
            self.val_entry["bg"] = "#FFFFFF"
        else:
            self.val_entry["bg"] = "#FFAAAA"
    
    def update_submit_button_state(self, args):
        '''
        Checks if all requirements are met to enable the submit button.
        The requirements are:
        1.  That both the variable & value entries length must exceed 0. 
        2.  The function combobox must have a selected item.
        '''
        var_length = len(self.var_entry.get())
        func_item = self.func_combobox.get()
        val_isdigit = util.isdigit(self.val_entry.get())

        if var_length > 0 and func_item != "" and (val_isdigit or func_item in ["Save", "Load"]):
            self.submit_button["state"] = tk.NORMAL
        else:
            self.submit_button["state"] = tk.DISABLED
    
    def submit_button_clicked_event(self):
        '''
        Inserts the variable data (var-name, func, value) to the variable list widget.
        '''
        var = self.var_entry.get()
        func = self.func_combobox.get()
        val = self.val_entry.get()

        self.var_treeview_obj.insert_variable(var, func, val)
        self.rules_frame_obj.update_combobox_values()

class VariableTreeViewFrame(tk.Frame):
    '''
    This frame holds the treeview that displays all the variables. Also,
    it holds buttons for deleting or editing functionality.
    '''
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup frames
        self.treeview_frame = tk.Frame(self)
        self.buttons_frame = tk.Frame(self)

        #Setup buttons
        self.remove_button = tk.Button(self.buttons_frame, 
                                        text = "remove", 
                                        state = tk.DISABLED,
                                        command = self.remove_button_clicked_event)
        self.edit_button = tk.Button(self.buttons_frame, 
                                        text = "edit", 
                                        state = tk.DISABLED,
                                        command = self.edit_button_clicked_event)

        #Setup treeview
        self.treeview = ttk.Treeview(self.treeview_frame, 
                                        columns = ["var", "function", "value"], 
                                        show = "headings",
                                        selectmode = "browse",
                                        height = 5)
        self.treeview.heading("var", text = "var")
        self.treeview.heading("function", text = "f(x)")
        self.treeview.heading("value", text = "value")

        #Setup treeview vertical scrollbar
        self.treeview_scrollbar = tk.Scrollbar(self.treeview_frame, 
                                                orient = tk.VERTICAL, 
                                                command = self.treeview.yview)
        self.treeview.configure(yscrollcommand = self.treeview_scrollbar.set)

        #Event bindings
        self.treeview.bind("<<TreeviewSelect>>", self.treeview_item_selected_event)

        #Adjust grid weights
        self.treeview_frame.columnconfigure(0, weight = 1)
        self.treeview_frame.columnconfigure(1, weight = 0)

        #Placement
        self.treeview_frame.pack(padx = 5, pady = 5)
        self.buttons_frame.pack(padx = 5, pady = (0, 5), fill = tk.X)

        self.treeview.grid(column = 0, row = 0, sticky = tk.W + tk.E)
        self.treeview_scrollbar.grid(column = 1, row = 0, sticky = tk.N + tk.S + tk.W + tk.E)

        self.remove_button.grid(column = 0, row = 0, padx = (0, 5))
        self.edit_button.grid(column = 1, row = 0)

    def set_instances(self, rules_frame):
        self.rules_frame_obj = rules_frame

    def insert_variable(self, var, func, val):
        '''
        Inserts the given parameters into the treeview
        '''
        self.treeview.insert("", tk.END, values = [var, func, val])

    def change_buttons_states(self, state):
        '''
        Changes both the remove & edit buttons states to the given state argument
        '''
        self.remove_button["state"] = state
        self.edit_button["state"] = state

    def treeview_item_selected_event(self, args):
        '''
        If an item from the treeview is selected the delete & edit buttons state
        will be set to NORMAL, making them able to be clicked.
        '''
        self.change_buttons_states(tk.NORMAL)

    def remove_button_clicked_event(self):
        '''
        First the function removes the selected item/variable from the treeview.
        After that it changes the state of both the buttons - remove & edit - to disabled.
        '''
        selected_item = self.treeview.selection()[0]
        self.treeview.delete(selected_item)
        self.change_buttons_states(tk.DISABLED)

        self.rules_frame_obj.update_combobox_values()

    def edit_button_clicked_event(self):
        '''
        Open a temporary window with widgets to edit the selected item/variable
        from the treeview.
        '''
        pass

    def get_tree_rows_data(self, column_index):
        '''
        Returns all the data from the specified column name, from the treeview. 
        '''
        data = []
        for child in self.treeview.get_children():
            data.append(self.treeview.item(child)["values"][column_index])
        return data
    

class RulesFrame(tk.Frame):
    def __init__(self, master = None, **kw):
        super().__init__(master = master, **kw)

        #Setup frames
        self.labelframe = tk.LabelFrame(self, text = "Rules", font = ("", 9, "bold"))
        self.list_frame = tk.Frame(self)

        #Setup entries
        self.var_combobox = ttk.Combobox(self.labelframe, state = "readonly")

        #Setup buttons

        #Setup event bindings

        #Placement
        self.labelframe.pack(padx = 5, pady = 5, ipadx = 5, ipady = 5)

        self.var_combobox.pack()

    def set_instances(self, variable_treeview_frame):
        self.var_treeview_obj = variable_treeview_frame

    def update_combobox_values(self):
        '''
        Updates the values of the variable combobox to match the var names in the
        variable list.
        '''
        vars = set(self.var_treeview_obj.get_tree_rows_data(0))
        cbox_text = self.var_combobox.get()

        if cbox_text != "" and cbox_text not in vars:
            self.var_combobox.set("")
        if len(vars) == 0:
            self.var_combobox["values"] = ""
            self.var_combobox.set("")
        else:
            self.var_combobox["values"] = list(vars)
    
        



app = tk.Tk()

#declare widgets
varlist = VariableTreeViewFrame(app)
varinput = VariablesFrame(app)
rules = RulesFrame(app)

#Set instance binding
varlist.set_instances(rules)
varinput.set_instances(varlist, rules)
rules.set_instances(varlist)

#pack test
varinput.pack()
varlist.pack()
rules.pack()

app.mainloop()