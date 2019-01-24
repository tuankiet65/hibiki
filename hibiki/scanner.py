#!/usr/bin/env python3

import pathlib
from typing import List

from hibiki.objects import Track, AudioFormatNotSupported


class Scanner:
    def __init__(self):
        """

        """
        pass

    def scan(self, path: pathlib.Path) -> List[Track]:
        """

        :param path:
        :return:
        """
        result = []

        for file in path.glob("**"):
            if not file.is_file():
                continue
            try:
                result.append(Track(file))
            except AudioFormatNotSupported:
                # TODO: use logging instead
                print(f"WARNING: file not supported, ignoring: {file}.")

        return result
