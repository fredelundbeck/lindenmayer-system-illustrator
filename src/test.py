variables = {
    "f" : ("move", 100),
    "+" : ("rotate", 45),
    "-" : ("rotate", -45),
    "[" : ("save", None),
    "]" : ("load", None)
}

variables["z"] = ("squiggle", 100)

lsystem = "f+f[-f]f"

for c in lsystem:
    print(variables.get(c))
