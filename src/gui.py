import tkinter as tk
import tkinter.ttk as ttk
import lsystem as lsys


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
        if len(self.var_entry.get()) > 0 and len(self.value_entry.get()) > 0 and self.func_combobox.get() != "":
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
        #Frame for treeview
        self.treeview_frame = tk.Frame(self)

        #Treeview
        self.treeview = ttk.Treeview(self.treeview_frame, 
                                    columns = ["var", "function", "value"], 
                                    show = "headings",
                                    height = 5)

        self.treeview.heading("var", text = "var")
        self.treeview.heading("function", text = "f(x)")
        self.treeview.heading("value", text = "value")

        #Buttons & frame
        self.buttons_frame = tk.Frame(self)
        self.delete_button = tk.Button(self.buttons_frame, 
                                        text = "delete", 
                                        command = self.delete_button_clicked_event)

        self.edit_button = tk.Button(self.buttons_frame, text = "edit")
        
        #Placement
        self.treeview_frame.pack()
        self.treeview.pack(padx = 5, pady = 5)


        self.buttons_frame.pack(fill = "x", padx = 5)
        self.delete_button.grid(column = 0, row = 0)
        self.edit_button.grid(column = 2, row = 0, padx = 3)

    
    def insert_variable(self, var, func, value):
        self.treeview.insert("", tk.END, values = (var, func, value))
    
    def delete_button_clicked_event(self):
        item = self.treeview.focus()
        if item != "":
            self.treeview.delete(item)

class StartRules(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.__initialize_sub_widgets()

    def __initialize_sub_widgets(self):

        #Widgets
        self.main_frame = tk.Frame(self)

        self.rules_list_frame = tk.Frame(self.main_frame, padx = 10)

        #Input label frame
        self.input_labelframe = tk.LabelFrame(self.main_frame, text = "Rules",
                                        font = ("", 9, "bold"), 
                                        padx = 10,
                                        pady = 10)
                                        
        self.input_frame = tk.Frame(self.input_labelframe, pady = 10)
        self.var_label = tk.Label(self.input_frame, text = "var:")
        self.var_entry = tk.Entry(self.input_frame, width = 5)
        self.equal_label = tk.Label(self.input_frame, text = "=")
        self.mutation_entry = tk.Entry(self.input_frame)
        self.add_button = tk.Button(self.input_labelframe, text = "add rule", width = 15)

        #Rules list
        self.rules_list = tk.Listbox(self.rules_list_frame, height = 7)

        #Placement
        self.main_frame.pack()

        self.input_labelframe.grid(column = 0, row = 0)
        self.rules_list_frame.grid(column = 1, row = 0)
        self.rules_list.pack()

        self.input_frame.pack()
        self.var_label.grid(column = 0, row = 0)
        self.var_entry.grid(column = 1, row = 0)
        self.equal_label.grid(column = 2, row = 0)
        self.mutation_entry.grid(column = 3, row = 0)
        self.add_button.pack()

class DrawFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup canvas
        self.canvas = tk.Canvas(self)

        #Placement
        self.canvas.pack()

    def draw_lsystem(self, axiom, variables, rules, iteration, start_rot = 0, start_pos = (0, 0)):

        self.clear_canvas()

        states = []
        system = lsys.LSystem(axiom, rules)
        for _ in iteration:
            next(system)

    def clear_canvas(self):
        self.canvas.delete(tk.ALL)

    def change_canvas_background(self, color):
        self.canvas["bg"] = color
        


        

app = tk.Tk()
variables = VariableInputs(app)
treeview = VariablesTreeview(app)

startrules = StartRules(app, pady = 10)
variables.pack()
treeview.pack()
startrules.pack()

app.mainloop()