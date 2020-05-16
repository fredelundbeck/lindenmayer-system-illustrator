'''
Holds everything related to L-Systems
'''

import utilities as util
import math

#debug delete
import tkinter as tk
#

class LSystem:
    def __init__(self, axiom, rules):
        self.axiom = axiom
        self.rules = rules
        self.current_state = axiom
    
    def __next__(self):
        next_state = ""

        for char in self.current_state:
            found = False
            for var, rule in self.rules:
                if char == var:
                    next_state += rule
                    found = True
            if not found:
                next_state += char
        self.current_state = next_state
        return next_state

    def __str__(self):
        return self.current_state

def get_new_position(current_x, current_y, angle, step_length):

    new_x = math.cos(angle * math.pi / 180) * step_length + current_x
    new_y = math.sin(angle * math.pi / 180) * step_length + current_y

    return (new_x, new_y)

def get_new_color(color_num, colors):

    interval_length = 256 / (len(colors) - 1) #9 colors = 32 interval
    color_a_index = math.floor(color_num / interval_length)
    color_b_index = math.ceil(color_num / interval_length)

    #If both color indexes are the same, the color_num is pointing at an exact color
    #and we won't need to linear interpolate between two colors
    if color_a_index == color_b_index:
        return colors[color_a_index]

    #Get percentage of color_num between color_a and color_b
    percentage = (color_num - color_a_index * interval_length) / (color_b_index * interval_length - color_a_index * interval_length)
    
    #Convert color_a and color_b hex_strings to rgb tuple (r, g, b)
    color_a_tuple = util.hex_string_to_rgb_tuple(colors[color_a_index])
    color_b_tuple = util.hex_string_to_rgb_tuple(colors[color_b_index])

    #Use linear interpolation to find color between the two colors
    rgb_tuple = util.linear_interpolate_color(color_a_tuple, color_b_tuple, percentage)
    
    return util.rgb_tuple_to_hex_string(rgb_tuple)

#TODO: Find better solution to this way to long argument list
def draw_lsystem(canvas : tk.Canvas, lsystem, symbols, start_pos, 
                start_angle, turn_angle_amount, start_step, start_thickness,
                colors = ["#FFFFFF"], start_color_num = 0):

    states = []
    pos_x = start_pos[0]
    pos_y = start_pos[1]
    angle = start_angle
    turn_angle_amount = turn_angle_amount
    step_length = start_step
    thickness = start_thickness
    color_num = start_color_num % 256
    color_rgb = get_new_color(color_num, colors)
    directions_flipped = False

    for index, char in enumerate(lsystem):

        #Continue to next char if no operation is associated with it
        op = symbols.get(char, None)[0]
        if op == None:
            continue

        #Try getting number value after symbol if it exists
        value = util.try_get_number_from_str(lsystem, index)

        if op == "move_down":
            
            #Calculate end position and draw line
            new_pos = get_new_position(pos_x, pos_y, angle, step_length)
            canvas.create_line(pos_x, pos_y, new_pos[0], new_pos[1], width = thickness, fill = color_rgb)

            #Update current position
            pos_x = new_pos[0]
            pos_y = new_pos[1]
            
        elif op == "move_up":
            #Calculate end position 
            new_pos = get_new_position(pos_x, pos_y, angle, step_length)

            #Update current position
            pos_x = new_pos[0]
            pos_y = new_pos[1]

        elif op == "turn_right":
            #If reverse_turn is false, update angle normally
            if not directions_flipped:
                angle = (angle + turn_angle_amount) % 360

            else:
                angle = (angle - turn_angle_amount) % 360

        elif op == "turn_left":
            #If reverse_turn is false, update angle normally
            if not directions_flipped:
                angle = (angle - turn_angle_amount) % 360

            else:
                angle = (angle + turn_angle_amount) % 360

        elif op == "state_save":
            #Save current state to states list
            states.append(((pos_x, pos_y), angle, color_num, directions_flipped))

        elif op == "state_load":
            #Pop last state from states list
            latest_state = states.pop()

            #Update current settings to latest_state
            pos_x = latest_state[0][0]
            pos_y = latest_state[0][1]
            angle = latest_state[1]
            color_num = latest_state[2]
            color_rgb = get_new_color(color_num, colors)
            directions_flipped = latest_state[3]

        elif op == "color_up":
            #Increment color by found or default value & update color_rgb
            color_num = (color_num + (symbols.get(char)[1] if value == None else value)) % 256
            color_rgb = get_new_color(color_num, colors)   

        elif op == "color_down":
            #Decrement color by found or default value & update color_rgb
            color_num = (color_num - (symbols.get(char)[1] if value == None else value)) % 256
            color_rgb = get_new_color(color_num, colors)    

        elif op == "color_set":
            #Set color to found value after symbol or reset to start_color
            color_num = value if value != None else start_color_num

        elif op == "thickness_up":
            #Increment line thickness by found or default value
            thickness = thickness + (symbols.get(char)[1] if value == None else value)

        elif op == "thickness_down":
            #Decrement line thickness by found or default value
            thickness = thickness - (symbols.get(char)[1] if value == None else value)

        elif op == "thickness_set":
            #Set thickness to found value after symbol or reset to start_thickness
            thickness = value if value != None else start_thickness

        elif op == "multiply_step":
            #Multiply step by found or default value
            step_length = step_length * (symbols.get(char)[1] if value == None else value)

        elif op == "switch_directions":
            #Set directions_flipped to what directions_flipped is not
            directions_flipped = not directions_flipped


start_pos = (0, 0)
start_rot = 90

symbols = {
    "F" : ("move_down", None),
    "G" : ("move_up", None),
    "+" : ("turn_right", None),
    "-" : ("turn_left", None),
    "[" : ("state_save", None),
    "]" : ("state_load", None),
    "#" : ("thickness_up", 1),
    "%" : ("thickness_down", 1)
}

lsys = LSystem("F", [("F", "F-F+#+F-F")])
next(lsys)
next(lsys)
next(lsys)

app = tk.Tk()
app.geometry("900x900")

canvas = tk.Canvas(app, bg = "lightgreen")
canvas.pack(fill = tk.BOTH, expand = True)

#draw_lsystem(canvas, str(lsys), symbols, (450, 900), -80, 45, 20, 2)

colors = ["#ff0000", "#0000ff"]
mix_color = get_new_color(128, colors)

print(mix_color)

app.mainloop()


