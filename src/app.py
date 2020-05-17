import tkinter as tk
import tkinter.ttk as ttk
import widgets
import lsystem as lsys
import utilities as util
import os

#Get current working directory
cwd = os.path.split(os.getcwd())[0]

class VariablesFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Internal data
        self._symbols = []

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
        self.variable_entry = widgets.NonNumberEntry(self.input_frame, 1, width = 6)
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

    def insert_symbol(self, symbol, op, default_val = None):
        self.treeview._insert_row((symbol, op, default_val))
        self._symbols[symbol] = (util.op_conversion_dict[op], default_val)


    def load_defaults_button_clicked_event(self, args):
        '''
        Loads the default symbol settings to the symbol treeview
        '''
        #Clear symbols first, so it won't append
        self._symbols.clear()

        #Insert each symbol into treeview and symbols dict
        self._symbols.append(("F", "Move pen down"))
        self._symbols.append(("G", "Move pen up"))
        self._symbols.append(("+", "Turn right"))
        self._symbols.append(("-", "Turn left"))
        self._symbols.append(("!", "Switch turn directions"))
        self._symbols.append(("@", "Multiply step", 0.6))
        self._symbols.append(("[", "Save state"))
        self._symbols.append(("]", "Load state"))
        self._symbols.append(("<", "Color up", 1))
        self._symbols.append((">", "Color down", 1))
        self._symbols.append(("%", "Color set"))
        self._symbols.append(("(", "Thickness up", 1))
        self._symbols.append((")", "Thickness down", 1))
        self._symbols.append(("&", "Thickness set"))

        self.treeview.update_rows(self._symbols)

        #Clear entries for text
        self.clear_entries()

        #Set focus on frame again
        self.focus_set()

    def clear_entries(self):
        self.variable_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
        self.operation_combobox.set("")

    def get_symbols(self):

        #Convert to dictionary first
        dictionary = {}
        for symbol in self._symbols:
            dictionary[symbol[0]] = (util.op_conversion_dict[symbol[1]], symbol[2] if len(symbol) > 2 else None)
        
        return dictionary


class RulesFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Internal data
        self._rules = []

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
        self.add_button = tk.Button(
            self.buttons_frame, 
            text = "Add",
            state = tk.DISABLED,
            command = self.on_add_button_click)

        self.edit_button = tk.Button(
            self.buttons_frame,
            text = "Edit",
            state = tk.DISABLED,
            command = self.on_edit_button_click)

        self.delete_button = tk.Button(
            self.buttons_frame,
            text = "Delete",
            state = tk.DISABLED,
            command = self.on_delete_button_click)

        #Setup entries
        self.variable_entry = widgets.NonNumberEntry(self.entries_frame, 1, width = 2)
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

        #Setup event bindings
        self.treeview.treeview.bind("<<TreeviewSelect>>", self.on_treeview_selection)
        self.variable_entry.bind("<KeyRelease>", self.on_var_entry_keyrelease, add = "+")
        self.mutation_entry.bind("<KeyRelease>", self.on_mutation_entry_keyrelease, add = "+")

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
        self.edit_button.grid(column = 1, row = 0, padx = (0, 3))
        self.delete_button.grid(column = 2, row = 0)

    def update_add_button_state(self):

        var_exists = False
        current_var = self.variable_entry.get()
        
        #Check if current variable already exists in rules list
        for rule in self._rules:
            if current_var == rule[0]:
                var_exists = True

                #Enable the edit button
                self.edit_button["state"] = tk.NORMAL


        #If both variable and mutation entry has text and are legit
        if (len(self.variable_entry.get()) > 0 and self.variable_entry.is_legit() and
            len(self.mutation_entry.get()) > 0) and not var_exists:
            self.add_button["state"] = tk.NORMAL
        else:
            self.add_button["state"] = tk.DISABLED
            

    def insert_rule(self, var, mutation):
        self._rules.append((var, mutation))
        self.treeview.update_rows(self._rules)

    def delete_rule(self, index):
        self._rules.remove(self._rules[index])
        self.treeview.update_rows(self._rules)
        
    def get_rules(self):
        return self._rules

    def reenter_selected_in_entries(self):
        #Get iid from treeview focus and retrieve values tuple
        selected_iid = self.treeview.treeview.focus()
        values = self.treeview.treeview.item(selected_iid)["values"]

        #Delete text already in entries
        self.variable_entry.delete(0, tk.END)
        self.mutation_entry.delete(0, tk.END)

        #Insert selected values in entries
        self.variable_entry.insert(0, values[0])
        self.mutation_entry.insert(0, values[1])
    
    def clear_entries(self):
        self.variable_entry.delete(0, tk.END)
        self.mutation_entry.delete(0, tk.END)


    #Event functions

    def on_treeview_selection(self, event):
        #Add selected values in entries again & 
        #update delete button state
        self.reenter_selected_in_entries()
        self.delete_button["state"] = tk.NORMAL

    def on_add_button_click(self):
        #Add variable and mutation to treeview
        self.insert_rule(self.variable_entry.get(), self.mutation_entry.get())

        #Clear entries
        self.clear_entries()

        #Update add button state
        self.update_add_button_state()

        #Set focus on var entry
        self.variable_entry.focus_set()
    
    def on_edit_button_click(self):

        #Disable the edit button
        self.edit_button["state"] = tk.DISABLED

        #Get variable name and mutation to edit
        var_edit = self.variable_entry.get()
        mutation_edit = self.mutation_entry.get()

        #Find index of variable in rules and change it's value
        for i, rule in enumerate(self._rules):
            if rule[0] == var_edit:
                self._rules[i] = (var_edit, mutation_edit)
                break
        
        #Refresh the treeview with new updated rules list
        self.treeview.update_rows(self._rules)

        #Clear entries
        self.clear_entries()

        #Remove focus from entries by focusing on frame
        self.focus_set()

        
    def on_delete_button_click(self):
        #Get selected item so we can get the index of the selected item afterwards
        selected_item = self.treeview.treeview.focus()
        selected_index = self.treeview.treeview.index(selected_item)
        
        #Delete the selected item
        self.delete_rule(selected_index)

        self.delete_button["state"] = tk.DISABLED
        self.clear_entries()

    def on_var_entry_keyrelease(self, event):
        if len(self.variable_entry.get()) == 1 and self.variable_entry.is_legit():
            self.mutation_entry.focus_set()

        self.update_add_button_state()

    def on_mutation_entry_keyrelease(self, event):
        self.update_add_button_state()

class SettingsFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup frames
        self.label_frame = tk.LabelFrame(
            self, 
            text = "Settings", 
            font = ("", 12),
            pady = 5)

        self.color_palette_label_frame = tk.LabelFrame(
            self.label_frame,
            text = "Color palette",
            font = ("", 12))
        
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
        self.start_color_label = tk.Label(self.input_frame, text = "Start color:")

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
            state = "readonly",
            cursor = "arrow")

        self.line_thickness_spinbox = tk.Spinbox(
            self.input_frame, 
            width = 8,
            from_ = 1,
            to = 100,
            state = "readonly",
            cursor = "arrow")

        self.step_length_entry = widgets.NumberEntry(self.input_frame, width = 8)
        self.start_color_entry = widgets.NumberEntry(self.input_frame, 3, width = 8)

        #Setup ColorPaletteOptions
        self.color_palette_options = widgets.ColorPaletteOptions(self.color_palette_label_frame)

        #Insert default entry values
        self.position_x_entry.insert(0, 0)
        self.position_y_entry.insert(0, 0)
        self.angle_entry.insert(0, 90)
        self.turn_angle_entry.insert(0, 45)
        self.step_length_entry.insert(0, 25)
        self.start_color_entry.insert(0, 0)

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

        self.iteration_label.grid(column = 2, row = 0, sticky = tk.W, padx = (10, 0), pady = (0, 5))
        self.line_start_thickness_label.grid(column = 2, row = 1, sticky = tk.W, padx = (10, 0), pady = (0, 5))
        self.step_length_label.grid(column = 2, row = 2, sticky = tk.W, padx = (10, 0), pady = (0, 5))
        self.start_color_label.grid(column = 2, row = 3, sticky = tk.W, padx = (10, 0), pady = (0, 5))

        self.iteration_spinbox.grid(column = 3, row = 0, pady = (0, 5))
        self.line_thickness_spinbox.grid(column = 3, row = 1, pady = (0, 5))
        self.step_length_entry.grid(column = 3, row = 2, pady = (0, 5))
        self.start_color_entry.grid(column = 3, row = 3, pady = (0, 5))

        self.color_palette_label_frame.pack(fill = tk.X, padx = 5)
        self.color_palette_options.pack(fill = tk.X)

    def get_color_palette(self):
        return self.color_palette_options._colors

    def get_settings_dict(self):
        return {
            "axiom" : self.axiom_entry.get(),
            "pos_x" : float(self.position_x_entry.get()),
            "pos_y" : float(self.position_y_entry.get()),
            "angle" : int(self.angle_entry.get()),
            "turn_angle" : int(self.turn_angle_entry.get()),
            "iteration" : int(self.iteration_spinbox.get()),
            "line_thickness" : int(self.line_thickness_spinbox.get()),
            "step_length" : int(self.step_length_entry.get()),
            "start_color" : int(self.start_color_entry.get())
        }

class DrawButtonFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup draw button icon
        icon_image = tk.PhotoImage(file = cwd + r"\resources\drawing-button.png")

        #Setup button
        self.draw_button = tk.Button(
            self,
            font = ("", 14, "bold"),
            bg = "grey",
            fg = "white",
            image = icon_image,
            compound = tk.RIGHT,
            command = self.on_draw_button_click)

        self.draw_button.image = icon_image

        #Placement
        self.draw_button.pack(fill = tk.BOTH, expand = True, padx = 5, pady = (5, 0))

    def on_draw_button_click(self):

        #Gather information for drawing
        symbols = variables_frame.get_symbols()
        rules = rules_frame.get_rules()
        settings = settings_frame.get_settings_dict()
        colors = settings_frame.get_color_palette()

        #Initialize lsystem object
        lsystem = lsys.LSystem(settings["axiom"], rules)

        #Don't exactly know why im iterating the lsystem like this?
        for _ in range(settings["iteration"]):
            next(lsystem)
        
        #Clear canvas before drawing
        drawing_frame.draw_canvas.clear_canvas()

        lsys.draw_lsystem(
            drawing_frame.draw_canvas, 
            str(lsystem), 
            symbols,
            (settings["pos_x"], settings["pos_y"]),
            settings["angle"],
            settings["turn_angle"],
            settings["step_length"],
            settings["line_thickness"],
            colors,
            settings["start_color"])

class CanvasFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup draw canvas
        self.draw_canvas = widgets.DrawingCanvas(self, bg = "#212121")

        #Placement
        self.draw_canvas.pack(fill = tk.BOTH, expand = True)

app = tk.Tk()
app.title("Lindenmayer Systems Illustrator")
app.geometry("1150x770")
app.resizable(0,0)

#Setup main frames
control_frame = tk.Frame(app, padx = 5, pady = 5)
drawing_frame = CanvasFrame(app)

#Setup widgets
variables_frame = VariablesFrame(control_frame)
rules_frame = RulesFrame(control_frame)
settings_frame = SettingsFrame(control_frame)
draw_button_frame = DrawButtonFrame(control_frame)

#Placement
control_frame.place(relx = 0, rely = 0, relwidth = 0.3, relheight = 1)
drawing_frame.place(relx = 0.3, rely = 0, relwidth = 0.7, relheight = 1)

variables_frame.pack(fill = tk.X)
rules_frame.pack(fill = tk.X)
settings_frame.pack(fill = tk.X)
draw_button_frame.pack(fill = tk.BOTH, expand = True)

app.mainloop()