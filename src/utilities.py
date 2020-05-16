'''
Holds utility functions
'''
import random

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

def clamp_number_between(min, max, number):
    '''
    Takes in a number and returns a value clamped between min & max.
    If number is between min and max it's returned as is.
    '''
    if number < min:
        return min
    elif number > max:
        return max

    return number

def try_get_number_from_str(string, from_index, can_be_decimal = True):
    '''
    Tries to find and return a number in string at given index.
    If a number can't be found the return value will be None.
    '''
    value = ""
    dec_seperator_found = False
    incrementer = 1

    #While string length is longer than index we wanna inspect
    while (from_index + incrementer) < len(string):
        
        #If char element in string is a digit
        if string[from_index + incrementer].isdigit():
            value += string[from_index + incrementer]
        
        #In order to be just a fraction pythonic let's break up long if statements
        #https://www.python.org/dev/peps/pep-0008/#maximum-line-length
        elif (can_be_decimal and not dec_seperator_found and 
                string[from_index + incrementer] == '.'):
            
            #Try looking ahead to see if a digit comes after the dot
            if ((from_index + incrementer + 1) < len(string) and 
                string[from_index + incrementer + 1].isdigit()):

                dec_seperator_found = True
                value += '.'

        #Try to convert string value to float value and return it 
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

def rgb_tuple_to_hex_string(rgb_tuple):
    '''
    Takes in a RGB tuple (float, float, float) and returns the hex formatted RGB value (string)
    '''
    return "#%02x%02x%02x" % (int(rgb_tuple[0]), int(rgb_tuple[1]), int(rgb_tuple[2]))

def hex_string_to_rgb_tuple(hex_string):
    '''
    Takes in a rgb hex string ("#ffffff") and returns a rgb tuple (r, g, b)
    '''
    return (int(hex_string[1:3], 16), int(hex_string[3:5], 16), int(hex_string[5:7], 16))

def get_random_color_hex_string():
    '''
    Generates and returns a random color hex string.
    From #000000 to #FFFFFF
    '''
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return rgb_tuple_to_hex_string((r, g, b))
