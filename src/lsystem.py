from turtle import *

class LSystem:
    def __init__(self, axiom, rules):
        self.axiom = axiom
        self.rules = rules
        self.current_iteration = axiom
    
    def __next__(self):
        temp_current = ''
        for char in self.current_iteration:
            found = False
            for char_r, next_r  in self.rules:
                if char == char_r:
                    found = True
                    temp_current += next_r
            if not found:
                temp_current += char

        self.current_iteration = temp_current
        return self.current_iteration

    def __str__(self):
        return self.current_iteration