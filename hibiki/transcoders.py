#!/usr/bin/env python3

import abc
import enum
import ffmpeg
import pathlib

class BitrateMode(enum.Enum):
    CBR = "cbr"
    VBR = "vbr"

class TranscodingError(Exception):
    pass

class Transcoder(abc.ABC):
    """
    Abstract class for representing a transcoder. This class does nothing, use a subclass of this class instead
    (ex: FFmpegOpusTransocder, FFmpegMp3Transcoder, ...)
    """

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        """
        Abstract method for initializing the class.

        :param args:
        :param kwargs:
        """
        pass

    @abc.abstractmethod
    def transcode(self, src: pathlib.Path, dst: pathlib.Path = None) -> pathlib.Path:
        """
        Abstract method for performing transcoding operations. This method will be called with src as the source file,
        and dst as the destination. In case dst is None, the method shall transcode into a temporary file (using
        tempfile) and then the path to the temporary file shall be returned. If dst is not null, the method returns dst
        upon completion.

        This method blocks until either the operation is finished or TranscodingError is raised.

        This method must be overridden.
        :param src: path to source file
        :param dst: destination path, or None
        :return: dst if dst is not None, or path to temporary file
        """
        pass

class FFmpegOpusTranscoder(Transcoder):
    def __init__(self,
                 bitrate_mode: BitrateMode = BitrateMode.VBR,
                 bitrate: int = 128,
                 compression_level: int = 10):
        """

        :param bitrate_mode: Bitrate mode, can be BitrateMode.CBR (corresponds to hard-cbr) or BitrateMode.VBR
        :param bitrate: Bitrate, expresses in kilobits
        :param compression_level: (>= 0, <= 10) Algorithm complexity, 0 = faster, lower quality, 10 = slower, best
        """
        super().__init__()

        self.bitrate_mode = bitrate_mode
        self.bitrate = bitrate
        self.compression_level = compression_level

    def transcode(self, src: pathlib.Path, dst: pathlib.Path = None) -> pathlib.Path:
        """

        :param src:
        :param dst:
        :return:
        """

        if not dst:
            # TODO: create temp file
            pass

        stream = ffmpeg.input(src)
        stream = ffmpeg.output(dst,
                               vbr = {'on' if self.bitrate_mode == BitrateMode.VBR else 'off'},
                               audio_bitrate = f"{self.bitrate}k",
                               compression_level = f"{self.compression_level}")

        return dst

class FFmpegNativeAacTranscoder(Transcoder):
    pass

class FFmpegFdkAacTranscoder(Transcoder):
    pass

class FFmpegLameTranscoder(Transcoder):
    pass

class FFmpegVorbisTranscoder(Transcoder):
    pass

class NullTranscoder(Transcoder):
    """
    This transcoder does not perform any transcoding operations, rather it just copies file from src to dst
    """
    pass