from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

from src.game.sprites.player import Player
from src.core.assets import Images
from src.core.scene import Scene
from src.core.util import *
import pygame

class MainScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.player = Player(self)
        self.add(self.player)

    def update(self, dt: float) -> None:
        self.sprite_manager.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((50, 50, 50))
        screen.blit(Images.test, (0, 0))
        self.sprite_manager.draw(screen)
