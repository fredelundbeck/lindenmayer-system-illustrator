import json

def load_lsystem(filepath):
    '''
    Loads an lsystem object from the given path.
    '''
    
    with open(filepath, "r") as fp:
        return json.load(fp)
    

def save_lsystem(lsysobj, filepath):
    '''
    Saves the given lsystem object to the given filepath
    '''

    with open(filepath, "w") as fp:
        #Setting the indent keyword pretty prints the json to the file
        json.dump(lsysobj, fp, indent = 4, sort_keys = False)