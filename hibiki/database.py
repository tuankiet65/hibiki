#!/usr/bin/env python3

import abc
import pathlib


class Database(abc.ABC):
    pass


class LocalDatabase(Database):
    def scan(self, path: pathlib.Path):
        """

        :param path:
        :return:
        """
        pass

    pass


class RemoteDatabase(Database):
    def load(self, path: pathlib.Path):
        """

        :param path:
        :return:
        """
        pass

    pass
