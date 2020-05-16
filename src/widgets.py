'''
Holds special widgets used in the 
application.
'''

import tkinter as tk
import tkinter.colorchooser as colorchooser
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
            self["bg"] = "#ffffff"
        else:
            self["bg"] = "#ffaaaa"

class ColorPaletteOptions(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        
        self._MAX_PALETTE_SIZE = 9

        self._colors = ["#ffffff"]

        #Setup frames
        self.buttons_frame_left = tk.Frame(self)
        self.buttons_frame_right = tk.Frame(self)

        #Setup color canvas - 291 px, height: 46
        self.colors_canvas = tk.Canvas(self,  
            height = 40, 
            relief = tk.GROOVE,
            borderwidth = 4)

        #Setup labels

        #Setup buttons
        self.add_button = tk.Button(
            self.buttons_frame_left, 
            text = "Add",
            command = self.on_add_button_click)
            
        self.remove_button = tk.Button(self.buttons_frame_left, text = "Remove")

        self.randomize_button = tk.Button(
            self.buttons_frame_right, 
            text = "Randomize",
            command = self.on_randomize_button_click)

        self.clear_button = tk.Button(self.buttons_frame_right, text = "Clear")

        #Placement
        self.colors_canvas.pack(fill = tk.X, padx = 10, pady = (5, 2))
        self.buttons_frame_left.pack(side = tk.LEFT, padx = 10, pady = 5)
        self.buttons_frame_right.pack(side = tk.RIGHT, padx = 10, pady = 5)
        
        self.add_button.grid(column = 0, row = 0, padx = (0, 3))
        self.remove_button.grid(column = 1, row = 0)

        self.randomize_button.grid(column = 0, row = 0, padx = (0, 3))
        self.clear_button.grid(column = 1, row = 0)
        

        self._draw_colors_canvas()

    def _draw_colors_canvas(self):

        color_quad_length = 288 / len(self._colors) #TODO: fix magic numbers for width & height

        #Horrible magic numbers that need fixing here
        for index, color in enumerate(self._colors):
            self.colors_canvas.create_rectangle(
                3 + index * color_quad_length, 0,           #x1, y1
                3 + (index + 1) * color_quad_length, 46,    #x2, y2
                fill = self._colors[index],
                width = 0)

    def remove_color(self, index):
        self._colors.remove(self._colors[index])
        self._draw_colors_canvas()

    def reset_colors(self):
        self._colors.clear()
        self._draw_colors_canvas()            

    def generate_random_palette(self, amount):
        '''
        Generate a new random color palette
        '''
        self._colors.clear()
        for _ in range(util.clamp_number_between(1, self._MAX_PALETTE_SIZE, amount)):
            self._colors.insert(len(self._colors), util.get_random_color_hex_string())

    def pick_color(self):
        return colorchooser.askcolor()

    #Event functions

    def on_randomize_button_click(self):
        self.generate_random_palette(len(self._colors))
        self._draw_colors_canvas()

    def on_add_button_click(self):
        if len(self._colors) < self._MAX_PALETTE_SIZE:
            color = self.pick_color()
            if color != None:
                self._colors.append(color[1])
                self._draw_colors_canvas()

