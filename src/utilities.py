def isdigit(str):
    try:
        int(str)
        return True
    except ValueError:
        return False
