def isdigit(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def linear_interpolate_number(num_from, num_to, fraction):
    return (num_to - num_from) * fraction + num_from

def linear_interpolate_color(color_from, color_to, fraction):
    r = linear_interpolate_number(color_from[0], color_to[0], fraction)
    g = linear_interpolate_number(color_from[1], color_to[1], fraction)
    b = linear_interpolate_number(color_from[2], color_to[2], fraction)
    return (r, g, b)

def rgb_decimal_to_hex_string(color_dec):
    return "#%02x%02x%02x" % (int(color_dec[0]), int(color_dec[1]), int(color_dec[2]))

#Green to red 0.25

for i in range(5):
    rgb_dec = linear_interpolate_color((255, 0, 0), (0, 255, 0), (i * 0.25))
    print(rgb_decimal_to_hex_string(rgb_dec))
    