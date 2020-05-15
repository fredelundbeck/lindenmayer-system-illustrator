def is_str_digit(str):
    '''
    Takes in a string value and returns whether or not
    it can be cast to a float type.
    '''
    try:
        float(str)
        return True
    except ValueError:
        return False

def try_get_number_from_str(string, from_index, can_be_decimal = True):
    '''
    Tries to find and return a number in string at given index.
    If a number can't be found the return value will be None.
    '''
    value = ""
    dec_seperator_found = False
    incrementer = 1

    while (from_index + incrementer) < len(string):

        if string[from_index + incrementer].isdigit():
            value += string[from_index + incrementer]

        elif can_be_decimal and not dec_seperator_found and string[from_index + incrementer] == '.':
            
            #Look ahead
            if (from_index + incrementer + 1) < len(string) and string[from_index + incrementer + 1].isdigit():
                dec_seperator_found = True
                value += '.'    

        else:
            try:
                value = float(value)
                return value
        
            except ValueError:
                return None

        incrementer += 1


def linear_interpolate_number(num_from, num_to, fraction):
    '''
    Returns an interpolated value betweeen num_from and num_to
    '''
    return (num_to - num_from) * fraction + num_from

def linear_interpolate_color(color_from, color_to, fraction):
    '''
    Returns a tuple containing R, G & B number values, that's been interpolated between 
    two other given tuples (RGB colors)
    '''
    r = linear_interpolate_number(color_from[0], color_to[0], fraction)
    g = linear_interpolate_number(color_from[1], color_to[1], fraction)
    b = linear_interpolate_number(color_from[2], color_to[2], fraction)
    return (r, g, b)

def rgb_decimal_to_hex_string(color_dec):
    '''
    Takes in a RGB tuple (float, float, float) and returns the hex formatted RGB value (string)
    '''
    return "#%02x%02x%02x" % (int(color_dec[0]), int(color_dec[1]), int(color_dec[2]))

    