#!/usr/bin/env python3

import abc
import pathlib

class Resizer(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        """

        """
        pass

    def resize(self, src: pathlib.Path, dst: pathlib.Path = None) -> pathlib.Path:
        """

        :param src:
        :param dst:
        :return:
        """
        pass

class PillowResizer(Resizer):
    pass

class Waifu2xResizer(Resizer):
    """
    https://github.com/DeadSix27/waifu2x-converter-cpp
    """
    pass