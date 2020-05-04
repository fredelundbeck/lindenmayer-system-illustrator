class lsystem:
    def __init__(self, axiom, ruleset):
        self.axiom = axiom
        self.ruleset = ruleset
        self.current_gen = axiom
    
    def __iter__(self):
        return self
    
    def __next__(self):
        next_gen = ''
        for c in self.current_gen:
            for letter, evolution  in self.ruleset:
                if letter == c:
                    next_gen += evolution
                    break
        self.current_gen = next_gen
        return self.current_gen

lindenmayer = lsystem('F', [('F', 'FF+[F-F-F]-[-F+F+F]')])

