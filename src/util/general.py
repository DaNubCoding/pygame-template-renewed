from typing import Iterable, TypeVar
from src.util.vector import Vec
from src.util.typing import *
from pathlib import Path
from math import floor
import weakref
import pygame
import sys
import os

T = TypeVar("T")
BUNDLE_DIR = getattr(
    sys, "_MEIPASS",
    Path(os.path.abspath(os.path.dirname(__file__))).parent
)

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

# Technically the return type should be weakref.ProxyType[T], but that breaks
# IntelliSense for attribute access on the proxy object, so we will pretend it
# is just T :P
def ref_proxy(obj: T) -> T:
    """Create a weak reference proxy to an object if it isn"t already one.

    Args:
        obj: The object to create a weak reference proxy to.

    Returns:
        The weak reference proxy.
    """
    if isinstance(obj, weakref.ProxyTypes):
        return obj
    return weakref.proxy(obj)

def read_file(path: str) -> str:
    """Opens a file, read the contents of the file, then closes it.

    Args:
        path: The path of the file to read from.

    Returns:
        The full contents of the file.
    """
    with open(path, "r") as file:
        return file.read()

def inttup(tup: Coord) -> tuple:
    """Convert a tuple of 2 numbers to a tuple of 2 ints.

    This uses the floor function to convert the numbers to ints.

    Args:
        tup: The tuple to convert.

    Returns:
        The integer tuple.
    """
    return (floor(tup[0]), floor(tup[1]))

def iter_rect(left: int, right: int, top: int, bottom: int) -> Iterable[IntCoord]:
    """Iterate over the coordinates of a rectangle.

    Args:
        left: The leftmost x-coordinate (inclusive).
        right: The rightmost x-coordinate (inclusive).
        top: The topmost y-coordinate (inclusive).
        bottom: The bottommost y-coordinate (inclusive).

    Yields:
        The coordinates of the rectangle.
    """
    for x in range(int(left), int(right) + 1):
        for y in range(int(top), int(bottom) + 1):
            yield Vec(x, y)

def iter_square(size: int) -> Iterable[IntCoord]:
    """Iterate over the coordinates of a square.

    Args:
        size: The size of the square.

    Yields:
        The coordinates of the square.
    """
    yield from iter_rect(0, size - 1, 0, size - 1)

__all__ = [
    "pathof",
    "ref_proxy",
    "read_file",
    "inttup",
    "iter_rect",
    "iter_square",
]
