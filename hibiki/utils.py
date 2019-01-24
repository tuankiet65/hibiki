#!/usr/bin/env python3

import hashlib
import pathlib

PARTIAL_HASH_PORTION = 32768  # 32 kB


def get_file_partial_hash(file_path: pathlib.Path) -> str:
    """
    Return MD5 hash for the first PARTIAL_HASH_PORTION bytes of file_path

    :param file_path: Path to file
    :return: MD5 hash, in hexadecimal string
    """

    with file_path.open("rb") as f:
        buffer = f.read(PARTIAL_HASH_PORTION)

    return hashlib.md5(buffer).hexdigest()
