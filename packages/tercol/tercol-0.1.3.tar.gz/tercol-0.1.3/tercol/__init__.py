"""TerCol, a useless library that colors text.
Copyright 2022 Sultan Marzouq"""

# Imports
from os import system as execc

# DISABLE THIS TO STOP IT FROM DOING os.system('')
autoOsSystem = True

# Color codes
__cblack = "\u001b[30m"
__cred = "\u001b[31m"
__cgreen = "\u001b[32m"
__cyellow = "\u001b[33m"
__cblue = "\u001b[34m"
__cmagenta = "\u001b[35m"
__ccyan = "\u001b[36m"
__cwhite = "\u001b[37m"
__cgray = "\u001b[0;90m"
__cbgblack = "\u001b[40m"
__cbgred = "\u001b[41m"
__cbggreen = "\u001b[42m"
__cbgyellow = "\u001b[43m"
__cbgblue = "\u001b[44m"
__cbgmagenta = "\u001b[45m"
__cbgcyan = "\u001b[46m"
__cbgwhite = "\u001b[47m"
__cbggray = "\u001b[0;100m"
__sbold = "\u001b[1m"
__sitalic = "\u001b[3m"
__sblink = "\u001b[5m"
__sanotherblink = "\u001b[6m"  # I dunno what the difference between 5m and 6m is but they both blink so I'm adding this just in case someone needs it
__sfadedout = "\u001b[2m"
__sunderlined = "\u001b[4m"
__sinverted = " \u001b[7m"
__endcolor = "\u001b[0m"

# hsv to rgb
def hsv_to_rgb(h, s, v):
    """
    THIS IS NOT IMPORTANT AND YOU WILL NOT NEED TO USE THIS IN YOUR CODE. This is just colorsys.hsv_to_rgb(). I am defining this instead of importing colorsys to achieve compatability.
    """
    if s == 0.0:
        return v, v, v
    i = int(h * 6.0)  # XXX assume int() truncates!
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q
    # Cannot get here


# RGB
def rgb(r, g, b, text):
    """
    Takes 4 values, the red, the blue, the green and the text. The color is based on what rgb you inputed.
    """
    if autoOsSystem:
        execc("")
    return f"\u001b[38;2;{r};{g};{b}m{text}{__endcolor}"


def bgrgb(r, g, b, text):
    """
    Same thing as rgb(r, g, b, text) but it colors the background instead.
    """
    if autoOsSystem:
        execc("")
    return f"\u001b[48;2;{r};{g};{b}m{text}{__endcolor}"


# Hex
def hex(hex: str, text):
    """
    Takes a hex code and a text, converts it to rgb and uses the existing rgb function in this library.
    """
    try:
        RGBHEX = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
        ]
        hexcode = hex.replace("#", "").casefold()
        hexr = int(RGBHEX.index(hexcode[0])) * 16
        hexr += int(RGBHEX.index(hexcode[1]))
        hexg = int(RGBHEX.index(hexcode[2])) * 16
        hexg += int(RGBHEX.index(hexcode[3]))
        hexb = int(RGBHEX.index(hexcode[4])) * 16
        hexb += int(RGBHEX.index(hexcode[5]))
        return rgb(hexr, hexg, hexb, text)
    except IndexError:
        raise Exception(red(underlined("Uh oh, invalid hex code...")))
    except ValueError:
        raise Exception(red(underlined("Uh oh, invalid hex code...")))
    except TypeError:
        raise Exception(
            red(
                underlined(
                    "Hex code can't be an actual hexdecimal input. Why? This is due to how the code works."
                )
            )
        )


