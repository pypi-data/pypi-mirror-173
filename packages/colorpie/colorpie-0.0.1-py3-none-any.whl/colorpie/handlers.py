# -*- coding: UTF-8 -*-

from os import environ, system
from string import Template
from sys import version_info
from typing import Union, Tuple, List

from .constants import ATTRIBUTES, HIGHLIGHTS, COLORS
from .mapping import __256_color__


class Style4Bit(object):
    """
    Colorise text (16-color mode).

    Available colours:
        black, red, green, yellow, blue, magenta, cyan, white,
        bright_black, bright_red, bright_green, bright_yellow,
        bright_blue, bright_magenta, bright_cyan and bright_white

    Available highlights:
        black, red, green, yellow, blue, magenta, cyan, white,
        bright_black, bright_red, bright_green, bright_yellow,
        bright_blue, bright_magenta, bright_cyan and bright_white

    Available attributes:
        reset, bold, dark, italic, underline,
        slow_blink, rapid_blink, reverse, concealed

    Example:
        style = Style4Bit(
            color='red',
            highlight='black',
            attributes=['bold', 'slow_blink']
        )
        print(style.format('Hello, World!'))
    """

    system("color")

    _escape: str = "\x1b[" if version_info.major > 2 else "\033["
    _reset: str = f"{_escape}{ATTRIBUTES.get('reset')}m"

    @staticmethod
    def _check_color(value: Union[str, int]) -> int:
        if isinstance(value, str):
            return COLORS.get(value)
        elif isinstance(value, int) and (value in COLORS.values()):
            return value

    @staticmethod
    def _check_highlight(value: Union[str, int]) -> int:
        if isinstance(value, str):
            return HIGHLIGHTS.get(value)
        elif isinstance(value, int) and (value in HIGHLIGHTS.values()):
            return value

    @staticmethod
    def _check_attributes(args: Union[tuple, list, str, int]) -> Tuple[int]:
        if isinstance(args, str) and (args in ATTRIBUTES):
            return (ATTRIBUTES.get(args),)

        elif isinstance(args, int) and (args in ATTRIBUTES.values()):
            return (args,)

        elif isinstance(args, (tuple, list)):
            items: List[int] = list()

            for arg in args:
                if isinstance(arg, str) and (arg in ATTRIBUTES):
                    items.append(ATTRIBUTES.get(arg))
                elif isinstance(arg, int) and (arg in ATTRIBUTES.values()):
                    items.append(arg)

            if len(items) > 0:
                return tuple(items)

    def __init__(self, **kwargs):
        self._color: int = self._check_color(kwargs.pop("color", None))
        self._highlight: int = self._check_highlight(kwargs.pop("highlight", None))
        self._attributes: Tuple[int] = self._check_attributes(kwargs.pop("attributes", None))

        # 'True' if any of the fields is not None else 'False'
        self._has_attrs: bool = any(
            [
                True if (item is not None) else False
                for item in [
                    self._color,
                    self._highlight,
                    self._attributes
                ]
            ]
        )

        # To avoid checking for the fields
        # every time we construct a string:
        self._template: Template = self._as_template()

    def format(self, text: str) -> str:

        if ("NO_COLOR" in environ) or ("ANSI_COLORS_DISABLED" in environ):
            return text

        if self._template is not None:
            return self._template.substitute(text=text)

        return text

    def _as_template(self) -> Template:
        template: str = "${text}"

        if self._has_attrs:

            if self._color is not None:
                template = self._join(self._color, template)

            if self._highlight is not None:
                template = self._join(self._highlight, template)

            if self._attributes is not None:
                for attr in self._attributes:
                    template = self._join(attr, template)

            return Template(f"{template}{self._reset}")

    def _join(self, style: int, text: str) -> str:
        return f"{self._escape}{style}m{text}"


class Style8Bit(Style4Bit):
    """
    Colorise text (256-color mode).

    For available colors and highlights see:
        `https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit`

    For attributes:
        reset, bold, dark, italic, underline,
        slow_blink, rapid_blink, reverse, concealed

    Example:
        style = Style8Bit(
            color=0,
            highlight=16,
            attributes=['bold']
        )
        print(style.format('Hello, World!'))

    Some colors can be referred to by their name:
        black, maroon, green, olive, navy, purple, teal, silver,
        grey, red, lime, yellow, blue, magenta, cyan, white, gold

    Also, by their hex or rgb values.
    (see `__256_color__` dict in `constants.py`).
    """

    def __init__(self, **kwargs):

        self._name_keys: dict = {
            value.name.lower(): key
            for key, value in __256_color__.items()
            if value.name is not None
        }

        self._hex_keys: dict = {
            value.hex.__repr__(): key
            for key, value in __256_color__.items()
        }

        self._rgb_keys: dict = {
            value.rgb.__repr__(): key
            for key, value in __256_color__.items()
        }

        super(Style8Bit, self).__init__(**kwargs)

    def _check_color(self, value: Union[str, int]) -> int:

        if isinstance(value, int) and (value in __256_color__):
            return value

        elif isinstance(value, str):
            if value.lower() in self._name_keys:
                return self._name_keys.get(value.lower())
            elif value in self._hex_keys:
                self._hex_keys.get(value)
            elif value in self._rgb_keys:
                self._rgb_keys.get(value)

    def _check_highlight(self, value: Union[str, int]) -> int:
        return self._check_color(value)

    def _as_template(self) -> Template:
        template: str = "${text}"

        if self._has_attrs:

            if self._color is not None:
                template = self._join_color(self._color, template)

            if self._highlight is not None:
                template = self._join_highlight(self._highlight, template)

            if self._attributes is not None:
                for attr in self._attributes:
                    template = self._join(attr, template)

            return Template(f"{template}{self._reset}")

    def _join_color(self, style: int, text: str) -> str:
        return f"{self._escape}38;5;{style}m{text}"

    def _join_highlight(self, style: int, text: str) -> str:
        return f"{self._escape}48;5;{style}m{text}"
