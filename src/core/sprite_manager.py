from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.scene import Scene

from src.core.render_layer import RenderLayer
from src.core.sprite import Sprite
from src.game.settings import *
from src.core.util import *
import pygame

class SpriteManager:
    def __init__(self, scene: Scene) -> None:
        self.scene = ref_proxy(scene)
        self.layers = {layer: RenderLayer() for layer in scene.Layer}

    def update(self, dt: float) -> None:
        for layer in self.layers.values():
            layer.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        for layer in self.layers.values():
            layer.draw(screen)

    def add(self, sprite: Sprite) -> None:
        self.layers[sprite.layer].add(sprite)

    def remove(self, sprite: Sprite) -> None:
        self.layers[sprite.layer].remove(sprite)
