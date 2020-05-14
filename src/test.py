import tkinter as tk
import tkinter.ttk as ttk
import widgets

class RulesFrame(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        #Setup frames
        self.label_frame = tk.LabelFrame(self, 
                                        text = "Rules", 
                                        font = ("", 9, "bold"),
                                        padx = 0, 
                                        pady = 5)
        self.input_frame = tk.Frame(self.label_frame)
        self.treeview_frame = tk.Frame(self.label_frame)

        #Setup labels
        self.variable_label = tk.Label(self.input_frame, text = "var:")
        self.equals_label = tk.Label(self.input_frame, text = "=")

        #Setup entries
        self.variable_combobox = ttk.Combobox(self.input_frame, width = 2, values = ["A", "B"])

        self.mutation_entry = tk.Entry(self.input_frame)

        #Setup buttons
        self.submit_button = tk.Button(self.input_frame, text = "submit", font = ("", 9))

        #Setup seperator
        self.seperator = ttk.Separator(self.label_frame, orient = tk.HORIZONTAL)

        #Setup treeview
        
        self.treeview = widgets.ScrollableTreeview(self.treeview_frame, 
                                    columns = ["var", "mutation"],
                                    show = "headings",
                                    selectmode = "browse",
                                    height = 4)
        self.treeview.heading("var", text = "var")
        self.treeview.heading("mutation", text = "mutation")
        self.treeview.column("var", minwidth = 30, width = 30)
        

        #Setup event bindings

        #Configure columns & rows
        self.treeview_frame.grid_columnconfigure(0, weight = 1)
        self.treeview_frame.grid_columnconfigure(1, weight = 0)

        #Placement
        self.label_frame.pack(fill = tk.BOTH)
        self.input_frame.grid(column = 0, row = 0)

        self.variable_label.grid(column = 0, row = 0)
        self.variable_combobox.grid(column = 1, row = 0)
        self.equals_label.grid(column = 2, row = 0)
        self.mutation_entry.grid(column = 3, row = 0)

        self.submit_button.grid(column = 0, row = 1, columnspan = 4, sticky = tk.W + tk.E, pady = (5, 0))


        self.seperator.pack(pady = 8, fill = tk.X)

        self.treeview_frame.pack(padx = 8, fill = tk.X)

        self.treeview.grid(column = 0, row = 0, sticky = tk.EW)
        


app = tk.Tk()
app.geometry("1250x750")

#Setup main frames
settingsframe = tk.Frame(app, padx = 5, pady = 5)
canvasframe = tk.Frame(app, bg = "#212121")

rules = RulesFrame(settingsframe)

#Setup widgets


#Placement
settingsframe.place(relx = 0, rely = 0, relwidth = 0.3, relheight = 1)
canvasframe.place(relx = 0.3, rely = 0, relwidth = 0.7, relheight = 1)

rules.pack(fill = tk.X)

app.mainloop()