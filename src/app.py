import tkinter as tk

#window consts
TITLE = 'Lindenmayer Systems Illustrator'
WND_HEIGHT = 600
WND_WIDTH = 1000

#color consts
DRAW_CANVAS_CLR =       '#121212'
CONTROL_FRAME_CLR =    '#3f3f4f'
BUTTON_CLR =            '#4f4f54'
BUTTON_TEXT_CLR =       '#f3f3f3'

#program info consts
C_VERSION = 'version 0.1'

#setup window settings
wnd_handle = tk.Tk()
wnd_handle.resizable(0, 0)
wnd_handle.title(TITLE)

wnd_frame = tk.Frame(wnd_handle, width=WND_WIDTH, height=WND_HEIGHT)
wnd_frame.pack()

def save():
    print('saving')

#menubar
menubar = tk.Menu(wnd_handle)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='New')
filemenu.add_separator()
filemenu.add_command(label='Save settings', command=save)
filemenu.add_command(label='Load settings', command=wnd_frame.quit)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=wnd_handle.quit)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label='About')

menubar.add_cascade(label='File', menu=filemenu)
menubar.add_cascade(label='Help', menu=helpmenu)

wnd_handle.config(menu=menubar)

#controls frame
controls_frame = tk.Frame(wnd_frame, bg=CONTROL_FRAME_CLR)
controls_frame.place(relx=0, rely=0, relwidth=0.35, relheight=1)

#drawing canvas
drawing_canvas = tk.Canvas(wnd_frame, bg=DRAW_CANVAS_CLR)
drawing_canvas.place(relx=0.35, rely=0, relwidth=0.65, relheight=1)

#inputs labelframe
inputs_label_frame = tk.LabelFrame(controls_frame, text='System inputs', bg=CONTROL_FRAME_CLR, fg='#FFFFFF')
inputs_label_frame.place(relx=0.01, rely=0.01, relwidth=0.97, relheight=0.2)

#version label
version_label = tk.Label(controls_frame, text=C_VERSION, bg=CONTROL_FRAME_CLR, fg='#D3D3D3')
version_label.place(relx=0, rely=0.965)

#call the tk mainloop
wnd_handle.mainloop()