def bghex(hex: str, text):
    """
    Same thing as hex(hex, text) but it colors the background instead.
    """
    try:
        RGBHEX = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
        ]
        hexcode = hex
        hexr = int(RGBHEX.index(hexcode[0])) * 16
        hexr += int(RGBHEX.index(hexcode[1]))
        hexg = int(RGBHEX.index(hexcode[2])) * 16
        hexg += int(RGBHEX.index(hexcode[3]))
        hexb = int(RGBHEX.index(hexcode[4])) * 16
        hexb += int(RGBHEX.index(hexcode[5]))
        return bgrgb(hexr, hexg, hexb, text)
    except IndexError:
        raise Exception(red(underlined("Uh oh, invalid hex code...")))
    except ValueError:
        raise Exception(red(underlined("Uh oh, invalid hex code...")))
    except TypeError:
        raise Exception(
            red(
                underlined(
                    "Hex code can't be an actual hexadecimal input. Why? This is due to how the code works."
                )
            )
        )


# HSV
def hsv(h, s, v, text):
    """
    Takes a hue, saturation, and value, and then converts it to RGB, and returns the value of rgb(ConvertedHue, ConvertedSaturation, ConvertedValue, text).
    This does not take a floating point number, it does actually take numbers from 0 to 100! (0 to 360 for hue)
    """
    try:
        h, s, v = int(h), int(s), int(v)
    except ValueError:
        raise ValueError(red(underlined("HSV is invalid.")))
    if h > 360 or h < 0:
        raise ValueError(red(underlined("HSV is invalid. Hue must be between 0-360!")))
    if s > 100 or s < 0:
        raise ValueError(
            red(underlined("HSV is invalid. Saturation must be between 0-100!"))
        )
    if v > 100 or v < 0:
        raise ValueError(
            red(underlined("HSV is invalid. Value must be between 0-100!"))
        )
    h, s, v = h / 360, s / 100, v / 100
    ConvertedHue = round(hsv_to_rgb(h, s, v)[0] * 255)
    ConvertedSaturation = round(hsv_to_rgb(h, s, v)[1] * 255)
    ConvertedValue = round(hsv_to_rgb(h, s, v)[2] * 255)
    return rgb(ConvertedHue, ConvertedSaturation, ConvertedValue, text)


def bghsv(h, s, v, text):
    """
    hsv(Hue, Saturation, Value, Text) but for the background,
    This does not take a floating point number, it does actually take numbers from 0 to 100! (0 to 360 for hue)
    """
    try:
        h, s, v = int(h), int(s), int(v)
    except ValueError:
        raise ValueError(red(underlined("HSV is invalid.")))
    if h > 360 or h < 0:
        raise ValueError(red(underlined("HSV is invalid. Hue must be between 0-360!")))
    if s > 100 or s < 0:
        raise ValueError(
            red(underlined("HSV is invalid. Saturation must be between 0-100!"))
        )
    if v > 100 or v < 0:
        raise ValueError(
            red(underlined("HSV is invalid. Value must be between 0-100!"))
        )
    h, s, v = h / 360, s / 100, v / 100
    ConvertedHue = round(hsv_to_rgb(h, s, v)[0] * 255)
    ConvertedSaturation = round(hsv_to_rgb(h, s, v)[1] * 255)
    ConvertedValue = round(hsv_to_rgb(h, s, v)[2] * 255)
    return bgrgb(ConvertedHue, ConvertedSaturation, ConvertedValue, text)


# Color Functions
def black(text):
    if autoOsSystem:
        execc("")
    return f"{__cblack}{text}{__endcolor}"


def red(text):
    if autoOsSystem:
        execc("")
    return f"{__cred}{text}{__endcolor}"


def green(text):
    if autoOsSystem:
        execc("")
    return f"{__cgreen}{text}{__endcolor}"


def yellow(text):
    if autoOsSystem:
        execc("")
    return f"{__cyellow}{text}{__endcolor}"


def blue(text):
    if autoOsSystem:
        execc("")
    return f"{__cblue}{text}{__endcolor}"


def magenta(text):
    if autoOsSystem:
        execc("")
    return f"{__cmagenta}{text}{__endcolor}"


