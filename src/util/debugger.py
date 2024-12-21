from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

from typing import Any, Callable
from datetime import datetime
from functools import wraps
import tomllib
import pygame
import os

class Debug:
    """A simple debugging class that can be used to enable or disable debug
    output in the game.

    This class will dynamically read the `debug.toml` file and check if the
    given debug type is enabled. If the file does not exist, the debug type
    will be disabled. If a list of entries is provided in the file, the class
    will evaluate them and display the results on the screen.
    """

    @staticmethod
    def on() -> bool:
        return Debug.get_debug_config("debug")

    @staticmethod
    def requires_debug(type: str = "debug") -> Callable[..., Any]:
        """Any function decorated with this will only run if the given debug
        type is enabled in the debug.toml file.

        Args:
            type: The type of debug to check for. Defaults to "debug".

        Returns:
            The decorated function.

        Example:
            ```python
            @Debug.requires_debug()
            def my_function():
                print("This will only run if the 'debug' type is enabled.")

            @Debug.requires_debug("warn")
            def my_function():
                print("This will only run if the 'warn' type is enabled.")
            ```
        """
        def outer_wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def inner_wrapper(*args, **kwargs) -> Any:
                if Debug.get_debug_config(type):
                    return func(*args, **kwargs)
            return inner_wrapper
        return outer_wrapper

    _conf_cache = None
    _conf_last_modified = None

    @staticmethod
    def get_debug_item(name: str) -> Any:
        try:
            last_modified = os.path.getmtime("debug.toml")
            # Only read the file if it has been modified since the last read
            if Debug._conf_cache is None or Debug._conf_last_modified != last_modified:
                with open("debug.toml", "rb") as file:
                    Debug._conf_cache = tomllib.load(file)
                    Debug._conf_last_modified = last_modified
            return Debug._conf_cache.get(name)
        except FileNotFoundError:
            return None

    @staticmethod
    def get_debug_config(type: str) -> bool:
        try:
            return Debug.get_debug_item(type)
        except KeyError:
            return False

    _debug_entries = {}
    _debug_font = None
    _visible = True
    _paused = False

    @staticmethod
    def toggle_visibility() -> None:
        Debug._visible = not Debug._visible

    @staticmethod
    def toggle_paused() -> None:
        Debug._paused = not Debug._paused

    @staticmethod
    def paused() -> bool:
        return Debug._paused

    @staticmethod
    @requires_debug()
    def draw(game: Game) -> None:
        if not Debug._visible: return

        Debug._debug_entries = Debug.get_debug_item("entries")
        if Debug._debug_entries is None: return

        # Define locals
        scene = game.scene

        if Debug._debug_font is None:
            Debug._debug_font = pygame.font.SysFont("monospace", 16)

        for i, (name, source) in enumerate(Debug._debug_entries.items()):
            value = eval(source)
            text = Debug._debug_font.render(f"{name}: {value}", True, (255, 255, 255), (0, 0, 0))
            text.set_alpha(150)
            game.screen.blit(text, (0, i * 19))

__all__ = ["Debug"]
