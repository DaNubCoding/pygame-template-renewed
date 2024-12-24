from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.game.scenes.main_scene import MainScene

from src.core.render_layer import Layer
from src.core.sprite import Sprite
from src.core.assets import Images
from src.core.util import *
import pygame

class Player(Sprite):
    def __init__(self, scene: MainScene) -> None:
        super().__init__(scene, Layer.DEFAULT)
        self.pos = Vec(0, 0)
        self.image = Images.player

    def update(self, dt: float) -> None:
        self.pos.x += 50 * dt
        self.pos.y += 20 * dt

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.pos - Vec(self.image.size) / 2)
