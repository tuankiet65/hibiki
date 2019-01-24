#!/usr/bin/env python3

import pathlib

class Track:
    """
    Class representing a track, more formally, an audio file on disk.
    """
    title: str = None
    album: str = None
    file_path: pathlib.Path = None
    file_hash: str = None
    lossless: bool = False

    @property
    def __init__(self, file_path: pathlib.Path):
    pass


class Album:
    pass
