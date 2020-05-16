import tkinter as tk
import tkinter.ttk as ttk
import widgets

class VariablesFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup frames
        self.label_frame = tk.LabelFrame(
            self,
            text = "Symbols",
            font = ("", 12),
            padx = 0,
            pady = 5)
        
        self.input_frame = tk.Frame(self.label_frame)
        self.buttons_frame = tk.Frame(self.label_frame)

        #Setup label
        self.variable_label = tk.Label(self.input_frame, text = "Var:")
        self.value_label = tk.Label(self.input_frame, text = "Default:")
        self.operation_label = tk.Label(self.input_frame, text = "f(x):")

        #Setup entries
        self.variable_entry = widgets.Entry(self.input_frame, width = 6)
        self.value_entry = widgets.NumberEntry(self.input_frame, width = 6)
        self.operation_combobox = ttk.Combobox(
            self.input_frame,
            values = ["Move pen down", "Move pen up", "Turn right", "Turn left", "Multiply step", 
                "Color up", "Color down", "Color set", "Switch turn directions", 
                "Thickness up", "Thickness down", "Thickness set", "Save state", "Load state"],
            state = "readonly")

        #Setup buttons
        self.add_button = tk.Button(self.buttons_frame, text = "Add", state = tk.DISABLED)
        self.delete_button = tk.Button(self.buttons_frame, text = "Delete", state = tk.DISABLED)
        self.load_defaults_button = tk.Button(self.buttons_frame, text = "Load defaults")

        #Setup treeview
        self.treeview = widgets.ScrollableTreeviewFrame(self.label_frame)
        self.treeview.configure_treeview(
            columns = ["sym", "op", "def"],
            show = "headings",
            selectmode = "browse",
            height = 6)
        
        self.treeview.modify_heading("sym", text = "Symbol")
        self.treeview.modify_heading("op", text = "Operation")
        self.treeview.modify_heading("def", text = "Default")
        self.treeview.modify_column("sym", minwidth = 30, width = 10)
        self.treeview.modify_column("op", minwidth = 30, width = 100)
        self.treeview.modify_column("def", minwidth = 30, width = 30)

        #Setup binding events
        self.load_defaults_button.bind("<Button-1>", self.load_defaults_button_clicked_event)

        #Placement
        self.label_frame.pack(fill = tk.BOTH)

        self.treeview.pack(fill = tk.X, padx = 5, pady = (5, 0))

        self.input_frame.pack(side = tk.LEFT, padx = 5, pady = (5, 0))
        self.variable_label.grid(column = 0, row = 0)
        self.variable_entry.grid(column = 1, row = 0)
        self.value_label.grid(column = 2, row = 0)
        self.value_entry.grid(column = 3, row = 0)
        self.operation_label.grid(column = 0, row = 1, pady = 5)
        self.operation_combobox.grid(column = 1, row = 1, columnspan = 3)

        self.buttons_frame.pack(side = tk.RIGHT, anchor = tk.N, padx = 5, pady = 5)
        self.add_button.grid(column = 0, row = 0, padx = (0, 3))
        self.delete_button.grid(column = 1, row = 0)
        self.load_defaults_button.grid(column = 0, row = 1, columnspan = 2, pady = (4, 0))

    def load_defaults_button_clicked_event(self, args):
        '''
        Loads the default symbol settings to the symbol treeview
        '''
        #Clear treeview first, so the settings aren't appended
        self.treeview.clear_rows()

        #Insert each symbol into treeview
        self.treeview.insert_row(("F", "Move pen down"))
        self.treeview.insert_row(("G", "Move pen up"))
        self.treeview.insert_row(("+", "Turn right"))
        self.treeview.insert_row(("-", "Turn left"))
        self.treeview.insert_row(("!", "Switch turn directions"))
        self.treeview.insert_row(("@", "Multiply step", 0.6))
        self.treeview.insert_row(("[", "Save state"))
        self.treeview.insert_row(("]", "Load state"))
        self.treeview.insert_row(("<", "Color up", 1))
        self.treeview.insert_row((">", "Color down", 1))
        self.treeview.insert_row(("%", "Color set", 0))
        self.treeview.insert_row(("(", "Thickness up", 1))
        self.treeview.insert_row((")", "Thickness down", 1))
        self.treeview.insert_row(("&", "Thickness set", 0))

class RulesFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup frames
        self.label_frame = tk.LabelFrame(
            self, 
            text = "Rules", 
            font = ("", 12), 
            pady = 5)
        
        self.input_frame = tk.Frame(self.label_frame)
        self.entries_frame = tk.Frame(self.input_frame)
        self.buttons_frame = tk.Frame(self.input_frame)

        #Setup buttons
        self.add_button = tk.Button(self.buttons_frame, text = "Add", state = tk.DISABLED)
        self.delete_button = tk.Button(self.buttons_frame, text = "Delete", state = tk.DISABLED)

        #Setup entries
        self.variable_entry = widgets.Entry(self.entries_frame, width = 2)
        self.mutation_entry = widgets.Entry(self.entries_frame)

        #Setup labels
        self.var_label = tk.Label(self.entries_frame, text = "Var:")

        #Setup treeview
        self.treeview = widgets.ScrollableTreeviewFrame(self.label_frame)
        self.treeview.configure_treeview(
            columns = ["var", "mut"],
            show = "headings",
            selectmode = "browse",
            height = 4)

        self.treeview.modify_heading("var", text = "Variable")
        self.treeview.modify_heading("mut", text = "Mutation")
        self.treeview.modify_column("var", minwidth = 30, width = 0)
        self.treeview.modify_column("mut", minwidth = 30, width = 0)

        #Placement
        self.label_frame.pack(fill = tk.BOTH)
        self.treeview.pack(fill = tk.X, padx = 5, pady = (5, 0))
        self.input_frame.pack(fill = tk.X, padx = 5, pady = 5)

        self.entries_frame.pack(side = tk.LEFT)
        self.var_label.grid(column = 0, row = 0)
        self.variable_entry.grid(column = 1, row = 0, padx = (0, 5))
        self.mutation_entry.grid(column = 2, row = 0)

        self.buttons_frame.pack(side = tk.RIGHT)
        self.add_button.grid(column = 0, row = 0, padx = (0, 3))
        self.delete_button.grid(column = 1, row = 0)

class SettingsFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup frames
        self.label_frame = tk.LabelFrame(
            self, text = "Settings", 
            font = ("", 12),
            pady = 5)
        
        self.input_frame = tk.Frame(self.label_frame)

        #Setup labels
        self.axiom_label = tk.Label(self.input_frame, text = "Axiom:")
        self.position_x_label = tk.Label(self.input_frame, text = "Position X:")
        self.position_y_label = tk.Label(self.input_frame, text = "Position Y:")
        self.angle_label = tk.Label(self.input_frame, text = "Angle (deg):")
        self.turn_angle_label = tk.Label(self.input_frame, text = "Turn angle (deg):")

        self.iteration_label = tk.Label(self.input_frame, text = "Iterations:")
        self.line_start_thickness_label = tk.Label(self.input_frame, text = "Line thickness:")
        self.step_length_label = tk.Label(self.input_frame, text = "Step length:")

        #Setup entries
        self.axiom_entry = widgets.Entry(self.input_frame, width = 8)
        self.position_x_entry = widgets.NumberEntry(self.input_frame, width = 8)
        self.position_y_entry = widgets.NumberEntry(self.input_frame, width = 8)
        self.angle_entry = widgets.NumberEntry(self.input_frame, width = 8)
        self.turn_angle_entry = widgets.NumberEntry(self.input_frame, width = 8)

        var = tk.IntVar(value = 4)
        self.iteration_spinbox = tk.Spinbox(
            self.input_frame, 
            width = 8, 
            from_ = 1, 
            to = 10,
            textvariable = var,
            state = "readonly")

        self.line_thickness_spinbox = tk.Spinbox(
            self.input_frame, 
            width = 8,
            from_ = 1,
            to = 100,
            state = "readonly")

        self.step_length_entry = widgets.NumberEntry(self.input_frame, width = 8)

        #Insert default entry values
        self.position_x_entry.insert(0, 0)
        self.position_y_entry.insert(0, 0)
        self.angle_entry.insert(0, 90)
        self.turn_angle_entry.insert(0, 45)
        self.step_length_entry.insert(0, 25)

        #Placement
        self.label_frame.pack(fill = tk.BOTH)
        self.input_frame.pack(fill = tk.BOTH, padx = 5, pady = 5)

        self.axiom_label.grid(column = 0, row = 0, sticky = tk.W, pady = (0,5))
        self.position_x_label.grid(column = 0, row = 1, sticky = tk.W, pady = (0,5))
        self.position_y_label.grid(column = 0, row = 2, sticky = tk.W, pady = (0,5))
        self.angle_label.grid(column = 0, row = 3, sticky = tk.W, pady = (0,5))
        self.turn_angle_label.grid(column = 0, row = 4, sticky = tk.W, pady = (0,5))

        self.axiom_entry.grid(column = 1, row = 0, pady = (0,5))
        self.position_x_entry.grid(column = 1, row = 1, pady = (0,5))
        self.position_y_entry.grid(column = 1, row = 2, pady = (0,5))
        self.angle_entry.grid(column = 1, row = 3, pady = (0,5))
        self.turn_angle_entry.grid(column = 1, row = 4, pady = (0,5))

        self.iteration_label.grid(column = 2, row = 0, sticky = tk.W, padx = (10, 0), pady = (0,5))
        self.line_start_thickness_label.grid(column = 2, row = 1, sticky = tk.W, padx = (10, 0), pady = (0,5))
        self.step_length_label.grid(column = 2, row = 2, sticky = tk.W, padx = (10, 0), pady = (0,5))

        self.iteration_spinbox.grid(column = 3, row = 0, pady = (0, 5))
        self.line_thickness_spinbox.grid(column = 3, row = 1, pady = (0, 5))
        self.step_length_entry.grid(column = 3, row = 2, pady = (0, 5))




app = tk.Tk()
app.title("Lindenmayer Systems Illustrator")
app.geometry("1150x750")
app.resizable(0,0)

#Setup main frames
control_frame = tk.Frame(app, padx = 5, pady = 5)
drawing_frame = tk.Frame(app, bg = "#212121")

#Setup widgets
variables_frame = VariablesFrame(control_frame)
rules_frame = RulesFrame(control_frame)
settings_frame = SettingsFrame(control_frame)

#Placement
control_frame.place(relx = 0, rely = 0, relwidth = 0.3, relheight = 1)
drawing_frame.place(relx = 0.3, rely = 0, relwidth = 0.7, relheight = 1)

variables_frame.pack(fill = tk.X)
rules_frame.pack(fill = tk.X)
settings_frame.pack(fill = tk.X)

app.mainloop()