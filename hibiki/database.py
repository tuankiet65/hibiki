#!/usr/bin/env python3

import abc
import json
import pathlib

from typing import Dict, Any
from hibiki.objects import Album, Track

from hibiki import utils


class Database(abc.ABC):
    """

    """

    def __init__(self):
        """

        """
        self.__albums: Dict[str, Album] = {}

    def add_track(self, track: Track):
        """

        :param track:
        :return:
        """

        album_id = self.__get_album_id(track)
        if album_id not in self.__albums:
            self.__albums[album_id] = Album(track.album)
            self.__albums[album_id].add_track(track)

    def as_dict(self) -> Dict[str, Dict]:
        result = {}
        for album_id, album in self.__albums.items():
            result[album_id] = album.as_dict()
        return result

    def __get_album_id(self, track: Track):
        s = f"{track.album}/{track.year}"
        return utils.get_str_md5(s)


class LocalDatabase(Database):
    def scan(self, path: pathlib.Path):
        """

        :param path:
        :return:
        """
        pass

    pass


class RemoteDatabase(Database):
    def __init__(self, encoder_settings):
        super().__init__()
        self.__encoder_settings = encoder_settings
        pass

    def load(self, path: pathlib.Path):
        """

        :param path:
        :return:
        """
        pass

    def save(self, path: pathlib.Path):
        """

        :param path:
        :return:
        """

        pass

    def as_dict(self) -> Dict[str, Any]:
        result = {
            "encoder": self.__encoder_settings.to_dict(),
            "albums": super().as_dict()
        }

        return result
