# color_name = (RED, GREEN, BLUE)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
cyan = (0, 240, 240)
brown = (80, 40, 40)
yellow = (255, 255, 0)
pink = (255, 0, 255)
purple = (128, 0, 255)
grey = (128, 128, 128)
orange = (255, 128, 0)
light_blue = (0, 128, 255)
light_grey = (192, 192, 192)
dark_green = (0, 128, 0)
dark_blue = (0, 0, 128)
dark_red = (128, 0, 0)


def darken(color, amount):
    for rgb in color:
        rgb -= amount
        return color


def lighten(color, amount):
    for rgb in color:
        rgb += amount
        return color

# TODO: FIX THESE FUNCTIONS ^^^^
