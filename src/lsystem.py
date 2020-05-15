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

def draw_lsystem(lsystem, symbols : dict, start_pos : tuple, start_rot : tuple):
    states = []
    curr_pos_x = start_pos[0]
    curr_pos_y = start_pos[1]
    curr_rotation = start_rot

    for index, char in enumerate(lsystem):
        #Get symbol operation, if it exists
        op = symbols.get(char, None)
        if op == None:
            continue

        #Get number value after symbol if it exists
        value = ""
        v_index = 1
        while (index + v_index) < len(lsystem):
            if lsystem[index + v_index].isdigit() or lsystem[index + v_index] == '.':
                pass
            pass



start_pos = (0, 0)
start_rot = 90

symbols = {
    "F" : ("Move forward", 100),
    "P" : ("Print hello, world"),
    "H" : ("LOL"),
    "[" : ("hmm"),
    "]" : ("what"),
    "M" : ("Good stuff", 12),
    "R" : ("Okay then", 200)
}

lsystem = "F3PH[]M3.1"

draw_lsystem(lsystem, symbols, start_pos, start_rot)



        