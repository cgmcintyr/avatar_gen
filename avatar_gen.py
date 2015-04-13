# Vers: 0.1
# Auth: Chrisopher McIntyre (github: chrsintyre)
# Pub:  13 April 2015
# Desc: A python module to generate avatars, using a given user's username as a seed 
#       for a recursive function. Usernames should be comprised of letters, numbers 
#       and underscores. The default image size is 420. This module is based upon 
#       Jeremy Kun's (github: j2kun) blogpost on generating random psychedelic art 
#       in python.

import math
from PIL import Image, ImageDraw

class BaseEvaluate:
    """
    Used as base case for value_to_exp() 
    """
    return_x = lambda self, x, y: x
    return_y = lambda self, x, y: y
    return_xy = lambda self, x, y: x*y

    def __init__(self, string_value):
        if int(string_value) % 3 == 0:
            self.evaluate = self.return_x
        elif int(string_value) % 2 == 0:
            self.evaluate = self.return_xy
        else:
            self.evaluate = self.return_y

    def __str__(self):
        if self.evaluate == self.return_x:
            return "x"
        elif self.evaluate == self.return_y:
            return "y"
        else:
            return "xy"

class SinPi:
    """
    Used to add 'math.sin(math.pi*' to the outside of the expression being built
    by value_to_exp()
    """
    def __init__(self, value, step):
        value = int(value)
        self.arg = value_to_exp(value * 0.9, step + 1)
   
    def __str__(self):
        return "sin(pi*" + str(self.arg) + ")"

    def evaluate(self, x, y):
        return math.sin(math.pi * self.arg.evaluate(x,y))

class CosPi:
    """
    Used to add 'math.cos(math.pi*' to the outside of the expression being built
    by value_to_exp()
    """
    def __init__(self, value, step):
        value = int(value)
        self.arg = value_to_exp(value * 0.9, step + 1)

    def __str__(self):
        return "cos(pi*" + str(self.arg) + ")"

    def evaluate(self, x, y):
        return math.cos(math.pi * self.arg.evaluate(x,y))

class Times:
    """
    Used to build two new expressions and multiply them together. This helps 
    increase the complexity of the function being built by value_to_exp() 
    """
    def __init__(self, value, step):
        if value < 50:
            value = 12

        self.lhs = value_to_exp(value * 0.8, step + 1)
        self.rhs = value_to_exp(value * 0.8, step + 1)

    def __str__(self):
        return str(self.lhs) + "*" + str(self.rhs)

    def evaluate(self, x, y):
        return self.lhs.evaluate(x,y) * self.rhs.evaluate(x,y)

def gen_string_values(s):
    """
    This function takes a string, divides it into three parts, and generates 
    a value for each part.

    returns: list containing three floats, where for each int n, 0 <= n < 36
    """
    s = s.lower()
    third = int(len(s) / 3)
    s1 = s[0:third]
    s2 = s[third:2*third]
    s3 = s[2*third:]

    parts = (s1, s2, s3)
    vals  = [] 
    for string in parts:
        val = 0
        for char in string:
            if char=='_':
                val += 35
            try:
                val += int(char)
            except:
                val += ord(char) - 97 
        vals.append(float(val)/len(string))

    return vals 
 
def value_to_exp(val, step=0):
    """
    Uses given float value as a seed for generating a complex expression

    returns: function
    """
    if step == 0:
        if val < 40:
            return Times(val * math.pi, step) 
        elif val < 30:
            return CosPi(val, step)
        else:
            return SinPi(val, step)
    elif step < 6:
        if int(val) % 3 == 0:
            return SinPi(val, step)
        elif int(val) % 2 == 0:
            return CosPi(val, step) 
        else:
            return Times(val, step)
    else:
        return BaseEvaluate(val) 

def plot_intensity(func, pixels_per_unit):
    """
    Creates a grayscale image using given function.
    
    returns: Grayscale Image object
    """
    canvas_width = 2 * pixels_per_unit 
    canvas = Image.new("L", (canvas_width, canvas_width))

    for py in range(canvas_width):
        for px in range(canvas_width):
            # Convert pixel location to [-1,1] coordinates
            x = float(px - pixels_per_unit) / pixels_per_unit
            y = -float(py - pixels_per_unit) / pixels_per_unit 
            z = func.evaluate(x,y)

            # Scale [-1,1] result to [0,255].
            intensity = int(z * 127.5 + 127.5)
            canvas.putpixel((px,py), intensity)
    
    return canvas

def plot_color(red_func, green_func, blue_func, pixels_per_unit):
    """
    Generate grayscale images for each function and then merge them into a 
    single RGB image.

    returns: RGB Image object
    """
    red_plane   = plot_intensity(red_func, pixels_per_unit)
    green_plane = plot_intensity(green_func, pixels_per_unit)
    blue_plane  = plot_intensity(blue_func, pixels_per_unit)
    return Image.merge("RGB", (red_plane, green_plane, blue_plane))

def make_image(username, pixels_per_unit=210):
    """
    Generates an image using the given username string as a seed. The size
    of the image generated defaults to 420 (2*pixels_per_unit).

    returns: RGB Image object
    """
    s1, s2, s3 = gen_string_values(username)
    
    red_func   = value_to_exp(50 - s1) 
    green_func = value_to_exp(50 - s2) 
    blue_func  = value_to_exp(50 - s3) 

    im = plot_color(red_func, green_func, blue_func, pixels_per_unit)
    return im
    
