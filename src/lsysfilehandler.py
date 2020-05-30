import json

def load_lsystem(filepath):
    
    #Try to open a file stream and use the json module 
    #to load a py object from the json file
    try:
        with open(filepath, "r") as fp:
            return json.load(fp)

    except OSError:
        #TODO: handle exception better
        print("Something went wrong!")
    

def save_lsystem(lsysobj, filepath):
    json.dump(lsysobj, filepath)