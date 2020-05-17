'''
Holds special widgets used in the 
application.
'''

import tkinter as tk
import tkinter.colorchooser as colorchooser
import tkinter.ttk as ttk
import utilities as util
import math 

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

    def update_rows(self, row_list):
        #Delete everything and insert list
        self.__clear_rows()
        for row in row_list:
            self.__insert_row(row)

    def __insert_row(self, values):
        self.treeview.insert("", tk.END, values = values)

    def __clear_rows(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)
    
    def get_row_values(self):
        rows = []
        for row in self.treeview.get_children():
            rows.append(self.treeview.item(row)["values"])
        return rows

class Entry(tk.Entry):
    def __init__(self, master = None, max_chars = None, **kw):
        super().__init__(master=master, **kw)

        self._max_chars = max_chars

        self.configure(
            font = ("", 9), 
            relief = tk.FLAT,
            highlightthickness = 1,
            highlightbackground = "gray")

        self.bind("<KeyRelease>", self.on_entry_keyrelease)

    def on_entry_keyrelease(self, event):
        
        if self._max_chars != None and len(self.get()) > self._max_chars:
            self.delete(self._max_chars, tk.END)


class NumberEntry(Entry):
    def __init__(self, master = None, max_chars = None, **kw):
        super().__init__(master=master, max_chars = max_chars, **kw)

        self.bind("<KeyRelease>", self.on_number_entry_keyrelease, add = "+")

    def on_number_entry_keyrelease(self, event):
        '''
        Checks if the value entry text can be converted to a number.
        If not it highlights the value entry background with red.
        '''
        value = self.get()
        if util.is_str_digit(value) or value == "":
            self["bg"] = "#ffffff"
        else:
            self["bg"] = "#ffaaaa"

class NonNumberEntry(Entry):
    def __init__(self, master=None, max_chars = None, **kw):
        super().__init__(master=master, max_chars = max_chars, **kw)

        self._is_legit = True

        self.bind("<KeyRelease>", self.on_non_number_entry_keyrelease, add = "+")

    def on_non_number_entry_keyrelease(self, event):
        
        value = self.get()
        if util.is_str_digit(value) or value == " ":
            self["bg"] = "#ffaaaa"
            self._is_legit = False
        else:
            self["bg"] = "#ffffff"
            self._is_legit = True

    def is_legit(self):
        return self._is_legit


