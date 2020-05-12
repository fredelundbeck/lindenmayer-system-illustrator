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