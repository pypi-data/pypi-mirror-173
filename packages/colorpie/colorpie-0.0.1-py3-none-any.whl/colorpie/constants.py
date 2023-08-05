# -*- coding: UTF-8 -*-


ATTRIBUTES = {
    "reset": 0,
    "bold": 1,  # or increased intensity
    "dark": 2,
    "italic": 3,  # not widely supported
    "underline": 4,
    "slow_blink": 5,  # not widely supported
    "rapid_blink": 6,  # not widely supported
    "reverse": 7,  # swap foreground and background colors
    "concealed": 8  # not widely supported.
}


COLORS: dict = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,

    "bright_black": 90,
    "bright_red": 91,
    "bright_green": 92,
    "bright_yellow": 93,
    "bright_blue": 94,
    "bright_magenta": 95,
    "bright_cyan": 96,
    "bright_white": 97,
}

HIGHLIGHTS: dict = {
    "black": 40,
    "red": 41,
    "green": 42,
    "yellow": 43,
    "blue": 44,
    "magenta": 45,
    "cyan": 46,
    "white": 47,

    "bright_black": 100,
    "bright_red": 101,
    "bright_green": 102,
    "bright_yellow": 103,
    "bright_blue": 104,
    "bright_magenta": 105,
    "bright_cyan": 106,
    "bright_white": 107,
}