class ColorPaletteOptions(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        
        self._MAX_PALETTE_SIZE = 9
        self._DEFAULT_COLOR = "#ffffff"

        self._colors = ["#ffffff"]

        #Setup frames
        self.buttons_frame_left = tk.Frame(self)
        self.buttons_frame_right = tk.Frame(self)

        #Setup color canvas - 291 px, height: 46
        self.colors_canvas = tk.Canvas(self,  
            height = 40, 
            relief = tk.GROOVE,
            borderwidth = 4,
            cursor = "hand2")

        #Setup buttons
        self.add_button = tk.Button(
            self.buttons_frame_left, 
            text = "Add",
            command = self.on_add_button_click)

        self.remove_button = tk.Button(
            self.buttons_frame_left, 
            text = "Remove",
            command = self.on_remove_button_click)

        self.randomize_button = tk.Button(
            self.buttons_frame_right, 
            text = "Randomize",
            command = self.on_randomize_button_click)

        self.clear_button = tk.Button(
            self.buttons_frame_right, 
            text = "Clear",
            command = self.on_clear_button_click)

        #Setup event bindings
        self.colors_canvas.bind("<Button-1>", self.on_color_canvas_click)

        #Placement
        self.colors_canvas.pack(fill = tk.X, padx = 10, pady = (5, 2))
        self.buttons_frame_left.pack(side = tk.LEFT, padx = 10, pady = 5)
        self.buttons_frame_right.pack(side = tk.RIGHT, padx = 10, pady = 5)
        
        self.add_button.grid(column = 0, row = 0, padx = (0, 3))
        self.remove_button.grid(column = 1, row = 0)

        self.randomize_button.grid(column = 0, row = 0, padx = (0, 3))
        self.clear_button.grid(column = 1, row = 0)
        

        self.redraw_color_canvas()

    def redraw_color_canvas(self):

        color_quad_length = 288 / len(self._colors) #TODO: fix magic numbers for width & height

        #Horrible magic numbers that need fixing here
        for index, color in enumerate(self._colors):
            self.colors_canvas.create_rectangle(
                3 + index * color_quad_length, 0,           #x1, y1
                3 + (index + 1) * color_quad_length, 51,    #x2, y2
                fill = self._colors[index],
                width = 0)

    def remove_color_from_palette(self, index):
        self._colors.remove(self._colors[index])

    def clear_palette(self):
        self._colors.clear()
        self._colors.append(self._DEFAULT_COLOR)

    def randomize_palette(self, amount):
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
        self.randomize_palette(len(self._colors))
        self.redraw_color_canvas()

    def on_add_button_click(self):
        #If palette has less than 9 colors
        if len(self._colors) < self._MAX_PALETTE_SIZE:

            #Open color dialog and return result
            color = self.pick_color()

            #If color result is not None, append color to colors and redraw 
            if color[0] != None:
                self._colors.append(color[1])
                self.redraw_color_canvas()

    def on_remove_button_click(self):
        #If palette has more than one color
        if len(self._colors) > 1:
            self.remove_color_from_palette(len(self._colors) - 1)
            self.redraw_color_canvas()       
    
    def on_clear_button_click(self):
        self.clear_palette()
        self.redraw_color_canvas()

    def on_color_canvas_click(self, event):
        color_index = math.floor(event.x / (296 / len(self._colors)))
        new_color = self.pick_color()

        if new_color[0] != None:
            self._colors[color_index] = new_color[1]
            self.redraw_color_canvas()


class DrawingCanvas(tk.Canvas):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        # x = 800, y = 766

        self._FOREGROUND_COLOR = "#ffffff"
        self._SHADOW_COLOR = "#000000"

        self.draw_coordination_help()

    def clear_canvas(self):
        self.delete(tk.ALL)
    
    def draw_coordination_help(self):
        '''
        Draw coordination and rotation info on canvas
        '''
        #Magic numbers everywhere until I can figure out how to update ui positions before
        #these these functions are called

        #Draw coordinate
        self.__draw_text(32, 15, ("-1, -1", 13, "bold"))
        self.__draw_text(775, 15, ("1, -1", 13, "bold"))
        self.__draw_text(32, 750, ("-1, 1", 13, "bold"))
        self.__draw_text(775, 750, ("1, 1", 13, "bold"))

    
        #Draw angle info
        graphics_len = 60

        self.create_oval(
            400 - graphics_len, 383 - graphics_len, 400 + graphics_len, 383 + graphics_len,
            outline = self._FOREGROUND_COLOR)

        self.create_line(
            400, 383, 400 + graphics_len, 383, 
            width = 1, 
            fill = self._FOREGROUND_COLOR)

        self.create_line(
            400, 383 - graphics_len, 400, 383, 
            width = 1, 
            fill = self._FOREGROUND_COLOR)

        self.__draw_text(400 + graphics_len + 12, 383, ("0°", 10, "normal"), False)
        self.__draw_text(400, 383 - graphics_len - 12, ("90°", 10, "normal"), False)

    def __draw_text(self, x, y, text_options, shadow = True):
        
        if shadow:
            self.create_text(
                x + 3, y + 3, 
                text = text_options[0], 
                font = ("", text_options[1], text_options[2]),
                fill = self._SHADOW_COLOR)
        
        self.create_text(
            x, y, 
            text = text_options[0], 
            font = ("", text_options[1], text_options[2]),
            fill = self._FOREGROUND_COLOR)
            