def cyan(text):
    if autoOsSystem:
        execc("")
    return f"{__ccyan}{text}{__endcolor}"


def white(text):
    if autoOsSystem:
        execc("")
    return f"{__cwhite}{text}{__endcolor}"


def gray(text):
    if autoOsSystem:
        execc("")
    return f"{__cgray}{text}{__endcolor}"


def grey(text):
    return gray(text)


def brightblack(text):
    return gray(text)


def lightblack(text):
    return gray(text)


def rainbowtext(text):
    """
    Enjoy I guess
    """
    if autoOsSystem:
        execc("")
    formedstr = ""
    i = 0
    for char in text:
        if char in " \t\n":
            formedstr += char
            continue
        mi = i % 7
        if mi == 0:
            formedstr += hex("f33444", char)
        elif mi == 1:
            formedstr += hex("ff8901", char)
        elif mi == 2:
            formedstr += hex("fad716", char)
        elif mi == 3:
            formedstr += hex("00ba70", char)
        elif mi == 4:
            formedstr += hex("00c0dd", char)
        elif mi == 5:
            formedstr += hex("00408a", char)
        elif mi == 6:
            formedstr += hex("5e2779", char)
        i += 1
    return formedstr


# Background colors


def bgblack(text):
    if autoOsSystem:
        execc("")
    return f"{__cbgblack}{text}{__endcolor}"


def bgred(text):
    if autoOsSystem:
        execc("")
    return f"{__cbgred}{text}{__endcolor}"


def bggreen(text):
    if autoOsSystem:
        execc("")
    return f"{__cbggreen}{text}{__endcolor}"


def bgyellow(text):
    if autoOsSystem:
        execc("")
    return f"{__cbgyellow}{text}{__endcolor}"


def bgblue(text):
    if autoOsSystem:
        execc("")
    return f"{__cbgblue}{text}{__endcolor}"


def bgmagenta(text):
    if autoOsSystem:
        execc("")
    return f"{__cbgmagenta}{text}{__endcolor}"


def bgcyan(text):
    if autoOsSystem:
        execc("")
    return f"{__cbgcyan}{text}{__endcolor}"


def bgwhite(text):
    if autoOsSystem:
        execc("")
    return f"{__cbgwhite}{text}{__endcolor}"


def bggray(text):
    if autoOsSystem:
        execc("")
    return f"{__cbggray}{text}{__endcolor}"


def bggrey(text):
    return bggray(text)


def bgbrightblack(text):
    return bggray(text)


def bglightblack(text):
    return bggray(text)


# Style/Look
def bold(text):
    """
    Makes your text bold.
    """
    if autoOsSystem:
        execc("")
    return f"{__sbold}{text}{__endcolor}"


def italic(text):
    """
    Makes your text italic.
    """
    if autoOsSystem:
        execc("")
    return f"{__sitalic}{text}{__endcolor}"


def underlined(text):
    """
    Shows a line under your text.
    """
    if autoOsSystem:
        execc("")
    return f"{__sunderlined}{text}{__endcolor}"


def inverted(text):
    """
    I can't explain this, just try it and see what it looks like for you.
    """
    if autoOsSystem:
        execc("")
    return f"{__sinverted}{text}{__endcolor}"


def blink(text):
    """Blink

    [insert faded out version of "Blink"]

    Blink

    [insert faded out version of "Blink"]

    Blink

    [insert faded out version of "Blink"]"""
    if autoOsSystem:
        execc("")
    return f"{__sblink}{text}{__endcolor}"


def anotherblink(text):
    """
    There are two ANSI codes that blink, So I'm adding this just in case.
    """
    if autoOsSystem:
        execc("")
    return f"{__sanotherblink}{text}{__endcolor}"


def fadedout(text):
    """
    You can use this to do a manual blinking text if you want.
    """
    return f"{__sfadedout}{text}{__endcolor}"


def dim(text):
    """
    Alias for fadedout()
    """
    return fadedout(text)
