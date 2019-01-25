#!/usr/bin/env python3

import pathlib
from typing import List, Dict, Any

from PIL import Image
from tinytag import TinyTag, TinyTagException

from hibiki import utils


class CoverArt:
    __file_path: pathlib.Path = None
    __file_hash: str = None
    __width: int = None
    __height: int = None

    def __init__(self, file_path: pathlib.Path):
        """

        :param file_path:
        """
        self.__file_path = file_path
        self.__populate()

    def __populate(self) -> None:
        """

        :return:
        """
        try:
            img = Image.open(self.__file_path)
            self.__width, self.__height = img.size
        except IOError as e:
            # TODO: properly handle this exception
            raise ImageFormatNotSupported

        self.__file_hash = utils.get_file_partial_hash(self.__file_path)

    @property
    def file_path(self):
        return self.__file_path

    @property
    def file_hash(self):
        return self.__file_hash

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def __eq__(self, other) -> bool:
        """

        :param other:
        :return:
        """
        if not isinstance(other, CoverArt):
            return False
        return self.file_path == other.file_path

    def as_dict(self) -> Dict[str, Any]:
        """

        :return:
        """
        result = {
            "file_hash": self.file_hash
        }

        return result


class Track:
    """
    Class representing a track, or more formally, an audio file on disk.
    """
    LOSSLESS_SUFFIXES = [
        ".flac",  # Free Lossless Audio Codec
        ".tta",  # True Audio
        ".wav",  # Wave
        ".alac",  # Apple Lossless Audio Codec
        ".aiff",  #
        ".ape",  # Monkey's Audio
    ]

    COVER_ART_FILENAMES = [
        "cover.png",
        "cover.jpg",
        "cover.jpeg",
        "folder.png",
        "folder.jpg",
        "folder.jpeg",
        "front.png",
        "front.jpg",
        "front.jpeg"
    ]

    def __init__(self, file_path: pathlib.Path):
        """

        :param file_path:
        """
        self.__file_path = file_path
        self.__populate()

    def __populate(self) -> None:
        """

        :return: None
        """

        self.__populate_metadata()
        self.__populate_cover_art()
        self.__file_hash = utils.get_file_partial_hash(self.__file_path)

        # TODO: an OGG file can also contain a FLAC stream, so matching by
        # suffixes is not enough
        self.__lossless = self.__file_path.suffix in self.LOSSLESS_SUFFIXES

    def __populate_metadata(self) -> None:
        """

        :return: None
        """
        if not TinyTag.is_supported(str(self.__file_path)):
            # TODO: fallback to ffprobe?
            raise AudioFormatNotSupported
        try:
            metadata = TinyTag.get(str(self.__file_path))
            self.__title = metadata.title
            self.__album = metadata.album
            self.__track = metadata.track
            self.__filesize = metadata.filesize
            self.__year = metadata.year
        except TinyTagException as _:
            # TODO: Properly handle this exception
            raise AudioFormatNotSupported

    def __populate_cover_art(self):
        self.__cover_art = None
        for cover_art_filename in self.COVER_ART_FILENAMES:
            path = self.__file_path.parent / cover_art_filename
            if path.exists():
                self.__cover_art = CoverArt(path)
                return

    @property
    def cover_art(self):
        return self.__cover_art

    @property
    def lossless(self):
        return self.__lossless

    @property
    def file_path(self):
        return self.__file_path

    @property
    def file_hash(self):
        return self.__file_hash

    @property
    def title(self):
        return self.__title

    @property
    def album(self):
        return self.__album

    @property
    def track(self):
        return self.__track

    @property
    def filesize(self):
        return self.__filesize

    @property
    def year(self):
        return self.__year

    def as_dict(self) -> Dict[str, Any]:
        """

        :return:
        """

        result = {
            "file_hash": self.file_hash,
            "album": self.album,
            "title": self.title,
            "track": self.track,
        }

        return result


class Album:
    """
    Class representing an album, or more formally, a collection of tracks and
    a cover art
    """

    def __init__(self, title: str, tracks: List[Track] = None):
        """

        """
        self.__title = title

        self.__tracks = []
        if tracks:
            for track in tracks:
                self.add_track(track)

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__title = title

    @property
    def tracks(self) -> List[Track]:
        return self.__tracks

    def add_track(self, track: Track) -> None:
        """

        :param track:
        :return:
        """

        self.__tracks.append(track)

    @property
    def cover_art(self) -> CoverArt or None:
        all_cover_arts = [track.cover_art for track in self.__tracks]
        if None in all_cover_arts:
            return None
        else:
            comparison_result = \
                [cover_art == all_cover_arts[0] for cover_art in all_cover_arts]
            if all(comparison_result):
                return all_cover_arts[0]
            else:
                return None

    def as_dict(self) -> Dict[str, Dict]:
        """
        Converting self into a dictionary suitable for use with JSON/YAML
        
        :return: Dictionary representation of self 
        """
        result = {
            "tracks": [track.as_dict() for track in self.tracks],
            "cover_art": self.cover_art.to_dict()
        }

        return result


class ImageFormatNotSupported(Exception):
    pass


class AudioFormatNotSupported(Exception):
    pass
