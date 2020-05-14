def isdigit(str):
    try:
        float(str)
        return True
    except ValueError:
        return False
