# -*- coding: UTF-8 -*-

from dataclasses import dataclass, field
from typing import Union, List, Generator

from .utils import del_prefix


@dataclass
class RGB(object):
    """
    `rgb(RED, GREEN, BLUE)`

    Each parameter defines the intensity of the
    color as an integer between `0` and `255`.
    """

    red: int = field(default=0)
    green: int = field(default=0)
    blue: int = field(default=0)

    def __repr__(self) -> str:
        return f"rgb({self.red}, {self.green}, {self.blue})"


@dataclass
class HEX(object):
    """
    `#RRGGBB`

    RR (red), GG (green) and BB (blue) are
    hexadecimal integers between `00` and `FF`
    specifying the intensity of the color.
    """

    red: str = field(default="00")
    green: str = field(default="00")
    blue: str = field(default="00")

    def __repr__(self) -> str:
        return f"#{self.red}{self.green}{self.blue}"


@dataclass
class COLOR(object):

    id: int = field(default=None)
    name: str = field(default=None)
    hex: HEX = field(default=None)
    rgb: RGB = field(default=None)

    # Hsl: hsl(195, 100%, 50%)
    # Hwb: hwb(195, 0%, 0%)
    # Cmyk: cmyk(100%, 25%, 0%, 0%)
    # Ncol: C25, 0%, 0%


class Colors(object):

    @staticmethod
    def _as_string(value: Union[int, str]) -> str:
        if not isinstance(value, str):
            return str(value)
        return value

    @staticmethod
    def _ascii() -> List[str]:
        return ["A", "B", "C", "D", "E", "F"]

    @staticmethod
    def _digits() -> List[int]:
        return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    @staticmethod
    def str_2_hex(value: str) -> HEX:
        length: int = len(value)

        if not (6 <= length <= 7):
            raise ValueError(f"Incorrect value '{value}'!")

        if length == 7:
            value = del_prefix(value, "#")

        return HEX(
            red=value[:2],
            green=value[2:4],
            blue=value[4:6],
        )

    def __init__(self):

        # hexadecimal int keys:
        self._hex_keys: dict = {
            key: value
            for key, value in self._items()
        }

        # rgb int keys:
        self._int_keys: dict = {
            value: key
            for key, value in self._items()
        }

    def hex_2_rgb(self, value: HEX) -> RGB:
        return RGB(
            red=self._hex_keys.get(value.red),
            green=self._hex_keys.get(value.green),
            blue=self._hex_keys.get(value.blue),
        )

    def rgb_2_hex(self, value: RGB) -> HEX:
        return HEX(
            red=self._int_keys.get(value.red),
            green=self._int_keys.get(value.green),
            blue=self._int_keys.get(value.blue),
        )

    def generator(self) -> Generator:
        count: int = 0
        for item_1, count_1 in self._items():
            for item_2, count_2 in self._items():
                for item_3, count_3 in self._items():
                    yield COLOR(
                        id=count,
                        hex=HEX(item_1, item_2, item_3),
                        rgb=RGB(count_1, count_2, count_3),
                    )
                    count += 1

    def _items(self) -> Generator:
        chars: list = self._chars()
        count: int = 0

        for char_1 in chars:
            for char_2 in self._chars():
                yield f"{char_1}{char_2}", count
                count += 1

    def _chars(self) -> List[str]:
        return [
            self._as_string(char)
            for sublist in [self._digits(), self._ascii()]
            for char in sublist
        ]
