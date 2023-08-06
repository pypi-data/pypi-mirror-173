# SPDX-FileCopyrightText: 2022-present abhishek-compro <abhishek.prasad@noorahealth.org>
#
# SPDX-License-Identifier: MIT

import io
import sys
import threading
from datetime import datetime, timedelta

CLEAR_LINE_ESCAPE_SEQUENCE = "\33[2K\r"


def clear_line(file_pointer: io.IOBase = sys.stdout):
    file_pointer.write(CLEAR_LINE_ESCAPE_SEQUENCE)


class printl:
    """Print with a indefinite loader

    Print a message with a loader and elapsed time

    Parameters
    ----------
    message : str
        Message to be printed while loading
    update_every : float  (default: 1)
        Update interval (in seconds) of loader.
        Set to 0 to disable updating the loader.
    loading_chars : list[str]  (default: [".", "..", "..."])
        List of string that will be displayed one by one per update while loading
    loading_fmt : str  (default: "({elapsed_time}) {message} {loading_char}")
        Format to be used while printing loading message
    done_fmt : str  (default: "({elapsed_time}) {message} ✓\n")
        Format to be used while printing done message
    file_pointer : io.IOBase  (default: sys.stdout)
        File to print onto

    Examples
    --------

    >>> import time
    >>> with printl("sleeping"):
    ...     time.sleep(3)
    >>> with printl("sleeping", update_every=0):
    ...     time.sleep(3)
    >>> import requests
    >>> with printl("loading python.org", loading_chars=["－", "\",  "|", "/"], update_every=0.1):
    ...     response = requests.get("https://python.org")
    """

    def __init__(
        self,
        message: str,
        update_every: float = 1,
        loading_chars: list[str] = [".", "..", "..."],
        loading_fmt: str = "({elapsed_time}) {message} {loading_char}",
        done_fmt: str = "({elapsed_time}) {message} ✓\n",
        file_pointer: io.IOBase = sys.stdout,
    ):
        if not file_pointer.writable():
            raise io.UnsupportedOperation("not writable")
        self.message = message
        self.loading_fmt = loading_fmt
        self.done_fmt = done_fmt
        self.start_time: datetime = None
        self.loading_chars = loading_chars
        self.file_pointer = file_pointer
        self.__counter = -1
        self.__update_every = update_every if update_every > 0 else 0
        self.__timer: threading.Timer = None
        self.__timer_lock = threading.Lock()

    def elapsed_time(self) -> timedelta:
        return datetime.utcnow() - self.start_time

    def elapsed_time_str(self) -> str:
        try:
            et = self.elapsed_time()
        except TypeError:
            return f"0d 00h 00m 00.00s"
        micros = et.microseconds // 10000
        secs = et.seconds % 60
        mins = et.seconds // 60
        hrs = et.seconds // 3600
        return f"{et.days}d {hrs:02}h {mins:02}m {secs:02}.{micros:0>2}s"

    def next_loading_char(self):
        if len(self.loading_chars) == 0:
            return ""
        self.__counter = (self.__counter + 1) % len(self.loading_chars)
        return self.loading_chars[self.__counter]

    def print_loading(self):
        clear_line(self.file_pointer)
        self.file_pointer.write(
            self.loading_fmt.format(
                message=self.message,
                elapsed_time=self.elapsed_time_str(),
                loading_char=self.next_loading_char(),
            )
        )
        self.file_pointer.flush()

    def __print_loading_loop(self):
        if self.__update_every <= 0:
            return

        with self.__timer_lock:
            self.print_loading()

            self.__timer = threading.Timer(
                self.__update_every, self.__print_loading_loop
            )
            self.__timer.daemon = True  # join not needed
            self.__timer.start()

    def __unset_timer(self):
        if self.__timer is None:
            return

        with self.__timer_lock:
            self.__timer.cancel()
            self.__timer = None

    def __enter__(self):
        if self.__update_every > 0:
            self.__print_loading_loop()
        else:
            self.print_loading()
        self.start_time = datetime.utcnow()
        return self

    def __exit__(self, *args):
        if self.__timer is not None:
            self.__unset_timer()
        clear_line(self.file_pointer)
        self.file_pointer.write(
            self.done_fmt.format(
                message=self.message, elapsed_time=self.elapsed_time_str()
            )
        )
        self.file_pointer.flush()

    def __del__(self):
        if self.__timer is not None:
            self.__unset_timer()
