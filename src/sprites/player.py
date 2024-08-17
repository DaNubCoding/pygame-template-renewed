from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.scene import Scene

from src.core.render_layer import Layer
from src.core.sprite import Sprite
from src.utils import Vec

import pygame

class Player(Sprite):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layer.DEFAULT)
        self.pos = Vec(0, 0)

    def update(self, dt: float) -> None:
        self.pos.x += 1 * dt

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (255, 0, 0), (*self.pos, 50, 50))
