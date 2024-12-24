from enum import Enum, auto

class Layer(Enum):
    BACKGROUND = auto()
    DEFAULT = auto()
    HUD = auto()

TITLE = "Game"
WIDTH = 960
HEIGHT = 540
SIZE = WIDTH, HEIGHT
