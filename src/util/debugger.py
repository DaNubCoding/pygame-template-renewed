from typing import Any, Callable
from datetime import datetime
from functools import wraps
import tomllib
import os

class Debug:
    """
    """

    @staticmethod
    def requires_debug(type: str = "debug") -> Callable[..., Any]:
        """Any function decorated with this will only run if the given debug
        type is enabled in the debug.toml file.

        Args:
            type: The type of debug to check for. Defaults to "debug".

        Returns:
            The decorated function.
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
    def get_debug_config(type: str) -> bool:
        try:
            last_modified = os.path.getmtime("debug.toml")
            # Only read the file if it has been modified since the last read
            if Debug._conf_cache is None or Debug._conf_last_modified != last_modified:
                with open("debug.toml", "rb") as file:
                    Debug._conf_cache = tomllib.load(file)
                    Debug._conf_last_modified = last_modified
            # If the debug type exists in the toml file, return the value
            # Default to False if the type does not exist (which can happen
            # while the file is being edited)
            return Debug._conf_cache.get(type, False)
        except FileNotFoundError:
            return False

    @staticmethod
    def on() -> bool:
        return Debug.get_debug_config("debug")

__all__ = ["Debug"]