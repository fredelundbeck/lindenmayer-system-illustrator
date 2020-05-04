import tkinter as tk

#Consts
TITLE = 'Lindenmayer Systems Illustrator'
WND_HEIGHT = 700
WND_WIDTH = 650

#Setup window settings
wnd_handle = tk.Tk()
wnd_handle.resizable(0, 0)
wnd_handle.title(TITLE)

wnd_frame = tk.Frame(wnd_handle, width=WND_WIDTH, height=WND_HEIGHT)
wnd_frame.pack()

draw_canvas = tk.Canvas(wnd_frame, bg='black')
draw_canvas.place(relwidth=0.95, relheight=0.7, relx=0.025, rely=0.025)

inputs_frame = tk.Frame(wnd_frame, bg='light gray')
inputs_frame.place(relwidth=0.95, relheight=0.24, relx=0.025, rely=0.74)

test_label = tk.Label(inputs_frame, text='hello friend!')
test_label.pack()

#Call the tk mainloop
wnd_handle.mainloop()