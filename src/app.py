import tkinter as tk
import tkinter.ttk as ttk

#constants
COLOR_MAIN        = "#adcbe3"
COLOR_MAIN_LIGHT  = "#e7eff6"
COLOR_MAIN_DARK   = "#4b86b4"
COLOR_MAIN_DARKER = "#2a4d69"

GENERAL_FONT_SIZE = 9

#### setup window ####
window = tk.Tk()
window.geometry("950x600")
window.title("Lindenmeyer Systems Illustrator")
window.resizable(0,0)
window["background"] = "black"


#### menubar ####

menubar = tk.Menu(window)
window.config(menu = menubar)

filemenu = tk.Menu(menubar, tearoff = 0)
filemenu.add_command(label = "Open")
filemenu.add_separator()
filemenu.add_command(label = "Save")
filemenu.add_command(label = "Save as")
filemenu.add_separator()
filemenu.add_command(label = "Exit", command = window.destroy)

settingsmenu = tk.Menu(menubar, tearoff = 0)
settingsmenu.add_command(label = "Edit settings")
settingsmenu.add_command(label = "Reset settings")

helpmenu = tk.Menu(menubar, tearoff = 0)
helpmenu.add_command(label = "About")

menubar.add_cascade(label = "File", menu = filemenu)
menubar.add_cascade(label = "Settings", menu = settingsmenu)
menubar.add_cascade(label = "Help", menu = helpmenu)

#### left frame ####

left_frame = tk.Frame(window)
left_frame["background"] = COLOR_MAIN_DARKER
left_frame.place(relx = 0, rely = 0, relwidth = 0.35, relheight = 1)

#### variables labelframe ####

var_labelframe = tk.LabelFrame(left_frame)
var_labelframe["text"] = "Variables"
var_labelframe["background"] = COLOR_MAIN_DARKER
var_labelframe["foreground"] = COLOR_MAIN_LIGHT
var_labelframe.place(relx = 0.01, rely = 0, relwidth = 0.98, relheight = 0.4)

#### variables treeview ####

var_treeview = ttk.Treeview(var_labelframe)
var_treeview["columns"] = ("func", "val")
var_treeview.heading("#0", text = "var", anchor = tk.W)
var_treeview.heading("func", text = "f(x)", anchor = tk.W)
var_treeview.heading("val", text = "value", anchor = tk.W)

var_treeview.column("#0", width = 60, minwidth = 60, stretch = tk.NO)
var_treeview.column("func", width = 80, minwidth = 80, stretch = tk.NO)
var_treeview.column("val", width = 100, minwidth = 100, stretch = tk.NO)

var_treeview.insert("", "end", text = "F", values = ("MOVE", "60"), tags = "odd")
var_treeview.insert("", "end", text = "R", values = ("ROTATE", "45"), tags = "even")
var_treeview.insert("", "end", text = "L", values = ("ROTATE", "-45"), tags = "odd")
var_treeview.insert("", "end", text = "[", values = ("SAVE"), tags = "even")
var_treeview.insert("", "end", text = "]", values = ("LOAD"), tags = "odd")

var_treeview.place(relx = 0.02, rely = 0.05, relwidth = 0.9, relheight = 0.6)

#### variables treeview scrollbar ####

var_treeview_scrollbar = ttk.Scrollbar(var_labelframe)
var_treeview_scrollbar["orient"] = "vertical"
var_treeview_scrollbar["command"] = var_treeview.yview

var_treeview_scrollbar.place(relx = 0.92, rely = 0.05, relheight = 0.6)

var_treeview.configure(yscrollcommand = var_treeview_scrollbar.set)

#### variable entry label ####
var_label = tk.Label(var_labelframe)
var_label["text"] = "var:"
var_label["font"] = GENERAL_FONT_SIZE
var_label["background"] = COLOR_MAIN_DARKER
var_label["foreground"] = COLOR_MAIN_LIGHT
var_label.place(relx = 0.02, rely = 0.66)

#### variable entry ####

var_entry = tk.Entry(var_labelframe)
var_entry.place(relx = 0.12, rely = 0.67, relwidth=0.1)

#### function input label ####

func_label = tk.Label(var_labelframe)
func_label["text"] = "f(x):"
func_label["font"] = GENERAL_FONT_SIZE
func_label["background"] = COLOR_MAIN_DARKER
func_label["foreground"] = COLOR_MAIN_LIGHT
func_label.place(relx = 0.26, rely = 0.66)

#### function combobox ####

func_combobox = ttk.Combobox(var_labelframe)
func_combobox["values"] = ("MOVE", "ROTATE", "SAVE", "LOAD")
func_combobox["state"] = "readonly"
func_combobox.place(relx = 0.36, rely = 0.67, relwidth = 0.3)

#### submit variable button ####

def button_clicked_event(btn_event_args):
    pass

submit_var_btn = tk.Button(var_labelframe)
submit_var_btn["text"] = "Insert"
submit_var_btn["font"] = GENERAL_FONT_SIZE
submit_var_btn.bind("<Button-1>", button_clicked_event)
submit_var_btn.place(relx = 0.83, rely = 0.835) 

#### drawing canvas ####

canvas = tk.Canvas(window)
canvas["background"] = COLOR_MAIN_LIGHT
canvas["borderwidth"] = 3
canvas["relief"] = "ridge"
canvas["highlightthickness"] = 0
canvas.place(relx = 0.35, rely = 0, relwidth = 0.65, relheight = 1)

window.mainloop()