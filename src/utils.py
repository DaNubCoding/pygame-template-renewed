from typing import Self, Callable, Any
from multimethod import multimeta
from pygame.math import Vector2
from datetime import datetime
from functools import wraps
from pathlib import Path
from math import floor
import tomllib
import sys
import os

BUNDLE_DIR = getattr(sys, '_MEIPASS', Path(os.path.abspath(os.path.dirname(__file__))).parent)
def pathof(file: str) -> str:
    """Gets the path to the given file that will work with exes.
    Args:
        file (str): The original path to go to
    Returns:
        str: The bundled - exe compatible file path
    """

    abspath = os.path.abspath(os.path.join(BUNDLE_DIR, file))
    if not os.path.exists(abspath):
        abspath = file
    return abspath

def read_file(path: str) -> str:
    """Opens a file, read the contents of the file, then closes it.

    Args:
        path: The path of the file to read from.

    Returns:
        The full contents of the file.
    """
    with open(path, "r") as file:
        return file.read()

def inttup(tup: tuple[float, float]) -> tuple:
    """Convert a tuple of 2 floats to a tuple of 2 ints.

    Args:
        tup: The tuple to convert.

    Returns:
        The integer tuple.
    """
    return (floor(tup[0]), floor(tup[1]))

class Vec(Vector2, metaclass=multimeta):
    def normalize(self) -> Self:
        try:
            return super().normalize()
        except ValueError:
            return Vec(0, 0)

    def normalize_ip(self) -> None:
        try:
            return super().normalize_ip()
        except ValueError:
            pass

    def clamp_magnitude(self, max_length: float) -> Self:
        try:
            return super().clamp_magnitude(max_length)
        except ValueError:
            return Vec(0, 0)

    def clamp_magnitude(self, min_length: float, max_length: float) -> Self:
        try:
            return super().clamp_magnitude(min_length, max_length)
        except ValueError:
            return Vec(0, 0)

    def clamp_magnitude_ip(self, max_length: float) -> None:
        try:
            return super().clamp_magnitude_ip(max_length)
        except ValueError:
            pass

    def clamp_magnitude_ip(self, min_length: float, max_length: float) -> None:
        try:
            return super().clamp_magnitude_ip(min_length, max_length)
        except ValueError:
            pass

    def __hash__(self) -> int:
        return tuple(self).__hash__()

class Debug:
    """A simple debug logging class that can be used to log messages to the
    console. This class will only log messages if a file named "debug.toml"
    exists in the root directory of the project. Based on the configuration in
    the file, the class will only log messages of the specified types.

    The file should be initially formatted as follows:
    ```
    debug = true
    info = true
    warn = true
    error = true
    ```

    The class has three logging methods: `info`, `warn`, and `error`. Each
    method takes a single argument, the message to log. The message will be
    prefixed with the type of message and the current time.

    The class also has a `on` method that will return a boolean indicating if
    the debug mode is enabled. This can be used to conditionally enable debug
    features in the code.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def _requires_debug(type: str) -> Callable[..., Any]:
        def outer_wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def inner_wrapper(*args, **kwargs) -> Any:
                if Debug._parse_debug_toml(type):
                    return func(*args, **kwargs)
            return inner_wrapper
        return outer_wrapper

    _toml_cache = None
    _toml_last_modified = None

    @staticmethod
    def _parse_debug_toml(type: str) -> bool:
        try:
            last_modified = os.path.getmtime("debug.toml")
            # Only read the file if it has been modified since the last read
            if Debug._toml_cache is None or Debug._toml_last_modified != last_modified:
                with open("debug.toml", "rb") as file:
                    Debug._toml_cache = tomllib.load(file)
                    Debug._toml_last_modified = last_modified
            # If the debug type exists in the toml file, return the value
            # Default to False if the type does not exist (which can happen
            # while the file is being edited)
            return Debug._toml_cache.get(type, False)
        except FileNotFoundError:
            return False

    @staticmethod
    def on() -> bool:
        try:
            last_modified = os.path.getmtime("debug.toml")
            # Only read the file if it has been modified since the last read
            if Debug._toml_cache is None or Debug._toml_last_modified != last_modified:
                with open("debug.toml", "rb") as file:
                    Debug._toml_cache = tomllib.load(file)
                    Debug._toml_last_modified = last_modified
            return Debug._toml_cache.get("debug", False)
        except FileNotFoundError:
            return False

    @staticmethod
    @_requires_debug("info")
    def info(message: str) -> None:
        dt = datetime.now().strftime("%H:%M:%S.%f")
        print(f"[{Debug.OKGREEN}INFO{Debug.ENDC} {Debug.UNDERLINE}{dt}{Debug.ENDC}] {message}")

    @staticmethod
    @_requires_debug("warn")
    def warn(message: str) -> None:
        dt = datetime.now().strftime("%H:%M:%S.%f")
        print(f"[{Debug.WARNING}WARNING{Debug.ENDC} {Debug.UNDERLINE}{dt}{Debug.ENDC}] {message}")

    @staticmethod
    @_requires_debug("error")
    def error(message: str) -> None:
        dt = datetime.now().strftime("%H:%M:%S.%f")
        print(f"[{Debug.BOLD}{Debug.FAIL}CRITICAL{Debug.ENDC} {Debug.UNDERLINE}{dt}{Debug.ENDC}] {message}")
